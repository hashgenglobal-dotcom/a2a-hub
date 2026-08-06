"""Canonical Resource entity — the platform domain object.

Agent Cards are protocol inputs only; Resources are what we store and search.
"""

from __future__ import annotations

import hashlib
import re
from datetime import datetime, timezone
from typing import Any

from pydantic import BaseModel, Field


def _slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return slug[:64] or "resource"


def make_resource_id(card_url: str, name: str | None = None) -> str:
    """Build a stable unverified Resource ID from the canonical Agent Card URL.

    Format: ``urn:air:unverified:<sha256-of-card-url>:<slug>``
    Publisher verification is intentionally out of scope for MVP.
    """
    digest = hashlib.sha256(card_url.encode("utf-8")).hexdigest()
    slug = _slugify(name) if name else digest[:12]
    return f"urn:air:unverified:{digest}:{slug}"


class Resource(BaseModel):
    """Platform-agnostic AI resource (canonical store/search entity)."""

    id: str
    name: str
    description: str | None = None
    endpoint_url: str
    publisher: str = "unverified"
    skills: list[Any] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    # Provenance helpers (not all columns exist in Day 1 schema yet)
    card_url: str | None = None
    resource_type: str = "a2a-agent"
