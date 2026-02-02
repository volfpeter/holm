# HTML layout

This guide shows how to convert the [quick-start-guide](quick-start-guide.md) application to use an HTML layout instead of a Python-based layout component.

The application is identical to the quick start guide in every way except for two key differences:

1. **HTML layout**: Uses `layout.html` instead of `layout.py` for the root layout.
2. **Package structure**: The app is wrapped in a Python package (required for HTML layouts to enable resource loading).

The entire source code of this application can be found in the [examples/html-layout](https://github.com/volfpeter/holm/tree/main/examples/html-layout) directory of the repository.

Before you continue, make sure you have installed `holm` and either `uvicorn` or `fastapi-cli`!

## File structure

As already mentioned, the HTML layout version requires a Python package structure, because HTML layouts are loaded as package resources:

```
html-layout/             # Root directory
└── my_app/              # Application package
    ├── __init__.py      # Makes this a Python package (required for HTML layouts)
    ├── main.py          # Application entry point
    ├── layout.html      # Root HTML layout (instead of layout.py)
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

Don't forget to add `__init__.py` in `my_app` to make it a Python package.

## Create the HTML layout

Next we create `my_app/layout.html` to define the application's root layout:

```html hl_lines="4 22"
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
      <nav>
        <ul>
          <li><a href="/">Home</a></li>
          <li><a href="/about">About</a></li>
        </ul>
      </nav>
    </header>
    <main class="container">
      <!-- slot[children] -->
    </main>
    <footer class="container">
      <p>© 2026 My App</p>
    </footer>
  </body>
</html>
```

HTML layouts are **plain Python format strings**:

- `{metadata[title]}` interpolates the page title from each page's metadata.
- `<!-- slot[children] -->` is an HTML comment placeholder where page content is inserted.

!!! note "Slots and htmy"

    Slots are standard HTML comments that follow `htmy.Snippet` and `htmy.Slot` conventions. For more information, see the [htmy documentation](https://volfpeter.github.io/htmy).

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

| Feature              | Python layout (`layout.py`)          | HTML layout (`layout.html`)                  |
| -------------------- | ------------------------------------ | -------------------------------------------- |
| **File type**        | Python module with callable `layout` | Plain HTML file                              |
| **Package required** | No                                   | Yes (for resource loading)                   |
| **Metadata access**  | `Metadata.from_context(context)`     | `{metadata[key]}` format string              |
| **Children slot**    | Function argument (e.g. `children`)  | HTML comment (`<!-- slot[children] -->`)     |
| **Dynamic logic**    | Full Python logic in component       | Static HTML with format string interpolation |
| **Customization**    | Full Python flexibility              | Customizable via `str_to_layout` parameter   |
| **Precedence**       | Used if present                      | Python layout used if both exist             |

## Run your application

That's it, the application is ready. You can now run it using `uvicorn` or `fastapi-cli`:

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

Now that you understand the basics of HTML layouts:

- Learn how to use multiple layout slots for more complex page structures in the [HTML multi-slot layout guide](guides/html-multi-slot-layout.md)
- Learn how to provide default slot content that appears on every page in the [HTML layout default slots guide](guides/html-layout-default-slots.md)
