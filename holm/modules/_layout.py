from __future__ import annotations

import inspect
from dataclasses import dataclass
from typing import TYPE_CHECKING, Protocol

from fastapi import Depends
from htmy import as_component_type

if TYPE_CHECKING:
    from collections.abc import Callable
    from typing import Any, TypeGuard

    from htmy import Component

    from holm.fastapi import FastAPIDependency
    from holm.typing import Layout, LayoutFactory, TextToLayoutConverter


class LayoutDefinition(Protocol):
    """Protocol definition for objects (usually modules) that define a layout."""

    @property
    def layout(self) -> Layout: ...


@dataclass(frozen=True, slots=True)
class CustomLayoutDefinition:
    """
    Custom layout definition that wraps a layout callable.

    This class allows creating layout definitions from any layout function,
    including those generated dynamically (e.g., from HTML files).
    """

    layout: Layout
    """The layout callable."""


def make_str_to_layout_definition_transformer(
    text_to_layout: TextToLayoutConverter,
) -> Callable[[str], LayoutDefinition]:
    """
    Returns a function that converts plain string content to a `LayoutDefinition`.

    This is just a utility wrapper for creating `CustomLayoutDefinition` instances.

    Arguments:
        text_to_layout: The function to use to convert the plain string content to a `Layout` function.
    """

    def make_layout(content: str) -> LayoutDefinition:
        return CustomLayoutDefinition(text_to_layout(content))

    return make_layout


def is_layout_definition(obj: Any) -> TypeGuard[LayoutDefinition]:
    """Type guard for `LayoutDefinition`."""
    layout = getattr(obj, "layout", None)
    return callable(layout)


@dataclass(frozen=True, slots=True)
class without_layout:
    """
    Marker that signals that the component it contains should not be
    wrapped by the application in any parent layouts.

    This utility must only be used as a return value wrapper in application
    components whose return value could be wrapped in a parent layout by
    `holm`. For example pages, submit handlers, layouts.

    Attempting to render an instance of this class results in a `RuntimeError`.
    The only reason it implements the `htmy()` method is to make static code
    analysis tools accept it as an `htmy.Component`.
    """

    component: Component
    """The wrapped component."""

    def htmy(self, _: Any) -> Component:
        raise RuntimeError(f"{type(self).__name__} must never be part of the htmy component tree!")


def combine_layouts_to_dependency(
    outer_dep: FastAPIDependency[LayoutFactory],
    inner: Layout | None,
) -> FastAPIDependency[LayoutFactory]:
    """
    Creates a layout factory dependency that wraps the inner layout inside the outer layout.

    Arguments:
        outer_dep: FastAPI dependency that returns the layout factory of the outer layout.
        inner: The inner layout component.
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
            if inspect.isawaitable(inner_result):
                inner_result = await inner_result

            if isinstance(inner_result, without_layout):
                return inner_result.component

            result = outer(as_component_type(inner_result))
            if inspect.isawaitable(result):
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
    if inspect.iscoroutinefunction(layout):

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
