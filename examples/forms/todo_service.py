from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Todo:
    """A simple TODO item."""

    title: str
    description: str


todos = [
    Todo(
        title="Home page",
        description="It should show the list of TODOs.",
    ),
    Todo(
        title="Add filtering",
        description="Add a form that filters the TODO list using substring search on the title.",
    ),
    Todo(
        title="Add a creation form",
        description="Add a form that submits a creation form with a POST request to a submit handler.",
    ),
]
"""The list of existing TODO items. This list acts as a database for the application."""


def find_todos(query: str) -> list[Todo]:
    """Returns a list of TODOs whose title contains the given query string."""
    query = query.lower()
    return [todo for todo in todos if query in todo.title.lower()]


def create_todo(title: str, description: str) -> Todo:
    """Creates a new TODO with the given title and description and stores it in the database."""
    todo = Todo(title=title, description=description)
    todos.append(todo)
    return todo
