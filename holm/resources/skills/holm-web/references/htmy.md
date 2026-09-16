# htmy

Any object with a sync or async `htmy(context: Context)` method is a component

Strings are components (automatically escaped unless `SafeStr` is used)

Lists/tuples of components are valid; nested lists are not (use `Fragment` or unpacking)

## Typing

- `ComponentType`: single component, use for type annotation
- `ComponentSequence`: `list` or `tuple` of `ComponentType` use for type annotation
- `Component`: union of both, avoid for type annotations unless necessary

`holm` auto-wraps `page()`/`layout()` list/tuple returns in `Fragment`

`htmy` does not flatten nested sequences

## Component kinds

```python
from htmy import ComponentType, Context, component, html


def heading(text: str) -> ComponentType:
    # Component factory, no access to context
    return html.h1(text)


@component.context_only
def navbar(context: Context) -> ComponentType:
    # Context-only function component, no props
    return html.nav("Hello", context.get("user"))


@component
def user_card(user: User, context: Context) -> ComponentType:
    # Component with props (User) and context
    return html.div(user.name)


class User:
    # Regular component, object with `htmy` method
    async def htmy(self, context: Context) -> ComponentType:
        return html.div(self.name)
```

- Use component factory if the `htmy` `context` is not used
- `@component` / `@component.context_only` for standalone functions
- `@component.method` / `@component.context_only_method` for instance methods

## `html` module

All baseline HTML tags: `html.div(...)`, `html.input_(...)`, etc.

Attribute formatting:

- `data_theme` → `data-theme`
- `class_` / `for_` → `class` / `for`
- `bool` → `"true"`/`"false"`
- `None` → skipped
- `disabled=XBool.true` → `disabled`, `disabled=XBool.false` → attribute skipped
- Lists/dicts/tuples/sets → JSON
- Dates → ISO

## Core utilities (`core.py`)

- `Fragment`: wraps children without markup
- `SafeStr`: unescaped string, only for trusted input
- `WithContext`: context provider, needs `htmy_context() -> Context` and must be a component
- `ContextAware`: base class for typed context utilities
- `ErrorBoundary`: fallback on render failure
- `xml_format_string()`: escape `<`, `>`, `&`

## Snippets and Markdown (`snippet.py`, `md.py`)

Use `Snippet` or `MD` for static HTML/markdown instead of building large component trees. For `holm` Jinja layouts, see `references/jinja.md`; `Snippet` is a lower-level `htmy` tool.

```python
from htmy import Snippet, Slots, md

Snippet("template.html", text_resolver=Slots({"header": my_header()}))
md.MD("page.md")
```

- `Slots` replaces `<!-- slot[key] -->` with component (this is `htmy.Snippet` syntax, not `layout.jinja`)
- `MD` parses markdown, uses `MarkdownParser` from context
- Input is treated as **trusted**! Always escape untrusted input first!

## Utils (htmy `utils.py`)

- `join_components(components, separator, pad=False)`: generator
- `join(*items, separator=" ")`: join strings, skip `None`, alias: `join_classes`
- `is_component_sequence()`, `as_component_sequence()`, `as_component_type()`

## Jinja templates

`holm` supports Jinja2 templates as `htmy` components (`holm.JinjaTemplate`) and `layout.jinja` layouts. See `references/jinja.md` — only relevant when using Jinja in holm.
