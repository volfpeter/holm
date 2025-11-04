from fastapi import Depends, HTTPException
from htmy import ComponentType, html

from holm import action


def metadata(page_variant: str = "default") -> dict[str, str]:
    return {"title": f"Users page | {page_variant}"}


def page(page_variant: str = "default") -> dict[str, ComponentType]:
    return {
        "main": html.ul(
            html.li("User 1"),
            html.li("User 2"),
            html.li("User 3"),
        ),
        "footer": html.div(
            html.p("Footer content"),
        ),
    }


def _require_token(token: str | None = None) -> None:
    """
    Dependency that requires the client to submit a `token` query parameter.

    If no token is provided, an `HTTPException` is raised with a non-standard status code.
    """
    if not token:
        raise HTTPException(499, "_requires_token called, no token provided")


@action.get(dependencies=[Depends(_require_token)])
@action.get("/a/list_users", dependencies=[Depends(_require_token)])
def list_users() -> ComponentType:
    return html.ul(
        html.li("User 1"),
        html.li("User 2"),
        html.li("User 3"),
    )


@action.post(dependencies=[Depends(_require_token)])
@action.post("/a/create_user", dependencies=[Depends(_require_token)])
async def create_user() -> ComponentType:
    return html.p("User created")


@action.put(dependencies=[Depends(_require_token)])
@action.put("/a/update_user_with_put", dependencies=[Depends(_require_token)])
def update_user_with_put() -> ComponentType:
    return html.p("User updated with PUT request")


@action.patch(dependencies=[Depends(_require_token)])
@action.patch("/a/update_user_with_patch", dependencies=[Depends(_require_token)])
async def update_user_with_patch() -> ComponentType:
    return html.p("User updated with PATCH request")


@action.delete(dependencies=[Depends(_require_token)])
@action.delete("/a/delete_user", dependencies=[Depends(_require_token)])
async def delete_user() -> ComponentType:
    return html.p("User deleted")


rendered_page_dense_layout_grid = """
<!DOCTYPE html><html >
<head >
<title >Users page | dense</title>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@picocss/pico@2/css/pico.min.css"/>
</head>
<body class="container-fluid">
<header class="container">
<p >Root layout header</p>
</header>
<main class="container">
<div >
<p >user layout, variant: grid</p>
<div >
Main content:
</div>
<ul >
<li >User 1</li>
<li >User 2</li>
<li >User 3</li>
</ul>
<div >
footer
</div>
<div >
<p >Footer content</p>
</div>
</div>
</main>
<footer class="container">
Root layout footer
</footer>
</body>
</html>
""".strip()


class RenderedAction:
    list_users = "\n".join(
        (
            "<ul >",
            "<li >User 1</li>",
            "<li >User 2</li>",
            "<li >User 3</li>",
            "</ul>",
        )
    )

    create_user = "<p >User created</p>"
    update_user_with_put = "<p >User updated with PUT request</p>"
    update_user_with_patch = "<p >User updated with PATCH request</p>"
    delete_user = "<p >User deleted</p>"
