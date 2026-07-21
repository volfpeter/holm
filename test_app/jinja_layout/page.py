from htmy import Component, html

metadata: dict[str, str] = {
    "title": "HTML Layout Test Page",
    "description": "Testing layout with jinja and metadata projection",
}


def page() -> Component:
    return html.div("Page content in HTML layout")


rendered_page = (
    "<div>\n"
    "    <h1>HTML Layout</h1>\n"
    f"    <h4>Page title: {metadata['title']}</h4>\n"
    f"    <p>Description: {metadata['description']}</p>\n"
    "    <p>Request method: GET</p>\n"
    "    <div >\n"
    "Page content in HTML layout\n"
    "</div>\n"
    "</div>"
)
