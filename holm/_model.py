from __future__ import annotations

import inspect
import logging
from collections.abc import Callable
from dataclasses import dataclass, field
from importlib import import_module
from pathlib import Path
from typing import Any, TypeGuard, TypeVar

from .typing import ModuleName, URLSegment

_TModule = TypeVar("_TModule")


@dataclass(frozen=True, kw_only=True, slots=True)
class AppConfig:
    """
    Stores basic configuration Information about the application.
    """

    root_dir: Path
    """The root directory (as in Python import root)."""

    app_dir_name: str
    """The name of the application directory/package."""

    app_url_prefix_length: int
    """The length of the application URL prefix to remove (`len(app_dir_name) + 1`)."""

    app_dir: Path
    """Path to the application directory."""

    # Overriding __init__ and calculating inferred values automatically would serve the
    # default case well, but it would complicate things if we ever need to support
    # different application structures (for example an app in tests). So we use
    # alternative initializers instead.

    @classmethod
    def default(cls) -> AppConfig:
        """
        Creates a default instance for the standard application configuration.

        Raises:
            ValueError: If the application package cannot be determined.
        """
        root_dir = Path.cwd()
        app_dir_name = cls._find_app_package_name()
        len_app_dir_name = len(app_dir_name)

        return cls(
            root_dir=root_dir,
            app_dir_name=app_dir_name,
            # Support applications that are not wrapped in a Python package.
            # In that case app_dir_name is "".
            app_url_prefix_length=len_app_dir_name + 1 if len_app_dir_name > 0 else 0,
            app_dir=root_dir / app_dir_name,
        )

    @classmethod
    def _find_app_package_name(cls) -> str:
        """
        Attempts to find and return the application package name.

        The method uses the assumption that the application package is the one from which
        the call stack directly led to this library.

        Raises:
            ValueError: If the application package cannot be determined.
        """
        # We assume the app package is the one from which the call stack led to this library.
        lib_root = __name__.split(".")[0]
        stack = inspect.stack()
        for i in range(1, len(stack)):
            caller_frame = stack[i]
            caller_module = inspect.getmodule(caller_frame.frame)
            caller_package = caller_module.__package__ if caller_module else None
            if caller_package is None:
                break  # Couldn't find app package.

            if not caller_package.startswith(lib_root):
                # The call stack is no longer in this library, so we've found the app package.
                return caller_package

        raise ValueError("Could not determine the application package.")


@dataclass(frozen=True, kw_only=True, slots=True)
class PackageInfo:
    """
    Information about a single package.

    This class most importantly describes how a package can be imported and
    what should be the web URL of its contents.
    """

    package_dir: Path
    """
    Relative path to the package directory.

    It is basically the path matching the package name / import path.
    """

    package_name: str
    """
    The import name (path) of the package.
    """

    url: str
    """
    The web URL for the contents of the package.
    """

    def __hash__(self) -> int:
        return hash((PackageInfo, self.package_name))

    def import_module(
        self, name: ModuleName, validate: Callable[[Any], TypeGuard[_TModule]]
    ) -> _TModule | None:
        """
        Imports the module with the given name from the package.

        Arguments:
            name: The name of the module to import.
            validate: A function that validates the imported module.

        Returns:
            The imported module or `None` if the module does not exist.

        Raises:
            ValueError: If the module is invalid.
        """
        # Check if the module exists. Trying to import it and catching the exception would hide possible
        # import error that occur in within the module, which is undesired because it would be hard for
        # users to find why an API is not registered.
        if not (self.package_dir / f"{name}.py").is_file():
            return None

        # Support applications that are not wrapped in a Python package.
        # In that case `self.package_name` is ".".
        import_name = name if self.package_name == "." else f"{self.package_name}.{name}"
        try:
            module = import_module(import_name)
        except Exception:
            import traceback

            # Handle potential misconfigurations with a simple warning, instead of an exception.
            logger = logging.getLogger("holm")
            logger.warning(f"Failed to import module {name} at: {import_name}")
            logger.warning(traceback.format_exc())
            return None

        if not validate(module):
            raise ValueError(f"Invalid module: {name}")

        return module

    @classmethod
    def from_marker_file(cls, file_path: Path, *, config: AppConfig) -> PackageInfo:
        """
        Creates a `PackageInfo` instance from a so called "marker" that is located in the package.
        """
        package_dir = file_path.relative_to(config.root_dir).parent
        package_dir_str = str(package_dir)
        package_name = package_dir_str.replace("/", ".")
        # Create the base version of the URL
        url = "/" if package_dir_str == "." else f"/{package_dir_str[config.app_url_prefix_length :]}"
        # Technically there can be packages/directories with names like `{name}`. They can be
        # directly used as URL segments and they could even be imported with `import_module()`,
        # but they are invalid package names and static code analysis tools rightly complain
        # about them, so we need an alternative option.
        # That option is to use the `_name_` pattern instead and convert such package/directory
        # names to the `{name}` format here and use that as the URL segment.
        url = "/".join(
            (f"{{{p[1:-1]}}}" if len(p) > 2 and p[0] == p[-1] == "_" else p for p in url.split("/"))
        )
        return cls(package_dir=package_dir, package_name=package_name, url=url)

    def __lt__(self, other: PackageInfo) -> bool:
        return self.package_name < other.package_name


@dataclass(frozen=True, slots=True)
class AppNode:
    """
    The description of an application tree.
    """

    url: str
    """The full URL of this node."""

    subtree: dict[URLSegment, AppNode] = field(default_factory=dict)
    """
    Maps sub-URLs to child nodes.
    """

    _package: PackageInfo | None = None
    """The package that belongs to this node."""

    @property
    def last_url_segment(self) -> URLSegment:
        """The last URL segment of this node."""
        return f"/{self.url.rsplit('/', 1)[1]}"

    @property
    def package(self) -> PackageInfo | None:
        """The package that belongs to this node."""
        return self._package

    def add(self, item: PackageInfo) -> None:
        """
        Adds the given package to this node.

        If the package belongs in the subtree and not directly to this node, then the
        entire subtree is created automatically.
        """
        self_url = self.url
        if not item.url.startswith(self_url):
            raise ValueError(f"{item.url} must start with {self_url}")

        if item.url == self_url:
            if self._package is not None:
                raise ValueError(
                    (
                        f"Package already set for {self_url}: "
                        f"current is {self._package.package_name} "
                        f"new is {item.package_name}"
                    )
                )

            # Class is frozen so this is only way to set _package.
            object.__setattr__(self, "_package", item)
            return

        if self_url == "/":  # Root node
            sub_url = item.url
            url_prefix = ""
        else:
            sub_url = item.url.removeprefix(self_url)
            url_prefix = self_url

        first_segment: URLSegment = f"/{sub_url.split('/', 2)[1]}"  # First segment after leading slash
        child = self.subtree.get(first_segment)
        if child is None:
            # The URL for this node must be constructed this way to not skip intermediate nodes
            # that may not have a discovered package.
            child = AppNode(f"{url_prefix}{first_segment}")
            self.subtree[first_segment] = child

        child.add(item)
