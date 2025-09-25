from fastapi import APIRouter
from fasthx.htmy import HTMY
from htmy import html


def api(htmy: HTMY) -> APIRouter:
    api = APIRouter()

    # The package has a page, so the "/" route is already taken.

    @api.get("/info")
    @htmy.hx(
        # Respond with the rendered user card to HTMX requests
        # and with the plain JSON payload to non-HTMX ones.
        user_card,
    )
    async def get_user(id: str) -> dict[str, str]:
        return {"id": id, "name": "John"}

    # Don't forget to return the API.

    return api


def user_card(user: dict[str, str]) -> html.div:
    return html.div(
        html.h2(user["name"]),
        html.p(f"ID: {user['id']}"),
    )
