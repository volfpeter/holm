# Layouts

## `layout.py`

```python
from fastapi import Request
from htmy import ComponentSequence, Context, component, html
from holm import Metadata

async def layout(children: ComponentType, request: Request) -> ComponentSequence:
    # Layout route/dependency
    return _layout_component(children=children)


@component
def _layout_component(children: ComponentType, context: Context) -> ComponentSequence:
    # Layout component
    metadata = Metadata.from_context(context)
    return (
        html.DOCTYPE.html,
        html.html(
            html.head(html.title(metadata.get("title", "App"))),
            html.body(children),
        ),
    )
```

- `layout` is a sync or async FastAPI dependency with a mandatory `children` argument plus any FastAPI dependencies
- `_layout_component` is the `htmy` function component used for the layout, separation of route and component is preferred if route is a component
- Layouts wrap all pages and sub-layouts in the same package and subpackages
- Sub-package layouts wrap their own pages and are themselves wrapped by parent layouts
- Can provide `htmy` context for the entire subtree with a `ContextProvider` component

## Jinja layouts (`layout.jinja`)

Alternative to `layout.py`: standard Jinja2 templates picked up automatically when present in a package. If both `layout.py` and `layout.jinja` exist, the Python layout takes precedence. See `references/jinja.md` for full details.

## `without_layout()`

- Breaks out of parent layout wrapping
- The innermost `without_layout()` takes effect
- Only works as a return value from `page`, `handle_submit`, or `layout`
