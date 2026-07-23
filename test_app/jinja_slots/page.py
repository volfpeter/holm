from htmy import Component, html

from holm import JinjaTemplate

metadata = {"title": "Jinja slots"}


def page() -> Component:
    return html.div(
        html.h3("Page content"),
        html.p("Renders inside a Jinja layout with default navbar slot."),
        JinjaTemplate("test_app/jinja_slots/leaf.jinja", jinja_context={"name": "Nested leaf"}),
    )
