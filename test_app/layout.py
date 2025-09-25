from htmy import Component, ComponentType, Context, component, html

from holm import Metadata


@component
def layout(children: ComponentType, context: Context) -> Component:
    """Layout that is a plain, sync HTMY component."""
    metadata = Metadata.from_context(context)

    return (
        html.DOCTYPE.html,
        html.html(
            html.head(
                html.title(metadata.get("title", "App")),
                html.meta(charset="utf-8"),
                html.meta(name="viewport", content="width=device-width, initial-scale=1"),
                html.link(  # Use PicoCSS to add some default styling.
                    rel="stylesheet", href="https://cdn.jsdelivr.net/npm/@picocss/pico@2/css/pico.min.css"
                ),
            ),
            html.body(
                html.header(html.p("Root layout header"), class_="container"),
                html.main(children, class_="container"),
                html.footer("Root layout footer", class_="container"),
                class_="container-fluid",
            ),
        ),
    )
