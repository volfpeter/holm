from typing import Any, Protocol, TypeAlias

from holm.fastapi import FastAPIDependency

SubmitHandler: TypeAlias = FastAPIDependency[Any]
"""FastAPI dependency that returns the properties for the layout that wraps it
(for example a `Component`).

If the submit handler is not wrapped by a layout, then it must return a `Component`
"""


class SubmitHandlerOwner(Protocol):
    """Protocol definition for objects (usually modules) that define a submit handler."""

    @property
    def handle_submit(self) -> SubmitHandler: ...


def get_submit_handler(obj: Any) -> SubmitHandler | None:
    """Loads and returns the submit handler if it exists in the given object."""
    submit_handler = getattr(obj, "handle_submit", None)
    return submit_handler if callable(submit_handler) else None
