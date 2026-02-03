from __future__ import annotations

from typing import TYPE_CHECKING, Protocol

if TYPE_CHECKING:
    from typing import Any, TypeGuard

    from holm.typing import Page


class PageDefinition(Protocol):
    """Protocol definition for objects (usually modules) that define a page."""

    @property
    def __name__(self) -> str:
        """
        Page definitions are expected to have a `__name__` attribute,
        since they are modules.
        """
        ...

    @property
    def page(self) -> Page:
        """The page implementation."""
        ...


def is_page_definition(obj: Any) -> TypeGuard[PageDefinition]:
    """Type guard for `PageDefinition`."""
    page = getattr(obj, "page", None)
    return callable(page)
