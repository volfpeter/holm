from fastapi import APIRouter, Request

api = APIRouter()


@api.get("/urls")
def list_urls(request: Request) -> list[str]:
    """Lists some urls to demonstrate `request.url_for()` usage."""
    return [
        str(request.url_for("test_app.page")),
        str(request.url_for("test_app.calculator.page")),
        str(request.url_for("test_app.user.page")),
        str(request.url_for("test_app.user._user_id_.page", user_id="1")),
    ]
