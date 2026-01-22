from fastapi import Request
from htmy import Component, ComponentType, Context, XBool, component, html

from holm import Metadata


@component.context_only
def head(context: Context) -> ComponentType:
    """
    Helper component that returns the entire head element of the page.

    It uses `Metadata` to correctly set the page title. This way we do not
    need to access the `htmy` context in the layout itself, so the layout
    doesn't need to be a `htmy` component, it can be a simple `holm` layout
    function with dependencies.
    """
    metadata = Metadata.from_context(context)
    return html.head(
        html.title(metadata.get("title", "TODO App")),
        html.meta(charset="utf-8"),
        html.meta(name="viewport", content="width=device-width, initial-scale=1"),
        html.link(  # Use PicoCSS to add some default styling.
            rel="stylesheet", href="https://cdn.jsdelivr.net/npm/@picocss/pico@2/css/pico.min.css"
        ),
    )


def search_form(q: str, *, autofocus: bool) -> ComponentType:
    """
    Search form for the layout.

    Arguments:
        q: The current value of the `q` input.
        autofocus: Whether the search input should be focused on page load.
    """
    return html.form(
        html.input_(
            type="search",
            name="q",  # The name of our filter query parameter.
            value=q,  # Keep the value of the input field.
            placeholder="Search...",
            # Focus automatically after GET requests. autofocus is a bool HTML
            # attribute, so to disable it, we must either omit the attribute or
            # use the XBool htmy utility.
            autofocus=XBool.true if autofocus else XBool.false,
        ),
        html.button("Find", type="submit"),
        role="search",
    )


def layout(children: ComponentType, request: Request, q: str = "") -> Component:
    """Root layout wrapping all pages."""
    return (
        html.DOCTYPE.html,
        html.html(
            # Use our head component.
            head(),
            html.body(
                html.header(
                    # Global search form, present in all pages, always submitted
                    # with a GET request to the current URL. The input named "q"
                    # contains the search query in the HTML, this is why the
                    # layout has a matching q query parameter dependency.
                    # Pages can use the same dependency for filtering.
                    search_form(q, autofocus=request.method == "GET"),
                    class_="container",
                ),
                html.main(children, class_="container"),
                html.footer(html.p("© 2026 TODO App"), class_="container"),
                class_="container-fluid",
            ),
        ),
    )
