import json
import os
import re
import typing
from datetime import datetime
from pathlib import Path

from jinja2 import Environment
from mkdocs.config.defaults import MkDocsConfig
from mkdocs.exceptions import PluginError
from mkdocs.plugins import BasePlugin, event_priority, get_plugin_logger
from mkdocs.structure.files import File, Files
from mkdocs.structure.nav import Navigation, Section, StructureItem
from mkdocs.structure.pages import Page

from .config import McDicBlogPluginConfig
from .constants import EARLY_EVENT_PRIORITY, LATE_EVENT_PRIORITY
from .ga4 import ViewDataValue
from .ga4 import fetch_data as fetch_ga4_views_data
from .ga4 import get_client as get_ga4_client
from .git import get_date_from_git

logger = get_plugin_logger("mcdic")


P = typing.ParamSpec("P")
Ret = typing.TypeVar("Ret")
McDicBlogMethod = typing.Callable[P, Ret | None]


def skip_if_disabled(
    method: McDicBlogMethod[typing.Concatenate["McDicBlogPlugin", P], Ret | None]
) -> McDicBlogMethod[typing.Concatenate["McDicBlogPlugin", P], Ret | None]:
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

    TITLE_SUFFIX: typing.Final[str] = " - McDic's Blog"
    RE_POSTFINDER: typing.Final[re.Pattern] = re.compile(
        r"^posts\/[a-zA-Z\-]+\/[a-zA-Z\-]*[0-9]+\.md$"
    )

    def __init__(self) -> None:
        super().__init__()
        self._views: dict[str, ViewDataValue] = {}
        self._force_update_views: bool = False
        self._series: dict[str, Section] = {}
        self._root_found_on_nav: bool = False
        self._series_section: Section = Section("Series", [])

    @staticmethod
    def aggregate_views(obj0: ViewDataValue, *objs: ViewDataValue) -> ViewDataValue:
        """
        Aggregate view statistics.
        """
        result = obj0.copy()
        for obj in objs:
            for key in obj:
                result[key] = max(result[key], obj[key])  # type: ignore[literal-required] # noqa: E501
        return result

    @staticmethod
    def get_category(file_or_page: File | Page) -> str | None:
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
        return categories[0] if categories else None

    def _load_series_by_categories(self, files: Files):
        """
        Load series by categories.
        This method is carefully implemented to
        not duplicate entries on the navigation.
        """

        used_pages: dict[str, list[Page]] = {}

        for file in files:
            if file.page is None:
                continue

            category = self.get_category(file)
            if category is None:
                continue
            elif category not in self._series:
                self._series[category] = Section(category, [])

            if category not in used_pages:
                used_pages[category] = []
            used_pages[category].append(file.page)

            # Removing all prev/next pages is needed
            file.page.parent = self._series[category]
            file.page.previous_page = None
            file.page.next_page = None

        for category, this_section in self._series.items():
            pages: list[Page] = used_pages[category]  # type: ignore[assignment]
            this_section.children = pages  # type: ignore[assignment]
            pages.sort(
                key=(
                    lambda page: (
                        self.pop_category_id(page.title)
                        if isinstance(page.title, str)
                        else -1
                    )
                )
            )
            for i, page in enumerate(pages):
                page.previous_page = pages[i - 1] if i > 0 else None
                page.next_page = pages[i + 1] if i + 1 < len(pages) else None
                page.parent = this_section
            if this_section.parent is None:
                this_section.parent = self._series_section
                self._series_section.children.append(this_section)
            logger.info("Loaded %s series", category)

        self._series_section.children.sort(key=(lambda item: item.title or ""))
        logger.info("Loaded all series")

    @staticmethod
    def pop_category_id(title: str) -> int:
        """
        Pop category id, if applicable.
        """
        return int(title.split(".")[0].split(" ")[-1])

    @event_priority(EARLY_EVENT_PRIORITY)
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
        if command == "gh-deploy":
            self._force_update_views = True

    def _get_views(self) -> None:
        """
        Get views data.
        """

        if self.config.post_views:
            self._force_update_views = (
                self._force_update_views or self.config.post_views.forced_update
            )

        if (
            self.config.post_views
            and self.config.post_views.local_path
            and not self._force_update_views
        ):
            with open(self.config.post_views.local_path) as post_views_file:
                self._views = json.load(post_views_file)
        elif self._force_update_views:
            logger.info("Views data is forcibly updating..")
            client = get_ga4_client()
            self._views = fetch_ga4_views_data(client)

        for title, views in list(self._views.items()):
            if not isinstance(views, dict) or set(views.keys()) != {
                "views",
                "total_users",
            }:
                raise ValueError(
                    f"Validation failed, views = {views} is not an integer"
                )

            del self._views[title]
            if not title.endswith(" - McDic's Blog"):
                logger.info(f'Invalid page title "{title}" is removed from views data')
            else:
                replaced_title = title.replace(self.TITLE_SUFFIX, "")
                if replaced_title in self._views:
                    self._views[replaced_title] = self.aggregate_views(
                        self._views[replaced_title], views
                    )
                else:
                    self._views[replaced_title] = views

    @event_priority(EARLY_EVENT_PRIORITY)
    @skip_if_disabled
    def on_config(self, config: MkDocsConfig) -> MkDocsConfig | None:
        """
        Load McDic Blog configs.
        """
        self._get_views()
        return None

    @event_priority(EARLY_EVENT_PRIORITY)
    @skip_if_disabled
    def on_files(self, files: Files, *, config: MkDocsConfig) -> Files | None:
        """
        Editing file destination wouldn't work properly after this event,
        therefore I edit some files here.
        """
        logger.debug("site_dir = %s", config.site_dir)

        for file in files.documentation_pages():
            if self.RE_POSTFINDER.match(file.src_path):
                logger.debug(
                    "Originally, src = %s, dest_path = %s, "
                    "abs_dest_path = %s, dest_uri = %s, url = %s",
                    file.src_path,
                    file.dest_path,
                    file.abs_dest_path,
                    file.dest_uri,
                    file.url,
                )
                _, series, filename = file.src_path.split("/")
                index: int = int(filename.replace(series, "").replace(".md", ""))
                file.dest_uri = f"series/{series}/{index}/index.html"
                file.abs_dest_path = os.path.join(config.site_dir, file.dest_path)
                file.url = f"series/{series}/{index}"

        return files

    @staticmethod
    def _get_git_date(file: File) -> tuple[datetime, datetime]:
        """
        Get created date and the last updated date of a file from git system.
        """
        path: Path = Path(file.abs_src_path)
        return get_date_from_git(path, "created"), get_date_from_git(path, "updated")

    @event_priority(LATE_EVENT_PRIORITY)
    @skip_if_disabled
    def on_page_markdown(
        self, markdown: str, *, page: Page, config: MkDocsConfig, files: Files
    ) -> str | None:
        """
        Since this is the earliest possible moment where metadata is available,
        I directly modify the metadata here.
        """
        page.meta["views"] = self._views.get(page.title, None)
        logger.debug(
            "Getting git date of page %s.. (%s)", page.title, page.file.abs_src_path
        )
        created_date, updated_date = self._get_git_date(page.file)
        page.meta["date"] = {
            "created": created_date.strftime(self.config.date_format),
            "updated": updated_date.strftime(self.config.date_format),
        }
        return None

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
                iterable.insert(i + 1, self._series_section)
                self._series_section.parent = (
                    section if isinstance(section, Section) else None
                )
            elif isinstance(item, Section):
                self._modify_nav_on_root_page(item)

    @event_priority(LATE_EVENT_PRIORITY)
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

    @event_priority(LATE_EVENT_PRIORITY)
    @skip_if_disabled
    def on_env(
        self, env: Environment, *, config: MkDocsConfig, files: Files
    ) -> Environment | None:
        """
        After all pages are populated, I change prev/next page buttons here.
        """
        self._load_series_by_categories(files)
        return None
