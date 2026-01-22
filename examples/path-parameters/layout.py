from htmy import Component, ComponentType, Context, component, html

from holm import Metadata


@component
def layout(children: ComponentType, context: Context) -> Component:
    """Root layout wrapping all pages."""
    metadata = Metadata.from_context(context)
    title = "Admin App"
    # Let pages set only their subpage title, and add the application name automatically.
    if subpage_title := metadata.get("title"):
        title = f"{title} | {subpage_title}"

    return (
        html.DOCTYPE.html,
        html.html(
            html.head(
                html.title(title),
                html.meta(charset="utf-8"),
                html.meta(name="viewport", content="width=device-width, initial-scale=1"),
                html.link(  # Use PicoCSS to add some default styling.
                    rel="stylesheet", href="https://cdn.jsdelivr.net/npm/@picocss/pico@2/css/pico.min.css"
                ),
            ),
            html.body(
                html.header(
                    html.nav(
                        html.ul(
                            html.li(html.a("Home", href="/")),
                            html.li(html.a("Users", href="/user")),
                        )
                    ),
                    class_="container",
                ),
                html.main(children, class_="container"),
                html.footer(html.p("© 2026 Admin App"), class_="container"),
                class_="container-fluid",
            ),
        ),
    )
