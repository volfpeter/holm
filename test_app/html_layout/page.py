from htmy import Component, html

metadata: dict[str, str] = {
    "title": "HTML Layout Test Page",
    "description": "Testing layout with snippet and text processor",
}


def page() -> Component:
    return html.div("Page content in HTML layout")


rendered_page_with_html_layout = """
<div>
    <h1>HTML Layout</h1>
    <h4>Page title: {metadata[title]}</h4>
    <p>Description: {metadata[description]}</p>
    <p>Request method: GET</p>
    <div >\nPage content in HTML layout\n</div>
</div>
""".strip().format(metadata=metadata)
