# Utilities

## `without_layout()`

You can use `without_layout()` in `page()`, `handle_submit()`, or `layout()` functions to opt their return value out of automatic layout wrapping.

When you wrap the **return value** of a layout, page, or submit handler with `without_layout()`, `holm` will break the layout wrapping chain at that point and render the wrapped component directly, without passing it to further parent layouts. In other words, always the innermost `without_layout()` use -- the one closest to the page or submit handler -- will take effect.

This is particularly useful for rendering partial HTML fragments from pages or submit handlers, a common requirement when working with libraries like HTMX. For example, you can serve the full HTML document on initial page load, but return only the updated portion of the page for subsequent HTMX requests.

Here is an example of a `page` that serves a full HTML document for regular browser requests, but returns only a partial (the page content) for HTMX requests:

```python
from fastapi import Request
from htmy import Component, html

from holm import without_layout


def page(request: Request) -> Component:
    content = html.h1("This is the page content")

    if request.headers.get("HX-Request") == "true":
        # It's an HTMX request, return only the page content
        # without the layouts that wrap it.
        return without_layout(content)

    # It's a regular request, return props for the parent layout
    # to render the full page.
    return content
```
