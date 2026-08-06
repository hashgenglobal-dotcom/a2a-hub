"""Domain model unit tests."""

from __future__ import annotations

from a2a_hub.models import CrawlResult, RawAgentCard, Resource, make_resource_id


def test_make_resource_id_is_stable_for_card_url() -> None:
    card_url = "https://example.com/.well-known/agent.json"
    first = make_resource_id(card_url, name="Agent X")
    second = make_resource_id(card_url, name="Agent X")

    assert first == second
    assert first.startswith("urn:air:unverified:")
    assert first.endswith(":agent-x")


def test_raw_agent_card_preserves_extra_fields() -> None:
    card = RawAgentCard.from_json_dict(
        {
            "name": "Agent X",
            "url": "https://example.com/a2a",
            "customExtension": {"foo": 1},
        }
    )

    assert card.name == "Agent X"
    assert card.url == "https://example.com/a2a"
    assert card.model_extra is not None
    assert card.model_extra["customExtension"] == {"foo": 1}


def test_resource_is_platform_entity() -> None:
    resource = Resource(
        id=make_resource_id("https://example.com/.well-known/agent.json", "Agent X"),
        name="Agent X",
        endpoint_url="https://example.com/a2a",
        card_url="https://example.com/.well-known/agent.json",
    )

    assert resource.publisher == "unverified"
    assert resource.resource_type == "a2a-agent"


def test_crawl_result_can_hold_raw_body() -> None:
    result = CrawlResult(
        url="https://example.com/.well-known/agent.json",
        status_code=200,
        response_body='{"name":"Agent X"}',
        content_type="application/json",
        headers={"content-type": "application/json"},
        duration_ms=42,
    )

    assert result.response_body is not None
    assert result.duration_ms == 42
