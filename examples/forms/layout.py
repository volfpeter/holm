from fastapi import Request
from htmy import Component, ComponentType, Context, XBool, component, html

from holm import Metadata


@component.context_only
def _head(context: Context) -> html.head:
    """
    Helper component that returns the entire head element of the page.

    It uses `Metadata` to correctly set the page title. This way we do not need
    to access the `htmy` context in the layout itself, so that doesn't need to
    be a `htmy` component, it can be a simple `holm` layout function with dependencies.
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


def layout(children: ComponentType, request: Request, q: str = "") -> Component:
    """Root layout wrapping all pages."""
    return (
        html.DOCTYPE.html,
        html.html(
            # Use our _head component.
            _head(),
            html.body(
                html.header(
                    # Global search form, present in all pages, always submitted with a GET request to
                    # the current URL. The q query parameter contains the search query, this is why
                    # the layout has a q query parameter dependency. Pages can also use this dependency
                    # to filter their content.
                    html.form(
                        # This is the form for searching TODOs.
                        # It is submitted to the current URL by default with a HTTP GET request,
                        # so the page itself will handle the form submission.
                        # This is why the page has an optional title query parameter dependency,
                        # whose name matches the name of the input field.
                        html.input_(
                            type="search",
                            name="q",
                            # Keep the value of the input field.
                            value=q,
                            # Focus automatically after GET requests. autofocus is a bool HTML
                            # attribute, so to set it to False, we must use the XBool utility.
                            autofocus=XBool.true if request.method == "GET" else XBool.false,
                            placeholder="Search by title",
                        ),
                        html.button("Find", type="submit"),
                        role="search",
                    ),
                    class_="container",
                ),
                html.main(children, class_="container"),
                html.footer(html.p("© 2025 TODO App"), class_="container"),
                class_="container-fluid",
            ),
        ),
    )
