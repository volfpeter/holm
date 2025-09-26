import pytest
from fastapi.testclient import TestClient


@pytest.mark.parametrize(
    ("path",),
    (
        ("/_not_in_app",),
        ("/_not_in_app/inner",),
    ),
)
def test_page(client: TestClient, path: str) -> None:
    response = client.get(path)
    # Request should be handled by the not found error handler.
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "text/html; charset=utf-8"
    assert response.text == "<div >\n<h1 >Page not found</h1>\n</div>"
