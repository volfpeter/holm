---
name: holm-web
description: >
  Use when working on web apps built with holm, or to answer questions about holm.
  Covers file-system routing, layouts, pages, actions, page metadata, form handling, error handling,
  partial HTML and HTMX considerations.
---

# Building holm web applications

## Architecture summary

- `FastAPI`: underlying web framework; all `holm` pages, layouts, actions, and metadata are FastAPI dependencies (so they can all be `async`)
- `htmy`: async, pure-Python HTML component engine; JSX-like syntax with `html.div(...)`, full typing, async support, and context (no prop drilling)
- `FastHX` (`fasthx.htmy.HTMY`): the rendering layer; `htmy.page()` renders HTML for all requests; `htmy.hx()` renders HTML only for HTMX requests, otherwise keeps FastAPI route behavior
- `holm`: file-system based routing (similar to Next.js), automatic layout composition, page metadata, actions, and submit handlers
- Optional Jinja2 layout/template support via `layout.jinja` and `holm.JinjaTemplate` — see `references/jinja.md`

## Application initialization

```python
from holm import App

app = App()
```

Call `holm.App()` directly within a module in the root application package

Optional:
- pass a pre-configured `FastAPI` app
- pass a custom `fasthx.htmy.HTMY` renderer

## File-system based routing

| File | Purpose | HTTP method |
|------|---------|-------------|
| `page.py` | Page callable | GET `/` |
| `page.py` + `handle_submit` | Submit handler | POST `/` |
| `layout.py` | Layout callable, wraps pages/layouts in subpackages | — |
| `layout.jinja` | Jinja2-based layout (alternative to `layout.py`) | — |
| `actions.py` | Action functions decorated with `@action.*` | custom paths/methods |
| `api.py` | `APIRouter` (JSON or rendering APIs) | custom paths/methods |
| `error.py` / `errors.py` | Error handlers (root only) | — |

Dynamic routes: `_id_` or `{id}` package names become path parameters (`/user/{id}`)

Private packages: prefix with underscore (`_components`) — ignored entirely

The default path for actions is the decorated function's name, underscores replaced with hyphens

Apply REST principles whenever possible

## URL construction

```python
from fastapi import Request


def some_page(request: Request) -> ComponentType:
    url = request.url_for("my_app.users.page")
    return html.a("Users", href=str(url))
```

- Pages and submit handlers: `"my_app.page"`, `"my_app.users.page"` (path is the same, method is different)
- Actions: `"my_app.users.actions.enable_user"`

## Pages vs Actions

- **Pages** (`page.py`) return full HTML (wrapped in layouts); they handle regular browser navigation requests
- **Actions** (`@action.*`) return HTML fragments without layouts by default; ideal for HTML/HTMX partials

## Reference files

| File | Load when… |
|------|------------|
| `references/layouts.md` | Creating or modifying layouts |
| `references/jinja.md` | Using Jinja2 templates/layouts (`layout.jinja`, `JinjaTemplate`) |
| `references/pages.md` | Creating or modifying pages or page metadata |
| `references/actions.md` | Creating actions or HTMX partials |
| `references/forms.md` | Creating submit handlers or form submissions |
| `references/apis.md` | Creating custom `api.py` routers with JSON or mixed rendering |
| `references/htmx-integration.md` | Adding HTMX interactivity, partial rendering, or boosted navigation |
| `references/htmy-context.md` | Working with the htmy rendering context or request processors |
| `references/htmy.md` | Creating or modifying `htmy` components |
| `references/error-handling.md` | Setting up custom error handlers |

## Gotchas

1. Forms without `method="POST"` submit as GET and hit `page()`, not `handle_submit()`
2. `page.py` and `actions.py` and `api.py` in the same package have their routes merged into a single `APIRouter`
3. Returning `Response` objects from pages, actions, or handlers bypasses rendering
4. `holm` auto-wraps `page()` and `layout()` list/tuple returns in `Fragment`. Do not return a list/tuple unless it is a component sequence
5. `htmy` does not flatten nested component sequences: `[comp1, comp2]` is valid, but `[[comp1, comp2]]` is not. Use list unpacking or `Fragment` when mapping/generating components
6. Strongly prefer `ComponentType` and `ComponentSequence` return type annotations over `Component` to avoid component nesting problems!
7. `holm` uses `htmy.page()` for both pages and actions automatically. Actions always return HTML; use `api.py` if you need standard FastAPI behavior
8. Path parameters from `_id_` or `{id}` packages are available as standard FastAPI dependencies in pages, layouts, actions, metadata, and APIs
