"""Crawl repository and CLI integration tests (no external network)."""

from __future__ import annotations

import json
from pathlib import Path

from a2a_hub.config import Settings
from a2a_hub.crawler.seeds import load_seed_urls, resolve_seed_url
from a2a_hub.main import cmd_crawl
from a2a_hub.models.crawl import CrawlResult
from a2a_hub.store.database import Database
from a2a_hub.store.repository import CrawlRepository


def _write_seeds(tmp_path: Path, card_paths: list[Path]) -> Path:
    seeds_path = tmp_path / "seeds.json"
    seeds_path.write_text(
        json.dumps(
            {
                "seeds": [{"url": p.as_uri()} for p in card_paths],
                "public_seeds": [],
            }
        ),
        encoding="utf-8",
    )
    return seeds_path


def test_load_seed_urls_from_config(tmp_path: Path) -> None:
    card = tmp_path / "card.json"
    card.write_text("{}", encoding="utf-8")
    seeds_path = _write_seeds(tmp_path, [card])

    urls = load_seed_urls(seeds_path=seeds_path, base_dir=tmp_path)
    assert urls == [card.as_uri()]


def test_resolve_relative_file_seed(tmp_path: Path) -> None:
    rel = "samples/agent_cards/sample_resume_parser.json"
    resolved = resolve_seed_url(f"file:{rel}", base_dir=tmp_path)
    assert resolved.startswith("file:")


def test_persist_crawl_results(tmp_path: Path) -> None:
    from a2a_hub.models.crawl import CrawlJobStatus

    db = Database(tmp_path / "crawl.db")
    db.initialize()
    repo = CrawlRepository(db)

    job_id = repo.create_job()
    result = CrawlResult(
        url="https://example.com/.well-known/agent.json",
        status_code=200,
        response_body='{"name":"Agent X"}',
        content_type="application/json",
        headers={"content-type": "application/json"},
        duration_ms=12,
    )
    row_id = repo.insert_result(result)
    repo.finish_job(job_id, status=CrawlJobStatus.COMPLETE)

    assert row_id > 0
    stored = repo.list_results()
    assert len(stored) == 1
    assert stored[0].response_body == '{"name":"Agent X"}'
    assert stored[0].headers == {"content-type": "application/json"}
    assert stored[0].duration_ms == 12
    assert repo.count_results() == 1


def test_cli_crawl_fetches_local_seeds_and_persists(tmp_path: Path) -> None:
    card = tmp_path / "agent.json"
    card.write_text(
        json.dumps({"name": "CLI Agent", "url": "https://example.com/a2a"}),
        encoding="utf-8",
    )
    seeds_path = _write_seeds(tmp_path, [card])
    db_path = tmp_path / "cli.db"

    settings = Settings(
        database_path=db_path,
        seeds_path=seeds_path,
        log_level="WARNING",
    )
    code = cmd_crawl(settings)

    assert code == 0
    repo = CrawlRepository(Database(db_path))
    results = repo.list_results()
    assert len(results) == 1
    assert results[0].error is None
    assert results[0].response_body is not None
    assert "CLI Agent" in results[0].response_body
