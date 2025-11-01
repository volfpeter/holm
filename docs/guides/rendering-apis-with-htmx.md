# Rendering APIs with HTMX

This guide demonstrates how to enhance a basic `holm` application with a rendering API and HTMX for dynamic, interactive web applications. We'll build upon the [quick start guide](quick-start-guide.md) to add server-rendered partial updates and seamless navigation.

Very basic familiarity with [HTMX](https://htmx.org/) is helpful for this guide, but it can be followed even without it.

Before you continue, make sure you have the basic application from the [quick start guide](quick-start-guide.md) working, as we will be expanding that application.

We will cover:

- How to integrate HTMX for dynamic content updates.
- How to enhance navigation with the `hx-boost` HTMX attribute.
- How to create API endpoints that return rendered HTML components, often called fragments or partials.
- How to use [fasthx](https://volfpeter.github.io/fasthx/examples/htmy/) for seamless server-side rendering of [htmy](https://volfpeter.github.io/htmy/) components.

The entire source code of this application can be found in the [examples/rendering-apis-with-htmx](https://github.com/volfpeter/holm/tree/main/examples/rendering-apis-with-htmx) directory of the repository.

## Add HTMX to the application

Modify `layout.py` to include the HTMX script and enable `hx-boost` on the `nav` tag for enhanced navigation:

```python hl_lines="21 30"
from htmy import Component, ComponentType, Context, component, html

from holm import Metadata


@component
def layout(children: ComponentType, context: Context) -> Component:
    """Root layout wrapping all pages."""
    metadata = Metadata.from_context(context)

    return (
        html.DOCTYPE.html,
        html.html(
            html.head(
                html.title(metadata.get("title", "My App")),
                html.meta(charset="utf-8"),
                html.meta(name="viewport", content="width=device-width, initial-scale=1"),
                html.link(  # Use PicoCSS to add some default styling.
                    rel="stylesheet", href="https://cdn.jsdelivr.net/npm/@picocss/pico@2/css/pico.min.css"
                ),
                html.script(src="https://unpkg.com/htmx.org@2.0.7"),
            ),
            html.body(
                html.header(
                    html.nav(
                        html.ul(
                            html.li(html.a("Home", href="/")),
                            html.li(html.a("About", href="/about")),
                        ),
                        hx_boost="true",
                    ),
                    class_="container",
                ),
                html.main(children, class_="container"),
                html.footer(html.p("© 2025 My App"), class_="container"),
                class_="container-fluid",
            ),
        ),
    )
```

The changes in the layout are trivial, we simply:

- added the HTMX script tag to the `head` element of the webpage with `html.script(src="https://unpkg.com/htmx.org@2.0.7")`;
- and set the `hx_boost` attribute on the `nav` element in the page `header` to [boost our anchors](https://htmx.org/attributes/hx-boost/).

## Create the rendering API

Next we create our rendering API in an `api.py` module. We will place it at the root of our project (next to `main.py`), because we want this API to exist directly under the root `/` URL prefix.

Note: `holm` applies file-system based routing to both pages and APIs! If both an API (`api.py`) and a page (`page.py`) exists in a directory, `holm` combines their routes into a single `APIRouter` for that path.

The API we create will be very simple, it will have a single `/welcome-message` route that returns a welcome message in a randomly chosen language. The returned message is just a string (which happens to be a `htmy` `Component`), so all we need to do is decorate the path operation function with `@htmy.hx()`. You can learn more about using `fasthx.htmy.HTMY` [here](https://volfpeter.github.io/fasthx/examples/htmy/).

```python hl_lines="16 18 20-21 25"
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
```

Important details:

- The `htmy.hx()` decorator is responsible for rendering the route's return value. It must be wrapped by the `@api` decorator.
- Within the `api()` function, everything is standard FastAPI and FastHX functionality.
- While this example only adds a rendering route, you can freely mix rendering and JSON APIs.

## Add dynamic behavior to the home page

Finally we add dynamic content to the home page (`page.py` in the root directory) with a couple of simple HTMX attributes.

On the `h1` element, which contains our welcome message, we set:

- `hx_get` to the use our newly created `/welcome-message` route when HTMX is triggered.
- `hx_trigger` to `every 2s` to make the page load a new welcome message from our API every 2 seconds.

These two attributes together will replace the displayed welcome message every two seconds without reloading the entire page.

For the sake of completeness, we also wrap the link at the bottom in a `div` and use `hx_boost` as before to enhance the navigation experience.

```python hl_lines="12-13"
from htmy import Component, html

# Static metadata for this page
metadata = {"title": "Home | My App"}


def page() -> Component:
    """Home page content."""
    return html.div(
        html.h1(
            "Welcome to My App",
            hx_get="/welcome-message",
            hx_trigger="every 2s",
        ),
        html.p("This is a minimal holm application demonstrating:"),
        html.ul(
            html.li("File-system based routing"),
            html.li("Automatic layout composition"),
            html.li("Dynamic metadata"),
            html.li("Server-side rendering with htmy"),
            html.li("Custom API with HTML rendering support"),
            html.li("HTMX integration"),
        ),
        html.div(
            html.a("Learn more about us", href="/about"),
            hx_boost="true",  # Explicit hx-boost for this link
        ),
    )
```

That's it! You can now run your application using `uvicorn` or `fastapi-cli`:

```bash
uvicorn main:app --reload
```

Or with the FastAPI CLI if installed:

```bash
fastapi dev main.py
```

You can now open your browser and navigate to `http://localhost:8000/` to see your application in action.

If you followed every step correctly, then you will see the welcome message changing every two seconds on the home page.

If you are curious to see how your API is called and how it responds, you can inspect requests on the Network tab of your browser's developer tools.
