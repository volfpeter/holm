from fastapi.testclient import TestClient

from test_app.html_layout.page import rendered_page_with_html_layout


def test_html_layout(client: TestClient) -> None:
    response = client.get("/html-layout/")
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "text/html; charset=utf-8"
    assert rendered_page_with_html_layout in response.text
