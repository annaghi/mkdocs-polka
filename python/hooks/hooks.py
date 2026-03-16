"""
MkDocs hooks.

Replaces MkDocs' built-in Markdown rendering with polka's
attribute-aware HTML output.
"""

from pathlib import Path

from mkdocs.config.defaults import MkDocsConfig
from mkdocs.structure.files import Files
from mkdocs.structure.pages import Page

from hooks import generate_html


def on_page_markdown(markdown: str, *, page: Page, config: MkDocsConfig, files: Files) -> str:
    """
    Generate HTML from Markdown and store in page.meta.

    Returns empty string to bypass MkDocs' Markdown rendering.
    """
    icon_dirs = []

    custom_dir = config.theme.custom_dir
    if custom_dir:
        custom_icon_dir_candidate = Path(custom_dir) / ".icons"
        if custom_icon_dir_candidate.exists():
            icon_dirs.append(str(custom_icon_dir_candidate))

    page.meta["_html"] = generate_html(page.file.name, markdown, icon_dirs)
    return ""


def on_page_content(html: str, *, page: Page, config: MkDocsConfig, files: Files) -> str:
    """
    Return the pre-rendered HTML from page.meta.
    """
    return page.meta.pop("_html", html)
