from holm import action


@action.get()
@action.get("/get/wl", with_layout=True)
def get() -> str:
    return "GET action"


@action.post()
@action.post("/post/wl", with_layout=True)
def post() -> str:
    return "POST action"


@action.put()
@action.put("/put/wl", with_layout=True)
def put() -> str:
    return "PUT action"


@action.patch()
@action.patch("/patch/wl", with_layout=True)
def patch() -> str:
    return "PATCH action"


@action.delete()
@action.delete("/delete/wl", with_layout=True)
def delete() -> str:
    return "DELETE action"


def _in_layout(rendered_action: str) -> str:
    return "\n".join(
        [
            "<!DOCTYPE html><html >",
            "<head >",
            "<title >App</title>",
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

    class post:
        without_layout = "POST action"
        with_layout = _in_layout(without_layout)

    class put:
        without_layout = "PUT action"
        with_layout = _in_layout(without_layout)

    class patch:
        without_layout = "PATCH action"
        with_layout = _in_layout(without_layout)

    class delete:
        without_layout = "DELETE action"
        with_layout = _in_layout(without_layout)
