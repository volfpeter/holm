from htmy import Component, html


def metadata() -> dict[str, str]:
    return {
        "title": "Dict Slots Test Page",
        "description": "Testing page with dict return value for HTML layout slots.",
    }


def page() -> dict[str, Component]:
    return {
        "header": html.p("Header slot", id="header-slot"),
        "content": html.p("Content slot", id="content-slot"),
        "footer": html.p("Footer slot", id="footer-slot"),
    }


rendered_page_with_html_layout = """
<div id="dict-slots-layout">
    <p id="header-slot">Header slot</p>
    <p id="content-slot">Content slot</p>
    <p id="footer-slot">Footer slot</p>
</div>
""".strip()
