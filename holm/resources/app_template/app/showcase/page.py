from components import (
    alert,
    avatar,
    badge,
    button,
    card,
    dialog,
    field,
    item,
    separator,
    switch,
)
from components.dialog import show_dialog_button
from htmy import ComponentType, html

metadata = {"title": "Showcase"}


def _demo_card(
    title: str,
    description: str,
    *content: ComponentType,
    content_class: str = "mt-4 flex flex-wrap items-center gap-2",
) -> ComponentType:
    return card.card(
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
        button.button("Default"),
        button.button("Outline", variant="outline"),
        button.button("Secondary", variant="secondary"),
        button.button("Ghost", variant="ghost"),
        button.button("Destructive", variant="destructive"),
        button.button("Link", variant="link"),
        button.button("Small", variant="outline", size="sm"),
        button.button("Large", size="lg"),
    )


def _badges_card() -> ComponentType:
    return _demo_card(
        "Badges",
        "Small status descriptors.",
        badge.badge("Badge"),
        badge.badge("Secondary", variant="secondary"),
        badge.badge("Outline", variant="outline"),
        badge.badge("Destructive", variant="destructive"),
    )


def _nav_item(initial: str, title: str, description: str, href: str) -> ComponentType:
    return item.item_link(
        html.figure(avatar.avatar(html.span(initial), class_="size-9 rounded-full")),
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
        item.item_group(
            _nav_item("D", "Design", "How the application is put together", "/design"),
            separator.separator,
            _nav_item("S", "Showcase", "The component catalog in action", "/showcase"),
            separator.separator,
            _nav_item("H", "Home", "The landing page", "/"),
        ),
        content_class="mt-4 flex flex-col items-stretch",
    )


def _alerts_card() -> ComponentType:
    return _demo_card(
        "Alerts",
        "Callouts for user attention.",
        alert.alert("A standard alert to present information worth noticing.", title="Heads up"),
        alert.alert(
            "A destructive alert for errors and warnings.",
            title="Something went wrong",
            destructive=True,
        ),
        content_class="mt-4 flex flex-col items-stretch gap-2",
    )


def _forms_card() -> ComponentType:
    return card.card(
        html.header(
            html.h3("Forms", class_="font-medium"),
            html.p("Inputs and switches, ready to submit to an action.", class_="description"),
        ),
        html.section(
            field.field(
                html.label("Email", for_="demo-email", class_="label"),
                html.input_(
                    type="email",
                    id="demo-email",
                    placeholder="you@example.com",
                    class_="input",
                ),
                html.p("We never share your email.", class_="text-muted-foreground text-xs"),
            ),
            html.label(
                switch.switch(name="demo-notifications", checked=True),
                "Send notifications",
                class_="label flex items-center gap-2",
            ),
            button.button("Subscribe", variant="outline"),
            class_="mt-4 flex flex-col items-start gap-4",
        ),
    )


def _dialog_card() -> ComponentType:
    return _demo_card(
        "Dialog",
        "A modal rendered by a plain Python component, opened with one function call.",
        show_dialog_button("Open dialog", dialog_id="demo-dialog"),
        dialog.dialog(
            html.p(
                "Everything in this modal (header, body, footer) comes from "
                "components/ in your project. Open those files and change them.",
                class_="text-sm",
            ),
            id="demo-dialog",
            title="Example dialog",
            description="Dialogs are just Python functions.",
            footer=html.footer(dialog.close_button("Close")),
        ),
    )


def page() -> ComponentType:
    """Component showcase, served at /showcase."""
    return html.div(
        html.header(
            html.h1("Showcase", class_="pt-12 text-3xl font-bold tracking-tight"),
            html.p(
                "A few of the BasecoatUI components that ship with this application. Each "
                "one is a typed Python function call. This page is ",
                html.code("app/showcase/page.py"),
                ". The components live in ",
                html.code("components/"),
                ", and you can edit them.",
                class_="description mt-2 max-w-xl",
            ),
            class_="pb-8",
        ),
        html.div(
            _buttons_card(),
            _badges_card(),
            _items_card(),
            _alerts_card(),
            _forms_card(),
            _dialog_card(),
            html.p(
                "The rest of the catalog (accordion, dropdown menu, table, tabs, toast, "
                "and more) is already in ",
                html.code("components/"),
                ". Open those files and change them; they are ordinary Python in your project.",
                class_="description text-center sm:col-span-2",
            ),
            class_="grid gap-4 sm:grid-cols-2",
        ),
    )
