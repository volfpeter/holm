# Custom applications

This guide demonstrates how to use a custom FastAPI application and `fasthx.htmy.HTMY` instance (HTML renderer) in your `holm` application. This allows you to leverage `holm`'s features while keeping full control over all underlying software components.

In the vast majority of applications, using a default FastAPI application (one created by simply calling `FastAPI()`, as `holm` internally does) is not enough. Exception handlers, for example, can be registered with `holm`, but you often need to set up a lifespan method, register middlewares, or customize the OpenAPI documentation to your needs. As a matter of fact, you could even add routes to your application manually, just make sure their paths don't conflict with the routes `holm` registers for you automatically!

When it comes to HTML rendering, you may occasionally need to configure the `fasthx.htmy.HTMY` instance with [custom request processors](https://volfpeter.github.io/fasthx/examples/htmy/), formatters, translation utilities, or global rendering context.

Doing all of this in `holm` is very straightforward, all you need to do is:

1. Create a `FastAPI` instance somewhere in your codebase and configure it, just like you would do in any FastAPI project.
2. Create a `fasthx.htmy.HTMY` instance and configure it.
3. Pass the created instances to the `holm.App()` function as `App(app=my_fastapi_instance, htmy=my_htmy_instance)`.

The below example demonstrates these steps as simply as possible, through creating:

- a `FastAPI` instance with a `/health-check` route, and
- a `fasthx.htmy.HTMY` instance with a request processor.

If you followed the [quick-start-guide](quick-start-guide.md), then you can make these changes in the `main.py` file and immediately see the result in action.

```python hl_lines="6-14 17 26"
from fastapi import FastAPI
from fasthx.htmy import HTMY

from holm import App

app = FastAPI()
htmy = HTMY(
    request_processors=[
        # Add a request processor that inserts an "is_htmx_request" key
        # into htmy rendering contexts, making this information available
        # to htmy components as `context["is_htmx_request"]`.
        lambda request: {"is_htmx_request": request.headers.get("HX-Request") == "true"}
    ]
)


@app.get("/health-check")
def health_check() -> dict[str, str]:
    """Health check route registered directly on the FastAPI application."""
    return {"status": "ok"}


# If holm.App() receives a FastAPI application instance, then it does its job and
# returns the same object. This means you don't need to keep a separate reference
# to the returned value, the already existing app variable is enough.
App(app=app, htmy=htmy)
```

That's it! If you start the application and open its OpenAPI documentation (`http://localhost:8000/docs`) in your browser, you will see the health check route you registered, in addition to all the routes `holm` discovered and registered automatically for you.

Note: If you return a `htmy` component from a manually registered route, it will **not** be rendered as HTML automatically! The reason for this is simple: `holm` must not modify the behavior of user-defined application parts in any way. You can still do HTML rendering manually using the `htmy` instance in the same way as in `holm` API modules (see the [Rendering APIs with HTMX guide](rendering-apis-with-htmx.md)).
