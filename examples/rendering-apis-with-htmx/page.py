from htmy import Component, html

# Static metadata for this page
metadata = {"title": "Home | My App"}


def page() -> Component:
    """Home page content."""
    return html.div(
        html.h1(
            "Welcome to My App",
            hx_get="/welcome-message",
            hx_trigger="every 2s",
        ),
        html.p("This is a minimal holm application demonstrating:"),
        html.ul(
            html.li("File-system based routing"),
            html.li("Automatic layout composition"),
            html.li("Dynamic metadata"),
            html.li("Server-side rendering with htmy"),
        ),
        html.div(
            html.a("Learn more about us", href="/about"),
            hx_boost="true",  # Explicit hx-boost for this link
        ),
    )
