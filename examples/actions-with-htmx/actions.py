import random

from holm import action

_welcome_message: list[str] = [
    "Welcome to My App! Powered By HTMX.",
    "Bienvenido a My App! Powered By HTMX.",
    "Bienvenue dans My App! Powered By HTMX.",
    "Willkommen bei My App! Powered By HTMX.",
    "Benvenuti nella mia app! Powered By HTMX.",
    "Üdvözöljük a My App-ban! Powered By HTMX.",
]


@action.get()
def welcome_message() -> str:
    """
    Action that returns a welcome message component, which in this
    case is a simple string.

    No path was provided for the action decorator, by default it
    creates the path from the decorator function's name, so the
    path will be "/welcome_message" within the router that contains
    the actions module.
    """
    return random.choice(_welcome_message)  # noqa: S311
