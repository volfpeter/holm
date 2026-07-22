from fastapi.testclient import TestClient


def test_jinja_autoescape(client: TestClient) -> None:
    response = client.get("/jinja-escaping/")
    assert response.status_code == 200
    assert "&lt;script&gt;alert(1)&lt;/script&gt;" in response.text
    assert "<script>alert(1)</script>" not in response.text
