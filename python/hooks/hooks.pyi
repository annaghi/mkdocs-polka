def version() -> str:
    """
    Return package version string.
    """

def generate_html(filename: str, content: str, icon_dirs: list[str] | None = None) -> str:
    """
    Generate HTML from Markdown with jotdown-style attribute support.
    """

# ----------------------------------------------------------------------------

__all__ = ["generate_html", "version"]
