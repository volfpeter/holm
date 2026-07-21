from fastapi.testclient import TestClient

from test_app.jinja_layout.page import rendered_page


def test_jinja_layout(client: TestClient) -> None:
    response = client.get("/jinja-layout/")
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "text/html; charset=utf-8"
    assert rendered_page in response.text
