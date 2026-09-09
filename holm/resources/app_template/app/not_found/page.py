from htmy import ComponentType, html

metadata = {"title": "Not Found"}


def page() -> ComponentType:
    """Not-found page; the 404 handler redirects here."""
    return html.div(
        html.h1("404", class_="text-4xl font-bold tracking-tight sm:text-5xl"),
        html.p(
            "The page you are looking for was not found.",
            class_="text-muted-foreground mx-auto mt-4 max-w-xl text-lg",
        ),
        html.p(
            html.a("Back to the homepage", href="/", class_="font-medium underline underline-offset-4"),
            class_="mt-6",
        ),
        class_="flex flex-1 flex-col items-center justify-center text-center",
    )
