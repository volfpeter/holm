from htmy import Component, html

# Static metadata for this page
metadata = {"title": "Home | My App"}


def page() -> dict[str, Component]:
    """Home page content."""
    return {
        # Content for the intro slot of the layout.
        "intro": html.div(
            html.h1("Welcome to My App"),
            html.p("This is a minimal holm application demonstrating:"),
        ),
        # Content for the details slot of the layout.
        "details": html.div(
            html.ul(
                html.li("File-system based routing"),
                html.li("Automatic layout composition"),
                html.li("Dynamic metadata"),
                html.li("Server-side rendering with htmy"),
            ),
            html.a("Learn more about us", href="/about"),
        ),
    }
