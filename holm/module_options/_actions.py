import sys
from collections.abc import Callable, Collection, Sequence
from dataclasses import dataclass
from enum import Enum
from typing import Any, Literal, TypeAlias, TypeGuard

from fastapi.params import Depends as DependsParam

from holm.fastapi import FastAPIDependency

ActionDependency: TypeAlias = FastAPIDependency[Any]
"""
FastAPI action dependency.

Actions must normally return a `Component` or a FastAPI `Response`, but if they are wrapped
in a layout, then they must be allowed to return whatever their parent layout expects.
"""

ActionDependencyDecorator: TypeAlias = Callable[[ActionDependency], ActionDependency]


@dataclass(slots=True, eq=False, kw_only=True)
class ActionDescriptor:
    action: ActionDependency
    route_args: dict[str, Any]
    with_layout: bool


ActionDescriptors: TypeAlias = dict[str, ActionDescriptor]
"""
Typing for the value of `_actions_variable`.

Dictionary that maps action paths to action descriptors. This allows
decorator stacking (registering the same action with multiple paths).
"""

HTTPMethod: TypeAlias = Literal["GET", "POST", "PUT", "PATCH", "DELETE"]


_actions_variable = "_holm_action_descriptors"
"""The name of the variable that stores action descriptors in modules."""


def get_actions(obj: Any) -> ActionDescriptors | None:
    """
    Loads and returns the action descriptors mapping if it exists in the given object.

    Action owners must have a variable whose name must match the value of `_actions_variable`,
    and the value must be a dictionary mapping action paths to action descriptors.
    """
    actions = getattr(obj, _actions_variable, None)
    return actions if isinstance(actions, dict) else None


def has_actions(obj: Any) -> TypeGuard[Any]:
    """
    "Type guard" that returns `True` if the given object contains actions.
    """
    return bool(get_actions(obj))


