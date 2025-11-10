from htmy import ComponentType, html


def layout(props: ComponentType, user_id: str) -> dict[str, ComponentType]:
    return {"main": props, "footer": html.div(html.p(f"footer for user ID {user_id}, added by layout"))}
