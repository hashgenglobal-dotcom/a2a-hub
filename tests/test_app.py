"""Application startup smoke tests."""

from __future__ import annotations

import json
from pathlib import Path

from fastapi.testclient import TestClient

from a2a_hub.api.app import create_app
from a2a_hub.config import Settings
from a2a_hub.main import build_parser, cmd_crawl


def test_health_endpoint_starts_and_returns_ok(tmp_path: Path) -> None:
    settings = Settings(database_path=tmp_path / "app.db", log_level="WARNING")
    app = create_app(settings)

    with TestClient(app) as client:
        response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
    assert (tmp_path / "app.db").exists()


def test_cli_parser_requires_command() -> None:
    parser = build_parser()
    assert parser.parse_args(["crawl"]).command == "crawl"
    assert parser.parse_args(["serve"]).command == "serve"


def test_cmd_crawl_initializes_database_and_stores_results(tmp_path: Path) -> None:
    card = tmp_path / "agent.json"
    card.write_text('{"name":"Smoke","url":"https://example.com/a2a"}', encoding="utf-8")
    seeds = tmp_path / "seeds.json"
    seeds.write_text(
        json.dumps({"seeds": [{"url": card.as_uri()}], "public_seeds": []}),
        encoding="utf-8",
    )

    settings = Settings(
        database_path=tmp_path / "crawl.db",
        seeds_path=seeds,
        log_level="WARNING",
    )
    code = cmd_crawl(settings)

    assert code == 0
    assert (tmp_path / "crawl.db").exists()
