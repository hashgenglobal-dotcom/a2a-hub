"""Search API and repository retrieval tests (no external network)."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import quote

from fastapi.testclient import TestClient

from a2a_hub.api.app import create_app
from a2a_hub.config import Settings
from a2a_hub.main import cmd_crawl
from a2a_hub.models.resource import Resource, make_resource_id
from a2a_hub.store.database import Database
from a2a_hub.store.repository import ResourceRepository


def _seed_resource(tmp_path: Path, *, name: str, description: str, skills: list) -> Resource:
    db = Database(tmp_path / "api.db")
    db.initialize()
    repo = ResourceRepository(db)
    card_url = f"https://example.com/{name.lower().replace(' ', '-')}.json"
    resource = Resource(
        id=make_resource_id(card_url, name),
        name=name,
        description=description,
        endpoint_url=f"https://example.com/a2a/{name.lower().replace(' ', '-')}",
        publisher="unverified",
        skills=skills,
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
        card_url=card_url,
    )
    return repo.upsert(resource)


def test_api_health(tmp_path: Path) -> None:
    settings = Settings(database_path=tmp_path / "health.db", log_level="WARNING")
    with TestClient(create_app(settings)) as client:
        response = client.get("/health")
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ok"
    assert body["database"] == "connected"
    assert body["resources"] == 0
    assert body["version"] == "0.1.0"


def test_search_returns_matching_resource(tmp_path: Path) -> None:
    resource = _seed_resource(
        tmp_path,
        name="Finance Analyst",
        description="Helps with budgeting",
        skills=[{"id": "finance", "name": "Finance"}],
    )
    settings = Settings(database_path=tmp_path / "api.db", log_level="WARNING")
    with TestClient(create_app(settings)) as client:
        response = client.get("/search", params={"q": "finance"})

    assert response.status_code == 200
    body = response.json()
    assert body["total"] == 1
    assert len(body["results"]) == 1
    assert body["results"][0]["id"] == resource.id
    assert body["results"][0]["name"] == "Finance Analyst"
    assert body["results"][0]["endpoint_url"] == resource.endpoint_url


def test_search_handles_no_results(tmp_path: Path) -> None:
    _seed_resource(
        tmp_path,
        name="Echo Agent",
        description="Echoes",
        skills=[{"id": "echo"}],
    )
    settings = Settings(database_path=tmp_path / "api.db", log_level="WARNING")
    with TestClient(create_app(settings)) as client:
        response = client.get("/search", params={"q": "nonexistent-keyword-xyz"})

    assert response.status_code == 200
    body = response.json()
    assert body["results"] == []
    assert body["total"] == 0


def test_resource_detail_retrieval(tmp_path: Path) -> None:
    resource = _seed_resource(
        tmp_path,
        name="Detail Agent",
        description="Full detail",
        skills=[{"id": "detail"}],
    )
    settings = Settings(database_path=tmp_path / "api.db", log_level="WARNING")
    with TestClient(create_app(settings)) as client:
        response = client.get(f"/resources/{quote(resource.id, safe='')}")

    assert response.status_code == 200
    body = response.json()
    assert body["id"] == resource.id
    assert body["name"] == "Detail Agent"
    assert body["description"] == "Full detail"
    assert body["publisher"] == "unverified"
    assert body["skills"][0]["id"] == "detail"


def test_resource_detail_not_found(tmp_path: Path) -> None:
    settings = Settings(database_path=tmp_path / "missing.db", log_level="WARNING")
    with TestClient(create_app(settings)) as client:
        response = client.get("/resources/urn:air:unverified:missing:none")
    assert response.status_code == 404


def test_search_limit_parameter(tmp_path: Path) -> None:
    db = Database(tmp_path / "limit.db")
    db.initialize()
    repo = ResourceRepository(db)
    for i in range(5):
        name = f"Research Agent {i}"
        card_url = f"https://example.com/research-{i}.json"
        repo.upsert(
            Resource(
                id=make_resource_id(card_url, name),
                name=name,
                description="research helper",
                endpoint_url=f"https://example.com/a2a/{i}",
                skills=[{"id": "research"}],
            )
        )

    settings = Settings(database_path=tmp_path / "limit.db", log_level="WARNING")
    with TestClient(create_app(settings)) as client:
        response = client.get("/search", params={"q": "research", "limit": 2})

    body = response.json()
    assert body["total"] == 5
    assert len(body["results"]) == 2
    assert body["limit"] == 2


def test_full_pipeline_card_to_search_api(tmp_path: Path) -> None:
    card = tmp_path / "agent.json"
    card.write_text(
        json.dumps(
            {
                "name": "Pipeline Search Agent",
                "description": "Discoverable via keyword search",
                "url": "https://example.com/a2a/pipeline-search",
                "skills": [{"id": "discovery", "name": "Discovery"}],
                "provider": {"organization": "Fixtures"},
                "capabilities": {"streaming": False},
            }
        ),
        encoding="utf-8",
    )
    seeds = tmp_path / "seeds.json"
    seeds.write_text(
        json.dumps({"seeds": [{"url": card.as_uri()}], "public_seeds": []}),
        encoding="utf-8",
    )
    db_path = tmp_path / "pipeline-api.db"
    settings = Settings(
        database_path=db_path,
        seeds_path=seeds,
        log_level="WARNING",
    )
    assert cmd_crawl(settings) == 0

    with TestClient(create_app(settings)) as client:
        search = client.get("/search", params={"q": "discovery"})
        assert search.status_code == 200
        results = search.json()["results"]
        assert len(results) == 1
        assert results[0]["name"] == "Pipeline Search Agent"

        detail = client.get(f"/resources/{quote(results[0]['id'], safe='')}")
        assert detail.status_code == 200
        assert detail.json()["endpoint_url"] == "https://example.com/a2a/pipeline-search"
