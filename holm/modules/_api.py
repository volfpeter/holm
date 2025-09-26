from collections.abc import Callable
from typing import Any, Protocol, TypeAlias, TypeGuard

from fastapi import APIRouter
from fasthx.htmy import HTMY

PlainAPIFactory: TypeAlias = Callable[[], APIRouter]
RenderingAPIFactory: TypeAlias = Callable[[HTMY], APIRouter]

APIFactory: TypeAlias = PlainAPIFactory | RenderingAPIFactory
"""
`APIRouter` factory definition.

It is a callable that optionally accepts a `HTMY` instance as an argument to make sure
the same renderer is used throughout the application if the API does HTML rendering.
Otherwise the argument can be omitted.
"""


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
    # Check APIRouter first, because that's also callable.
    return isinstance(api, APIRouter) or callable(api)
