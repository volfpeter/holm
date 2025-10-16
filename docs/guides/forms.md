# Forms

Let's explore how `holm` simplifies form handling by building a functional TODO application.

We will cover:

- How to handle HTTP GET forms, by creating a global search bar with a form that uses a query parameter for filtering.
- How to handle HTTP POST forms, by implementing a form for creating new TODOs using `POST` requests, utilizing `holm`'s submit handler feature.
- Basic server-side form validation and error rendering.
- How to create reusable user interface components.

The guide assumes you are familiar with the core concepts of `holm`, including [layouts](../application-components.md#layouts-and-pages), [pages](../application-components.md#layouts-and-pages), and [submit handlers](../application-components.md#page-submit-handlers), and you are looking to put these features into practice.

The entire source code of this application can be found in the [examples/forms](https://github.com/volfpeter/holm/tree/main/examples/forms) directory of the repository.

Before you continue, ensure you have installed `holm` and either `uvicorn` or `fastapi-cli` (`pip install holm uvicorn` or `pip install holm fastapi-cli`)!

## Create the application structure

First, create the following directory structure:

```
my_app/
├── main.py          # Application entry point
├── layout.py        # Root layout with global search bar
├── page.py          # Home page with a TODO creation form and a TODO list
└── todo_service.py  # Business logic for TODOs
```

## Initialize your application

Create `main.py` first, our application's entry point.

If you've read the [quick start guide](quick-start-guide.md), then the application setup will already be familiar to you. If not, it's just two lines of code:

```python
from holm import App

app = App()
```

That's it. When you start the application, `holm` automatically discovers your application's structure and registers all routes for you.

## Data model and services

Let's continue by implementing the `todo_service.py` module. It acts as our data layer, and defines a `Todo` model and two services for listing and creating TODOs.

```python
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Todo:
    """A simple TODO item."""

    title: str
    description: str


todos = [
    Todo(
        title="Home page",
        description="It should show the list of TODOs.",
    ),
    Todo(
        title="Add filtering",
        description="Add a form that filters the TODO list using substring search on the title.",
    ),
    Todo(
        title="Add a creation form",
        description="Add a form that submits a creation form with a POST request to a submit handler.",
    ),
]
"""The list of existing TODO items. This list acts as a database for the application."""


def find_todos(query: str) -> list[Todo]:
    """Returns a list of TODOs whose title contains the given query string."""
    query = query.lower()
    return [todo for todo in todos if query in todo.title.lower()]


def create_todo(title: str, description: str) -> Todo:
    """Creates a new TODO with the given title and description and stores it in the database."""
    todo = Todo(title=title, description=description)
    todos.append(todo)
    return todo
```

We now have all the basics in place. Let's move on to the interesting part, the user interface.

## Layout with a global search form

The layout of this application will be a bit more complex than the one in the quick start guide:

- We will move the entire HTML `head` declaration into a separate component. This way the layout itself does not need to be a `htmy` component, because it does not need to access the `htmy` rendering context.
- The `header` component will contain a form that can be used for filtering on all pages.

With that said, let's create `layout.py`, import everything we need, and start by implementing the mentioned custom HTML `head` component:

```python
from fastapi import Request
from htmy import Component, ComponentType, Context, XBool, component, html

from holm import Metadata


@component.context_only
def head(context: Context) -> html.head:
    """
    Helper component that returns the entire head element of the page.

    It uses `Metadata` to correctly set the page title. This way we do not need
    to access the `htmy` context in the layout itself, so that doesn't need to
    be a `htmy` component, it can be a simple `holm` layout function with dependencies.
    """
    metadata = Metadata.from_context(context)
    return html.head(
        html.title(metadata.get("title", "TODO App")),
        html.meta(charset="utf-8"),
        html.meta(name="viewport", content="width=device-width, initial-scale=1"),
        html.link(  # Use PicoCSS to add some default styling.
            rel="stylesheet", href="https://cdn.jsdelivr.net/npm/@picocss/pico@2/css/pico.min.css"
        ),
    )
```

`head` is a simple, context-only `htmy` function component. The only `holm`-specific part in this bit of code is `Metadata`, which gives the component access to the metadata that's provided by the currently rendered page.

Next we can add the search form:

```python
def search_form(q: str, *, autofocus: bool) -> html.form:
    """
    Search form for the layout.

    Arguments:
        q: The current value of the `q` input.
        autofocus: Whether the search input should be focused on page load.
    """
    return html.form(
        html.input_(
            type="search",
            name="q",  # The name of our filter query parameter.
            value=q,  # Keep the value of the input field.
            placeholder="Search...",
            # Focus automatically after GET requests. autofocus is a bool HTML
            # attribute, so to disable it, we must either omit the attribute or
            # use the XBool htmy utility.
            autofocus=XBool.true if autofocus else XBool.false,
        ),
        html.button("Find", type="submit"),
        role="search",
    )
```

The most important thing to note in the search form is that the input's `name` attribute is set to `"q"`. This is the name the browser will use to submit the value of our search input. As a consequence, our layout must have a `q: str` query parameter dependency in order to access the submitted value. Of course, pages that do filtering should also have the same dependency.

Okay, we're done with all the complex parts! We can add the `layout` itself, which is quite simple: just a FastAPI dependency with the usual `children` property, a `request: Request` dependency that we use to decide whether to autofocus the search input, and the `q: str` query parameter dependency that we use to persist the search query between page loads.

```python
def layout(children: ComponentType, request: Request, q: str = "") -> Component:
    """Root layout wrapping all pages."""
    return (
        html.DOCTYPE.html,
        html.html(
            # Use our head component.
            head(),
            html.body(
                html.header(
                    # Global search form, present in all pages, always submitted
                    # with a GET request to the current URL. The input named "q"
                    # contains the search query in the HTML, this is why the
                    # layout has a matching q query parameter dependency.
                    # Pages can  usethe same dependency for filtering.
                    search_form(q, autofocus=request.method == "GET"),
                    class_="container",
                ),
                html.main(children, class_="container"),
                html.footer(html.p("© 2025 TODO App"), class_="container"),
                class_="container-fluid",
            ),
        ),
    )
```

## Home page with a TODO creation form

Create `page.py` for your home page. The page will:

- Show a form for creating new TODO items, demonstrating `holm`'s submit handler feature.
- Display the list of TODOs, always filtered by the search query (coming from the search form in our layout) if there is one.
- Do server-side form validation and error rendering, to forbid TODOs with empty or whitespace-only titles and descriptions.
- Show the fresh TODO list after successful creation, with an empty TODO creation form.
- Show the TODO list after failed creation, keeping the form data and marking invalid inputs (using the `aria-invalid` attribute).

The description implies that the page looks essentially the same both on initial load and after TODO creation attempts, so it makes sense to extract the page content into a function (let's call it `page_content`) that we can use both in `page()` (our GET route) and in `handle_submit()` (our creation/POST route). Let's start with this component, which will actually be the bulk of our `page.py` module:

```python
from typing import Annotated

from fastapi import Form
from htmy import Component, XBool, html
from todo_service import create_todo, find_todos


def page_content(
    q: str,
    *,
    title: str = "",
    title_invalid: bool = False,
    description: str = "",
    description_invalid: bool = False,
) -> html.div:
    """
    Returns the common page content for `page()` and `handle_submit()`.

    Arguments:
        q: The current query string for TODO list filtering.
        title: The text to show in the title input.
        title_invalid: Whether the title should be marked as invalid.
        description: The text to show in the description input.
        description_invalid: Whether the description should be marked as invalid.
    """
    return html.div(
        html.form(
            # TODO creation form. It has a `title` and a `description` input field.
            html.input_(
                type="text",
                name="title",
                value=title,
                autofocus="",  # Try to focus this input by default.
                # aria-invalid is a bool HTML attribute, so to disable it, we must
                # either omit the attribute or use the XBool utility from htmy.
                aria_invalid=XBool.true if title_invalid else XBool.false,
            ),
            html.input_(
                type="text",
                name="description",
                value=description,
                # aria-invalid is a bool HTML attribute, so to disable it, we must
                # either omit the attribute or use the XBool utility from htmy.
                aria_invalid=XBool.true if description_invalid else XBool.false,
            ),
            html.button("Create TODO", type="submit"),
            # We don't need to set the form action, the default browser behavior is
            # to submit forms to the current URL. We must set the method to POST
            # though, to direct the request to our `handle_submit()` function,
            # which is our POST request handler!
            method="POST",
        ),
        html.hr(),
        html.div(
            *(  # Create a PicoCSS Card for each TODO.
                html.article(
                    html.header(html.strong(todo.title)),
                    html.p(todo.description),
                )
                for todo in find_todos(q)
            )
        ),
    )
```

That's quite a few lines of code, but not too bad if you skip the in-code explanations.

Let's also add the page metadata and our `page` function (our GET route):

```python
# Static metadata
metadata = {"title": "Home | TODO App"}


def page(q: str = "") -> Component:
    """Home page content."""
    return page_content(q)
```

As you can see, we use the same `q: str` query parameter as in our layout, so we can filter the TODO list.

`handle_submit` (our TODO creation/POST route) will be slightly more complex, because it needs to do basic input validation and TODO creation as well. Apart from this extra bit of logic, this function is also just a `page_content` call:

```python
def handle_submit(
    title: Annotated[str, Form()],
    description: Annotated[str, Form()],
    q: str = "",
) -> Component:
    """
    Submit handler that expects a TODO title and description as form data.

    It returns the page content the same way as `page()` does. The returned
    component is wrapped in the page's layout the same way as it happens
    with `page()`.
    """
    title, description = title.strip(), description.strip()
    title_invalid, description_invalid = title == "", description == ""
    if not (title_invalid or description_invalid):
        create_todo(title, description)  # Create the todo
        # Reset the value of form fields before rendering the page.
        title = description = ""

    return page_content(
        q,
        title=title,
        title_invalid=title_invalid,
        description=description,
        description_invalid=description_invalid,
    )
```

That's it, the application is ready. This was a long guide, congratulations if you've made it all the way through!

If you found this topic complex, don't worry, we covered a lot and you've already built up the necessary intuition to start building interactive applications with `holm` on your own!

## Run your application

You can now run your application using `uvicorn` or `fastapi-cli`, and see your work in action at `http://localhost:8000`:

```bash
uvicorn main:app --reload
```

Or with the FastAPI CLI if installed:

```bash
fastapi dev main.py
```

*Don't be surprised: the application uses an in-memory data layer (`todo_service.py` module), so it will be reset every time the application restarts.*
