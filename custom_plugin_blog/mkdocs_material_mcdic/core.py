import json
import typing

from mkdocs.config.defaults import MkDocsConfig
from mkdocs.exceptions import PluginError
from mkdocs.plugins import BasePlugin, event_priority, get_plugin_logger
from mkdocs.structure.files import File, Files
from mkdocs.structure.pages import Page

from .config import McDicBlogPluginConfig
from .constants import EARLY_EVENT_PRIORITY, LATE_EVENT_PRIORITY
from .ga4 import ViewDataValue
from .ga4 import fetch_data as fetch_ga4_views_data
from .ga4 import get_client as get_ga4_client

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

    def __init__(self) -> None:
        super().__init__()
        self._views: dict[str, ViewDataValue] = {}
        self._force_update_views: bool = False
        self._series: dict[str, list[Page]] = {}
        self._loaded_series: bool = False

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
        This method is created to sort pages only once efficiently.
        """
        if self._loaded_series:
            return
        self._loaded_series = True

        for file in files:
            if file.page is None:
                continue

            category = self.get_category(file)
            if category is None:
                continue
            elif category not in self._series:
                self._series[category] = []
            self._series[category].append(file.page)

        for pages in self._series.values():
            pages.sort(
                key=(
                    lambda page: (
                        self.pop_category_id(page.title)
                        if isinstance(page.title, str)
                        else -1
                    )
                )
            )

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

    @event_priority(EARLY_EVENT_PRIORITY)
    @skip_if_disabled
    def on_config(self, config: MkDocsConfig) -> MkDocsConfig | None:
        """
        Load McDic Blog configs.
        """

        # =====================================================================
        # Post Views

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

        # =====================================================================
        return None

    @event_priority(EARLY_EVENT_PRIORITY)
    @skip_if_disabled
    def on_page_markdown(
        self, markdown: str, *, page: Page, config: MkDocsConfig, files: Files
    ) -> str | None:
        """
        Since this is the earliest possible moment where metadata is available,
        I directly modify the metadata here.
        """
        page.meta["views"] = self._views.get(page.title, None)
        return None

    @event_priority(LATE_EVENT_PRIORITY)
    @skip_if_disabled
    def on_page_content(
        self, html: str, *, page: Page, config: MkDocsConfig, files: Files
    ) -> str | None:
        """
        This is the latest moment on page populations,
        so I change prev/next page buttons here.
        """

        self._load_series_by_categories(files)
        this_category: str | None = self.get_category(page)

        if this_category:  # Fetch prev/next pages
            relative_pages = self._series[this_category]
            index = relative_pages.index(page)
            page.previous_page = relative_pages[index - 1] if index > 0 else None
            page.next_page = (
                relative_pages[index + 1] if index + 1 < len(relative_pages) else None
            )
        else:  # No siblings
            page.previous_page = None
            page.next_page = None

        logger.debug(
            'Page title = "%s", meta = %s, prev = %s, next = %s',
            page.title,
            page.meta,
            page.previous_page.title if page.previous_page else None,
            page.next_page.title if page.next_page else None,
        )
        return None
