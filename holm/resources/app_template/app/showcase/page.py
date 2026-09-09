from components.alert import alert
from components.avatar import avatar
from components.badge import badge
from components.button import button
from components.card import card
from components.dialog import close_button, dialog, show_dialog_button
from components.item import item_group, item_link
from components.separator import separator
from components.table import table, table_container
from components.tabs import tab_button, tab_panel, tabs
from htmy import ComponentType, html

metadata = {"title": "Showcase"}


def page() -> ComponentType:
    """Component showcase, served at /showcase."""
    return html.div(
        html.header(
            html.h1("Showcase", class_="pt-12 text-3xl font-bold tracking-tight"),
            html.p(
                "A slice of the BasecoatUI catalog that ships with this application, vendored as "
                "typed Python in ",
                html.code("components/"),
                ". Everything below is a plain function call in ",
                html.code("app/showcase/page.py"),
                ".",
                class_="description mt-2 max-w-xl",
            ),
            class_="pb-8",
        ),
        html.div(
            _buttons_card(),
            _tabs_card(),
            _table_card(),
            _items_card(),
            _alerts_card(),
            _dialog_card(),
            html.p(
                "More of the catalog (accordion, dropdown menus, toasts, charts, and more) is already in ",
                html.code("components/"),
                ". Open those files and change them; they are ordinary Python in your project.",
                class_="description text-center sm:col-span-2",
            ),
            class_="grid gap-4 sm:grid-cols-2",
        ),
    )


def _demo_card(
    title: str,
    description: str,
    *content: ComponentType,
    content_class: str = "mt-4 flex flex-wrap items-center gap-2",
) -> ComponentType:
    return card(
        html.header(
            html.h3(title, class_="font-medium"),
            html.p(description, class_="description"),
        ),
        html.section(*content, class_=content_class),
    )


def _buttons_card() -> ComponentType:
    return _demo_card(
        "Buttons",
        "Variants and sizes of the button component.",
        button("Default"),
        button("Outline", variant="outline"),
        button("Secondary", variant="secondary"),
        button("Ghost", variant="ghost"),
        button("Destructive", variant="destructive"),
        button("Link", variant="link"),
        button("Small", variant="outline", size="sm"),
        button("Large", size="lg"),
    )


def _tabs_card() -> ComponentType:
    return _demo_card(
        "Tabs",
        "Client-side tab switching, rendered by Python functions.",
        tabs(
            tab_panel(
                html.p(
                    "Typed Python components with JSX-like syntax, rendered on the server.",
                    class_="text-sm",
                ),
                id="demo-panel-python",
                button_id="demo-tab-python",
                selected=True,
            ),
            tab_panel(
                html.p(
                    "Endpoints return HTML fragments the browser swaps in. No client framework.",
                    class_="text-sm",
                ),
                id="demo-panel-htmx",
                button_id="demo-tab-htmx",
            ),
            tab_panel(
                html.p(
                    "Utility classes for the application and every component in it.",
                    class_="text-sm",
                ),
                id="demo-panel-tailwind",
                button_id="demo-tab-tailwind",
            ),
            buttons=[
                tab_button("Python", id="demo-tab-python", panel_id="demo-panel-python", selected=True),
                tab_button("HTMX", id="demo-tab-htmx", panel_id="demo-panel-htmx"),
                tab_button("Tailwind", id="demo-tab-tailwind", panel_id="demo-panel-tailwind"),
            ],
        ),
        content_class="mt-4 flex flex-col items-stretch",
    )


_rows: tuple[tuple[str, str, str], ...] = (
    ("dialog", "Overlay", "Stable"),
    ("tabs", "Navigation", "Stable"),
    ("chart", "Data viz", "Beta"),
)


def _table_card() -> ComponentType:
    return _demo_card(
        "Tables & badges",
        "Dense data with small status descriptors.",
        table_container(
            table(
                html.thead(html.tr(html.th("Component"), html.th("Kind"), html.th("Status"))),
                html.tbody(
                    *[
                        html.tr(
                            html.td(html.code(name)),
                            html.td(kind),
                            html.td(badge(status, variant="outline" if status == "Beta" else "secondary")),
                        )
                        for name, kind, status in _rows
                    ]
                ),
            )
        ),
        content_class="mt-4 flex flex-col items-stretch",
    )


def _nav_item(initial: str, title: str, description: str, href: str) -> ComponentType:
    return item_link(
        html.figure(avatar(html.span(initial), class_="size-9 rounded-full")),
        html.section(
            html.h3(title, class_="text-sm font-medium"),
            html.p(description),
        ),
        href=href,
    )


def _items_card() -> ComponentType:
    return _demo_card(
        "Items & avatars",
        "Link rows for lists and navigation.",
        item_group(
            _nav_item("D", "Design", "How the application is put together", "/design"),
            separator,
            _nav_item("S", "Showcase", "The component catalog in action", "/showcase"),
            separator,
            _nav_item("H", "Home", "The landing page", "/"),
        ),
        content_class="mt-4 flex flex-col items-stretch",
    )


def _alerts_card() -> ComponentType:
    return _demo_card(
        "Alerts",
        "Callouts for user attention.",
        alert("A standard alert to present information worth noticing.", title="Heads up"),
        alert(
            "A destructive alert for errors and warnings.",
            title="Something went wrong",
            destructive=True,
        ),
        content_class="mt-4 flex flex-col items-stretch gap-2",
    )


def _dialog_card() -> ComponentType:
    return _demo_card(
        "Dialog",
        "A modal rendered by a plain Python component, opened with one function call.",
        show_dialog_button("Open dialog", dialog_id="demo-dialog"),
        dialog(
            html.p(
                "Everything in this modal (header, body, footer) comes from "
                "components/ in your project. Open those files and change them.",
                class_="text-sm",
            ),
            id="demo-dialog",
            title="Example dialog",
            description="Dialogs are just Python functions.",
            footer=html.footer(close_button("Close")),
        ),
    )
