from typing import Literal, TypeAlias, get_args

PackageModuleName: TypeAlias = Literal["actions", "api", "layout", "page"]
"""Recognized module names."""

RootOnlyModuleName: TypeAlias = Literal["error"]
"""Modules names that are only supported at the root level."""

ModuleName: TypeAlias = PackageModuleName | RootOnlyModuleName
"""All recognized module names, including ones that are only supported at the root level."""

# get_args() doesn't return the correct tuple for the ModuleName union type.
module_names: set[ModuleName] = {*get_args(PackageModuleName), *get_args(RootOnlyModuleName)}
"""Set of all recognized module names."""

URLSegment: TypeAlias = str
"""
A URL that consists of a leading slash followed by a non-empty URL part
that includes no more slashes.

Valid examples: "/about".

Invalid examples: "/", "/about/us".
"""
