from fastapi.testclient import TestClient


def test_jinja_slots_layout(client: TestClient) -> None:
    response = client.get("/jinja-slots/")
    assert response.status_code == 200
    assert "jinja-slots-layout" in response.text
    # Metadata projection (holm JinjaTemplate subclass).
    assert "Jinja slots" in response.text
    # Default `navbar` slot (App(layout_slots=...)).
    assert ">Slots</a>" in response.text
    # `children` slot (page content).
    assert "Page content" in response.text
    # Leaf `holm.JinjaTemplate` embedded in the page.
    assert 'id="leaf"' in response.text
    assert "Leaf template, name: Nested leaf" in response.text
    # `url_for` resolves a named route.
    assert 'href="/">Home</a>' in response.text
