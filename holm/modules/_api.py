from __future__ import annotations

from typing import TYPE_CHECKING, Protocol

from fastapi import APIRouter

if TYPE_CHECKING:
    from typing import Any, TypeGuard

    from holm.typing import APIFactory


class APIDefinition(Protocol):
    """Protocol definition for objects (usually modules) that define an API."""

    @property
    def api(self) -> APIFactory | APIRouter:
        """
        The property may be an `APIFactory` or a plain `APIRouter` instance."""
        ...


def is_api_definition(obj: Any) -> TypeGuard[APIDefinition]:
    """Type guard for `APIDefinition`."""
    api = getattr(obj, "api", None)
    # APIRouter is also callable, so callable(api) would be enough,
    # but let's be a bit more thorough in this case.
    return isinstance(api, APIRouter) or callable(api)
