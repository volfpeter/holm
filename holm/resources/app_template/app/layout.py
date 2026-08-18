from components import theme_switcher
from htmy import ComponentSequence, ComponentType, html

from .head import head


def layout(children: ComponentType) -> ComponentSequence:
    """Root layout wrapping all pages."""
    return (
        html.DOCTYPE.html,
        html.html(
            head(),
            html.body(
                html.main(
                    html.div(
                        html.header(
                            html.span("__holm_name__", class_="text-lg font-semibold"),
                            theme_switcher.theme_switcher(),
                            class_="flex items-center justify-between py-2",
                        ),
                        children,
                        class_="mx-auto w-full max-w-screen-md p-6",
                    ),
                    class_="min-h-screen",
                ),
            ),
        ),
    )
