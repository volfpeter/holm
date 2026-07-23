# Pages

## `page.py`

```python
from htmy import ComponentType, html

metadata = {"title": "Home"}

def page() -> ComponentType:
    return html.h1("Hello")
```

- `page` is a FastAPI dependency, can be `async`
- Handles `GET /` for its package's URL path
- Returns props for the direct parent layout, or a `Component` if there is no layout
- `metadata`: static mapping or a FastAPI dependency returning a mapping
- Access metadata in any component: `Metadata.from_context(context)`
