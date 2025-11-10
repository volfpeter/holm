import pytest
from fastapi.testclient import TestClient

from test_app.user.page import RenderedAction, rendered_page_dense_layout_grid


def test_page(client: TestClient) -> None:
    response = client.get("/user?layout_variant=grid&page_variant=dense")
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "text/html; charset=utf-8"
    assert response.text == rendered_page_dense_layout_grid


@pytest.mark.parametrize(
    ("action_path", "method", "expected"),
    [
        # -- Automatic action path generation from function name.
        ("/list-users", "GET", RenderedAction.list_users),
        ("/create-user", "POST", RenderedAction.create_user),
        ("/update-user-with-put", "PUT", RenderedAction.update_user_with_put),
        ("/update-user-with-patch", "PATCH", RenderedAction.update_user_with_patch),
        ("/delete-user", "DELETE", RenderedAction.delete_user),
        # -- Custom path support. No underscore replacement.
        ("/a/list_users", "GET", RenderedAction.list_users),
        ("/a/create_user", "POST", RenderedAction.create_user),
        ("/a/update_user_with_put", "PUT", RenderedAction.update_user_with_put),
        ("/a/update_user_with_patch", "PATCH", RenderedAction.update_user_with_patch),
        ("/a/delete_user", "DELETE", RenderedAction.delete_user),
    ],
)
def test_page_actions(client: TestClient, action_path: str, method: str, expected: str) -> None:
    # Don't send a token to test the action's dependency which raises an error.
    response = client.request(method, f"/user{action_path}")
    assert response.status_code == 499

    # Send a token, expect successful response.
    response = client.request(method, f"/user{action_path}?token=pass")
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "text/html; charset=utf-8"
    assert response.text == expected
