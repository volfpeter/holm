from collections.abc import Iterable

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from holm import OriginCheckMiddleware


def _client(
    trusted_origins: Iterable[str] | None = None,
    allow_missing: bool = True,
    skip_if_no_cookies: bool = True,
) -> TestClient:
    app = FastAPI()

    @app.api_route("/submit", methods=["GET", "POST", "PUT", "PATCH", "DELETE"])
    def submit() -> dict[str, str]:
        return {"status": "ok"}

    return TestClient(
        OriginCheckMiddleware(
            app,
            trusted_origins=trusted_origins,
            allow_missing=allow_missing,
            skip_if_no_cookies=skip_if_no_cookies,
        )
    )


@pytest.mark.parametrize(
    ("method", "headers", "expected"),
    [
        ("GET", {"origin": "https://evil.com", "cookie": "s"}, 200),
        ("POST", {"origin": "http://testserver", "cookie": "s"}, 200),
        ("POST", {"origin": "https://evil.com", "cookie": "s"}, 403),
        ("POST", {"origin": "null", "cookie": "s"}, 403),
        ("POST", {"origin": "", "cookie": "s"}, 403),
        ("POST", {"referer": "http://testserver/page", "cookie": "s"}, 200),
        ("POST", {"referer": "https://evil.com/", "cookie": "s"}, 403),
        ("POST", {"referer": "null", "cookie": "s"}, 200),
        ("POST", {"referer": "", "cookie": "s"}, 200),
        ("POST", {"cookie": "s"}, 200),
        ("POST", {"origin": "https://evil.com"}, 200),
    ],
)
def test_origin_check(method: str, headers: dict[str, str], expected: int) -> None:
    assert _client().request(method, "/submit", headers=headers).status_code == expected


def test_origin_required_without_allow_missing() -> None:
    assert _client(allow_missing=False).post("/submit", headers={"cookie": "s"}).status_code == 403


def test_referer_null_treated_as_missing() -> None:
    client = _client(allow_missing=False)
    assert client.post("/submit", headers={"referer": "null", "cookie": "s"}).status_code == 403
    assert client.post("/submit", headers={"referer": "", "cookie": "s"}).status_code == 403


def test_cookieless_requests_checked_when_not_skipped() -> None:
    assert (
        _client(skip_if_no_cookies=False)
        .post("/submit", headers={"origin": "https://evil.com"})
        .status_code
        == 403
    )


def test_trusted_origins() -> None:
    client = _client(trusted_origins=["https://app.example.com"])
    response = client.post("/submit", headers={"origin": "https://app.example.com", "cookie": "s"})
    assert response.status_code == 200
    response = client.post("/submit", headers={"referer": "https://app.example.com/x", "cookie": "s"})
    assert response.status_code == 200
