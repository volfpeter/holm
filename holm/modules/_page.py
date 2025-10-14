from typing import Any, Protocol, TypeAlias, TypeGuard

from holm.fastapi import FastAPIDependency

Page: TypeAlias = FastAPIDependency[Any]
"""FastAPI page dependency.

A page may return either the properties for the layout that wraps it (for example a `Component`)
or a FastAPI `Response`.

If the page is not wrapped by a layout and it doesn't return a `Response`,
then it must return a `Component`.
"""


class PageDefinition(Protocol):
    """Protocol definition for objects (usually modules) that define a page."""

    @property
    def page(self) -> Page: ...


def is_page_definition(obj: Any) -> TypeGuard[PageDefinition]:
    """Type guard for `PageDefinition`."""
    page = getattr(obj, "page", None)
    return callable(page)
