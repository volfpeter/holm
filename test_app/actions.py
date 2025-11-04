from holm import action


@action.get()
@action.get("/get/wl", use_layout=True)
@action.get("/get/wlm", use_layout=True, metadata={"title": "GET action title"})
def get() -> str:
    return "GET action"


@action.post()
@action.post("/post/wl", use_layout=True)
@action.post("/post/wlm", use_layout=True, metadata={"title": "POST action title"})
def post() -> str:
    return "POST action"


@action.put()
@action.put("/put/wl", use_layout=True)
@action.put("/put/wlm", use_layout=True, metadata=lambda: {"title": "PUT action title"})
def put() -> str:
    return "PUT action"


@action.patch()
@action.patch("/patch/wl", use_layout=True)
@action.patch("/patch/wlm", use_layout=True, metadata=lambda: {"title": "PATCH action title"})
def patch() -> str:
    return "PATCH action"


@action.delete()
@action.delete("/delete/wl", use_layout=True)
@action.delete("/delete/wlm", use_layout=True, metadata={"title": "DELETE action title"})
def delete() -> str:
    return "DELETE action"


def _in_layout(rendered_action: str, title: str = "App") -> str:
    return "\n".join(
        [
            "<!DOCTYPE html><html >",
            "<head >",
            f"<title >{title}</title>",
            '<meta charset="utf-8"/>',
            '<meta name="viewport" content="width=device-width, initial-scale=1"/>',
            '<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@picocss/pico@2/css/pico.min.css"/>',
            "</head>",
            '<body class="container-fluid">',
            '<header class="container">',
            "<p >Root layout header</p>",
            "</header>",
            '<main class="container">',
            rendered_action,
            "</main>",
            '<footer class="container">',
            "Root layout footer",
            "</footer>",
            "</body>",
            "</html>",
        ]
    )


class RenderedAction:
    class get:
        without_layout = "GET action"
        use_layout = _in_layout(without_layout)
        use_layout_and_metadata = _in_layout(without_layout, f"{without_layout} title")

    class post:
        without_layout = "POST action"
        use_layout = _in_layout(without_layout)
        use_layout_and_metadata = _in_layout(without_layout, f"{without_layout} title")

    class put:
        without_layout = "PUT action"
        use_layout = _in_layout(without_layout)
        use_layout_and_metadata = _in_layout(without_layout, f"{without_layout} title")

    class patch:
        without_layout = "PATCH action"
        use_layout = _in_layout(without_layout)
        use_layout_and_metadata = _in_layout(without_layout, f"{without_layout} title")

    class delete:
        without_layout = "DELETE action"
        use_layout = _in_layout(without_layout)
        use_layout_and_metadata = _in_layout(without_layout, f"{without_layout} title")
