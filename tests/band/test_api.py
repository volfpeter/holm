from fastapi.testclient import TestClient


def test_api(client: TestClient) -> None:
    response = client.get("/band")
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json"
    assert response.json() == [
        {"id": "one", "name": "John"},
        {"id": "two", "name": "Paul"},
        {"id": "three", "name": "George"},
        {"id": "four", "name": "Ringo"},
    ]
