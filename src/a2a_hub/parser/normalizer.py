"""Normalize a validated RawAgentCard into a canonical Resource.

Never mutates the input card — always returns a new Resource.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from a2a_hub.models.agent_card import RawAgentCard
from a2a_hub.models.resource import Resource, make_resource_id


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


def _normalize_skills(skills: list[Any]) -> list[Any]:
    """Pass through skill entries; keep lists/dicts as-is for MVP storage."""
    return list(skills) if skills else []


def normalize_agent_card(card: RawAgentCard, *, card_url: str) -> Resource:
    """Map a valid RawAgentCard to a Resource.

    ``card_url`` is the canonical Agent Card location (crawl URL), used for
    stable ``make_resource_id``. Publisher is always ``unverified`` in MVP.
    """
    name = (card.name or "").strip()
    endpoint_url = (card.url or "").strip()
    description = (
        card.description.strip()
        if isinstance(card.description, str) and card.description.strip()
        else None
    )
    now = _utc_now()
    return Resource(
        id=make_resource_id(card_url, name),
        name=name,
        description=description,
        endpoint_url=endpoint_url,
        publisher="unverified",
        skills=_normalize_skills(card.skills),
        created_at=now,
        updated_at=now,
        card_url=card_url,
        resource_type="a2a-agent",
    )
