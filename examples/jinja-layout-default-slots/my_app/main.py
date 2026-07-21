from holm import App

from .navbar import navbar

# `layout_slots` makes the `navbar` slot available to every Jinja layout in the
# application. A page can override it by returning a slot mapping containing the
# same `navbar` key.
app = App(layout_slots={"navbar": navbar})
