import pytest
from fastapi.testclient import TestClient

from test_app.actions import RenderedAction


@pytest.mark.parametrize(
    ("action_path", "method", "expected"),
    [
        # Plain actions.
        ("/get", "GET", RenderedAction.get.without_layout),
        ("/post", "POST", RenderedAction.post.without_layout),
        ("/put", "PUT", RenderedAction.put.without_layout),
        ("/patch", "PATCH", RenderedAction.patch.without_layout),
        ("/delete", "DELETE", RenderedAction.delete.without_layout),
        # Actions with layout.
        ("/get/wl", "GET", RenderedAction.get.with_layout),
        ("/post/wl", "POST", RenderedAction.post.with_layout),
        ("/put/wl", "PUT", RenderedAction.put.with_layout),
        ("/patch/wl", "PATCH", RenderedAction.patch.with_layout),
        ("/delete/wl", "DELETE", RenderedAction.delete.with_layout),
        # Actions with layout and metadata
        ("/get/wlm", "GET", RenderedAction.get.with_layout_and_metadata),
        ("/post/wlm", "POST", RenderedAction.post.with_layout_and_metadata),
        ("/put/wlm", "PUT", RenderedAction.put.with_layout_and_metadata),
        ("/patch/wlm", "PATCH", RenderedAction.patch.with_layout_and_metadata),
        ("/delete/wlm", "DELETE", RenderedAction.delete.with_layout_and_metadata),
    ],
)
def test_action(client: TestClient, action_path: str, method: str, expected: str) -> None:
    response = client.request(method, action_path)
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "text/html; charset=utf-8"
    assert response.text == expected
