"""Jinja2 discovery UI tests (no external network)."""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import quote

from fastapi.testclient import TestClient

from a2a_hub.api.app import create_app
from a2a_hub.config import Settings
from a2a_hub.models.resource import Resource, make_resource_id
from a2a_hub.store.database import Database
from a2a_hub.store.repository import ResourceRepository

_HTML = {"Accept": "text/html"}


def _app_with_resource(tmp_path: Path) -> tuple[Settings, Resource]:
    db_path = tmp_path / "ui.db"
    db = Database(db_path)
    db.initialize()
    repo = ResourceRepository(db)
    card_url = "https://example.com/research.json"
    resource = repo.upsert(
        Resource(
            id=make_resource_id(card_url, "Research Agent"),
            name="Research Agent",
            description="Helps with research tasks",
            endpoint_url="https://example.com/a2a/research",
            publisher="unverified",
            skills=[{"id": "research", "name": "Research"}],
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
            card_url=card_url,
        )
    )
    settings = Settings(database_path=db_path, log_level="WARNING")
    return settings, resource


def test_home_page_loads(tmp_path: Path) -> None:
    settings = Settings(database_path=tmp_path / "home.db", log_level="WARNING")
    with TestClient(create_app(settings)) as client:
        response = client.get("/", headers=_HTML)

    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    assert "A2A" in response.text
    assert "Search" in response.text or "search" in response.text


def test_search_query_displays_results(tmp_path: Path) -> None:
    settings, resource = _app_with_resource(tmp_path)
    with TestClient(create_app(settings)) as client:
        response = client.get("/", params={"q": "research"}, headers=_HTML)

    assert response.status_code == 200
    assert "Research Agent" in response.text
    assert "Helps with research tasks" in response.text
    assert resource.endpoint_url in response.text
    assert "Research" in response.text


def test_resource_detail_renders(tmp_path: Path) -> None:
    settings, resource = _app_with_resource(tmp_path)
    with TestClient(create_app(settings)) as client:
        response = client.get(
            f"/resources/{quote(resource.id, safe='')}",
            headers=_HTML,
        )

    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    assert "Research Agent" in response.text
    assert resource.id in response.text
    assert resource.endpoint_url in response.text
    assert "unverified" in response.text


def test_missing_resource_returns_404(tmp_path: Path) -> None:
    settings = Settings(database_path=tmp_path / "missing.db", log_level="WARNING")
    with TestClient(create_app(settings)) as client:
        response = client.get(
            "/resources/urn:air:unverified:missing:none",
            headers=_HTML,
        )
    assert response.status_code == 404


def test_json_resource_detail_still_works(tmp_path: Path) -> None:
    """API clients without HTML Accept still receive JSON."""
    settings, resource = _app_with_resource(tmp_path)
    with TestClient(create_app(settings)) as client:
        response = client.get(
            f"/resources/{quote(resource.id, safe='')}",
            headers={"Accept": "application/json"},
        )
    assert response.status_code == 200
    assert response.json()["name"] == "Research Agent"
