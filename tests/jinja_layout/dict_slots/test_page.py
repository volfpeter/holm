from fastapi.testclient import TestClient

from test_app.jinja_layout.dict_slots.page import rendered_page


def test_jinja_layout_dict_slots(client: TestClient) -> None:
    response = client.get("/jinja-layout/dict-slots/")
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "text/html; charset=utf-8"
    assert rendered_page in response.text
