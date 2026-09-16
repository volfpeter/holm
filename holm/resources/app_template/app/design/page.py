from pathlib import Path

from htmy import ComponentType, Snippet

_page_html = Path(__file__).parent / "page.html"

metadata = {"title": "Design"}


def page() -> ComponentType:
    """The design page at /design, based on DESIGN.md."""
    return Snippet(_page_html)
