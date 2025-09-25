from fastapi.testclient import TestClient

from test_app.page import rendered_page


def test_page(client: TestClient) -> None:
    response = client.get("/")
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "text/html; charset=utf-8"
    assert response.text == rendered_page
