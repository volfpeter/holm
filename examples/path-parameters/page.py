from htmy import Component, html

# Static metadata for this page
metadata = {"title": "Dashboard"}


def page() -> Component:
    """Home page content."""
    return html.div(
        html.h1("Welcome to Admin App"),
        html.p("This is a minimal holm application demonstrating:"),
        html.ul(
            html.li("How to use path parameters, also known as dynamic routing"),
            html.li("File-system based routing with dynamic routes"),
        ),
        html.a("Navigate to the User page to start exploring", href="/user"),
    )
