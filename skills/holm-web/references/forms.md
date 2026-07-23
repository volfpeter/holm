# Forms

## Submit handlers (`page.py`)

```python
from typing import Annotated
from fastapi import Form
from htmy import ComponentType, html

def page() -> ComponentType:
    return html.form(html.input_(name="q"), method="POST")

def handle_submit(q: Annotated[str, Form()]) -> ComponentType:
    return html.p(f"You submitted: {q}")
```

- FastAPI dependency, can be `async`
- Creates a `POST /` route alongside the `GET /` page route
- `method="POST"` in the form is required to reach `handle_submit`; otherwise the form submits to `page()` via GET
- `handle_submit()` has the same rules and default behavior as `page()`

## HTMX form submissions to `handle_submit`

```python
from holm import without_layout

def page() -> ComponentType:
    return html.form(
        html.input_(name="title"),
        method="POST",
        hx_post=".",
        hx_target="#todo-list",
        hx_swap="beforeend",
    )

def handle_submit(request: Request, title: Annotated[str, Form()]) -> ComponentType:
    todo = add_todo(title)
    content = html.li(todo.title)
    is_htmx = request.headers.get("HX-Request") == "true"
    is_boosted = request.headers.get("HX-Boosted") == "true"
    return without_layout(content) if is_htmx and not is_boosted else content
```

- `hx_post="."` submits to the current URL
- Prefer only full page responses in submit handlers, use actions for partials
- Custom HTMX partial logic in `handle_submit()`
