from htmy import Component, ComponentType, html


async def layout(props: dict[str, ComponentType], layout_variant: str = "default") -> Component:
    """Layout whose props is not a component."""
    return html.div(
        html.p(f"user layout, variant: {layout_variant}"),
        html.div("Main content:"),
        props["main"],  # Expect "main" in props
        html.div("footer"),
        props["footer"],  # Expect "footer" in props
    )
