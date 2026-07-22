from __future__ import annotations

import inspect
from functools import lru_cache
from itertools import chain
from pathlib import Path
from typing import TYPE_CHECKING, Any, cast

from fastapi import APIRouter, Depends, FastAPI, Response
from fasthx.htmy import HTMY
from htmy import Component, Context, MutableContext, WithContext, as_component_sequence, as_component_type
from htmy.jinja import DefaultSlots, JinjaTemplates

from ._jinja import make_jinja_layout_definition, make_jinja_templates
from ._model import AppConfig, AppNode, PackageInfo, module_names
from .module_options._actions import get_actions, has_actions
from .module_options._metadata import Metadata, MetadataMapping, empty_metadata_dep, get_metadata_dependency
from .module_options._submit_handler import get_submit_handler
from .modules._api import is_api_definition
from .modules._error import load_error_handler_owner, register_error_handlers
from .modules._layout import (
    combine_layouts_to_dependency,
    empty_layout_dependency,
    is_layout_definition,
    without_layout,
)
from .modules._page import is_page_definition
from .typing import LayoutFactory, PlainAPIFactory, RenderingAPIFactory

if TYPE_CHECKING:
    from collections.abc import Iterable, Mapping

    from .fastapi import FastAPIDependency


def App(
    *,
    app: FastAPI | None = None,
    htmy: HTMY | None = None,
    layout_slots: Mapping[str, Component] | None = None,
) -> FastAPI:
    """
    Creates a FastAPI application with all the routes that are defined in the application package.

    The app-scope default context (default/layout slots, and metadata if any) is automatically
    injected into the `htmy` rendering context whenever `holm` is responsible for rendering.

    -----

    Jinja template rendering:

    When `holm` creates and owns the `htmy` renderer (the `htmy` argument is `None`), a
    `htmy.jinja.JinjaTemplates` instance is automatically injected into the default `htmy`
    rendering context. Its template source is created lazily, only when necessary.

    The templates root is the Python import root (the directory containing the app package,
    not the app package itself). Template names are relative to that root, so they must be
    prefixed with the app package name (e.g. `<app_package>/some_path/my-component.jinja`).
    Templates may also live outside the app package, for example in a sibling `templates/`
    directory, and are referenced the same way, relative to the import root.

    If you provide your own `htmy` and want to use `holm.JinjaTemplate` components in your
    application, you must add a pre-configured `htmy.jinja.JinjaTemplates` object to its
    default context yourself.

    Arguments:
        app: Optional FastAPI application to use. If `None`, a FastAPI instance is automatically created.
        htmy: Optional `fasthx.htmy.HTMY` instance to use for server-side rendering. If `None`,
            a default instance is created. See "Jinja template rendering" above for how `holm`
            configures Jinja support on an owned renderer, and what you need to do if you pass
            your own.
        layout_slots: Optional mapping of default named slots, made available as `DefaultSlots`
            to every `htmy` component (including Jinja layouts) that's automatically rendered
            by `holm`.
    """
    if app is None:
        app = FastAPI()

    config = AppConfig.default()
    if htmy is None:
        config.add_to_default_context(
            JinjaTemplates(lambda: make_jinja_templates(config.root_dir)).to_context()
        )

        htmy = HTMY()

    if layout_slots is not None:
        config.add_to_default_context(DefaultSlots(layout_slots).to_context())

    packages = _discover_app_packages(config)
    root_node = _build_app_tree(packages)

    # Register error handlers
    if pkg := root_node.package:
        register_error_handlers(app, load_error_handler_owner(pkg), htmy=htmy)

    # Build the API
    app.include_router(_build_api(root_node, htmy=htmy, config=config))

    return app


def _build_api(
    node: AppNode,
    *,
    base_layout_dep: FastAPIDependency[LayoutFactory] = empty_layout_dependency,
    config: AppConfig,
    htmy: HTMY,
) -> APIRouter:
    """
    Recursively builds an `APIRouter` based on the application defined by `node`.

    Arguments:
        node: Application definition.
        base_layout_dep: The base layout dependency to use for the API.
        config: The application configuration.
        htmy: The `fasthx.htmy.HTMY` instance to use for server-side rendering.
    """
    layout_dep = base_layout_dep  # In case there is no package or it has no layout module.
    pkg = node.package
    api = _make_api_router_for_package(pkg, htmy)
    if pkg is not None:
        # -- Try to import all relevant modules.
        layout_definition = pkg.import_module("layout", is_layout_definition)
        if layout_definition is None:
            layout_definition = make_jinja_layout_definition(pkg, config)

        page_definition = pkg.import_module("page", is_page_definition)
        actions_module = pkg.import_module("actions", has_actions)

        # -- Resolve dependencies.
        layout_dep = combine_layouts_to_dependency(
            base_layout_dep, None if layout_definition is None else layout_definition.layout
        )
        page_dep, submit_handler_dep, metadata_dep = (
            (None, None, None)
            if page_definition is None
            else (
                page_definition.page,
                get_submit_handler(page_definition),
                get_metadata_dependency(page_definition),
            )
        )

        # -- Register the page.
        if page_dep is not None:
            path_operation = _make_page_path_operation(
                layout_dep=layout_dep,
                metadata_dep=empty_metadata_dep if metadata_dep is None else metadata_dep,
                page_dep=page_dep,
                config=config,
            )

            # Register the route with rendering.
            api.get(
                "/",
                response_model=None,
                # mypy can't infer that the modules is not None.
                name=page_definition.__name__,  # type: ignore[union-attr]
                description=page_dep.__doc__,
                tags=["Page"],
            )(htmy.page(_components_with_context)(path_operation))

        # -- Register the submit handler.
        if submit_handler_dep is not None:
            path_operation = _make_page_path_operation(
                layout_dep=layout_dep,
                metadata_dep=empty_metadata_dep if metadata_dep is None else metadata_dep,
                page_dep=submit_handler_dep,
                config=config,
            )

            # Register the route with rendering.
            api.post(
                "/",
                response_model=None,
                # mypy can't infer that the modules is not None.
                name=f"{page_definition.__name__}.handle_submit",  # type: ignore[union-attr]
                description=submit_handler_dep.__doc__,
                tags=["Page", "Submit"],
            )(htmy.page(_components_with_context)(path_operation))

        # -- Register actions from every action owner.
        for actions in (a for a in (get_actions(page_definition), get_actions(actions_module)) if a):
            for action_key, desc in actions.items():
                # Always route through `_make_page_path_operation()` so every action render
                # receives the app-scope default context via the component tree.
                path_operation = _make_page_path_operation(
                    layout_dep=layout_dep if desc.use_layout else empty_layout_dependency,
                    metadata_dep=get_metadata_dependency(desc),
                    page_dep=desc.action,
                    config=config,
                )
                route = htmy.page(_components_with_context)(path_operation)

                api.api_route(action_key[0], **desc.route_args)(route)

    for sub_url, child_node in node.subtree.items():
        api.include_router(
            _build_api(
                child_node,
                base_layout_dep=layout_dep,
                config=config,
                htmy=htmy,
            ),
            prefix=sub_url,
        )

    return api


