# `holm` in a hurry

`holm` is a Python web framework that applies the development patterns of Next.js to a Python environment. It is built on:

- Standard FastAPI as its web server layer.
- `htmy` as its engine for building HTML components in pure Python, with full typing and async support.

**File-system based routing** takes a central role in `holm`. Instead of manually defining routes, your application's package structure is automatically discovered and mapped to a corresponding API structure. This process also included full UI composition from your layouts and pages.

## Application initialization

Your application is initialized with a single call to `holm.App()` within your application's root package. This call triggers the discovery process where `holm` walks your project structure, finds all the application components described below, and registers the corresponding routes in the underlying FastAPI instance.

`holm.App()` optionally accepts a FastAPI instance to use. If provided, it registers all routes in the given application, giving you full control over your application's configuration.

## Application structure and components

`holm` builds your application by scanning your project directory for packages with specially-named files.

- **Packages as URL segments**: Each Python package maps to a URL segment. Nesting packages creates nested routes. For example, a package at `my_app/users/settings` (with `holm.App()` being called in a module in `my_app/`) corresponds to the `/users/settings` URL path.
- **Dynamic routes**: To create routes with path parameters (e.g., `/users/{id}`), name your package with underscores (`_id_`) or curly braces (`{id}`). The path parameter is then available as a standard FastAPI dependency (e.g., `def page(id: int): ...`).
- **Special files mark application components**: `holm` looks for specific filenames within your application package (in this example `my_app/`) to discover and wire up your application. The most important application components are discussed individually below.
- **Private packages**: To exclude a directory from the application discovery process, prefix its name with an underscore (e.g., `_components`). `holm` completely ignores these "private" packages and their subpackages, no matter what they contain.

A key feature of `holm` is its deep integration with FastAPI's dependency injection system. Page, layout, action, and metadata functions are just FastAPI dependencies, allowing you to use FastAPI's dependency injection mechanism as you would in any other FastAPI dependency or path operation.

It means if you have already used FastAPI, then you can transfer all your experience and existing codebase to `holm` without any adaptation.

## Pages (`page.py`)

The `page.py` module (and the `page` callable in it) defines the web page for the route segment of the package that contains it.

- The `page` variable must be a callable, which is treated as a **FastAPI dependency**.
- It handles `GET` requests for its package's URL path.
- It usually returns an `htmy.Component`, the children for the layout that wraps it, but the return value can be anything the owner layout accepts (if there is one).

## Layouts (`layout.py`)

The `layout.py` module defines a shared UI that wraps pages and other layouts in its subdirectories.

The module must have a callable `layout` variable. Its first positional argument is provided by `holm` and it is the return value of the child component (usually a page or another layout) it wraps. Any subsequent arguments are resolved as standard **FastAPI dependencies**.

Example:

```python
# my_app/page.py
from htmy import html

def page() -> html.div:
    return html.div("Hello, world!")
```

```python
# my_app/layout.py
from htmy import html

def layout(children: html.div) -> html.html:
    return html.html(
        html.head(html.title("My App")),
        html.body(children),  # <- The html.div page() returns
    )
```

## Page metadata (`page.py`)

A `page.py` module can also have a `metadata` variable. This can be a simple dictionary or a **FastAPI dependency** that returns one. This mapping is made available to every `htmy.Component` in the HTML component tree through the `Metadata.from_context()` utility. A typical use case is to set page-specific information, like the title or meta tags, for layouts.

Example:

```python
# my_app/page.py
from htmy import html

def metadata() -> dict[str, str]:
    """Metadata dependency for the page."""
    return {"title": "My App"}

def page() -> html.div:
    return html.div("Hello, world!")
```

```python
# my_app/layout.py
from htmy import Context, component, html

from holm import Metadata

@component
def head(default_title: str, context: Context) -> html.head:
    """Custom head component that can access page metadata from the htmy context."""
    metadata = Metadata.from_context(context)  # <- The mapping the `metadata` dependency of the page returned
    title = metadata.get("title", default_title)
    return html.head(html.title(title))

def layout(children: html.div) -> html.html:
    return html.html(
        head("My App"),  # <- Our custom head component
        html.body(children),  # <- The html.div page() returns
    )
```

## Actions (`actions.py` or `page.py`)

An action is a function decorated with a `@action` decorator (`@action.get()`, `@action.post()`, etc.). As you probably expect, actions must be **FastAPI dependencies** as well, and they must normally return an `htmy.Component`. The default URL segment for an action is the decorated function's name.

Actions can be defined in `actions.py` and `page.py` modules, and they are ideal for returning HTML fragments (partials) for client-side libraries like HTMX. The returned component is not wrapped in a layout by default, but you have the option to enable layout wrapping (`@action.get(use_layout=True)`) and even define action metadata (`@action.post(metadata={"title": "Post"})`).

## Form submissions (`page.py`)

A `page.py` file can define a `handle_submit()` function (also a **FastAPI dependency**) alongside the `page()` function. Submit handlers behave exactly the same as pages, the only difference is their purpose and that they are HTTP `POST` routes, instead of `GET` routes.

## Custom APIs (`api.py`)

This is where you can create a custom `APIRouter` for the package, as an `api` variable which can be an `APIRouter` instance or a function that returns an `APIRouter`.

It is most often used to configure the `APIRouter` of the package, for example by settings its dependencies, tags, or other options. You can also use it for defining JSON endpoints. Additionally, it can be used for serving HTML fragments (using the FastHX library), although actions provide a more convenient way for that.
