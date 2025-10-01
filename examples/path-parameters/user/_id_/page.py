from typing import Annotated

from fastapi import Depends
from htmy import html

from ..service import User, get_user

# The `get_user()` function expects an `id: int`. The argument's name and type
# matches the `{id}` path parameter, which means we can use `get_user()` as
# a FastAPI dependency without any additional work (FastAPI will resolve the
# `id: int` argument correctly from the `{id}` path parameter)! Let's do this.
DependsUser = Annotated[User | None, Depends(get_user)]


def metadata(id: int, user: DependsUser) -> dict[str, str]:
    """
    Metadata function that uses the `DependsUser` annotated FastAPI dependency
    to get the user whose ID was submitted in the `{id}` path parameter (which
    is the URL segment corresponding to the `_id_` package name.)

    Just to show that the user was indeed loaded based on the submitted ID,
    the metadata function also uses the `id: int` argument, that is resolved
    by FastAPI from the `{id}` path parameter.
    """
    user_title = "Not Found" if user is None else user.name
    if user and user.id != id:
        raise ValueError(
            "id and user.id should match, because both values originate "
            "from the `{id}` path parameter the client submitted."
        )
    return {
        "title": f"User | {user_title}",
    }


async def page(user: DependsUser) -> html.div:
    """
    Page function that uses the `DependsUser` annotated FastAPI dependency
    to get the user whose ID was submitted in the `{id}` path parameter.

    FastAPI resolves each dependency once, meaning we're only loading the user
    once, and we share it between application components through FastAPI's
    dependency injection system.
    """
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
