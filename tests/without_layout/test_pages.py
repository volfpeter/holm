import pytest
from fastapi.testclient import TestClient

from test_app.without_layout.inner.page import RenderedHandleSubmit, RenderedPage


@pytest.mark.parametrize(
    (
        "url",
        "method",
        "expected",
    ),
    (
        # -- No inner layout.
        (
            "without_layout/inner?no_inner_layout=true",
            "GET",
            RenderedPage.no_inner_layout,
        ),
        (
            "without_layout/inner?no_inner_layout=true",
            "POST",
            RenderedHandleSubmit.no_inner_layout,
        ),
        # -- No mix and match, only the innermost without_layout declaration counts.
        (
            "without_layout/inner?no_middle_layout=false&no_inner_layout=true",
            "GET",
            RenderedPage.no_inner_layout,
        ),
        (
            "without_layout/inner?no_middle_layout=false&no_inner_layout=true",
            "POST",
            RenderedHandleSubmit.no_inner_layout,
        ),
        # -- No middle layout.
        (
            "without_layout/inner?no_middle_layout=true",
            "GET",
            RenderedPage.no_middle_layout,
        ),
        (
            "without_layout/inner?no_middle_layout=true",
            "POST",
            RenderedHandleSubmit.no_middle_layout,
        ),
        # -- No root layout.
        (
            "without_layout/inner?no_root_layout=true",
            "GET",
            RenderedPage.no_root_layout,
        ),
        (
            "without_layout/inner?no_root_layout=true",
            "POST",
            RenderedHandleSubmit.no_root_layout,
        ),
    ),
)
def test_page(client: TestClient, url: str, method: str, expected: str) -> None:
    response = client.request(method, url)
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "text/html; charset=utf-8"
    assert response.text == expected
