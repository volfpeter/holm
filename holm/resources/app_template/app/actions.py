from holm import action
from htmy import ComponentType, html

_greetings: tuple[tuple[str, str], ...] = (
    ("en", "Welcome"),
    ("de", "Willkommen"),
    ("es", "Bienvenido"),
    ("fr", "Bienvenue"),
    ("it", "Benvenuto"),
    ("hu", "Üdvözöljük"),
    ("nl", "Welkom"),
    ("pt", "Bem-vindo"),
    ("ja", "ようこそ"),
    ("zh", "欢迎"),
)

_greeting_index: dict[str, int] = {lang: index for index, (lang, _) in enumerate(_greetings)}


@action.get()
def welcome(lang: str = "en") -> ComponentType:
    index = _greeting_index.get(lang, 0)
    next_lang = _greetings[(index + 1) % len(_greetings)][0]
    return html.span(
        _greetings[index][1],
        hx_get=f"/welcome?lang={next_lang}",
        hx_trigger="every 2s",
        hx_swap="outerHTML",
    )