def _build_app_tree(packages: Iterable[PackageInfo]) -> AppNode:
    """
    Returns an `AppNode` that represents the entire package tree of the application.

    Arguments:
        packages: The packages to include in the tree.
    """
    root = AppNode("/")

    for p in packages:
        root.add(p)

    return root


def _discover_app_packages(config: AppConfig) -> set[PackageInfo]:
    """
    Discovers all packages that are part of the application and returns them as a set.
    """

    @lru_cache()
    def is_excluded(path: Path) -> bool:
        """Returns whether the given file or package path should be excluded from the application."""
        return any(
            # Exclude if a path segment starts with an underscore but does not end with one.
            # Path segments that both start and end with an underscore represent path parameters!
            (p.startswith("_") and not p.endswith("_"))
            # Also exclude paths that start with a dot (virtual env, git, etc.)
            or p.startswith(".")
            for p in path.parts
        )

    packages: set[PackageInfo] = set()

    for f in chain(
        config.app_dir.rglob("*.py"),
        # Only `layout.jinja` is recognized as a Jinja layout module. Other `.jinja`
        # files are not valid holm modules and must not produce package markers.
        config.app_dir.rglob("layout.jinja"),
    ):
        if f.stem not in module_names:
            continue

        if not is_excluded(f.parent.relative_to(config.root_dir)):
            packages.add(PackageInfo.from_marker_file(f, config=config))

    return packages


def _make_api_router_for_package(pkg: PackageInfo | None, htmy: HTMY) -> APIRouter:
    """
    Creates an `APIRouter` for the given package.
    """
    api_module = None if pkg is None else pkg.import_module("api", is_api_definition)
    if api_module is None:
        return APIRouter()

    # api is either an APIRouter or a callable (is_api_definition validates that).
    api = api_module.api
    if isinstance(api, APIRouter):
        return api

    # Inspect the api callable instead of catching errors. Using a try-except with
    # a TypeError handler would hide many potential issues that would then be
    # hard to figure out without the exception trace.
    num_params = len(inspect.signature(api).parameters)
    if num_params == 0:
        api = cast(PlainAPIFactory, api)()
    elif num_params == 1:
        api = cast(RenderingAPIFactory, api)(htmy)

    if isinstance(api, APIRouter):
        return api

    raise ValueError(f"The api function of {cast(PackageInfo, pkg).package_name} must return an APIRouter.")


def _make_page_path_operation(
    *,
    layout_dep: FastAPIDependency[LayoutFactory],
    metadata_dep: FastAPIDependency[MetadataMapping | None],
    page_dep: FastAPIDependency[Any],
    config: AppConfig,
) -> FastAPIDependency[tuple[Component, Context] | Response]:
    """
    Creates the path operation for a page-like route.

    Returns a `(component, context)` tuple where `context` starts from the app-scope default
    context and is extended with the page metadata. A FastAPI `Response` short-circuits before
    the component selector runs.
    """

    async def path_operation(
        # Start by evaluating the page dependency, it is the most likely to raise an error
        # (could even be a performance improvement strategy when returning a Response).
        page: Component | Response = Depends(page_dep),  # noqa: B008
        # Next should be the metadata dependency. It is usually relatively lightweight.
        metadata: MetadataMapping | None = Depends(metadata_dep),  # noqa: B008
        # Evaluate the layout dependency last. It's often a sequence of nested dependencies
        # and it is also unlikely to fail.
        layout: LayoutFactory = Depends(layout_dep),  # noqa: B008
    ) -> tuple[Component, Context] | Response:
        if isinstance(page, Response):
            return page

        context: MutableContext = {}
        context.update(config.default_context)
        context.update(Metadata(metadata).to_context())  # always; empty Metadata when None

        if isinstance(page, without_layout):
            return page.component, context

        result = layout(as_component_type(page))
        # We must await here if result is an Awaitable, otherwise we would pass an
        # awaitable to htmy.page() and rendering that would fail.
        if inspect.isawaitable(result):
            result = await result

        return result, context

    return path_operation


def _components_with_context(data: tuple[Component, Context]) -> Component:
    """
    Stateless component selector that applies the per-request `htmy` context (metadata and
    app-scope default slots) to the layout-wrapped component tree via `WithContext`.
    """
    components, context = data
    return WithContext(*as_component_sequence(components), context=context)
