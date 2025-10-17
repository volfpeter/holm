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


# Static metadata
metadata = {"title": "Home | TODO App"}


def page(q: str = "") -> Component:
    """Home page content."""
    return page_content(q)


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
