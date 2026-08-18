from components import theme_switcher
from holm import Metadata
from htmy import ComponentType, Context, component, html

from .settings import settings


@component.context_only
def head(ctx: Context) -> ComponentType:
    metadata = Metadata.from_context(ctx)
    title = "__holm_name__"
    if (subtitle := metadata.get("title")) is not None:
        title = f"{subtitle} | {title}"

    return html.head(
        html.title(title),
        html.meta(charset="utf-8"),
        html.meta(name="viewport", content="width=device-width, initial-scale=1"),
        html.link(rel="stylesheet", href=f"/static/{settings.css_file}"),
        html.script(src=f"/static/{settings.js_file}"),
        theme_switcher.js,
    )
