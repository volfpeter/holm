from htmy import Component, html

from test_app.navbar import custom_navbar

metadata = {"title": "About slots"}


def page() -> dict[str, Component]:
    # Override the default `navbar` slot for this page; explicit slots win over defaults.
    return {
        "navbar": custom_navbar(),
        "children": html.div(
            html.h3("About page"),
            html.p("Overrode the navbar slot; the parent layout keeps the default navbar."),
        ),
    }
