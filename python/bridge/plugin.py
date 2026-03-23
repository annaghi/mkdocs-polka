"""
MkDocs plugin.

Replaces MkDocs' built-in Markdown rendering with polka's
attribute-aware HTML output.
"""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING, Any, Literal

from mkdocs.config.defaults import MkDocsConfig
from mkdocs.plugins import BasePlugin, get_plugin_logger
from mkdocs.structure.files import Files
from mkdocs.structure.pages import Page

from bridge import generate_html

if TYPE_CHECKING:
    from mkdocs.config.defaults import MkDocsConfig
    from mkdocs.structure.files import Files
    from mkdocs.structure.pages import Page


log = get_plugin_logger("[plugin]")


class BridgePlugin(BasePlugin):
    """
    MkDocs plugin that replaces the default Markdown renderer.

    Hooks into the page lifecycle to pre-render Markdown to HTML via
    :func:`generate_html`, bypassing MkDocs' built-in rendering pipeline.
    """

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """
        Initialize plugin and declare instance attributes.
        """
        super().__init__(*args, **kwargs)

        self.is_serve: bool

    def on_startup(self, *, command: Literal["build", "gh-deploy", "serve"], dirty: bool) -> None:
        """
        Set serve mode flag based on command.
        """
        self.is_serve = command == "serve"

    def on_page_markdown(self, markdown: str, *, page: Page, config: MkDocsConfig, files: Files) -> str:
        """
        Generate HTML from Markdown and store in page.meta.

        Returns empty string to bypass MkDocs' Markdown rendering.
        """
        page.meta["is_serve"] = self.is_serve

        icon_dirs = []
        custom_dir = config.theme.custom_dir
        if custom_dir:
            custom_icon_dir_candidate = Path(custom_dir) / ".icons"
            if custom_icon_dir_candidate.exists():
                icon_dirs.append(str(custom_icon_dir_candidate))

        page.meta["_html"] = generate_html(page.file.name, markdown, icon_dirs)
        return ""

    def on_page_content(self, html: str, *, page: Page, config: MkDocsConfig, files: Files) -> str:
        """
        Return the pre-rendered HTML from page.meta.
        """
        return page.meta.pop("_html", html)
