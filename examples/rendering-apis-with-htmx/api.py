import random

from fastapi import APIRouter
from fasthx.htmy import HTMY

_welcome_message: list[str] = [
    "Welcome to My App! Powered By HTMX.",
    "Bienvenido a My App! Powered By HTMX.",
    "Bienvenue dans My App! Powered By HTMX.",
    "Willkommen bei My App! Powered By HTMX.",
    "Benvenuti nella mia app! Powered By HTMX.",
    "Üdvözöljük a My App-ban! Powered By HTMX.",
]


def api(htmy: HTMY) -> APIRouter:
    """Rendering API factories need a `htmy: fasthx.htmy.HTMY` argument."""
    api = APIRouter()

    @api.get("/welcome-message")
    @htmy.hx()  # type: ignore[arg-type]
    async def get_welcome_message() -> str:
        return random.choice(_welcome_message)  # noqa: S311

    return api
