# Error handling

```python
from fastapi import Request
from fastapi.responses import RedirectResponse
from holm.fastapi import FastAPIErrorHandler


async def handle_404(request: Request, exc: Exception) -> RedirectResponse:
    return RedirectResponse(url="/not-found")


handlers: dict[int | type[Exception], FastAPIErrorHandler] = {
    404: handle_404,
}
```

- Handlers live in `error.py` or `errors.py` at the root package
- Error handlers may return a `htmy.Component` or a FastAPI `Response`. Components are automatically rendered to an `HTMLResponse`, responses are returned unchanged
- Prefer redirects over HTML responses in error handlers
