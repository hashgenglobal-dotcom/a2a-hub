"""Full pipeline fixture tests: sample card → crawl → resource (no network)."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from a2a_hub.config import Settings
from a2a_hub.main import cmd_crawl
from a2a_hub.models.agent_card import RawAgentCard
from a2a_hub.models.crawl import CrawlResult
from a2a_hub.models.resource import make_resource_id
from a2a_hub.parser.adapter import adapt_crawl_result
from a2a_hub.parser.normalizer import normalize_agent_card
from a2a_hub.store.database import Database
from a2a_hub.store.repository import ResourceRepository
from datetime import datetime, timezone


def _write_card_and_seeds(tmp_path: Path, payload: dict) -> tuple[Path, Path]:
    card = tmp_path / "agent.json"
    card.write_text(json.dumps(payload), encoding="utf-8")
    seeds = tmp_path / "seeds.json"
    seeds.write_text(
        json.dumps({"seeds": [{"url": card.as_uri()}], "public_seeds": []}),
        encoding="utf-8",
    )
    return card, seeds


def test_duplicate_crawl_updates_existing_resource(tmp_path: Path) -> None:
    card_url = "https://example.com/.well-known/agent.json"
    db = Database(tmp_path / "dup.db")
    db.initialize()
    repo = ResourceRepository(db)

    v1 = normalize_agent_card(
        RawAgentCard.from_json_dict(
            {
                "name": "Echo",
                "url": "https://example.com/a2a",
                "description": "v1",
                "skills": [{"id": "echo"}],
            }
        ),
        card_url=card_url,
    )
    first = repo.upsert(v1)
    created_at = first.created_at

    v2 = normalize_agent_card(
        RawAgentCard.from_json_dict(
            {
                "name": "Echo",
                "url": "https://example.com/a2a",
                "description": "v2 updated",
                "skills": [{"id": "echo"}, {"id": "ping"}],
            }
        ),
        card_url=card_url,
    )
    second = repo.upsert(v2)

    assert second.id == first.id == make_resource_id(card_url, "Echo")
    assert repo.count() == 1
    assert second.description == "v2 updated"
    assert len(second.skills) == 2
    assert second.created_at == created_at
    assert second.updated_at >= created_at


def test_full_pipeline_sample_card_to_resource(tmp_path: Path) -> None:
    payload = {
        "name": "Sample Resume Parser",
        "description": "Fixture agent",
        "url": "https://example.com/a2a/resume-parser",
        "provider": {"organization": "Fixtures"},
        "capabilities": {"streaming": True},
        "skills": [{"id": "resume-parsing", "name": "Resume Parsing"}],
    }
    card_path, seeds_path = _write_card_and_seeds(tmp_path, payload)
    db_path = tmp_path / "pipeline.db"

    settings = Settings(
        database_path=db_path,
        seeds_path=seeds_path,
        log_level="WARNING",
    )
    assert cmd_crawl(settings) == 0

    repo = ResourceRepository(Database(db_path))
    resources = repo.list_all()
    assert len(resources) == 1
    resource = resources[0]
    assert resource.name == "Sample Resume Parser"
    assert resource.endpoint_url == "https://example.com/a2a/resume-parser"
    assert resource.publisher == "unverified"
    assert resource.id == make_resource_id(card_path.as_uri(), "Sample Resume Parser")

    # Second crawl upserts same id
    assert cmd_crawl(settings) == 0
    assert repo.count() == 1


def test_adapt_from_crawl_result_fixture() -> None:
    body = json.dumps(
        {
            "name": "Pipeline Agent",
            "url": "https://example.com/a2a",
            "skills": [],
        }
    )
    crawl = CrawlResult(
        url="file:///tmp/agent.json",
        status_code=200,
        response_body=body,
        content_type="application/json",
        fetched_at=datetime.now(timezone.utc),
    )
    outcome = adapt_crawl_result(crawl)
    assert outcome.ok
    assert outcome.resource is not None
    assert outcome.validation is not None
    assert outcome.validation.is_valid
    assert outcome.resource.name == "Pipeline Agent"
