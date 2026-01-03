from fastapi import Request
from htmy import Component, html

from holm import FastAPIErrorHandler


async def _handle_404(_request: Request, _exc: Exception) -> Component:
    """Handle 404 Not Found errors with a custom HTML page."""
    return html.div(html.h1("Page not found"))


handlers: dict[int | Exception, FastAPIErrorHandler] = {
    404: _handle_404,
}
