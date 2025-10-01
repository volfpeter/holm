from dataclasses import dataclass


@dataclass(frozen=True, kw_only=True, slots=True)
class User:
    """User model."""

    id: int
    name: str
    email: str


users_by_id: dict[int, User] = {
    i: User(id=i, name=f"User {i}", email=f"user-{i}@holm.ccm") for i in range(10)
}
"""Dictionary that maps user IDs to the corresponding user objects."""


async def list_users() -> list[User]:
    """
    Lists all users.

    The function is async to demonstrate how easily async tools, for example ORMs
    can be used in `holm`.
    """
    return list(users_by_id.values())


async def get_user(id: int) -> User | None:
    """
    Returns the user with the given ID, if the user exists.

    The function is async to demonstrate how easily async tools, for example ORMs
    can be used in `holm`.
    """
    return users_by_id.get(id)
