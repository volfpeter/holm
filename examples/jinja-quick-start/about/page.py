from holm import JinjaTemplate


async def metadata(featured: bool = False) -> dict[str, str | bool]:
    """
    Dynamic metadata based on query parameters.

    This function could be both sync or async. It's just a standard FastAPI dependency.
    """
    title = "Featured About" if featured else "About"
    return {"title": f"{title} | My App", "featured": featured}


async def page() -> JinjaTemplate:
    """Renders the about page from a Jinja template, reading `featured` from metadata."""
    return JinjaTemplate("about/page.jinja")
