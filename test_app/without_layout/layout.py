from typing import Literal

from htmy import Component, ComponentType, html

from holm import without_layout


async def layout(children: ComponentType, no_root_layout: Literal["true", "false"] = "false") -> Component:
    content = html.div(
        html.div("without_layout/layout"),
        children,
    )

    return without_layout(content) if no_root_layout == "true" else content