@dataclass(slots=True, repr=False, eq=False)
class ActionDecorator:
    """Decorators for registering actions."""

    def __call__(
        self,
        path: str | None = None,
        *,
        with_layout: bool = False,
        methods: Collection[HTTPMethod] | None = None,
        dependencies: Sequence[DependsParam] | None = None,
        deprecated: bool | None = None,
        tags: list[str | Enum] | None = None,
    ) -> ActionDependencyDecorator:
        """
        Decorator for registering an action with arbitrary HTTP `methods`.

        Corresponding FastAPI route decorator: `APIRouter.api_route()`.

        Arguments:
            with_layout: Whether to render the action's return value in the
                containing package's layout (same as a page).
            path: The action's path (within the package's `APIRouter`). If `None`,
                the decorated function's name is used as the path.
        """

        def decorator(func: ActionDependency) -> ActionDependency:
            self._register_action(
                func,
                with_layout=with_layout,
                path=path,
                dependencies=dependencies,
                deprecated=deprecated,
                methods=methods,
                tags=tags,
            )
            return func

        return decorator

    def get(
        self,
        path: str | None = None,
        *,
        with_layout: bool = False,
        dependencies: Sequence[DependsParam] | None = None,
        deprecated: bool | None = None,
        tags: list[str | Enum] | None = None,
    ) -> ActionDependencyDecorator:
        """
        Decorator for registering an action with an HTTP GET method.

        Corresponding FastAPI route decorator: `APIRouter.get()`.

        Arguments:
            with_layout: Whether to render the action's return value in the
                containing package's layout (same as a page).
            path: The action's path (within the package's `APIRouter`). If `None`,
                the decorated function's name is used as the path.
        """

        def decorator(func: ActionDependency) -> ActionDependency:
            self._register_action(
                func,
                with_layout=with_layout,
                path=path,
                dependencies=dependencies,
                deprecated=deprecated,
                methods=("GET",),
                tags=tags,
            )
            return func

        return decorator

    def post(
        self,
        path: str | None = None,
        *,
        with_layout: bool = False,
        dependencies: Sequence[DependsParam] | None = None,
        deprecated: bool | None = None,
        tags: list[str | Enum] | None = None,
    ) -> ActionDependencyDecorator:
        """
        Decorator for registering an action with an HTTP POST method.

        Corresponding FastAPI route decorator: `APIRouter.post()`.

        Arguments:
            with_layout: Whether to render the action's return value in the
                containing package's layout (same as a page).
            path: The action's path (within the package's `APIRouter`). If `None`,
                the decorated function's name is used as the path.
        """

        def decorator(func: ActionDependency) -> ActionDependency:
            self._register_action(
                func,
                with_layout=with_layout,
                path=path,
                dependencies=dependencies,
                deprecated=deprecated,
                methods=("POST",),
                tags=tags,
            )
            return func

        return decorator

    def put(
        self,
        path: str | None = None,
        *,
        with_layout: bool = False,
        dependencies: Sequence[DependsParam] | None = None,
        deprecated: bool | None = None,
        tags: list[str | Enum] | None = None,
    ) -> ActionDependencyDecorator:
        """
        Decorator for registering an action with an HTTP PUT method.

        Corresponding FastAPI route decorator: `APIRouter.put()`.

        Arguments:
            with_layout: Whether to render the action's return value in the
                containing package's layout (same as a page).
            path: The action's path (within the package's `APIRouter`). If `None`,
                the decorated function's name is used as the path.
        """

        def decorator(func: ActionDependency) -> ActionDependency:
            self._register_action(
                func,
                with_layout=with_layout,
                path=path,
                dependencies=dependencies,
                deprecated=deprecated,
                methods=("PUT",),
                tags=tags,
            )
            return func

        return decorator

    def patch(
        self,
        path: str | None = None,
        *,
        with_layout: bool = False,
        dependencies: Sequence[DependsParam] | None = None,
        deprecated: bool | None = None,
        tags: list[str | Enum] | None = None,
    ) -> ActionDependencyDecorator:
        """
        Decorator for registering an action with an HTTP PATCH method.

        Corresponding FastAPI route decorator: `APIRouter.patch()`.

        Arguments:
            with_layout: Whether to render the action's return value in the
                containing package's layout (same as a page).
            path: The action's path (within the package's `APIRouter`). If `None`,
                the decorated function's name is used as the path.
        """

        def decorator(func: ActionDependency) -> ActionDependency:
            self._register_action(
                func,
                with_layout=with_layout,
                path=path,
                dependencies=dependencies,
                deprecated=deprecated,
                methods=("PATCH",),
                tags=tags,
            )
            return func

        return decorator

    def delete(
        self,
        path: str | None = None,
        *,
        with_layout: bool = False,
        dependencies: Sequence[DependsParam] | None = None,
        deprecated: bool | None = None,
        tags: list[str | Enum] | None = None,
    ) -> ActionDependencyDecorator:
        """
        Decorator for registering an action with an HTTP DELETE method.

        Corresponding FastAPI route decorator: `APIRouter.delete()`.

        Arguments:
            with_layout: Whether to render the action's return value in the
                containing package's layout (same as a page).
            path: The action's path (within the package's `APIRouter`). If `None`,
                the decorated function's name is used as the path.
        """

        def decorator(func: ActionDependency) -> ActionDependency:
            self._register_action(
                func,
                with_layout=with_layout,
                path=path,
                dependencies=dependencies,
                deprecated=deprecated,
                methods=("DELETE",),
                tags=tags,
            )
            return func

        return decorator

    def _register_action(
        self,
        action: ActionDependency,
        *,
        with_layout: bool = False,
        path: str | None,
        tags: list[str | Enum] | None,
        **route_args: Any,
    ) -> None:
        """
        Registers the given action in the module that contains it.

        Arguments:
            with_layout: Whether to render the action's return value in the
                containing package's layout (same as a page).
            path: The action's path (within the package's `APIRouter`). If `None`,
                the decorated function's name is used as the path.
        """
        action_module = action.__module__
        action_name = action.__name__
        module = sys.modules[action_module]
        module_actions: ActionDescriptors | None = getattr(module, _actions_variable, None)
        if module_actions is None:
            module_actions = {}
            setattr(module, _actions_variable, module_actions)

        if path is None:
            path = f"/{action_name}"

        route_args["name"] = f"{action_module}.{action_name}"
        # Use the Action tag if no tags were set by the user.
        route_args["tags"] = ["Action"] if tags is None else tags
        route_args["response_model"] = None  # Don't generate a response schema.

        # Register the action.
        module_actions[path] = ActionDescriptor(
            action=action,
            route_args=route_args,
            with_layout=with_layout,
        )


action = ActionDecorator()
"""
Decorator for registering actions.

Decorator arguments map directly to the corresponding FastAPI route decorator's arguments,
unless the documentation states otherwise.
"""
