from fastapi.testclient import TestClient


def test_python_layout_takes_precedence(client: TestClient) -> None:
    response = client.get("/html-and-python-layout/")
    assert response.status_code == 200
    assert "Python Layout" in response.text
    assert "This file should be ignored" not in response.text
