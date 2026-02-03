# HTML layout with default slots

This guide builds on the [HTML layout guide](html-layout.md) and the [HTML multi-slot layout guide](html-multi-slot-layout.md) to demonstrate how to use **default slots** for shared components that appear on every page.

We will cover:

- How to create a custom `str_to_layout` converter that provides default slots.
- How to build a reusable navigation component that highlights the current page.

The entire source code of this application can be found in the [examples/html-layout-default-slots](https://github.com/volfpeter/holm/tree/main/examples/html-layout-default-slots) directory of the repository.

Before you continue, make sure you have installed `holm` and either `uvicorn` or `fastapi-cli`!

## File structure

The application uses a Python package structure (required for HTML layouts):

```
html-layout-default-slots/  # Root directory
└── my_app/                 # Application package
    ├── __init__.py         # Makes this a Python package (required for HTML layouts)
    ├── main.py             # Application entry point with custom str_to_layout
    ├── layout.html         # Root HTML layout with navbar and children slots
    ├── navbar.py           # Shared navigation component
    ├── page.py             # Home page
    └── about/
        ├── __init__.py
        └── page.py         # About page
```

## Create the navigation component

First we create `my_app/navbar.py` with a navigation component that highlights the current page:

```python hl_lines="1 10 28-29 33-38"
from fasthx.htmy import CurrentRequest
from htmy import ComponentType, Context, component, html

highlight_style = "text-decoration: underline; text-decoration-thickness: 2px;"
"""
Inline style for highlighting the navigation item corresponding to the current page.
"""


def nav_item(text: str, *, href: str, current_path: str) -> ComponentType:
    """
    Creates a nav item with conditional styling if the link matches the current path.
    """
    return html.li(
        html.a(
            text,
            href=href,
            style=highlight_style if current_path == href else None,
        ),
    )


@component.context_only
def navbar(context: Context) -> ComponentType:
    """
    Navigation component that highlights the item corresponding to the current page.
    """
    request = CurrentRequest.from_context(context)
    current_path = request.url.path
    if current_path != "/":
        current_path = current_path.rstrip("/")

    return html.nav(
        html.ul(
            nav_item("Home", href="/", current_path=current_path),
            nav_item("About", href="/about", current_path=current_path),
        )
    )
```

These are the most important details you should notice:

- `CurrentRequest.from_context()` is used to get the current FastAPI request from the `htmy` rendering context.
- The `nav_item` helper applies highlighting when the link matches the current path.

## Create the custom layout converter

Create `my_app/main.py` with a custom `str_to_layout` converter that provides the navbar as a default slot:

```python hl_lines="2-3 5 8-14 18"
from holm import App
from holm.typing import Layout
from holm.utils import snippet_to_layout

from .navbar import navbar


def str_to_layout_with_navbar(content: str) -> Layout:
    """
    Custom string to `Layout` converter function for the application.

    It makes a `navbar` component available to every HTML layout in the `navbar` slot.
    """
    return snippet_to_layout(content, default_slot_mapping={"navbar": navbar})


app = App(str_to_layout=str_to_layout_with_navbar)
```

The important bit here is the `str_to_layout_with_navbar()` function (which wraps `snippet_to_layout`), and how we pass it to `App()`.

The `default_slot_mapping` argument specifies components that will be automatically provided for slots unless the page explicitly overrides them. In this case it means HTML layouts will always have access to our `navbar` without pages having to return it themselves.

## Create the HTML layout with slots

Create `my_app/layout.html` with slots for both the navbar and page content:

```html hl_lines="14-15 18-19"
<!doctype html>
<html>
  <head>
    <title>{metadata[title]}</title>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <link
      rel="stylesheet"
      href="https://cdn.jsdelivr.net/npm/@picocss/pico@2/css/pico.min.css"
    />
  </head>
  <body class="container-fluid">
    <header class="container">
      <!-- The navbar component added by the layout converter goes to the navbar slot: -->
      <!-- slot[navbar] -->
    </header>
    <main class="container">
      <!-- Page content goes here, to the usual children slot: -->
      <!-- slot[children] -->
    </main>
    <footer class="container">
      <p>© 2026 My App</p>
    </footer>
  </body>
</html>
```

Our layout has two slots:

- `<!-- slot[navbar] -->` receives the navbar component from the default slot mapping.
- `<!-- slot[children] -->` receives the page's main content.

## Create your home page

We can now create our home page in `my_app/page.py`, which is essentially the same as in the HTML layout guide:

```python hl_lines="16"
from htmy import Component, html

metadata = {"title": "Home | My App"}


def page() -> Component:
    """Home page content."""
    return html.div(
        html.h1("Welcome to My App"),
        html.p("This is a minimal holm application demonstrating:"),
        html.ul(
            html.li("File-system based routing"),
            html.li("Automatic layout composition"),
            html.li("Dynamic metadata"),
            html.li("Server-side rendering with htmy"),
            html.li("Default slots in layouts"),
        ),
        html.a("Learn more about us", href="/about"),
    )
```

## Create the about page

The about page remains unchanged from the previous guides:

```python
from htmy import Component, html


async def metadata(featured: bool = False) -> dict[str, str]:
    """
    Dynamic metadata based on query parameters.

    This function could be both sync or async. It's just a standard FastAPI dependency.
    """
    title = "Featured About" if featured else "About"
    return {"title": f"{title} | My App"}


async def page(featured: bool = False) -> Component:
    """Async about page with dynamic content."""
    if featured:
        return html.div(
            html.h1("About Us ⭐"),
            html.p("This is our featured about page!"),
            html.p("You're viewing the special featured version."),
            html.a("Regular version", href="/about"),
        )

    return html.div(
        html.h1("About Us"),
        html.p("We're building amazing web applications with holm."),
        html.p("Our framework combines the power of FastAPI with server-side rendering."),
        html.p("This example demonstrates how to use default slots in layouts."),
        html.a("Featured version", href="/about?featured=true"),
    )
```

## Run your application

That's it, the application is ready. You can now run it using `uvicorn` or `fastapi-cli`:

```bash
uvicorn my_app.main:app --reload
```

Or with FastAPI CLI if installed:

```bash
fastapi dev my_app/main.py
```

You can now open the application in the browser:

- `http://localhost:8000`: Home page with highlighted "Home" nav item
- `http://localhost:8000/about`: About page with highlighted "About" nav item
- `http://localhost:8000/about?featured=true`: Featured about page variant

You'll see the navigation bar on every page with the current page highlighted.
