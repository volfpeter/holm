import inspect
from asyncio import iscoroutinefunction
from collections.abc import Awaitable, Callable, Coroutine
from typing import Any, Protocol, TypeAlias, TypeGuard

from fastapi import Depends
from htmy import as_component_type

from holm.fastapi import FastAPIDependency


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


Layout: TypeAlias = SyncLayout | AsyncLayout
"""
Layout type definition.

A layout is a callable that expects a single positional argument the component or data returned
by the wrapped layout or page, and returns the properties for its wrapper layout. The root layout
must always return a `Component`.
"""

LayoutFactory: TypeAlias = Callable[[Any], Any | Coroutine[None, None, Any]]
"""
A layout factory is a sync or asynccallable that expects a single argument (the layout's properties)
and returns the properties for its wrapper layout.

The root layout factory must always return a `htmy` `Component`.
"""


class LayoutDefinition(Protocol):
    """Protocol definition for objects (usually modules) that define a layout."""

    @property
    def layout(self) -> Layout: ...


def is_layout_definition(obj: Any) -> TypeGuard[LayoutDefinition]:
    """Type guard for `LayoutDefinition`."""
    layout = getattr(obj, "layout", None)
    return callable(layout)


def combine_layouts_to_dependency(
    outer_dep: FastAPIDependency[LayoutFactory], inner: Layout | None
) -> FastAPIDependency[LayoutFactory]:
    """
    Creates a layout factory dependency that wraps the inner layout inside the outer layout.

    Arguments:
        outer: The outer layout factory.
        inner: The inner layout factory.
    """
    if inner is None:
        return outer_dep

    inner_dep = layout_to_dependency(inner)

    async def combined_layout_dep(
        outer: LayoutFactory = Depends(outer_dep),  # noqa: B008
        inner: LayoutFactory = Depends(inner_dep),  # noqa: B008
    ) -> LayoutFactory:
        async def layout_factory(props: Any) -> Any:
            inner_result = inner(props)
            if isinstance(inner_result, Awaitable):
                inner_result = await inner_result

            result = outer(as_component_type(inner_result))
            if isinstance(result, Awaitable):
                result = await result

            return result

        return layout_factory

    return combined_layout_dep


def empty_layout(props: Any) -> Any:
    """`LayoutFactory` that simply returns the received props."""
    return props


def empty_layout_dependency() -> FastAPIDependency[LayoutFactory]:
    """
    FastAPI dependency that returns `empty_layout`.
    """
    return empty_layout


def layout_to_dependency(layout: Layout) -> FastAPIDependency[LayoutFactory]:
    """
    Converts a layout to a FastAPI dependency that returns a layout factory.
    """
    # eval_str=True is necessary in case future __annotations__ is used
    # where the layout is function is defined.
    params = tuple(inspect.signature(layout, eval_str=True).parameters.values())
    props_index = next((i for i, p in enumerate(params) if p.name != "self"), -1)
    if props_index == -1:
        raise ValueError("Layout factory must at least one argument.")

    result: FastAPIDependency[LayoutFactory]
    if iscoroutinefunction(layout):

        async def async_layout_factory_dep(**kwargs: Any) -> LayoutFactory:
            async def layout_factory(props: Any) -> Any:
                return await layout(props, **kwargs)

            return layout_factory

        result = async_layout_factory_dep
    else:

        def sync_layout_factory_dep(**kwargs: Any) -> LayoutFactory:
            def layout_factory(props: Any) -> Any:
                return layout(props, **kwargs)

            return layout_factory

        result = sync_layout_factory_dep

    # Copy the dependencies part of the signature from the original function, so
    # FastAPI can resolve those arguments. The props argument must be excluded.
    result.__signature__ = inspect.Signature(params[props_index + 1 :])  # type: ignore[union-attr]

    return result
