from fasthx.htmy import CurrentRequest
from htmy import ComponentType, Context, component, html


def nav_item(text: str, *, href: str, current_path: str) -> ComponentType:
    style = "font-weight: bold;" if current_path == href else None
    return html.li(html.a(text, href=href, style=style))


@component.context_only
def navbar(context: Context) -> ComponentType:
    request = CurrentRequest.from_context(context)
    current_path = request.url.path.rstrip("/") or "/"
    return html.nav(
        html.ul(
            nav_item("Home", href="/", current_path=current_path),
            nav_item("Slots", href="/jinja-slots/", current_path=current_path),
        )
    )


def custom_navbar() -> ComponentType:
    """Page-provided navbar that overrides the default slot."""
    return html.nav(html.ul(html.li(html.a("Custom navbar", href="/"))))
