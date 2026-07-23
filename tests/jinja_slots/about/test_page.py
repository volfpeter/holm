from fastapi.testclient import TestClient


def test_nested_jinja_layout_resolves_by_relative_name(client: TestClient) -> None:
    response = client.get("/jinja-slots/about/")
    assert response.status_code == 200
    # Nested layout.jinja in a subpackage is resolved by package-relative name.
    assert "nested-about-layout" in response.text
    assert "Nested Jinja layout resolved by package-relative name." in response.text
    # Explicit page slot overrides the default navbar (explicit wins over defaults).
    assert "Custom navbar" in response.text
    # The parent (jinja_slots) layout still renders the default navbar.
    assert ">Slots</a>" in response.text
    # Page metadata propagates through nested layouts.
    assert "About slots" in response.text
    assert "About page" in response.text
