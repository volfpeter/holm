import pytest
from fastapi.testclient import TestClient


@pytest.mark.parametrize(
    ("path",),
    (
        ("/_not_in_app",),
        ("/_not_in_app/inner",),
    ),
)
def test_page(client: TestClient, path: str) -> None:
    response = client.get(path)
    assert response.status_code == 404
