# Jinja quick start

This guide builds on top of the [quick start guide](quick-start-guide.md) application to show how to use `holm`'s `JinjaTemplate` component and how to access `holm`-provided context inside Jinja templates.

The application is identical to the quick start guide in every way except one key difference: the about page uses the `JinjaTemplate` component instead of components like `html.div`. The home page and the root layout are kept as-is.

`JinjaTemplate` is itself a regular `htmy` component, so it composes naturally with other `htmy` components and you can use it anywhere similarly to other `htmy` components.

The entire source code of this application can be found in the [examples/jinja-quick-start](https://github.com/volfpeter/holm/tree/main/examples/jinja-quick-start) directory of the repository.

Before you continue, make sure you have installed `holm` and either `uvicorn` or `fastapi-cli` (`pip install holm uvicorn` or `pip install holm fastapi-cli`)!

## File structure

```
jinja-quick-start/            # Root directory
├── layout.py                 # Root layout, same as quick start
├── main.py                   # Application entry point
├── page.py                   # Home page
└── about/
    ├── __init__.py
    ├── page.jinja            # About page Jinja template
    └── page.py               # About page, renders page.jinja
```

## Create the application

Create `main.py` to initialize your `holm` application the usual way:

```python hl_lines="1 3"
from holm import App

app = App()
```

When `holm` creates the `htmy` renderer itself, it automatically registers an `htmy.jinja.JinjaTemplates` instance in the renderer's default context, so `JinjaTemplate` components work out of the box, you don't need to configure anything.

## Create the root layout

Create `layout.py` to define your application's root layout. This is the same layout as in the quick start guide:

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
                html.footer(html.p("© 2026 My App"), class_="container"),
                class_="container-fluid",
            ),
        ),
    )
```

The layout is an `htmy` component that renders its children inside the `html.main` tag. It does not matter what kinds of `htmy` components are in `children`, `JinjaTemplate` works just like `html.div` for example.

## Create your home page

Create `page.py` for your home page. The code is the same as in the quick start guide, building the page from `htmy.html` components:

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
            html.li("Server-side rendering with htmy and Jinja"),
        ),
        html.a("Learn more about us", href="/about"),
    )
```

## Create the about page using `JinjaTemplate`

First, create `about/__init__.py` (empty file) and `about/page.py`:

```python hl_lines="1 4 11 16"
from holm import JinjaTemplate


async def metadata(featured: bool = False) -> dict[str, str | bool]:
    """
    Dynamic metadata based on query parameters.

    This function could be either sync or async. It's just a standard FastAPI dependency.
    """
    title = "Featured About" if featured else "About"
    return {"title": f"{title} | My App", "featured": featured}


async def page() -> JinjaTemplate:
    """Renders the about page from a Jinja template."""
    return JinjaTemplate("about/page.jinja")
```

The about page differs from the quick start guide's about page in two important ways:

- `metadata` now returns the `featured` flag in addition to `title`, so the Jinja template can access and use it.
- `page` no longer builds the markup in Python. It returns a `JinjaTemplate` that renders the template named `about/page.jinja`.

Note that you don't need to pass `featured`, page metadata, or anything else besides the template path to `JinjaTemplate`. `holm` automates a lot of the necessary Jinja context creation for you:

- Page metadata is available in Jinja templates through the `metadata` key.
- The current FastAPI request is available as `request`, along with the usual FastAPI/Starlette Jinja context utilities like `url_for()`.
- The FastAPI route's resolved dependencies can be accessed as `route_params`.

The `JinjaTemplate` component of course provides lots of customization options, including `slots` handling, custom context variables, and so on. See the [htmy](https://volfpeter.github.io/htmy/api/jinja/) documentation for more information.

Let's now create the Jinja template in `about/page.jinja`:

```jinja hl_lines="1"
{% if metadata.featured %}
<div>
  <h1>About Us ⭐</h1>
  <p>This is our featured about page!</p>
  <p>You're viewing the special featured version.</p>
  <a href="/about">Regular version</a>
</div>
{% else %}
<div>
  <h1>About Us</h1>
  <p>We're building amazing web applications with holm.</p>
  <p>Our framework combines the power of FastAPI with server-side rendering.</p>
  <a href="/about?featured=true">Featured version</a>
</div>
{% endif %}
```

The `{% if %}` / `{% else %}` blocks branch on the `metadata.featured` flag, producing the same two variants of the page as in the quick start guide.

The template name passed to `JinjaTemplate` is resolved relative to the templates root directory. In `holm` this defaults to the application's Python import root directory. If you don't want to mix your Jinja templates with your Python code, you can create a separate folder for your templates in the application's root directory, e.g. `templates/`, and use templates like this: `JinjaTemplate("templates/about-page.jinja")`.

## Custom `htmy`

When you pass your own `fasthx.htmy.HTMY` to `App()`, `holm` does not modify it. You must ensure a `htmy.jinja.JinjaTemplates` instance is available in the rendering context (e.g. in the renderer's default context) for `JinjaTemplate` components to render.

Furthermore, the templates root directory must be the same as the Python import root directory for `JinjaTemplate` to resolve template names the same way as in this guide.

## Run your application

You can now run your application using `uvicorn` or `fastapi-cli`:

```bash
uvicorn main:app --reload
```

Or with the FastAPI CLI if installed:

```bash
fastapi dev main.py
```

Visit these URLs to see the application in action:

- `http://localhost:8000`: Home page
- `http://localhost:8000/about`: About page rendered from a Jinja template
- `http://localhost:8000/about?featured=true`: About page with dynamic content

## Next steps

- See the [quick start guide](quick-start-guide.md) for the basics of `holm` applications, routing, and layouts.
- Learn how to use a Jinja template for the root layout in the [Jinja layout guide](jinja-layout.md).
- Learn how to use multiple layout slots for more complex page structures in the [Jinja multi-slot layout guide](jinja-multi-slot-layout.md).
