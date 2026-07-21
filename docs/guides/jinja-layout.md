# Jinja layout

This guide shows how to convert the [quick-start-guide](quick-start-guide.md) application to use a Jinja layout instead of a Python-based layout component.

The application is identical to the quick start guide in every way except for two key differences:

1. **Jinja layout**: Uses `layout.jinja` instead of `layout.py` for the root layout.
2. **Package structure**: The app is wrapped in a Python package. This is idiomatic for `holm` applications; Jinja layouts do not require a package to work.

The entire source code of this application can be found in the [examples/jinja-layout](https://github.com/volfpeter/holm/tree/main/examples/jinja-layout) directory of the repository.

Before you continue, make sure you have installed `holm` and either `uvicorn` or `fastapi-cli`!

## File structure

```
jinja-layout/            # Root directory
└── my_app/              # Application package
    ├── __init__.py
    ├── layout.jinja     # Root Jinja layout (instead of layout.py)
    ├── main.py          # Application entry point
    ├── page.py          # Home page
    └── about/
        ├── __init__.py
        └── page.py      # About page
```

## Create the application

Create `my_app/main.py` to initialize your `holm` application the usual way:

```python
from holm import App

app = App()
```

When `holm` creates the `htmy` renderer itself and a `layout.jinja` file is discovered, it automatically registers a `Jinja2Templates` instance in the renderer's default context, so Jinja layouts and `JinjaTemplate` components work out of the box.

## Create the Jinja layout

Next we create `my_app/layout.jinja` to define the application's root layout:

```jinja hl_lines="4 22"
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
      <nav>
        <ul>
          <li><a href="/">Home</a></li>
          <li><a href="/about">About</a></li>
        </ul>
      </nav>
    </header>
    <main class="container">
      {{ slots.children }}
    </main>
    <footer class="container">
      <p>© 2026 My App</p>
    </footer>
  </body>
</html>
```

Jinja layouts are **standard Jinja2 templates** rendered automatically by `holm`:

- `{{ metadata.title }}` interpolates the page title from each page's metadata.
- `{{ slots.children }}` is the wrapped page content, pre-rendered to safe HTML.

## Create your home page

Create `my_app/page.py` for your home page:

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

This page is identical to what we created in the quick start guide.

## Create an about page with dynamic metadata

Create `my_app/about/page.py`:

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

This page is also identical to what we created in the quick start guide.

## Differences from Python layouts

| Feature             | Python layout (`layout.py`)          | Jinja layout (`layout.jinja`)    |
| ------------------- | ------------------------------------ | -------------------------------- |
| **File type**       | Python module with callable `layout` | Jinja2 template                  |
| **Metadata access** | `Metadata.from_context(context)`     | `{{ metadata.<attribute> }}`     |
| **Children slot**   | Function argument (e.g. `children`)  | `{{ slots.children }}`           |
| **Precedence**      | Used if present                      | Python layout used if both exist |

`layout.py` remains the escape hatch for FastAPI dependency injection and arbitrary Python logic. Python layouts and Jinja layouts compose in either order through holm's layout-composition machinery.

## Custom `htmy`

When you pass your own `fasthx.htmy.HTMY` to `App()`, `holm` does not modify it. You must ensure a `htmy.jinja.JinjaTemplates` instance is available in the rendering context (e.g. in the renderer's default context) for Jinja layouts and templates to render.

Furthermore, the templates root directory must be the same as the Python import root directory for Jinja layouts to work.

## Run your application

```bash
uvicorn my_app.main:app --reload
```

Or with FastAPI CLI if installed:

```bash
fastapi dev my_app/main.py
```

Visit these URLs to see the application in action:

- `http://localhost:8000`: Home page
- `http://localhost:8000/about`: About page
- `http://localhost:8000/about?featured=true`: About page with dynamic content

## Next steps

- Learn how to use multiple layout slots for more complex page structures in the [Jinja multi-slot layout guide](jinja-multi-slot-layout.md)
- Learn how to provide default slot content that appears on every page in the [Jinja layout default slots guide](jinja-layout-default-slots.md)
