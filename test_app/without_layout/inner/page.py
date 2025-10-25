from typing import Literal

from htmy import Component, html

from holm import without_layout


async def page(no_inner_layout: Literal["true", "false"] = "false") -> Component:
    content = html.div("without_layout/inner/page")
    return without_layout(content) if no_inner_layout == "true" else content


async def handle_submit(no_inner_layout: Literal["true", "false"] = "false") -> Component:
    content = html.div("without_layout/inner/page.handle_submit")
    return without_layout(content) if no_inner_layout == "true" else content


class RenderedPage:
    no_inner_layout = "<div >\nwithout_layout/inner/page\n</div>"
    no_middle_layout = "\n".join(
        [
            "<div >",
            "<div >\nwithout_layout/inner/layout\n</div>",
            no_inner_layout,
            "</div>",
        ]
    )
    no_root_layout = "\n".join(
        [
            "<div >",
            "<div >\nwithout_layout/layout\n</div>",
            no_middle_layout,
            "</div>",
        ]
    )


class RenderedHandleSubmit:
    no_inner_layout = "<div >\nwithout_layout/inner/page.handle_submit\n</div>"
    no_middle_layout = "\n".join(
        [
            "<div >",
            "<div >\nwithout_layout/inner/layout\n</div>",
            no_inner_layout,
            "</div>",
        ]
    )
    no_root_layout = "\n".join(
        [
            "<div >",
            "<div >\nwithout_layout/layout\n</div>",
            no_middle_layout,
            "</div>",
        ]
    )
