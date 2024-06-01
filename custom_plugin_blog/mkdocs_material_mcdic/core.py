import os
import re
import tempfile
import typing
from datetime import date, datetime, timedelta
from pathlib import Path

import pytz
from jinja2 import Environment
from mkdocs.config.defaults import MkDocsConfig
from mkdocs.exceptions import PluginError
from mkdocs.plugins import BasePlugin, event_priority, get_plugin_logger
from mkdocs.structure.files import File, Files
from mkdocs.structure.nav import Navigation, Section, StructureItem
from mkdocs.structure.pages import Page

from . import constants
from .config import McDicBlogPluginConfig
from .ga4 import ViewDataValue, fetch_ga4_data
from .ga4 import get_client as get_ga4_client
from .ga4 import parse_ga4_cache
from .git import get_date_from_git, get_github_edit_history_url
from .utils import dict_get, dict_merge_inplace

logger = get_plugin_logger("mcdic")


P = typing.ParamSpec("P")
Ret = typing.TypeVar("Ret")


def skip_if_disabled(
    method: typing.Callable[typing.Concatenate["McDicBlogPlugin", P], Ret | None]
) -> typing.Callable[typing.Concatenate["McDicBlogPlugin", P], Ret | None]:
    """
    Make method be skipped if plugin is disabled.
    """

    def new_method(
        self: "McDicBlogPlugin", *args: P.args, **kwargs: P.kwargs
    ) -> Ret | None:
        return method(self, *args, **kwargs) if self.config.enabled else None

    return new_method


