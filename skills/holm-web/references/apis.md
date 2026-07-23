# APIs (`api.py`)

`api.py` defines a custom `APIRouter` for the package. Plain variable, callable with no args, or callable with a single `HTMY` argument.

## Plain variable (no rendering)

```python
from fastapi import APIRouter

api = APIRouter()

@api.get("/count")
def get_count() -> int:
    return 42
```

## Callable with no arguments

```python
from fastapi import APIRouter

def api() -> APIRouter:
    router = APIRouter()
    @router.get("/count")
    def get_count() -> int:
        return 42
    return router
```

- Page and action routes are merged into the `APIRouter` in `api.py` if it exists in the package
- `api.py` is for `APIRouter` customization and standard FastAPI routes
- Strongly prefer pages and actions for HTML rendering routes, unless you need mixed HTML/JSON routes (in which case use `FastHX` to add rendering to these routes)
