from htmy import ComponentType, html


def layout(props: ComponentType, id: str) -> dict[str, ComponentType]:
    return {"main": props, "footer": html.div(html.p(f"footer for user ID {id}, added by layout"))}
