# Error handling

This short guide demonstrates how to add error handling to your `holm` application. We'll build upon the [quick start guide](quick-start-guide.md).

Before you continue, make sure you have the basic application from the [quick start guide](quick-start-guide.md) working, as we will be expanding that application.

As a reminder, you must write standard FastAPI error handlers (async functions with a `Request` and an `Exception` argument), as you would in any FastAPI application. The only difference is that error handlers can return `htmy.Component`s as well as FastAPI `Response` objects.

For additional rules and recommendations on error handling, please read the corresponding section of the [Application components](application-components.md) guide.

With all that said, let's set up error handling by adding the `error.py` file to the root of our project (next to `main.py`).

With the file in place, we need to:

- Create a standard FastAPI error handler that returns a component (`handle_404()` function).
- Create a `handlers` variable that maps HTTP error codes or exception types to the corresponding error handler.

```python
from fastapi import Request
from htmy import Component, html

from holm import FastAPIErrorHandler


async def handle_404(request: Request, exc: Exception) -> Component:
    """Handle 404 Not Found errors with a custom HTML page."""
    return html.div(
        html.h1("Page not found"),
        html.p("The page you're looking for doesn't exist."),
        html.a("Go back home", href="/")
    )


handlers: dict[int | type[Exception], FastAPIErrorHandler] = {
    404: handle_404,
}
"""Dictionary that maps HTTP error codes or exception types to error handlers."""
```

That's it! `holm` automatically discovers your error handlers, registers them in the application, and renders components as usual.

To test your work, you should run your application using `uvicorn` or `fastapi-cli`:

```bash
uvicorn main:app --reload
```

Or with the FastAPI CLI if installed:

```bash
fastapi dev main.py
```

You can now open your browser and navigate to a non-existent page, such as `http://localhost:8000/does-not-exist` to see your custom HTTP 404 page in action.
