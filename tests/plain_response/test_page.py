from fastapi.testclient import TestClient


def test_page(client: TestClient) -> None:
    response = client.get("/plain_response?a=4&b=6")
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json"
    assert response.json() == {"add": {"a": 4, "b": 6}, "result": 10}
