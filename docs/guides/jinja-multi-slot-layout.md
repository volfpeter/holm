# Jinja multi-slot layout

This guide builds on the [Jinja layout guide](jinja-layout.md) to demonstrate how to use **multiple layout slots** for more complex page structures.

We will cover:

- How to define multiple slots in a Jinja layout.
- How to return content for multiple slots from a page.

The entire source code of this application can be found in the [examples/jinja-multi-slot-layout](https://github.com/volfpeter/holm/tree/main/examples/jinja-multi-slot-layout) directory of the repository.

Before you continue, make sure you have installed `holm` and either `uvicorn` or `fastapi-cli`!

## File structure

```
jinja-multi-slot-layout/  # Root directory
└── my_app/               # Application package
    ├── __init__.py
    ├── layout.jinja      # Root Jinja layout with multiple slots
    ├── main.py           # Application entry point
    ├── page.py           # Home page returning a slot mapping
    └── about/
        ├── __init__.py
        └── page.py       # About page returning a slot mapping
```

## Create the application

First we initialize the application in `my_app/main.py` the usual way:

```python
from holm import App

app = App()
```

## Create the Jinja layout with multiple slots

Next we create `my_app/layout.jinja` with multiple slot placeholders. This is our application's root layout:

```jinja hl_lines="22-23 29-30"
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
      <!-- Intro slot comes here: -->
      {{ slots.intro }}
      <hr />
      <p style="text-align: center">
        <small>Separator between intro and details slots.</small>
      </p>
      <hr />
      <!-- Details slot comes here: -->
      {{ slots.details }}
    </main>
    <footer class="container">
      <p>© 2026 My App</p>
    </footer>
  </body>
</html>
```

The key difference from the Jinja layout guide is that we are using two slot placeholders instead of the default `{{ slots.children }}`: `{{ slots.intro }}` for an intro section, and `{{ slots.details }}` for the main page content.

You can define as many slots as you need. Slot names are arbitrary strings that match the keys in the dictionary returned by the wrapped page or layout. If the wrapped component returns a component, not a mapping, it will be available in the default `{{ slots.children }}` slot.

## Create your home page with multiple slots

We can now create our home page (`my_app/page.py`). It returns a dictionary (a slot mapping) that maps slot names to their content:

```python hl_lines="10-11 15-16"
from htmy import Component, html

# Static metadata for this page
metadata = {"title": "Home | My App"}


def page() -> dict[str, Component]:
    """Home page content."""
    return {
        # Content for the intro slot of the layout.
        "intro": html.div(
            html.h1("Welcome to My App"),
            html.p("This is a minimal holm application demonstrating:"),
        ),
        # Content for the details slot of the layout.
        "details": html.div(
            html.ul(
                html.li("File-system based routing"),
                html.li("Automatic layout composition"),
                html.li("Dynamic metadata"),
                html.li("Server-side rendering with htmy"),
            ),
            html.a("Learn more about us", href="/about"),
        ),
    }
```

The components assigned to the `"intro"` and `"details"` keys are rendered and placed in the corresponding slots of our Jinja layout.

## Create an about page with dynamic content

The about page (`my_app/about/page.py`) is also directly wrapped by our root Jinja layout, so it must also return a dictionary with the keys expected by the layout:

```python hl_lines="18 22 29 33"
from htmy import Component, html


async def metadata(featured: bool = False) -> dict[str, str]:
    """
    Dynamic metadata based on query parameters.

    This function could be both sync or async. It's just a standard FastAPI dependency.
    """
    title = "Featured About" if featured else "About"
    return {"title": f"{title} | My App"}


async def page(featured: bool = False) -> dict[str, Component]:
    """Async about page with dynamic content."""
    if featured:
        return {
            "intro": html.div(
                html.h1("About Us ⭐"),
                html.p("This is our featured about page!"),
            ),
            "details": html.div(
                html.p("You're viewing the special featured version."),
                html.a("Regular version", href="/about"),
            ),
        }

    return {
        "intro": html.div(
            html.h1("About Us"),
            html.p("We're building amazing web applications with holm."),
        ),
        "details": html.div(
            html.p("Our framework combines the power of FastAPI with server-side rendering."),
            html.a("Featured version", href="/about?featured=true"),
        ),
    }
```

## Run your application

```bash
uvicorn my_app.main:app --reload
```

Or with FastAPI CLI if installed:

```bash
fastapi dev my_app/main.py
```

Visit these URLs to see the application in action:

- `http://localhost:8000`: Home page with intro and details sections
- `http://localhost:8000/about`: About page with intro and details sections
- `http://localhost:8000/about?featured=true`: Featured about page variant with intro and details sections

You'll see a visual separator between the intro and details sections, demonstrating how each slot's content is placed independently in the layout.

## Next steps

- Learn how to provide default slot content that appears on every page in the [Jinja layout default slots guide](jinja-layout-default-slots.md).
- Review the [Jinja layout guide](jinja-layout.md) for the basics of Jinja layouts, custom `htmy` setups, and nested layouts.
