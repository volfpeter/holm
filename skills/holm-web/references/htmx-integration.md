# HTMX integration

`holm` does not require HTMX

The critical `holm`-specific concern is the relationship between pages (full HTML documents) and actions (fragments)

## Pages vs Actions in HTMX

- Pages and submit handlers (`page.py`) return full HTML wrapped in layouts by default; they serve regular browser requests AND `hx-boost` navigation
- Actions (`@action.*`) return HTML fragments without layouts by default; natural target for `hx-get`, `hx-post`, etc.

Strongly prefer full page rendering in pages and submit handlers, and actions partials

Pages and submit handlers can use `without_layout()` to avoid wrapping the result in parent layouts, this should be the exception
