from fastapi.testclient import TestClient

from test_app.user.page import rendered_page_dense_layout_grid


def test_page(client: TestClient) -> None:
    response = client.get("/user?layout_variant=grid&page_variant=dense")
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "text/html; charset=utf-8"
    assert response.text == rendered_page_dense_layout_grid
