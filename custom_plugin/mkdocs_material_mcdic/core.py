from mkdocs.config.defaults import MkDocsConfig
from mkdocs.exceptions import PluginError
from mkdocs.plugins import BasePlugin, event_priority
from mkdocs.structure.files import Files
from mkdocs.structure.pages import Page
from mkdocs.plugins import get_plugin_logger

from .constants import MY_EVENT_PRIORITY


logger = get_plugin_logger("mcdic")


class McDicBlogPlugin(BasePlugin):
    """
    A plugin solely developed for [McDic's Blog](https://blog.mcdic.net).
    See [mkdocs dev guide - plugins/events](https://www.mkdocs.org/dev-guide/plugins/#events).
    """

    config_scheme = ()

    @staticmethod
    def pop_category_id(title: str) -> int:
        """
        Pop category id, if applicable.
        """
        return int(title.split(".")[0].split(" ")[-1])

    @event_priority(MY_EVENT_PRIORITY)
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
                "Find unique category %s from page %s" % (this_category, page.title)
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

        return html
