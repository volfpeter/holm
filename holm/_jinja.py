from __future__ import annotations

from collections.abc import Mapping
from pathlib import Path
from typing import TYPE_CHECKING, Any

from fasthx.htmy import JinjaTemplate as _JinjaTemplate
from htmy import Context, is_component_type

from ._model import AppConfig, PackageInfo, no_app_package_roots
from .module_options._metadata import Metadata
from .modules._layout import CustomLayoutDefinition

if TYPE_CHECKING:
    from htmy.jinja import JinjaTemplateSource

    from .typing import Layout


class JinjaTemplate(_JinjaTemplate):
    """
    `fasthx.htmy.JinjaTemplate` subclass with holm-specific context awareness.

    In addition to the Jinja context utilities added by FastHX, this subclass adds page
    `Metadata` under the `metadata` key in the Jinja context as an always-present, but
    possibly empty dictionary.
    """

    __slots__ = ()

    def _build_context(self, htmy_context: Context) -> dict[str, Any]:
        result = super()._build_context(htmy_context)
        result["metadata"] = Metadata.from_context(htmy_context, None)
        return result


def make_jinja_layout_definition(pkg: PackageInfo, config: AppConfig) -> CustomLayoutDefinition | None:
    """
    Attempts to create a layout definition, backed by `JinjaTemplate`, from the `layout.jinja`
    file in the package, if such a file exists.

    The template name is the layout file path relative to `config.root_dir` with POSIX
    separators (e.g. `my_app/about/layout.jinja`), matching the root of the Jinja loader.
    """
    package_dir = _get_package_dir(pkg, config)
    layout_file = package_dir / "layout.jinja"
    if not layout_file.is_file():
        return None

    template_name = layout_file.relative_to(config.root_dir).as_posix()
    return CustomLayoutDefinition(_make_jinja_layout(template_name))


def make_jinja_templates(root_dir: Path) -> JinjaTemplateSource:
    """
    Returns a FastAPI/Starlette `Jinja2Templates` whose loader root is `root_dir`.

    Autoescape is enabled for the `jinja2.select_autoescape()` default extensions
    (`html`, `htm`, `xml`) plus `jinja`, since `holm` requires that extension for
    Jinja layouts.
    """
    import jinja2
    from fastapi.templating import Jinja2Templates

    env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(str(root_dir)),
        autoescape=jinja2.select_autoescape(["html", "htm", "xml", "jinja"]),
    )
    return Jinja2Templates(env=env)


def _make_jinja_layout(template_name: str) -> Layout:
    """
    Returns a `Layout` function that renders the Jinja template with the given name.

    The template's slots are derived from the wrapped props object (layout or page).

    Props-to-slots conversion: if `props` is a non-component `Mapping`, it is used
    directly as the slots mapping. Otherwise the value is assigned to the `children` slot
    as is.
    """

    def layout(props: Any) -> JinjaTemplate:
        if isinstance(props, Mapping) and not is_component_type(props):
            slots = props
        else:
            slots = {"children": props}
        return JinjaTemplate(template_name, slots=slots, use_default_slots=True)

    return layout


def _get_package_dir(pkg: PackageInfo, config: AppConfig) -> Path:
    """Returns the directory of the given package."""
    if pkg.package_name in no_app_package_roots:
        return config.app_dir
    return config.root_dir.joinpath(*pkg.package_name.split("."))
