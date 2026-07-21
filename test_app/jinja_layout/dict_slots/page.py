from htmy import Component, html


def metadata() -> dict[str, str]:
    return {
        "title": "Dict Slots Test Page",
        "description": "Testing page with dict return value for Jinja layout slots.",
    }


def page() -> dict[str, Component]:
    return {
        "header": html.p("Header slot", id="header-slot"),
        "content": html.p("Content slot", id="content-slot"),
        "footer": html.p("Footer slot", id="footer-slot"),
    }


rendered_page = (
    '<div id="dict-slots-layout">\n'
    '    <p id="header-slot">Header slot</p>\n'
    '    <p id="content-slot">Content slot</p>\n'
    '    <p id="footer-slot">Footer slot</p>\n'
    "</div>"
)
