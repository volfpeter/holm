from collections.abc import Callable, Coroutine
from typing import Any, TypeAlias, TypeVar

from fastapi import Request

_T = TypeVar("_T")

SyncFastAPIDependency: TypeAlias = Callable[..., _T]
AsyncFastAPIDependency: TypeAlias = Callable[..., Coroutine[None, None, _T]]

FastAPIDependency: TypeAlias = SyncFastAPIDependency[_T] | AsyncFastAPIDependency[_T]
"""FastAPI dependency typing."""

FastAPIErrorHandler: TypeAlias = Callable[[Request, Exception], Coroutine[None, None, Any]]
"""Generic FastAPI error handler typing."""
