from holm import action


@action.get()
@action.get("/get/wl", with_layout=True)
@action.get("/get/wlm", with_layout=True, metadata={"title": "GET action title"})
def get() -> str:
    return "GET action"


@action.post()
@action.post("/post/wl", with_layout=True)
@action.post("/post/wlm", with_layout=True, metadata={"title": "POST action title"})
def post() -> str:
    return "POST action"


@action.put()
@action.put("/put/wl", with_layout=True)
@action.put("/put/wlm", with_layout=True, metadata=lambda: {"title": "PUT action title"})
def put() -> str:
    return "PUT action"


@action.patch()
@action.patch("/patch/wl", with_layout=True)
@action.patch("/patch/wlm", with_layout=True, metadata=lambda: {"title": "PATCH action title"})
def patch() -> str:
    return "PATCH action"


@action.delete()
@action.delete("/delete/wl", with_layout=True)
@action.delete("/delete/wlm", with_layout=True, metadata={"title": "DELETE action title"})
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
        with_layout = _in_layout(without_layout)
        with_layout_and_metadata = _in_layout(without_layout, f"{without_layout} title")

    class post:
        without_layout = "POST action"
        with_layout = _in_layout(without_layout)
        with_layout_and_metadata = _in_layout(without_layout, f"{without_layout} title")

    class put:
        without_layout = "PUT action"
        with_layout = _in_layout(without_layout)
        with_layout_and_metadata = _in_layout(without_layout, f"{without_layout} title")

    class patch:
        without_layout = "PATCH action"
        with_layout = _in_layout(without_layout)
        with_layout_and_metadata = _in_layout(without_layout, f"{without_layout} title")

    class delete:
        without_layout = "DELETE action"
        with_layout = _in_layout(without_layout)
        with_layout_and_metadata = _in_layout(without_layout, f"{without_layout} title")
