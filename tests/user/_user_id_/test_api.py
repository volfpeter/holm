from fastapi.testclient import TestClient


def test_json_api(client: TestClient) -> None:
    response = client.get("/user/c0ffee/info")
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json"
    assert response.json() == {"id": "c0ffee", "name": "John"}


def test_hx_api(client: TestClient) -> None:
    response = client.get("/user/c0ffee/info", headers={"HX-Request": "true"})
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "text/html; charset=utf-8"
    assert response.text == "\n".join(["<div >", "<h2 >John</h2>", "<p >ID: c0ffee</p>", "</div>"])
