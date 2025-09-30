from typing import Annotated

from fastapi import Depends
from htmy import html

from ..service import User, get_user

# The `get_user()` function expects an `id: int`. The argument's name and type
# matches the `{id}` path parameter, which means we can use `get_user()` as
# a FastAPI dependency without any additional work (FastAPI will resolve the
# `id: int` argument correctly from the `{id}` path parameter)! Let's do this.
DependsUser = Annotated[User | None, Depends(get_user)]


def metadata(user: DependsUser) -> dict[str, str]:
    user_title = "Not Found" if user is None else user.name
    return {
        "title": f"User | {user_title}",
    }


async def page(user: DependsUser) -> html.div:
    if user is None:
        return html.div(
            html.h1("The user does not exist"),
        )

    return html.div(
        html.strong("Name:"),
        html.span(user.name),
        html.strong("ID:"),
        html.span(str(user.id)),
        html.strong("Email:"),
        html.span(user.email),
        style="display: grid; grid-template-columns: max-content 1fr; gap: 1rem;",
    )
