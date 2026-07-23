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
- There is not automatic error rendering, HTML responses must be rendered manually
- Prefer redirects over HTML responses in error handlers
