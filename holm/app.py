import inspect
from collections.abc import Awaitable, Iterable
from functools import lru_cache
from pathlib import Path
from typing import cast

from fastapi import APIRouter, Depends, FastAPI
from fastapi.responses import HTMLResponse
from fasthx.htmy import HTMY
from htmy import Component, as_component_type

from ._model import AppConfig, AppNode, PackageInfo
from .fastapi import FastAPIDependency
from .modules._api import PlainAPIFactory, RenderingAPIFactory, is_api_definition
from .modules._error import is_error_handler_owner, register_error_handlers
from .modules._layout import (
    LayoutFactory,
    combine_layouts_to_dependency,
    empty_layout_dependency,
    is_layout_definition,
)
from .modules._metadata import MetadataMapping, components_with_metadata, get_metadata_dependency
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
        layout_module = pkg.import_module("layout", is_layout_definition)
        page_module = pkg.import_module("page", is_page_definition)

        layout_dep = combine_layouts_to_dependency(
            base_layout_dep, None if layout_module is None else layout_module.layout
        )
        page_dep = None if page_module is None else page_module.page

        if page_dep is not None:
            metadata_dep = get_metadata_dependency(page_module)

            async def path_operation(
                layout: LayoutFactory = Depends(layout_dep),  # noqa: B008
                metadata: MetadataMapping | None = Depends(metadata_dep),  # noqa: B008
                page: Component = Depends(page_dep),  # noqa: B008
            ) -> tuple[Component, MetadataMapping | None]:
                result = layout(as_component_type(page))
                # We must await here if result is an Awaitable, otherwise we would pass an
                # awaitable to htmy.page() and rendering that would fail.
                if isinstance(result, Awaitable):
                    result = await result

                return result, metadata

            # Register the route with rendering.
            api.get(
                "/",
                response_class=HTMLResponse,
                response_model=None,
                name="page",
                description=page_dep.__doc__,
                tags=["Page"],
            )(htmy.page(components_with_metadata)(path_operation))

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
