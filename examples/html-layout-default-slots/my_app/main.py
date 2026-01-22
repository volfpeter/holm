from holm import App
from holm.modules._layout import Layout
from holm.utils import snippet_to_layout

from .navbar import navbar


def str_to_layout_with_navbar(content: str) -> Layout:
    """
    Custom string to `Layout` converter function for the application.

    It makes a `navbar` component available to every HTML layout in the `navbar` slot.
    """
    return snippet_to_layout(content, default_slot_mapping={"navbar": navbar})


app = App(str_to_layout=str_to_layout_with_navbar)
