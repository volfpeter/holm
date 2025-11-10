from fastapi.testclient import TestClient

from test_app.user._user_id_.page import rendered_page_dense_layout_grid_eric


def test_page(client: TestClient) -> None:
    response = client.get("/user/eric?layout_variant=grid&page_variant=dense")
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "text/html; charset=utf-8"
    assert response.text == rendered_page_dense_layout_grid_eric
