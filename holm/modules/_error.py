from collections.abc import Callable, Mapping
from typing import Any, Protocol, TypeAlias, TypeGuard

from fastapi import FastAPI, Request, Response
from fastapi.responses import HTMLResponse
from fasthx.htmy import HTMY

from holm._model import PackageInfo
from holm.fastapi import FastAPIErrorHandler
from holm.logging import logger

ErrorHandlerMapping: TypeAlias = Mapping[type[Exception] | int, FastAPIErrorHandler]
"""
Mapping type whose keys are exception types or HTTP status codes, and the
corresponding values are FastAPI error handlers.
"""


class ErrorHandlerOwner(Protocol):
    """
    Protocol definition for objects (usually modules) that define FastAPI exception handlers.
    """

    @property
    def handlers(self) -> ErrorHandlerMapping | Callable[[HTMY], ErrorHandlerMapping]: ...


def is_error_handler_owner(obj: Any) -> TypeGuard[ErrorHandlerOwner]:
    """Type guard for `ErrorHandlerOwner`."""
    handlers = getattr(obj, "handlers", None)
    return handlers is not None and (isinstance(handlers, Mapping) or callable(handlers))


def load_error_handler_owner(pkg: PackageInfo) -> ErrorHandlerOwner | None:
    """
    Loads the `ErrorHandlerOwner` from the given package.

    Arguments:
        pkg: The package where the error handler owner should be loaded from.

    Returns:
        The loaded `ErrorHandlerOwner` or `None` if it's not found.
    """
    errors_module = pkg.import_module("errors", is_error_handler_owner)
    error_module = pkg.import_module("error", is_error_handler_owner)

    if errors_module is not None and error_module is not None:
        logger.warning("Both 'errors.py' and 'error.py' modules found. Using 'errors.py'.")

    return errors_module if errors_module is not None else error_module


def register_error_handlers(app: FastAPI, owner: ErrorHandlerOwner | None, *, htmy: HTMY) -> None:
    """
    Registers the error handlers defined by the given owner on the application.

    Arguments:
        app: The FastAPI application instance.
        owner: The error handler owner, if any.
        htmy: The HTMY instance.
    """
    if owner is None:
        return

    handlers = owner.handlers
    handler_mapping: ErrorHandlerMapping = handlers(htmy) if callable(handlers) else handlers
    for key, handler in handler_mapping.items():
        app.exception_handler(key)(wrap_error_handler(handler, htmy))


def wrap_error_handler(error_handler: FastAPIErrorHandler, htmy: HTMY) -> FastAPIErrorHandler:
    """
    Wraps the given error handler in a function that automatically renders `htmy` `Component` return values.
    """

    async def rendering_error_handler_wrapper(request: Request, error: Exception) -> Response:
        result = await error_handler(request, error)
        if isinstance(result, Response):
            return result

        try:
            return HTMLResponse(await htmy.render_component(result, request))
        except Exception as e:
            raise ValueError(
                "HTML rendering failed. Make sure your error handler returns "
                "either a FastAPI.Response or an htmy.Component!"
            ) from e

    return rendering_error_handler_wrapper
