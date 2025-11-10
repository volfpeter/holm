from typing import Any

import pytest
from fastapi.testclient import TestClient

import test_app.calculator.page as calculator_page
import test_app.page as test_app_page
import test_app.user._user_id_.page as user_by_id_page
import test_app.user.page as user_page
from test_app.main import app


@pytest.mark.parametrize(
    ("path_name", "url", "path_params"),
    (
        ("test_app.page", "/", {}),
        (test_app_page.__name__, "/", {}),
        ("test_app.calculator.page", "/calculator/", {}),
        (calculator_page.__name__, "/calculator/", {}),
        ("test_app.user.page", "/user/", {}),
        (user_page.__name__, "/user/", {}),
        ("test_app.user._user_id_.page", "/user/1/", {"user_id": 1}),
        (user_by_id_page.__name__, "/user/1/", {"user_id": 1}),
        ("test_app.user._user_id_.page", "/user/C0FF33/", {"user_id": "C0FF33"}),
        (user_by_id_page.__name__, "/user/C0FF33/", {"user_id": "C0FF33"}),
    ),
)
def test_app_url_path_for_page(path_name: str, url: str, path_params: dict[str, Any]) -> None:
    """
    Tests that `app.url_path_for()` can construct URLs for pages
    based on page module name (import path).
    """
    assert app.url_path_for(path_name, **path_params) == url


@pytest.mark.parametrize(
    ("path_name", "url"),
    (("test_app.calculator.page.handle_submit", "/calculator/"),),
)
def test_app_url_path_for_handle_submit(path_name: str, url: str) -> None:
    """
    Tests that `app.url_path_for()` can construct URLs for submit handlers
    based on page module name (import path) with the `.handle_submit` suffix.
    """
    assert app.url_path_for(path_name) == url


def test_request_url_for(client: TestClient) -> None:
    response = client.get("/urls")
    assert response.status_code == 200
    assert response.json() == [
        "http://testserver/",
        "http://testserver/calculator/",
        "http://testserver/user/",
        "http://testserver/user/1/",
    ]
