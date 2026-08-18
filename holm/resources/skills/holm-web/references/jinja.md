# Jinja templates and layouts

`holm` 0.10+ ships first-class Jinja2 support. `layout.html` (Python `str.format()`) is gone.

## Jinja layouts (`layout.jinja`)

Alternative to `layout.py`, picked up automatically when present in a package.

```jinja
<!doctype html>
<html>
  <head><title>{{ metadata.title }}</title></head>
  <body>
    {{ slots.navbar }}
    <main>{{ slots.children }}</main>
  </body>
</html>
```

- Standard Jinja2 templates, rendered automatically by `holm`
- Default content slot: `{{ slots.children }}`
- Arbitrary named slots: `{{ slots.<name> }}`
- Page metadata: `{{ metadata.title }}` (always present, possibly empty dict)
- Current request: `{{ request.url.path }}`
- Resolved route params/dependencies: `{{ route_params.<name> }}`
- FastAPI/Starlette `url_for()` is available
- If a page/layout returns a mapping, its keys become slot names; a non-mapping return goes to `children`
- `layout.py` takes precedence when both `layout.py` and `layout.jinja` exist
- Autoescaping is on for `.html`, `.htm`, `.xml`, `.jinja`; `slots.*` are pre-rendered by `htmy` and are safe (never double-escaped)

## Default slots

App-wide default slots are configured on `App()`, not via any string-to-layout converter:

```python
from holm import App

app = App(layout_slots={"navbar": navbar})
```

- Injected into the `htmy` context as `htmy.jinja.DefaultSlots`
- Available in every Jinja layout as `{{ slots.navbar }}`
- Explicit slots returned by a page/layout take precedence over `layout_slots` for the same name

## `JinjaTemplate` component

`holm.JinjaTemplate` is a subclass of `fasthx.htmy.JinjaTemplate` that adds page `metadata` to the Jinja context. Use it anywhere a regular `htmy` component is accepted.

```python
from holm import JinjaTemplate
from htmy import Component


def page() -> Component:
    return JinjaTemplate(
        "my_app/components/card.jinja",
        jinja_context={"title": "Hello"},
    )
```

- Template names are resolved relative to the Python import root (the directory containing the app package), e.g. `my_app/about/page.jinja`
- Templates may live outside the app package, e.g. `templates/card.jinja`
- `metadata`, `request`, and `route_params` are available automatically

## Rendering setup

- When `App()` creates the `HTMY` renderer itself (`htmy=None`), a `htmy.jinja.JinjaTemplates` instance is automatically registered in the default context — zero config
- When you pass your own `HTMY`, `holm` does not modify it; add a pre-configured `htmy.jinja.JinjaTemplates` to its default context yourself, with the template root set to the Python import root and autoescape enabled for `html`, `htm`, `xml`, `jinja`