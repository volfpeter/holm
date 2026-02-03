from fasthx.htmy import CurrentRequest
from htmy import ComponentType, Context, component, html

highlight_style = "text-decoration: underline; text-decoration-thickness: 2px;"
"""
Inline style for highlighting the navigation item corresponding to the current page.
"""


def nav_item(text: str, *, href: str, current_path: str) -> ComponentType:
    """
    Creates a nav item with conditional styling if the link matches the current path.
    """
    return html.li(
        html.a(
            text,
            href=href,
            style=highlight_style if current_path == href else None,
        ),
    )


@component.context_only
def navbar(context: Context) -> ComponentType:
    """
    Navigation component that highlights the item corresponding to the current page.
    """
    request = CurrentRequest.from_context(context)
    current_path = request.url.path
    if current_path != "/":
        current_path = current_path.rstrip("/")

    return html.nav(
        html.ul(
            nav_item("Home", href="/", current_path=current_path),
            nav_item("About", href="/about", current_path=current_path),
        )
    )
