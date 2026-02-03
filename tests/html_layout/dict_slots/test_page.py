from fastapi.testclient import TestClient

from test_app.html_layout.dict_slots.page import rendered_page_with_html_layout


def test_dict_slots(client: TestClient) -> None:
    response = client.get("/html-layout/dict-slots/")
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "text/html; charset=utf-8"
    print("RESPONSE:")
    print(response.text)
    assert rendered_page_with_html_layout in response.text
