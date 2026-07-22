from holm import JinjaTemplate

metadata = {"title": "Jinja escaping"}


def page() -> JinjaTemplate:
    return JinjaTemplate(
        "test_app/jinja_escaping/escaped.jinja",
        jinja_context={"name": "<script>alert(1)</script>"},
    )
