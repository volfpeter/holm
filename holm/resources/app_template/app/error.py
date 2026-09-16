from fastapi import Request
from fastapi.responses import RedirectResponse
from holm.fastapi import FastAPIErrorHandler


async def handle_404(request: Request, exc: Exception) -> RedirectResponse:
    return RedirectResponse(url="/not-found")


handlers: dict[int | type[Exception], FastAPIErrorHandler] = {
    404: handle_404,
}
