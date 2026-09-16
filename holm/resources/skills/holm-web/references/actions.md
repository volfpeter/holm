# Actions

## `actions.py` (or `page.py`)

```python
from holm import action
from htmy import ComponentType, html


@action.get()
def user_list() -> ComponentType:
    return html.ul(html.li("Alice"), html.li("Bob"))
```

- FastAPI dependency, can be `async`
- Default path: function name with underscores replaced by hyphens, prefer the default
- Custom path: `@action.post("/do-something")`
- NOT wrapped in layouts by default, use `use_layout=True` to enable
- `metadata=...` for action metadata (useful with `use_layout=True`, usual metadata rules apply)
- Multiple decorators can be stacked on the same function to register multiple routes

## HTMX form submissions to actions

```python
html.form(
    html.input_(name="title"),
    hx_post="/create-todo",
    hx_target="#todo-list",
    hx_swap="beforeend",
)
```

```python
from typing import Annotated

from fastapi import Form


@action.post("/create-todo")
def create_todo(title: Annotated[str, Form()]) -> ComponentType:
    todo = add_todo(title)
    return html.li(todo.title)
```

- Actions are ideal for HTMX partials — they return HTML fragments without layouts by default
- Prefer actions over `handle_submit` for partial responses
