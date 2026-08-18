from pathlib import Path

from htmy import ComponentType, Snippet

_page_html = Path(__file__).parent / "page.html"


def page() -> ComponentType:
    """Home page."""
    return Snippet(_page_html)
