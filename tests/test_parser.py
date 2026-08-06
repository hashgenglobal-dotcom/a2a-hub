"""Parser: validation and normalization unit tests."""

from __future__ import annotations

from datetime import datetime, timezone

import pytest
from pydantic import ValidationError

from a2a_hub.models.agent_card import RawAgentCard
from a2a_hub.models.crawl import CrawlResult
from a2a_hub.models.resource import make_resource_id
from a2a_hub.parser.adapter import adapt_crawl_result
from a2a_hub.parser.normalizer import normalize_agent_card
from a2a_hub.parser.validator import validate_agent_card


def test_valid_agent_card_becomes_resource() -> None:
    card = RawAgentCard.from_json_dict(
        {
            "name": "Resume Parser",
            "url": "https://example.com/a2a/resume-parser",
            "description": "Parses resumes",
            "skills": [{"id": "resume-parsing", "name": "Resume Parsing"}],
            "capabilities": {"streaming": True},
            "provider": {"organization": "Fixtures"},
        }
    )
    card_url = "https://example.com/.well-known/agent.json"

    validation = validate_agent_card(card)
    assert validation.is_valid
    assert validation.errors == []

    resource = normalize_agent_card(card, card_url=card_url)
    assert resource.name == "Resume Parser"
    assert resource.endpoint_url == "https://example.com/a2a/resume-parser"
    assert resource.publisher == "unverified"
    assert resource.id == make_resource_id(card_url, "Resume Parser")
    assert resource.skills[0]["id"] == "resume-parsing"


def test_missing_required_fields() -> None:
    card = RawAgentCard.from_json_dict({"description": "only description"})
    result = validate_agent_card(card)

    assert not result.is_valid
    codes = {i.code for i in result.errors}
    assert "missing_name" in codes
    assert "missing_endpoint_url" in codes


def test_optional_fields_missing_are_warnings_only() -> None:
    card = RawAgentCard.from_json_dict(
        {"name": "Minimal Agent", "url": "https://example.com/a2a"}
    )
    result = validate_agent_card(card)

    assert result.is_valid
    warning_codes = {i.code for i in result.warnings}
    assert "missing_description" in warning_codes
    assert "missing_skills" in warning_codes
    assert "missing_capabilities" in warning_codes
    assert "missing_provider" in warning_codes

    resource = normalize_agent_card(
        card, card_url="https://example.com/.well-known/agent.json"
    )
    assert resource.description is None
    assert resource.skills == []


def test_stable_resource_id_generation() -> None:
    card_url = "https://example.com/.well-known/agent.json"
    card = RawAgentCard.from_json_dict(
        {"name": "Stable Agent", "url": "https://example.com/a2a"}
    )
    first = normalize_agent_card(card, card_url=card_url)
    second = normalize_agent_card(card, card_url=card_url)
    assert first.id == second.id
    assert first.id.startswith("urn:air:unverified:")


def test_raw_agent_card_not_mutated_by_validation() -> None:
    card = RawAgentCard.from_json_dict(
        {"name": "Immutable", "url": "https://example.com/a2a"}
    )
    validate_agent_card(card)
    with pytest.raises(ValidationError):
        card.name = "Changed"  # type: ignore[misc]


def test_adapt_crawl_result_invalid_json() -> None:
    crawl = CrawlResult(
        url="https://example.com/.well-known/agent.json",
        status_code=200,
        response_body="not-json",
        content_type="application/json",
        fetched_at=datetime.now(timezone.utc),
    )
    outcome = adapt_crawl_result(crawl)
    assert not outcome.ok
    assert outcome.parse_error is not None
    assert outcome.resource is None
