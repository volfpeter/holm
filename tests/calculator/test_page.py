from fastapi.testclient import TestClient

from test_app.calculator.page import rendered_page, rendered_submit_handler


def test_page_get(client: TestClient) -> None:
    response = client.get("/calculator")
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "text/html; charset=utf-8"
    assert response.text == rendered_page


def test_page_post(client: TestClient) -> None:
    response = client.post("/calculator")
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "text/html; charset=utf-8"
    assert response.text == rendered_submit_handler
