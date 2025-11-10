from fastapi.testclient import TestClient

from test_app.no_metadata.page import rendered_page

# Do not add metadata, Metadata.from_context() should still succeed in layouts.
# metadata = {}


def test_page(client: TestClient) -> None:
    response = client.get("/no-metadata")
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "text/html; charset=utf-8"
    assert response.text == rendered_page
