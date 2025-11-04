from collections.abc import ItemsView, Iterator, KeysView, Mapping, ValuesView
from typing import Any, TypeAlias, overload

from htmy import Component, ContextAware, as_component_sequence

from holm.fastapi import FastAPIDependency

MetadataMapping: TypeAlias = Mapping[Any, Any]
"""
A mapping representation of information to be placed in the `<head>` element of an HTML document.

It is usually a dictionary with string keys and values, but it is not enforced in runtime,
so the typing is more lenient.
"""

MetadataDependency: TypeAlias = FastAPIDependency[MetadataMapping | None]
"""Metadata dependency type."""

MetadataMappingOrDependency: TypeAlias = MetadataMapping | MetadataDependency
"""Metadata mapping or dependency type."""


def get_metadata_dependency(obj: Any) -> MetadataDependency:
    """
    Loads and returns the FastAPI `MetadataMapping` dependency based on the metadata definition
    in the given object.

    If the object is not a `MetadataOwner`, the dependency will simply return `None`.
    """
    metadata = getattr(obj, "metadata", None)
    if metadata is None:
        return empty_metadata_dep

    if isinstance(metadata, Mapping):
        return lambda: metadata

    if callable(metadata):
        return metadata  # type: ignore[no-any-return]

    raise ValueError(f"Invalid metadata object: {metadata}")


def empty_metadata_dep() -> None:
    """
    Metadata dependency that returns `None`.
    """
    return None


class Metadata(ContextAware):
    """
    Context-aware metadata provider.

    The class implements the `Mapping` protocol as a means of giving convenient access to
    the metadata it contains.
    """

    __slots__ = ("_metadata",)

    def __init__(self, metadata: MetadataMapping | None = None) -> None:
        """
        Initialization.

        Arguments:
            metadata: The actual metadata mapping.
        """
        self._metadata = {} if metadata is None else metadata
        """The metadata mapping."""

    @overload
    def get(self, key: Any, default: None = None) -> Any | None: ...

    @overload
    def get(self, key: Any, default: Any) -> Any: ...

    def get(self, key: Any, default: Any | None = None) -> Any | None:
        """Implements `Mapping.get()`."""
        return self._metadata.get(key, default)

    def __contains__(self, key: Any) -> bool:
        """Implements the `Container` protocol."""
        return key in self._metadata

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, Metadata) and self._metadata == other._metadata

    def __getitem__(self, key: Any) -> Any:
        """Implements the `Sequence` protocol."""
        return self._metadata[key]

    def __iter__(self) -> Iterator[Any]:
        """Implements the `Iterable` protocol."""
        return iter(self._metadata)

    def __len__(self) -> int:
        """Implements the `Sized` protocol."""
        return len(self._metadata)

    def __ne__(self, other: Any) -> bool:
        return not self.__eq__(other)

    def items(self) -> ItemsView[Any, Any]:
        """Implements `Mapping.items()`."""
        return self._metadata.items()

    def keys(self) -> KeysView[Any]:
        """Implements `Mapping.keys()`."""
        return self._metadata.keys()

    def values(self) -> ValuesView[Any]:
        """Implements `Mapping.values()`."""
        return self._metadata.values()


def components_with_metadata(data: tuple[Component, MetadataMapping | None]) -> Component:
    """
    Function that converts a `Component` and optional `MetadataMapping` tuple into a `Component`
    in which the received component is wrapped in a `MetadataContext`, making the given metadata
    available in all wrapped components using `Metadata.from_context()`.
    """
    components, metadata = data
    # Wrap the rendered components in Metadata context provider component.
    # This allows `Metadata.from_context()` to be used in all wrapped components.
    # The received components object is usually a ComponentSequence (doctype and html components),
    # so converting to a component sequence seems a tiny bit more efficient.
    return Metadata(metadata).in_context(*as_component_sequence(components))
