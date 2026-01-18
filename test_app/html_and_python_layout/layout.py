from htmy import Component, ComponentType, html


def layout(props: ComponentType) -> Component:
    return html.div(html.h1("Python Layout"), props)
