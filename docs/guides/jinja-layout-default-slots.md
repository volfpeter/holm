# Jinja layout default slots

This guide builds on the [Jinja layout guide](jinja-layout.md) and the [Jinja multi-slot layout guide](jinja-multi-slot-layout.md) to demonstrate how to use **default slots** for shared components that appear on every page.

We will cover:

- How to configure default slots with `App(layout_slots=...)`.
- How to render default slots in a Jinja layout.

The entire source code of this application can be found in the [examples/jinja-layout-default-slots](https://github.com/volfpeter/holm/tree/main/examples/jinja-layout-default-slots) directory of the repository.

Before you continue, make sure you have installed `holm` and either `uvicorn` or `fastapi-cli`!

## File structure

The application uses a Python package structure:

```
jinja-layout-default-slots/  # Root directory
└── my_app/                  # Application package
    ├── __init__.py
    ├── layout.jinja         # Root Jinja layout with navbar and children slots
    ├── main.py              # Application entry point
    ├── navbar.py            # Default navbar component
    ├── page.py              # Home page
    └── about/
        ├── __init__.py
        └── page.py          # About page
```

## Create the application with a default slot

Default slots are configured when you create the `holm` application:

```python hl_lines="8"
from holm import App

from .navbar import navbar

# `layout_slots` makes the `navbar` slot available to every component
# in the application, including Jinja layouts, through
# `htmy.jinja.DefaultSlots.from_context()`.
app = App(layout_slots={"navbar": navbar})
```

`layout_slots` takes a mapping from slot name to `htmy` component. These slots are injected into the `htmy` rendering context using `htmy.jinja.DefaultSlots` and merged with any explicit slots returned by the wrapped page or layout. When there is a slot name conflict, the explicit slot provided by the wrapped page or layout takes precedence.

## Create the default navbar component

First we create `my_app/navbar.py` with a navigation component that highlights the current page:

```python hl_lines="1 18 28"
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

The most important details:

- `CurrentRequest.from_context()` is used to get the current FastAPI request from the `htmy` rendering context.
- The `nav_item` helper applies highlighting when the link matches the current path.

## Create the Jinja layout with slots

Create `my_app/layout.jinja` with slots for both the navbar and page content:

```jinja hl_lines="4 14-15 18-19"
<!doctype html>
<html>
  <head>
    <title>{{ metadata.title }}</title>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <link
      rel="stylesheet"
      href="https://cdn.jsdelivr.net/npm/@picocss/pico@2/css/pico.min.css"
    />
  </head>
  <body class="container-fluid">
    <header class="container">
      <!-- The navbar component provided by `layout_slots` -->
      {{ slots.navbar }}
    </header>
    <main class="container">
      <!-- Page content goes here, to the usual children slot -->
      {{ slots.children }}
    </main>
    <footer class="container">
      <p>© 2026 My App</p>
    </footer>
  </body>
</html>
```

The layout has two slots:

- `{{ slots.navbar }}` receives the navbar component from `layout_slots`.
- `{{ slots.children }}` receives the page's main content.

## Create your home page

We can now create our home page in `my_app/page.py`, which is essentially the same as in the Jinja layout guide:

```python
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

    This function could be either sync or async. It's just a standard FastAPI dependency.
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

## Next steps

Now that you understand default slots:

- Review the [Jinja layout guide](jinja-layout.md) for the basics of Jinja layouts, custom `htmy` setups, and nested layouts.
- Learn how to use multiple layout slots for more complex page structures in the [Jinja multi-slot layout guide](jinja-multi-slot-layout.md).
