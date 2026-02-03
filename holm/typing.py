from collections.abc import Callable, Coroutine, Mapping
from typing import Any, Protocol, TypeAlias

from fastapi import APIRouter
from fasthx.htmy import HTMY

from holm.fastapi import FastAPIDependency, FastAPIErrorHandler

# -- Page typing

Page: TypeAlias = FastAPIDependency[Any]
"""
FastAPI page dependency.

A page may return either the properties for the layout that wraps it (for example a `Component`)
or a FastAPI `Response`.

If the page is not wrapped by a layout and it doesn't return a `Response`,
then it must return a `Component`.
"""

# -- Layout typing


class SyncLayout(Protocol):
    """
    Sync layout protocol definition.
    """

    def __call__(self, __props: Any, /, **dependencies: Any) -> Any: ...


class AsyncLayout(Protocol):
    """
    Async layout protocol definition.
    """

    async def __call__(self, __props: Any, /, **dependencies: Any) -> Any: ...


PropsOnlySyncLayout: TypeAlias = Callable[[Any], Any]
"""Sync layout that only accepts a single position argument, the layout's properties."""

PropsOnlyAsyncLayout: TypeAlias = Callable[[Any], Coroutine[Any, Any, Any]]
"""Async layout that only accepts a single position argument, the layout's properties."""

Layout: TypeAlias = SyncLayout | PropsOnlySyncLayout | AsyncLayout | PropsOnlyAsyncLayout
"""
Layout type definition.

A layout is a callable that expects a single positional argument the component or data returned
by the wrapped layout or page, and returns the properties for its wrapper layout. The root layout
must always return a `Component`.
"""

LayoutFactory: TypeAlias = Callable[[Any], Any | Coroutine[None, None, Any]]
"""
A layout factory is a sync or async callable that expects a single argument (the layout's
properties) and returns the properties for its wrapper layout.

The root layout factory must always return a `htmy` `Component`.
"""

TextToLayoutConverter: TypeAlias = Callable[[str], Layout]
"""
Type alias for functions that convert plain string to a `Layout` function.

The easiest way to create a `TextToLayoutConverter` is to create a wrapper
around `holm.utils.snippet_to_layout`.
"""

# -- Error handler typing

ErrorHandlerMapping: TypeAlias = Mapping[type[Exception] | int, FastAPIErrorHandler]
"""
Mapping type whose keys are exception types or HTTP status codes, and the
corresponding values are FastAPI error handlers.
"""

# -- API typing

PlainAPIFactory: TypeAlias = Callable[[], APIRouter]
"""
Plain, non-rendering `APIRouter` factory type definition.
"""

RenderingAPIFactory: TypeAlias = Callable[[HTMY], APIRouter]
"""
Rendering `APIRouter` factory type definition.
"""

APIFactory: TypeAlias = PlainAPIFactory | RenderingAPIFactory
"""
`APIRouter` factory definition.

It is a callable that optionally accepts a `HTMY` instance as an argument to make sure
the same renderer is used throughout the application if the API does HTML rendering.
Otherwise the argument can be omitted.
"""
