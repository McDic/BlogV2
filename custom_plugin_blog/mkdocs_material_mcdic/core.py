import itertools
import os
import re
import tempfile
import typing
from copy import deepcopy
from datetime import date, datetime
from pathlib import Path

import pytz
from jinja2 import Environment
from mkdocs.config.defaults import MkDocsConfig
from mkdocs.exceptions import PluginError
from mkdocs.plugins import BasePlugin, event_priority, get_plugin_logger
from mkdocs.structure.files import File, Files
from mkdocs.structure.nav import Link, Navigation, Section, StructureItem
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
        self._quiz_section: Section = Section("Quizzes", [])

        self._temp_dir: tempfile.TemporaryDirectory
        self._cached_sorted_pages_by_date: list[Page] = []

        # (series, index) -> (series, index)
        self._blog_post_proxies: dict[tuple[str, int], Page] = {}

        # (quiz_id, "answer" | "question") -> Page
        self._quiz_proxies: dict[
            tuple[int, typing.Literal["answer", "question"]], Page
        ] = {}

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
        return page.file.abs_src_path is not None and Path(
            page.file.abs_src_path
        ).is_relative_to(self._temp_dir.name)

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

    def _is_quiz_page(
        self, page: Page
    ) -> None | tuple[int, typing.Literal["answer", "question"]]:
        """
        Return if given `page` is a quiz page.
        """
        if self._check_page_by(page, constants.RE_QUIZ_FINDER, False):
            splitted = page.file.src_uri.split("/")
            return int(splitted[-2][1:]), (
                "answer" if "answer" in splitted[-1].replace(".md", "") else "question"
            )
        else:
            return None

    @staticmethod
    def aggregate_views(obj0: ViewDataValue, *objs: ViewDataValue) -> ViewDataValue:
        """
        Aggregate view statistics.
        """
        result = deepcopy(obj0)
        for obj in objs:
            for key in obj:
                result[key] += obj[key]  # type: ignore[literal-required] # noqa: E501
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

    def _link_quiz_pages(self, files: Files):
        """
        Link prev/next pages between quiz pages.
        """
        index_page: Page
        for file in files:
            if file.page is not None and file.page.is_index:
                index_page = file.page
                break
        else:
            raise PluginError("No index page found")
        quiz_keys = sorted(set(id_ for id_, _typ in self._quiz_proxies.keys()))

        # Clear quiz section
        self._quiz_section.children.clear()

        # Random question
        self._quiz_section.children.append(Link("Random", "/random/quiz.html"))

        # Question pages
        self._quiz_proxies[(quiz_keys[0], "question")].previous_page = index_page
        self._quiz_proxies[(quiz_keys[-1], "question")].next_page = index_page
        for qid_prev, qid_next in itertools.pairwise(quiz_keys):
            self._quiz_proxies[(qid_prev, "question")].next_page = self._quiz_proxies[
                (qid_next, "question")
            ]
            # fmt: off
            self._quiz_proxies[(qid_next, "question")].previous_page = (
                self._quiz_proxies[(qid_prev, "question")]
            )
            # fmt: on

        # Answer pages
        for qid in quiz_keys:
            self._quiz_proxies[(qid, "answer")].previous_page = self._quiz_proxies[
                (qid, "question")
            ]
            self._quiz_proxies[(qid, "answer")].next_page = None
            if (
                self._quiz_proxies[(qid, "question")].title
                != self._quiz_proxies[(qid, "answer")].title
            ):
                raise PluginError(
                    "Question and answer titles for #%d are different" % (qid,)
                )

        def recursive_sectioning(
            root: Section, i_begin: int, i_end: int, div: int, max_leaf: int = 20
        ):
            if i_end - i_begin < max_leaf:
                for i in quiz_keys[i_begin:i_end]:
                    root.children.append(self._quiz_proxies[(i, "question")])
                    self._quiz_proxies[(i, "question")].parent = root
                    self._quiz_proxies[(i, "answer")].parent = root
            else:
                step = (i_end - i_begin) // div
                for i_cut in range(i_begin, i_end, step):
                    naive_begin = i_cut
                    naive_end = min(i_cut + step, i_end)
                    child = Section(
                        f"Quiz {quiz_keys[naive_begin]}-{quiz_keys[naive_end - 1]}",
                        [],
                    )
                    child.parent = root
                    root.children.append(child)
                    recursive_sectioning(
                        child, i_cut, i_cut + div, div, max_leaf=max_leaf
                    )

        recursive_sectioning(self._quiz_section, 0, len(quiz_keys), 5)

    def _prepare_sorted_section(self, files: Files):
        """
        Prepare sorted section of nav.
        """

        self._sorted_section.children.clear()

        # Sorted posts
        for file in files.documentation_pages():
            page = file.page
            if page is None:
                continue
            elif self._is_recent_posts_page(page) or self._is_most_viewed_posts_page(
                page
            ):
                self._sorted_section.children.append(page)
                page.parent = self._sorted_section

        # Random blog
        self._sorted_section.children.append(Link("Random", "/random/blog.html"))

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

        # Navigation
        self._series_section.children.clear()
        for category, series_index_page in sorted(series_index_pages.items()):
            self._series_section.children.append(series_index_page)
            series_index_page.parent = self._series_section
            for page in used_pages[category]:
                page.parent = series_index_page  # type: ignore[assignment]

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
                raise ValueError("Validation failed, keys are different")

            del self._views[title]
            if (
                not title.endswith(constants.TITLE_SUFFIX)
                and title != constants.TITLE_SUFFIX[3:]  # Index Page
            ):
                logger.debug(f'Invalid page title "{title}" is removed from views data')
            else:
                if constants.TITLE_PREFIX.match(title):  # Remove prefix
                    title = ".".join(title.split(".", 1)[1:])
                title = (  # Remove suffix; If no suffix is found, use default
                    title.strip().replace(constants.TITLE_SUFFIX, "")
                    or constants.INDEX_TITLE
                ).lower()
                if title in self._views:
                    self._views[title] = self.aggregate_views(self._views[title], views)
                else:
                    self._views[title] = views

        logger.debug("Cleaned views = %s", self._views)

    def _get_views_by_titles(self, page: Page) -> int:
        """
        Get all views from given `page`.
        """
        result = 0
        for alternative_title in set(
            dict_get(page.meta, "alternative_titles", default=[]) + [page.title]
        ):
            if constants.TITLE_PREFIX.match(alternative_title):
                alternative_title = ".".join(alternative_title.split(".", 1)[1:])
            alternative_title = alternative_title.lower().strip()
            added = dict_get(self._views, alternative_title, "views", default=0)
            logger.debug("Result += %d from title '%s'", added, alternative_title)
            result += added
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
            if file.abs_src_path is not None and file.abs_src_path.startswith("/tmp/"):
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

        # Random redirection
        files.append(self._create_tempfile(config, "random", "blog.html"))
        files.append(self._create_tempfile(config, "random", "quiz.html"))

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
        assert file.abs_src_path is not None
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
        views = dict_get(post.meta, "views")
        edit_history_url = dict_get(post.meta, "edit_history")

        metadata_updated_date = datestr(
            updated_date, dict_get(post.meta, "commit", "updated")
        )
        metadata_created_date = datestr(
            original_date or created_date,
            dict_get(post.meta, "commit", "created") if original_date is None else None,
        )
        metadata_views = views if views > 0 else constants.METADATA_NOT_AVAILABLE
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
                "material-eye-plus" if views else "material-eye-remove",
                "octicons-git-commit-16",
                metadata_updated_date,
                metadata_created_date,
                metadata_views,
                metadata_history,
                "material-calendar-edit",
                metadata_updated_date,
                "material-calendar-plus",
                metadata_created_date,
                "material-eye-plus" if views else "material-eye-remove",
                metadata_views,
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

        contents: list[str] = []
        post_pointer: int = 0
        for index in range(1, self.pop_category_id(posts[-1].title) + 1):
            if (series, index) in self._blog_post_proxies:
                proxy_page = self._blog_post_proxies[(series, index)]
                proxy_category = self.get_category(proxy_page.file, abbreviated=True)
                proxy_index = self.pop_category_id(proxy_page.title)
                contents.append(
                    "### **[%s %d. (Moved)](%s)**"
                    % (series, index, proxy_page.canonical_url)
                )
                contents.append(
                    "This post is moved to **[%s %d](%s)**."
                    % (proxy_category, proxy_index, proxy_page.canonical_url)
                )
            elif index == self.pop_category_id(posts[post_pointer].title):
                contents.extend(self._get_page_excerpt(posts[post_pointer], config))
                post_pointer += 1
            else:
                continue

            contents.append("---")

        return "\n\n".join(
            [
                markdown,
                constants.SERIES_INDEX_PREFIX % (series, series),
                "---",
            ]
            + contents
        )

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

    @staticmethod
    def common_meta_procedure_on_special_pages(
        page: Page,
        delete_comments: bool = True,
        delete_views: bool = True,
        delete_search: bool = True,
    ) -> None:
        """
        Common procedure on special pages; Modifying some metadata.
        """
        if delete_comments:
            page.meta["no_comments"] = True
        if delete_views and "views" in page.meta:
            del page.meta["views"]
        if delete_search:
            dict_merge_inplace(page.meta, {"search": {"exclude": True}})

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
            assert page.file.abs_src_path is not None
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
        except (FileNotFoundError, AssertionError):
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

        # -------------------------------------------
        # Blog posts
        if self._is_blog_post_page(page):
            # Raise error on no excerpt
            if constants.EXCERPT_DIVIDER not in markdown:
                raise PluginError(
                    "Page '%s' does not have EXCERPT DIVIDER '%s'"
                    % (page.title, constants.EXCERPT_DIVIDER)
                )

            for title_numbering in page.meta.get("moved_from", []):
                proxy_category = title_numbering.split("-")[0]
                proxy_index = int(title_numbering.split("-")[1])
                self._blog_post_proxies[(proxy_category, proxy_index)] = page

        # -------------------------------------------
        # Non-blog posts

        # Is series index?
        elif self._is_series_index_page(page):
            self.common_meta_procedure_on_special_pages(page)
            series: str = page.file.src_uri.split("/")[-1].replace(".md", "").upper()
            return self._modify_markdown_on_series_index_page(
                markdown, series, files, config
            )

        # If recent posts?
        elif self._is_recent_posts_page(page):
            self.common_meta_procedure_on_special_pages(page, delete_views=False)
            page.meta["title"] = "Recent"
            return self._modify_markdown_on_recent_posts_page(markdown, files, config)

        # If most viewed?
        elif self._is_most_viewed_posts_page(page):
            self.common_meta_procedure_on_special_pages(page, delete_views=False)
            page.meta["title"] = "Most Viewed"
            return self._modify_markdown_on_most_viewed_posts_page(
                markdown, files, config
            )

        # If archives?
        elif self._is_archives_page(page):
            self.common_meta_procedure_on_special_pages(page)
            year = int(page.file.src_uri.split("/")[-1].replace(".md", ""))
            return self._modify_markdown_on_archives_page(year, markdown, files, config)

        # If quiz?
        elif info := self._is_quiz_page(page):
            self.common_meta_procedure_on_special_pages(
                page,
                delete_comments=(info[1] == "question"),
                delete_views=False,
            )
            self._quiz_proxies[info] = page
            if info[1] == "question":
                markdown += constants.QUIZ_QUESTION_SUFFIX
            elif info[1] == "answer":
                markdown += constants.QUIZ_ANSWER_SUFFIX

        # -------------------------------------------
        # If not returned yet(normal blog post, unknown type page, etc),
        # then following this logic.

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

        def insert(target_index: int, target_section: Section) -> int:
            iterable.insert(target_index, target_section)
            target_section.parent = section if isinstance(section, Section) else None
            return target_index + 1

        for i, item in enumerate(iterable):
            if isinstance(item, Page) and item.url in ("", "/"):
                if self._root_found_on_nav:
                    raise PluginError("Found duplicated root page entries")
                logger.debug("Entry of root page found: %s", item)
                self._root_found_on_nav = True

                target_index = i + 1
                target_index = insert(target_index, self._series_section)
                target_index = insert(target_index, self._archives_section)
                target_index = insert(target_index, self._sorted_section)
                target_index = insert(target_index, self._quiz_section)

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

    def _modify_random_redirections(self, files: Files) -> None:
        """
        Modify random redirection pages.
        """
        for file in files:
            if constants.RE_RANDOM_REDIRECT_FINDER.match(file.src_uri):
                filename = file.src_uri.split("/")[-1].replace(".html", "")
                targets: list[Page] = []
                if filename == "blog":
                    targets = list(self._yield_blog_posts(files))
                elif filename == "quiz":
                    targets = [
                        self._quiz_proxies[(qid, qtype)]
                        for qid, qtype in self._quiz_proxies
                        if qtype == "question"
                    ]
                else:
                    raise ValueError("Invalid random redirection type %s" % (filename,))
                file.content_string = constants.RANDOM_REDIRECT_HTML_TEMPLATE % (
                    str([target.abs_url for target in targets]),
                )
                logger.info("Random redirection on %s completed" % (file.src_uri,))

    @event_priority(constants.LATE_EVENT_PRIORITY)
    @skip_if_disabled
    def on_env(
        self, env: Environment, *, config: MkDocsConfig, files: Files
    ) -> Environment | None:
        """
        After all pages are populated, I do followings;

        - Alter global navigation and prev/next page buttons of each page.
        - Modify random redirection pages.
        """
        self._load_series_by_categories(files)
        self._link_archived_pages(files)
        self._link_quiz_pages(files)
        self._prepare_sorted_section(files)
        self._modify_random_redirections(files)
        return None

    @event_priority(constants.LATE_EVENT_PRIORITY)
    def on_shutdown(self) -> None:
        try:
            self._temp_dir.cleanup()
        except Exception:
            pass
