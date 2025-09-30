from htmy import Component, html

from .service import list_users

metadata: dict[str, str] = {"title": "User"}


async def page() -> Component:
    # Load users using an async service.
    users = await list_users()
    return html.div(
        html.h1("Users:"),
        html.ul(
            # Create list items with a link to the profile page for each user.
            # Don't forget to use the spread operator! html.ul expects its
            # children as positional arguments, not as a single list.
            *(html.li(html.a(user.name, href=f"/user/{user.id}")) for user in users),
        ),
    )
