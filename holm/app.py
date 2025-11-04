import inspect
from collections.abc import Awaitable, Iterable
from functools import lru_cache
from pathlib import Path
from typing import Any, cast

from fastapi import APIRouter, Depends, FastAPI, Response
from fasthx.htmy import HTMY
from htmy import Component, as_component_type

from ._model import AppConfig, AppNode, PackageInfo
from .fastapi import FastAPIDependency
from .module_options._actions import get_actions, has_actions
from .module_options._metadata import (
    MetadataMapping,
    components_with_metadata,
    empty_metadata_dep,
    get_metadata_dependency,
)
from .module_options._submit_handler import get_submit_handler
from .modules._api import PlainAPIFactory, RenderingAPIFactory, is_api_definition
from .modules._error import is_error_handler_owner, register_error_handlers
from .modules._layout import (
    LayoutFactory,
    combine_layouts_to_dependency,
    empty_layout_dependency,
    is_layout_definition,
    without_layout,
)
from .modules._page import is_page_definition
from .typing import module_names


def App(*, app: FastAPI | None = None, htmy: HTMY | None = None) -> FastAPI:
    """
    Creates a FastAPI application with all the routes that are defined in the application package.

    Arguments:
        app: Optional FastAPI application to use. If `None`, a new instance will be created.
        htmy: Optional `fasthx.htmy.HTMY` instance to use for server-side rendering. If `None`,
            a default instance will be created.
    """
    if app is None:
        app = FastAPI()

    if htmy is None:
        htmy = HTMY()

    config = AppConfig.default()
    packages = _discover_app_packages(config)
    root_node = _build_app_tree(packages)

    # Register error handlers
    if pkg := root_node.package:
        register_error_handlers(app, pkg.import_module("error", is_error_handler_owner), htmy=htmy)

    # Build the API
    app.include_router(_build_api(root_node, htmy=htmy))

    return app


def _build_api(
    node: AppNode,
    *,
    base_layout_dep: FastAPIDependency[LayoutFactory] = empty_layout_dependency,
    htmy: HTMY,
) -> APIRouter:
    """
    Recursively builds an `APIRouter` based on the application defined by `node`.

    Arguments:
        node: Application definition.
        base_layout: The base layout dependency to use for the API.
        htmy: The `fasthx.htmy.HTMY` instance to use for server-side rendering.
    """
    layout_dep = base_layout_dep  # In case there is no package or it has no layout module.
    pkg = node.package
    api = _make_api_router_for_package(pkg, htmy)
    if pkg is not None:
        # -- Try to import all relevant modules.
        layout_module = pkg.import_module("layout", is_layout_definition)
        page_module = pkg.import_module("page", is_page_definition)
        actions_module = pkg.import_module("actions", has_actions)

        # -- Resolve dependencies.
        layout_dep = combine_layouts_to_dependency(
            base_layout_dep, None if layout_module is None else layout_module.layout
        )
        page_dep, submit_handler_dep, metadata_dep = (
            (None, None, None)
            if page_module is None
            else (
                page_module.page,
                get_submit_handler(page_module),
                get_metadata_dependency(page_module),
            )
        )

        # -- Register the page.
        if page_dep is not None:
            path_operation = _make_page_path_operation(
                layout_dep=layout_dep,
                metadata_dep=empty_metadata_dep if metadata_dep is None else metadata_dep,
                page_dep=page_dep,
            )

            # Register the route with rendering.
            api.get(
                "/",
                response_model=None,
                # mypy can't infer that the modules is not None.
                name=page_module.__name__,  # type: ignore[union-attr]
                description=page_dep.__doc__,
                tags=["Page"],
            )(htmy.page(components_with_metadata)(path_operation))

        # -- Register the submit handler.
        if submit_handler_dep is not None:
            path_operation = _make_page_path_operation(
                layout_dep=layout_dep,
                metadata_dep=empty_metadata_dep if metadata_dep is None else metadata_dep,
                page_dep=submit_handler_dep,
            )

            # Register the route with rendering.
            api.post(
                "/",
                response_model=None,
                # mypy can't infer that the modules is not None.
                name=f"{page_module.__name__}.handle_submit",  # type: ignore[union-attr]
                description=submit_handler_dep.__doc__,
                tags=["Page", "Submit"],
            )(htmy.page(components_with_metadata)(path_operation))

        # -- Register actions from every action owner.
        for actions in (a for a in (get_actions(page_module), get_actions(actions_module)) if a):
            for action_path, desc in actions.items():
                if desc.use_layout or (desc.metadata is not None):
                    # Use _make_page_path_operation() if the action requires the layout or has
                    # metadata. If one is missing, the overhead is minimal, but the code is
                    # much simpler.
                    path_operation = _make_page_path_operation(
                        layout_dep=layout_dep if desc.use_layout else empty_layout_dependency,
                        metadata_dep=get_metadata_dependency(desc),
                        page_dep=desc.action,
                    )
                    route = htmy.page(components_with_metadata)(path_operation)
                else:
                    # No layout or metadata. Use the most efficient route registration.
                    route = htmy.page()(desc.action)

                api.api_route(action_path, **desc.route_args)(route)

    for sub_url, child_node in node.subtree.items():
        api.include_router(
            _build_api(child_node, base_layout_dep=layout_dep, htmy=htmy),
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

    return {
        PackageInfo.from_marker_file(f, config=config)
        for f in config.app_dir.rglob("*.py")
        if f.stem in module_names
        # Pass the relative path of the parent to make the best use of caching
        and not is_excluded(f.parent.relative_to(config.root_dir))
    }


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
) -> FastAPIDependency[tuple[Component, MetadataMapping | None] | Response]:
    """Creates the path operation for a page-like route."""

    async def path_operation(
        # Start by evaluating the page dependency, it is the most likely to raise an error
        # (could even be a performance improvement strategy when returning a Response).
        page: Component | Response = Depends(page_dep),  # noqa: B008
        # Next should be the metadata dependency. It is usually relatively lightweight.
        metadata: MetadataMapping | None = Depends(metadata_dep),  # noqa: B008
        # Evaluate the layout dependency last. It's often a sequence of nested dependencies
        # and it is also unlikely to fail.
        layout: LayoutFactory = Depends(layout_dep),  # noqa: B008
    ) -> tuple[Component, MetadataMapping | None] | Response:
        if isinstance(page, Response):
            return page

        if isinstance(page, without_layout):
            return page.component, metadata

        result = layout(as_component_type(page))
        # We must await here if result is an Awaitable, otherwise we would pass an
        # awaitable to htmy.page() and rendering that would fail.
        if isinstance(result, Awaitable):
            result = await result

        return result, metadata

    return path_operation