class McDicBlogPlugin(BasePlugin[McDicBlogPluginConfig]):
    """
    A plugin solely developed for [McDic's Blog](https://blog.mcdic.net).
    See [plugins/events](https://www.mkdocs.org/dev-guide/plugins/#events).
    """

    def __init__(self) -> None:
        super().__init__()
        self._views: dict[str, ViewDataValue] = {}
        self._build_mode: typing.Literal["gh-deploy", "serve", "build"]

        self._root_found_on_nav: bool = False
        self._series_section: Section = Section("Series", [])
        self._archives_section: Section = Section("Archives", [])
        self._sorted_section: Section = Section("Posts Sorted By", [])

        self._temp_dir: tempfile.TemporaryDirectory
        self._cached_sorted_pages_by_date: list[Page] = []

    def _make_new_tempdir(self) -> None:
        """
        Create new temporary directory.
        """
        try:
            self._temp_dir.cleanup()
        except Exception:
            pass
        self._temp_dir = tempfile.TemporaryDirectory()

    def _create_tempfile(
        self,
        config: MkDocsConfig,
        *src_paths: str,
        content: str = "",
    ) -> File:
        """
        Create temporary file and return it.
        """
        if not src_paths:
            raise PluginError("Given paths is empty on `_create_tempfile`")
        current_path = Path(self._temp_dir.name)
        for path in src_paths[:-1]:
            current_path = current_path / path
            current_path.mkdir(exist_ok=True)
        with open(current_path / src_paths[-1], "w") as raw_file:
            raw_file.write(content)

        return File(
            os.path.join(*src_paths),
            self._temp_dir.name,
            config.site_dir,
            use_directory_urls=True,
        )

    def _is_from_temp_dir(self, page: Page):
        """
        Check if this page is created on the temporary directory.
        """
        return Path(page.file.abs_src_path).is_relative_to(self._temp_dir.name)

    def _check_page_by(
        self, page: Page, finder: re.Pattern, check_relative_path: bool
    ) -> bool:
        """
        Common method to classify pages.
        """
        return bool(
            finder.match(page.file.src_path)
            and (not check_relative_path or self._is_from_temp_dir(page))
        )

    def _is_blog_post_page(self, page: Page) -> bool:
        """
        Return if given `page` is a blog post page.
        """
        return self._check_page_by(page, constants.RE_POST_FINDER, False)

    def _is_series_index_page(self, page: Page) -> bool:
        """
        Return if given `page` is a series index page.
        """
        return self._check_page_by(page, constants.RE_POST_INDEX_FINDER, True)

    def _is_recent_posts_page(self, page: Page) -> bool:
        """
        Return if given `page` is a recent posts page.
        """
        return self._check_page_by(page, constants.RE_RECENT_POSTS_FINDER, True)

    def _is_most_viewed_posts_page(self, page: Page) -> bool:
        """
        Return if given `page` is most viewed posts page.
        """
        return self._check_page_by(page, constants.RE_MOST_VIEWED_FINDER, True)

    def _is_archives_page(self, page: Page) -> bool:
        """
        Return if given `page` is archives page.
        """
        return self._check_page_by(page, constants.RE_ARCHIVES_FINDER, True)

    @staticmethod
    def aggregate_views(obj0: ViewDataValue, *objs: ViewDataValue) -> ViewDataValue:
        """
        Aggregate view statistics.
        """
        result = obj0.copy()
        for obj in objs:
            for key in obj:
                result[key] = sum(result[key], obj[key])  # type: ignore[literal-required] # noqa: E501
        return result

    @staticmethod
    def get_category(
        file_or_page: File | Page, abbreviated: bool = False
    ) -> str | None:
        """
        Get category of a file or page.
        If there are multiple categories, raise an error.
        If there is none, return `None`.
        """
        page: Page | None = (
            file_or_page if isinstance(file_or_page, Page) else file_or_page.page
        )
        if page is None:
            return None

        categories: list[str] = page.meta.get("categories", [])
        if len(categories) > 1:
            raise PluginError(f"Multiple categories {categories} on page {page.title}")
        if not categories:
            return None
        elif not abbreviated:
            return categories[0]
        else:
            return page.title.split(".")[0].split(" ")[0]

    def _link_archived_pages(self, files: Files):
        """
        Link prev/next pages between archive pages.
        """

        target_pages: list[tuple[int, Page]] = []
        for file in files.documentation_pages():
            page = file.page
            if page is not None and self._is_archives_page(page):
                year = int(file.src_path.split("/")[-1].replace(".md", ""))
                target_pages.append((year, page))
        target_pages.sort()

        self._archives_section.children = []
        for i, (year, page) in enumerate(target_pages):
            if i > 0:
                page.previous_page = target_pages[i - 1][1]
            if i + 1 < len(target_pages):
                page.next_page = target_pages[i + 1][1]
            self._archives_section.children.append(page)
            page.meta["title"] = str(year)
            page.parent = self._archives_section

    def _prepare_sorted_section(self, files: Files):
        """
        Prepare sorted section of nav.
        """

        self._sorted_section.children = []
        for file in files.documentation_pages():
            page = file.page
            if page is None:
                continue
            elif self._is_recent_posts_page(page) or self._is_most_viewed_posts_page(
                page
            ):
                self._sorted_section.children.append(page)
                page.parent = self._sorted_section

    def _load_series_by_categories(self, files: Files):
        """
        Load series by categories.
        This method is carefully implemented to
        not duplicate entries on the navigation.
        """

        used_pages: dict[str, list[Page]] = {}
        series_index_pages: dict[str, Page] = {}

        for file in files.documentation_pages():
            if file.page is None:
                logger.warning('File "%s" doesn\'t have a page yet' % (file,))
                continue

            category: str | None = None

            # Removing all prev/next pages is needed
            file.page.previous_page = None
            file.page.next_page = None

            if is_series_index_page := self._is_series_index_page(file.page):
                category = file.name.upper()
            else:
                category = self.get_category(file, abbreviated=True)

            if category is None:
                continue
            elif is_series_index_page:
                series_index_pages[category] = file.page
                file.page.meta["title"] = category
                continue

            if category not in used_pages:
                used_pages[category] = []
            used_pages[category].append(file.page)

        # Navigation
        self._series_section.children = [
            page for _, page in sorted(series_index_pages.items())
        ]
        for child in self._series_section.children:
            child.parent = self._series_section

        # Blog posts
        for category, pages in used_pages.items():
            pages.sort(
                key=(
                    lambda page: (
                        self.pop_category_id(page.title)
                        if isinstance(page.title, str)
                        else -1
                    )
                )
            )
            series_index_pages[category].next_page = pages[0]
            for i, page in enumerate(pages):
                page.previous_page = (
                    pages[i - 1] if i > 0 else series_index_pages[category]
                )
                page.next_page = (
                    pages[i + 1] if i + 1 < len(pages) else series_index_pages[category]
                )

            logger.info("Loaded %s series", category)

        logger.info("Loaded all series")

    @staticmethod
    def pop_category_id(title: str) -> int:
        """
        Pop category id, if applicable.
        """
        return int(title.split(".")[0].split(" ")[-1])

    @event_priority(constants.EARLY_EVENT_PRIORITY)
    @skip_if_disabled
    def on_startup(
        self,
        *,
        command: typing.Literal["build", "gh-deploy", "serve"],
        dirty: bool,
    ) -> None:
        """
        Make this update views on `gh-deploy`.
        """
        self._build_mode = command
        self._make_new_tempdir()

    def _get_views(self) -> None:
        """
        Get views data.
        """
        force_update_views: bool = self._build_mode == "gh-deploy"
        if self.config.post_views:
            force_update_views = (
                force_update_views or self.config.post_views.forced_update
            )

        if (
            self.config.post_views
            and self.config.post_views.local_path
            and not force_update_views
        ):
            self._views = parse_ga4_cache(self.config.post_views.local_path)

        elif force_update_views:
            logger.info("Views data is forcibly updating..")
            client = get_ga4_client()
            self._views = fetch_ga4_data(client)

        for title, views in list(self._views.items()):
            if not isinstance(views, dict) or set(views.keys()) != {
                "views",
                "total_users",
            }:
                raise ValueError(
                    f"Validation failed, views = {views} is not an integer"
                )

            del self._views[title]
            if (
                not title.endswith(constants.TITLE_SUFFIX)
                and title != constants.TITLE_SUFFIX[3:]  # Index Page
            ):
                logger.debug(f'Invalid page title "{title}" is removed from views data')
            else:
                replaced_title = (
                    title.strip().replace(constants.TITLE_SUFFIX, "")
                    or constants.INDEX_TITLE
                )
                if replaced_title in self._views:
                    self._views[replaced_title] = self.aggregate_views(
                        self._views[replaced_title], views
                    )
                else:
                    self._views[replaced_title] = views

    def _get_views_by_titles(self, page: Page) -> int:
        """
        Get all views from given `page`.
        """
        result = dict_get(self._views, page.title, "total_users", default=0)
        for alternative_title in dict_get(page.meta, "alternative_titles", default=[]):
            result += dict_get(self._views, alternative_title, "total_users", default=0)
            logger.debug(
                "Result += %d from alternative title '%s'",
                dict_get(self._views, alternative_title, "total_users", default=0),
                alternative_title,
            )
        return result

    @event_priority(constants.EARLY_EVENT_PRIORITY)
    @skip_if_disabled
    def on_pre_build(self, config: MkDocsConfig) -> None:
        """
        Get views in this step.
        """
        self._get_views()

    @event_priority(constants.EARLY_EVENT_PRIORITY)
    @skip_if_disabled
    def on_config(self, config: MkDocsConfig) -> MkDocsConfig | None:
        """
        Validate configs in this step.
        """
        if self.config.sorted.recent < 1:
            raise PluginError(
                "Number of recent posts to show should be positive integer"
            )
        if self.config.sorted.most_viewed < 1:
            raise PluginError(
                "Number of most viewed posts to show should be positive integer"
            )
        return None

    @event_priority(constants.EARLY_EVENT_PRIORITY)
    @skip_if_disabled
    def on_files(self, files: Files, *, config: MkDocsConfig) -> Files | None:
        """
        Editing file destination wouldn't work properly
        after this event, therefore I edit some files here.
        Also, I manipulate the file orders to make
        root page being rendered at the last, advised from
        https://github.com/mkdocs/mkdocs/discussions/3553#discussioncomment-8171415.
        """
        logger.debug("site_dir = %s", config.site_dir)

        # Delete tmp files first
        for file in files:
            if file.abs_src_path.startswith("/tmp/"):
                files.remove(file)

        # Manipulate individual series post
        used_series: set[str] = set()
        posts_num: int = 0
        for file in files.documentation_pages():
            # Should not use self._yield_blog_posts(),
            # because pages are not prepared yet
            if not constants.RE_POST_FINDER.match(file.src_uri):
                continue
            posts_num += 1
            _, series, filename = file.src_path.split("/")
            index: int = int(filename.replace(series, "").replace(".md", ""))
            file.dest_uri = f"series/{series}/{index}/index.html"
            file.abs_dest_path = os.path.join(config.site_dir, file.dest_path)
            file.url = f"series/{series}/{index}"
            used_series.add(series)

        # Make new series index files
        logger.info("Used series = %s", used_series)
        for series in used_series:
            files.append(
                self._create_tempfile(
                    config,
                    "series",
                    f"{series}.md",
                )
            )

        # Create sorted page
        files.append(self._create_tempfile(config, "sorted", "recent.md"))
        files.append(self._create_tempfile(config, "sorted", "most_viewed.md"))

        # Create archives pages
        for year in range(2021, date.today().year + 1):
            files.append(self._create_tempfile(config, "archives", f"{year}.md"))

        # Move root file to back
        root_file = files.get_file_from_path(constants.INDEX_SRC_URI)
        if root_file is None:
            raise PluginError(
                "There is no root page (%s/%s)"
                % (config.docs_dir, constants.INDEX_SRC_URI)
            )
        files.remove(root_file)
        files.append(root_file)
        return files

    @staticmethod
    def get_git_exclude_lines(file_or_page: File | Page) -> int:
        """
        Get the number of lines to exclude to search from the git system.
        """
        file: File = (
            file_or_page if isinstance(file_or_page, File) else file_or_page.file
        )
        if not file.is_documentation_page():
            raise PluginError(
                f"Given file {file.abs_src_path} is not a documentation page"
            )
        with open(file.abs_src_path) as raw_file:
            content = raw_file.read().strip()
        if constants.EXCERPT_DIVIDER in content:
            return content.split(constants.EXCERPT_DIVIDER)[0].count("\n") + 1
        else:
            return 0

    def _get_page_excerpt(self, post: Page, config: MkDocsConfig) -> list[str]:
        """
        Get page excerpt as separated lines.
        """

        def datestr(d: str | None, commit: str | None) -> str:
            """
            Format given `d` into datestring.
            """
            if d is None:
                return constants.METADATA_NOT_AVAILABLE
            elif commit is None:
                return d
            else:
                return "[%s](%s/commit/%s)" % (d, config.repo_url, commit)

        updated_date = dict_get(post.meta, "date", "updated")
        created_date = dict_get(post.meta, "date", "created")
        original_date = dict_get(post.meta, "date", "original")
        unique_users = dict_get(post.meta, "views")
        edit_history_url = dict_get(post.meta, "edit_history")

        metadata_updated_date = datestr(
            updated_date, dict_get(post.meta, "commit", "updated")
        )
        metadata_created_date = datestr(
            original_date or created_date,
            dict_get(post.meta, "commit", "created") if original_date is None else None,
        )
        metadata_unique_users = (
            f"{unique_users} users"
            if unique_users
            else constants.METADATA_NOT_AVAILABLE
        )
        metadata_history = (
            "[../%s](%s)" % (edit_history_url.split("/")[-1], edit_history_url)
            if edit_history_url
            else constants.METADATA_NOT_AVAILABLE
        )

        return [
            constants.METADATA_TABLE_MARKDOWN
            % (
                post.title,
                post.url,
                "material-calendar-edit",
                "material-calendar-plus",
                "material-eye-plus" if unique_users else "material-eye-remove",
                "octicons-git-commit-16",
                metadata_updated_date,
                metadata_created_date,
                metadata_unique_users,
                metadata_history,
                "material-calendar-edit",
                metadata_updated_date,
                "material-calendar-plus",
                metadata_created_date,
                "material-eye-plus" if unique_users else "material-eye-remove",
                metadata_unique_users,
                "octicons-git-commit-16",
                metadata_history,
            ),
            (post.markdown or "")
            .split(constants.EXCERPT_DIVIDER)[0]
            .replace(f"# {post.title}", ""),
            constants.EXCERPT_READMORE % (post.url,),
        ]

    def _yield_blog_posts(self, files: Files) -> typing.Generator[Page, None, None]:
        """
        Yield all blog posts.
        """
        yield from (
            file.page
            for file in files.documentation_pages()
            if file.page is not None and self._is_blog_post_page(file.page)
        )

    def _modify_markdown_on_series_index_page(
        self, markdown: str, series: str, files: Files, config: MkDocsConfig
    ) -> str:
        """
        Return a modified markdown text of series index page.
        """
        posts: list[Page] = sorted(
            (
                page
                for page in self._yield_blog_posts(files)
                if self.get_category(page.file, abbreviated=True) == series
            ),
            key=(lambda post: self.pop_category_id(post.title)),
        )
        joinlist = [markdown, constants.SERIES_INDEX_PREFIX % (series, series), "---"]
        for post in posts:
            joinlist.extend(self._get_page_excerpt(post, config))
            joinlist.append("---")
        return "\n\n".join(joinlist)

    def _get_sorted_pages_by_date(self, files: Files) -> list[Page]:
        """
        Create a sorted blog posts by updated/created date, and cache/return it.
        If this is already cached, return it without doing anything.
        """
        if not self._cached_sorted_pages_by_date:
            self._cached_sorted_pages_by_date = sorted(
                self._yield_blog_posts(files),
                reverse=True,
                key=(
                    lambda post: (
                        dict_get(
                            post.meta,
                            "date",
                            "updated_raw",
                            default=constants.MIN_DATETIME,
                        ),
                        dict_get(post.meta, "date", "original_raw")
                        or dict_get(
                            post.meta,
                            "date",
                            "created_raw",
                            default=constants.MIN_DATETIME,
                        ),
                        post.title,
                    )
                ),
            )
        return self._cached_sorted_pages_by_date

    def _modify_markdown_on_recent_posts_page(
        self, markdown: str, files: Files, config: MkDocsConfig
    ) -> str:
        """
        Return a modified markdown text for recent posts page.
        """
        joinlist: list[str] = [
            markdown,
            constants.RECENT_POSTS_PREFIX % (self.config.sorted.recent,),
            "---",
        ]
        for page in self._get_sorted_pages_by_date(files)[: self.config.sorted.recent]:
            joinlist.extend(self._get_page_excerpt(page, config))
            joinlist.append("---")
        return "\n\n".join(joinlist)

    def _modify_markdown_on_most_viewed_posts_page(
        self, markdown: str, files: Files, config: MkDocsConfig
    ) -> str:
        """
        Return a modified markdown text for most viewed posts page.
        """
        joinlist: list[str] = [
            markdown,
            constants.MOST_VIEWED_POSTS_PREFIX % (self.config.sorted.most_viewed,),
            "---",
        ]
        for page in sorted(
            self._yield_blog_posts(files),
            key=(lambda page: page.meta.get("views", 0)),
            reverse=True,
        )[: self.config.sorted.most_viewed]:
            joinlist.extend(self._get_page_excerpt(page, config))
            joinlist.append("---")
        return "\n\n".join(joinlist)

    def _modify_markdown_on_archives_page(
        self, year: int, markdown: str, files: Files, config: MkDocsConfig
    ) -> str:
        """
        Return a modified markdown text for archives page.
        """
        joinlist: list[str] = [
            markdown,
            constants.ARCHIVES_PREFIX % (year, year),
            "---",
        ]
        for page in sorted(
            filter(
                lambda page: (
                    (
                        page.meta.get("date", {}).get("original_raw", None)
                        or page.meta.get("date", {}).get("created_raw", date.min)
                    ).year
                    == year
                ),
                self._get_sorted_pages_by_date(files),
            ),
            key=(
                lambda page: page.meta["date"].get("original_raw")
                or page.meta["date"]["created_raw"]
            ),
        ):
            joinlist.extend(self._get_page_excerpt(page, config))
            joinlist.append("---")
        return "\n\n".join(joinlist)

    @event_priority(constants.LATE_EVENT_PRIORITY)
    @skip_if_disabled
    def on_page_markdown(
        self, markdown: str, *, page: Page, config: MkDocsConfig, files: Files
    ) -> str | None:
        """
        Since this is the earliest possible moment where metadata is available,
        I directly modify the metadata here.
        """
        # View metadata
        page.meta["views"] = self._get_views_by_titles(page)

        # History metadata
        if not self._is_from_temp_dir(page):
            page.meta["edit_history"] = get_github_edit_history_url(page.file.src_uri)
            logger.info("edit_history = %s", page.meta["edit_history"])

        # Disable analytics if serving
        if self._build_mode != "serve":
            page.meta["enable_analytics"] = True

        # Get meta lines
        page.meta["meta_lines"] = self.get_git_exclude_lines(page)

        # Get git date metadata
        try:
            meta_lines: int = dict_get(page.meta, "meta_lines")
            logger.debug('Meta lines = %s on page "%s"', meta_lines, page.title)
            created_hash, created_date = get_date_from_git(
                page.file.abs_src_path,
                "created",
                line_start=meta_lines + 1,
            )
            updated_hash, updated_date = get_date_from_git(
                page.file.abs_src_path,
                "updated",
                line_start=meta_lines + 1,
            )
        except FileNotFoundError:
            pass
        else:
            dict_merge_inplace(
                page.meta,
                {
                    "date": {
                        "created_raw": created_date,
                        "updated_raw": updated_date,
                        "created": created_date.strftime(self.config.git_dates.format),
                        "updated": updated_date.strftime(self.config.git_dates.format),
                    },
                    "commit": {"created": created_hash, "updated": updated_hash},
                },
            )

        # Modify original date if exists
        original_date: date | None = dict_get(page.meta, "date", "original")
        if original_date is not None:
            original_datetime = datetime.combine(
                original_date, constants.MIN_DATETIME.time(), pytz.UTC
            )
            dict_merge_inplace(
                page.meta,
                {
                    "date": {
                        "original_raw": original_datetime,
                        "original": original_datetime.strftime(
                            self.config.git_dates.format
                        ),
                    }
                },
                override=True,
            )

        # Raise error on no excerpt
        if self._is_blog_post_page(page) and constants.EXCERPT_DIVIDER not in markdown:
            raise PluginError(
                "Page '%s' does not have EXCERPT DIVIDER '%s'"
                % (page.title, constants.EXCERPT_DIVIDER)
            )

        # -------------------------------------------
        # Below cases are for generated pages

        # If series index?
        elif self._is_series_index_page(page):
            page.meta["no_comments"] = True
            series: str = page.file.src_uri.split("/")[-1].replace(".md", "").upper()
            return self._modify_markdown_on_series_index_page(
                markdown, series, files, config
            )

        # If recent posts?
        elif self._is_recent_posts_page(page):
            page.meta["no_comments"] = True
            page.meta["title"] = "Recent"
            return self._modify_markdown_on_recent_posts_page(markdown, files, config)

        # If most viewed?
        elif self._is_most_viewed_posts_page(page):
            page.meta["no_comments"] = True
            page.meta["title"] = "Most Viewed"
            return self._modify_markdown_on_most_viewed_posts_page(
                markdown, files, config
            )

        # If archives?
        elif self._is_archives_page(page):
            page.meta["no_comments"] = True
            year = int(page.file.src_uri.split("/")[-1].replace(".md", ""))
            return self._modify_markdown_on_archives_page(year, markdown, files, config)

        # -------------------------------------------
        # Below cases are for normal documents

        joinlist: list[str] = [markdown]

        # If it is migrated?
        if dict_get(page.meta, "date", "original"):
            joinlist.insert(0, constants.POST_MIGRATION_NOTICE)

        return "\n\n".join(joinlist)

    def _modify_nav_on_root_page(self, section: Navigation | Section):
        """
        Find the first homepage occurrence
        and then insert some series navigations.
        """
        iterable: list[StructureItem] = (
            section.children if isinstance(section, Section) else section.items
        )
        for i, item in enumerate(iterable):
            if isinstance(item, Page) and item.url in ("", "/"):
                if self._root_found_on_nav:
                    raise PluginError("Found duplicated root page entries")
                logger.debug("Entry of root page found: %s", item)
                self._root_found_on_nav = True

                target_index = i + 1

                iterable.insert(target_index, self._series_section)
                self._series_section.parent = (
                    section if isinstance(section, Section) else None
                )
                target_index += 1

                iterable.insert(target_index, self._archives_section)
                self._archives_section.parent = (
                    section if isinstance(section, Section) else None
                )
                target_index += 1

                iterable.insert(target_index, self._sorted_section)
                self._sorted_section.parent = (
                    section if isinstance(section, Section) else None
                )
                target_index += 1

            elif isinstance(item, Section):
                self._modify_nav_on_root_page(item)

    @event_priority(constants.LATE_EVENT_PRIORITY)
    @skip_if_disabled
    def on_nav(
        self, nav: Navigation, *, config: MkDocsConfig, files: Files
    ) -> Navigation | None:
        """
        Altering nav.
        """
        self._root_found_on_nav = False
        self._modify_nav_on_root_page(nav)
        if not self._root_found_on_nav:
            logger.warning("Root page entry not found on navigation")
        return nav

    @event_priority(constants.LATE_EVENT_PRIORITY)
    @skip_if_disabled
    def on_env(
        self, env: Environment, *, config: MkDocsConfig, files: Files
    ) -> Environment | None:
        """
        After all pages are populated, I do followings;
        - Alter global navigation and prev/next page buttons of each page.
        """
        self._load_series_by_categories(files)
        self._link_archived_pages(files)
        self._prepare_sorted_section(files)
        return None

    @event_priority(constants.LATE_EVENT_PRIORITY)
    def on_shutdown(self) -> None:
        try:
            self._temp_dir.cleanup()
        except Exception:
            pass
