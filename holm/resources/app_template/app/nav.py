from fasthx.htmy import CurrentRequest
from htmy import ComponentType, Context, component, html

_LINKS: tuple[tuple[str, str], ...] = (("Design", "/design"), ("Showcase", "/showcase"))


@component.context_only
def nav(ctx: Context) -> ComponentType:
    """Root navigation bar, highlights the link of the current page."""
    path = CurrentRequest.from_context(ctx).url.path.rstrip("/") or "/"
    return html.nav(
        html.a("__holm_name__", href="/", class_="text-lg font-semibold"),
        *(
            html.a(
                label,
                href=href,
                class_="nav-link",
                aria_current="page" if href == path else None,
            )
            for label, href in _LINKS
        ),
        class_="flex items-center gap-5",
    )
