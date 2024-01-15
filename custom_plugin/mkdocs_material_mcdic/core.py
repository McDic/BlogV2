import json
import typing
from pathlib import Path
from typing import Literal

from mkdocs.config import config_options as ConfigOptions
from mkdocs.config.base import Config, ConfigErrors, ConfigWarnings
from mkdocs.config.defaults import MkDocsConfig
from mkdocs.exceptions import PluginError
from mkdocs.plugins import BasePlugin, event_priority, get_plugin_logger
from mkdocs.structure.files import Files
from mkdocs.structure.pages import Page

from .constants import MY_EVENT_PRIORITY

logger = get_plugin_logger("mcdic")


class ViewDataValue(typing.TypedDict):
    """
    Represents view data value.
    """

    views: int
    total_users: int


class McDicBlogPluginConfig(Config):
    """
    Config class for McDic's Blog plugin.
    """

    enabled = ConfigOptions.Type(bool, default=True)
    post_views = ConfigOptions.Optional(ConfigOptions.File(exists=True))


P = typing.ParamSpec("P")
Ret = typing.TypeVar("Ret")
McDicBlogMethod = typing.Callable[P, Ret | None]


def skip_if_disabled(
    method: McDicBlogMethod[typing.Concatenate["McDicBlogPlugin", P], Ret]
) -> McDicBlogMethod[typing.Concatenate["McDicBlogPlugin", P], Ret]:
    """
    Make method be skipped if plugin is disabled.
    """

    def new_method(
        self: "McDicBlogPlugin", *args: P.args, **kwargs: P.kwargs
    ) -> Ret | None:
        return method(self, *args, **kwargs) if self.config.enabled else None

    return new_method


def aggregate_views(obj0: ViewDataValue, *objs: ViewDataValue) -> ViewDataValue:
    """
    Aggregate view statistics.
    """
    result = obj0.copy()
    for obj in objs:
        for key in obj:
            result[key] = max(result[key], obj[key])  # type: ignore[literal-required]
    return result


class McDicBlogPlugin(BasePlugin[McDicBlogPluginConfig]):
    """
    A plugin solely developed for [McDic's Blog](https://blog.mcdic.net).
    See [plugins/events](https://www.mkdocs.org/dev-guide/plugins/#events).
    """

    TITLE_SUFFIX: typing.Final[str] = " - McDic's Blog"

    def __init__(self) -> None:
        super().__init__()
        self.views: dict[str, ViewDataValue] = {}

    @staticmethod
    def pop_category_id(title: str) -> int:
        """
        Pop category id, if applicable.
        """
        return int(title.split(".")[0].split(" ")[-1])

    def load_config(
        self, options: dict[str, typing.Any], config_file_path: str | None = None
    ) -> tuple[ConfigErrors, ConfigWarnings]:
        return super().load_config(options, config_file_path)

    @event_priority(MY_EVENT_PRIORITY)
    @skip_if_disabled
    def on_config(self, config: MkDocsConfig) -> MkDocsConfig | None:
        if self.config.post_views:
            with open(self.config.post_views) as post_views_file:
                self.views = json.load(post_views_file)
        for title, views in list(self.views.items()):
            if not isinstance(views, dict) or set(views.keys()) != {
                "views",
                "total_users",
            }:
                raise ValueError(
                    f"Validation failed, views = {views} is not an integer"
                )

            del self.views[title]
            if not title.endswith(" - McDic's Blog"):
                logger.info(f'Invalid page title "{title}" is removed from views data')
            else:
                replaced_title = title.replace(self.TITLE_SUFFIX, "")
                if replaced_title in self.views:
                    self.views[replaced_title] = aggregate_views(
                        self.views[replaced_title], views
                    )
                else:
                    self.views[replaced_title] = views

        return config

    @event_priority(MY_EVENT_PRIORITY)
    @skip_if_disabled
    def on_page_markdown(
        self, markdown: str, *, page: Page, config: MkDocsConfig, files: Files
    ) -> str | None:
        page.meta["views"] = self.views.get(page.title, None)
        return markdown

    @event_priority(MY_EVENT_PRIORITY)
    @skip_if_disabled
    def on_page_content(
        self, html: str, *, page: Page, config: MkDocsConfig, files: Files
    ) -> str | None:
        relative_pages: list[Page] = []
        this_categories: set[str] = set(page.meta.get("categories", []))

        if len(this_categories) > 1:
            raise PluginError(
                "McDic's blog plugin is not compatible with multi-category posts"
            )

        elif len(this_categories) == 1:  # Fetch prev/next pages
            this_category = this_categories.pop()
            logger.info(
                'Found unique category "%s" from page "%s"'
                % (this_category, page.title)
            )
            for file in files:
                if file.page is None:
                    continue
                elif this_category in file.page.meta.get("categories", []):
                    relative_pages.append(file.page)
            relative_pages.sort(
                key=(
                    lambda page: self.pop_category_id(page.title)
                    if isinstance(page.title, str)
                    else "unknown"
                )
            )
            index = relative_pages.index(page)
            page.previous_page = relative_pages[index - 1] if index > 0 else None
            page.next_page = (
                relative_pages[index + 1] if index + 1 < len(relative_pages) else None
            )

        else:  # No siblings
            page.previous_page = None
            page.next_page = None

        logger.debug(f'Page title = "{page.title}", meta = {page.meta}')
        return html
