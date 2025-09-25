from fastapi import APIRouter


def api() -> APIRouter:
    api = APIRouter()

    @api.get("/")  # No page, the GET / route can be used.
    async def get_all() -> list[dict[str, str]]:
        return [
            {"id": "one", "name": "John"},
            {"id": "two", "name": "Paul"},
            {"id": "three", "name": "George"},
            {"id": "four", "name": "Ringo"},
        ]

    return api
