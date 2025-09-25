# Quick start guide

Let's create a minimal `holm` application with a layout, two pages, and dynamic page metadata!

This example will get you up and running quickly by demonstrating the following core concepts:

- File-system routing: URLs automatically match your directory structure (`/about` maps to `about/page.py`).
- Automatic layout composition: The root layout automatically wraps all pages without manual configuration.
- Dynamic metadata: Pages can have static metadata (a mapping) or dynamic metadata (as a FastAPI dependency).
- FastAPI integration: Use standard FastAPI features (dependencies) in layouts, pages, and metadata functions.
- htmy components: Build your UI in typed Python with a JSX-like syntax.

## Create the application structure

Before starting this guide, make sure you have installed `holm` and either `uvicorn` or `fastapi-cli` with `pip` (`pip install holm uvicorn` or `pip install holm fastapi-cli`)!

First, create the following directory structure:

```
my_app/
├── main.py          # Application entry point
├── layout.py        # Root layout
├── page.py          # Home page
└── about/
    ├── __init__.py
    └── page.py      # About page
```

## Initialize your application

Create `main.py` to initialize your `holm` application:

```python
from holm import App

app = App()
```

This is all you need! The `App()` call will automatically discover and register all your layouts and pages based on the file structure.

## Create a root layout

Create `layout.py` to define your application's root layout:

```python
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
            ),
            html.body(
                html.header(
                    html.nav(
                        html.ul(
                            html.li(html.a("Home", href="/")),
                            html.li(html.a("About", href="/about")),
                        )
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

## Create your home page

Create `page.py` for your home page:

```python
from htmy import Component, html

# Static metadata for this page
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
        ),
        html.a("Learn more about us", href="/about"),
    )
```

## Create an about page with dynamic metadata

Create `about/__init__.py` (empty file) and `about/page.py`:

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
        html.a("Featured version", href="/about?featured=true"),
    )
```

That's it! You now have a working application. From here, you can add more pages, create nested layouts, add API endpoints, and explore the full power of FastAPI, `htmy`, and FastHX.

## Run your application

You can now run your application using `uvicorn` or `fastapi-cli` :

```bash
uvicorn main:app --reload
```

Or with FastAPI CLI if installed:

```bash
fastapi dev main.py
```

Visit these URLs to see your application in action:

- `http://localhost:8000/`: Home page
- `http://localhost:8000/about`: About page
- `http://localhost:8000/about?featured=true`: About page with dynamic content
