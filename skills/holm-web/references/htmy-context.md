# Rendering context and request processors

## Automatically injected by fasthx

- `CurrentRequest`: the current `fastapi.Request`, access in `htmy` component: `CurrentRequest.from_context(context)`
- `RouteParams`: all resolved FastAPI route parameters, access in `htmy` component: `RouteParams.from_context(context)`

## Automatically injected by holm

- `Metadata`: page- or action-specific metadata, access in `htmy` component: `Metadata.from_context(context)`

For Jinja-specific context (`JinjaTemplates`, `DefaultSlots`, template variables), see `references/jinja.md`.

## Custom request processors

Pass `request_processors` to `HTMY` to inject request-specific data into the `htmy` context:

```python
from fasthx.htmy import HTMY
from holm import App

htmy = HTMY(
    request_processors=[
        lambda request: {"current_user": get_user(request)},
    ]
)

app = App(htmy=htmy)
```

Access in any component:

```python
@component.context_only
async def navbar(context: Context) -> ComponentType:
    user = context.get("current_user")
    ...
```
