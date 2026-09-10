from collections.abc import Mapping
from typing import Any

from holm import JinjaTemplate
from htmy import Component, is_component_type


def layout(props: Any) -> JinjaTemplate:
    """Root layout wrapping all pages, rendered by `layout.jinja`."""
    # holm automates all of this, you can remove this file and the
    # application will keep working identically to before. The reason
    # we have this file is to explain what holm does under the hood
    # when it encounters Jinja layouts without a Python counterpart.
    slots: Mapping[str, Component]
    if isinstance(props, Mapping) and not is_component_type(props):
        slots = props
    else:
        slots = {"children": props}
    return JinjaTemplate("app/layout.jinja", slots=slots, use_default_slots=True)
