from holm import App

from .navbar import navbar

# `layout_slots` makes the `navbar` slot available to every component
# in the application, including Jinja layouts, through
# `htmy.jinja.DefaultSlots.from_context()`.
app = App(layout_slots={"navbar": navbar})
