# Path parameters and dynamic routing

This guide demonstrates how to create pages with dynamic routes in a `holm` application. We'll build a simple application that lists users and shows a profile page for each user, with the user ID as a path parameter (dynamic URL segment).

We will cover:

- How to create dynamic routes using `holm`'s file-system-based routing.
- How to access path parameters in your page and metadata functions.
- How to execute async code in pages, layouts, or metadata functions.
- How to generate dynamic metadata for pages with dynamic routes.
- How to use FastAPI dependencies to fetch data and share it between application components.

The entire source code of this application can be found in the [examples/path-parameters](https://github.com/volfpeter/holm/tree/main/examples/path-parameters) directory of the repository.

This guide focuses on path parameters and dynamic routing, and has a lot in common with the [Quick start guide](quick-start-guide.md). It is assumed you have the necessary dependencies installed, as described in the quick start guide.

## Application structure

Our application will have a home page, a page listing all users, and a dynamic page for individual user profiles. The corresponding file structure looks like this:

```text hl_lines="6-8"
my_app/
├── layout.py
├── main.py
├── page.py
└── user/
    ├── _id_/
    │   ├── __init__.py
    │   └── page.py
    ├── __init__.py
    ├── page.py
    └── service.py
```

The most interesting part is the `user/_id_/page.py` module. `holm` interprets the `_id_` package name as a path parameter named `id`, and creates the `/user/{id}` route for it. It lets you have `id: IdType` dependencies in page, metadata, and layout functions in this package (including its subpackages).

## Application initialization

Let's start with `main.py`, our application's entry point. It's just two lines of code:

```python
from holm import App

app = App()
```

## Data model and services

Let's continue by implementing the `user/service.py` module. It acts as our data layer, and defines a `User` model and two `async` functions for fetching users. Think of it as a simple in-memory database with an `async` interface for demonstration.

```python hl_lines="4-5 13-16 19 29"
from dataclasses import dataclass


@dataclass(frozen=True, kw_only=True, slots=True)
class User:
    """User model."""

    id: int
    name: str
    email: str


users_by_id: dict[int, User] = {
    i: User(id=i, name=f"User {i}", email=f"user-{i}@holm.ccm") for i in range(10)
}
"""Dictionary that maps user IDs to the corresponding user objects."""


async def list_users() -> list[User]:
    """
    Lists all users.

    The function is async to demonstrate how easily async tools, for example ORMs
    can be used in `holm`.
    """
    return list(users_by_id.values())


async def get_user(id: int) -> User | None:
    """
    Returns the user with the given ID, if the user exists.

    The function is async to demonstrate how easily async tools, for example ORMs
    can be used in `holm`.
    """
    return users_by_id.get(id)
```

We now have everything in place to start working on the user interface!

## Root layout and home page

When it comes to the user interface, we should start with the application's layout and home page (`layout.py` and `page.py`, next to `main.py`).

These are essentially the same as what we implemented in the [Quick start guide](quick-start-guide.md), with minor changes in the layout's `nav` element and page content, so we won't go into the details here.

Here is the layout (`layout.py`):

```python hl_lines="9-13 29-32"
from htmy import Component, ComponentType, Context, component, html

from holm import Metadata


@component
def layout(children: ComponentType, context: Context) -> Component:
    """Root layout wrapping all pages."""
    metadata = Metadata.from_context(context)
    title = "Admin App"
    # Let pages set only their subpage title, and add the application name automatically.
    if subpage_title := metadata.get("title"):
        title = f"{title} | {subpage_title}"

    return (
        html.DOCTYPE.html,
        html.html(
            html.head(
                html.title(title),
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
                            html.li(html.a("Users", href="/user")),
                        )
                    ),
                    class_="container",
                ),
                html.main(children, class_="container"),
                html.footer(html.p("© 2026 Admin App"), class_="container"),
                class_="container-fluid",
            ),
        ),
    )
```

And here is the home page (`page.py`, next to `main.py`):

```python
from htmy import Component, html

# Static metadata for this page
metadata = {"title": "Dashboard"}


def page() -> Component:
    """Home page content."""
    return html.div(
        html.h1("Welcome to Admin App"),
        html.p("This is a minimal holm application demonstrating:"),
        html.ul(
            html.li("How to use path parameters, also known as dynamic routing"),
            html.li("File-system based routing with dynamic routes"),
        ),
        html.a("Navigate to the User page to start exploring", href="/user"),
    )
```

## The user list page

Next, we'll create the users page at the `/user` URL (`user/page.py`).

This page uses the `list_users()` service to load the list of users, and displays them as a HTML list. Each list item contains an anchor tag that we can use to navigate to the user's profile page.

```python hl_lines="10 17"
from htmy import Component, html

from .service import list_users

metadata: dict[str, str] = {"title": "Users"}


async def page() -> Component:
    # Load users using an async service.
    users = await list_users()
    return html.div(
        html.h1("Users:"),
        html.ul(
            # Create list items with a link to the profile page for each user.
            # Don't forget to use the spread operator! html.ul expects its
            # children as positional arguments, not as a single list.
            *(html.li(html.a(user.name, href=f"/user/{user.id}")) for user in users),
        ),
    )
```

## User profile page

We have finally reached the essence of this guide: the user profile page. Don't expect any magic though.

As explained at the start, `holm` automatically creates the `/user/{id}` URL for the page in the `user/_id_/page.py` module, so you can have `id: int` dependencies in page and metadata (even layout) functions. Or, as you will see and as you may expect if you are familiar with FastAPI, dependencies that depend on `id: int` in some way. The `id` argument is of course resolved from the `id` path parameter.

With that said, let's create the user profile page:

```python hl_lines="8-12 15 26 36"
from typing import Annotated

from fastapi import Depends
from htmy import ComponentType, html

from ..service import User, get_user

# The `get_user()` function expects an `id: int`. The argument's name and type
# matches the `{id}` path parameter, which means we can use `get_user()` as
# a FastAPI dependency without any additional work (FastAPI will resolve the
# `id: int` argument correctly from the `{id}` path parameter)! Let's do this.
DependsUser = Annotated[User | None, Depends(get_user)]


def metadata(id: int, user: DependsUser) -> dict[str, str]:
    """
    Metadata function that uses the `DependsUser` annotated FastAPI dependency
    to get the user whose ID was submitted in the `{id}` path parameter (which
    is the URL segment corresponding to the `_id_` package name.)

    Just to show that the user was indeed loaded based on the submitted ID,
    the metadata function also uses the `id: int` argument, that is resolved
    by FastAPI from the `{id}` path parameter.
    """
    user_title = "Not Found" if user is None else user.name
    if user and user.id != id:
        raise ValueError(
            "id and user.id should match, because both values originate "
            "from the `{id}` path parameter the client submitted."
        )
    return {
        "title": f"User | {user_title}",
    }


async def page(user: DependsUser) -> ComponentType:
    """
    Page function that uses the `DependsUser` annotated FastAPI dependency
    to get the user whose ID was submitted in the `{id}` path parameter.

    FastAPI resolves each dependency once, meaning we're only loading the user
    once, and we share it between application components through FastAPI's
    dependency injection system.
    """
    if user is None:
        return html.div(
            html.h1("The user does not exist"),
        )

    return html.div(
        html.strong("Name:"),
        html.span(user.name),
        html.strong("ID:"),
        html.span(str(user.id)),
        html.strong("Email:"),
        html.span(user.email),
        style="display: grid; grid-template-columns: max-content 1fr; gap: 1rem;",
    )
```

Here is a summary of the key takeaways:

- Packages names of `_identifier_` format correspond to `{identifier}` URL segments.
- `{identifier}` URL segments are FastAPI path parameters, and thus they enable dynamic routing.
- The `get_user(id: int)` service function can be used as a FastAPI dependency to conveniently get access to the requested user in page, metadata, and layout functions. This is also efficient, because FastAPI resolves each dependency only once.

## Run the application

That's it! You can now run your application using `uvicorn`:

```bash
uvicorn main:app --reload
```

Or with `fastapi-cli` if installed:

```bash
fastapi dev main.py
```

You can now open your browser, navigate to `http://localhost:8000/`, and start exploring your application in action.
