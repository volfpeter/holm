from htmy import Component, html


async def metadata(featured: bool = False) -> dict[str, str]:
    """
    Dynamic metadata based on query parameters.

    This function could be both sync or async. It's just a standard FastAPI dependency.
    """
    title = "Featured About" if featured else "About"
    return {"title": f"{title} | My App"}


async def page(featured: bool = False) -> Component:
    """Async about page with dynamic content."""
    if featured:
        return html.div(
            html.h1("About Us ⭐"),
            html.p("This is our featured about page!"),
            html.p("You're viewing the special featured version."),
            html.a("Regular version", href="/about"),
        )

    return html.div(
        html.h1("About Us"),
        html.p("We're building amazing web applications with holm."),
        html.p("Our framework combines the power of FastAPI with server-side rendering."),
        html.p("This example demonstrates how to use default slots in layouts."),
        html.a("Featured version", href="/about?featured=true"),
    )
