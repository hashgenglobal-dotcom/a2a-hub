"""A2A Agent Card — protocol input only, not the platform entity.

RawAgentCard is **immutable**. Never mutate it after construction.

Correct pipeline:

  HTTP Response
       │
       ▼
  RawAgentCard   ← frozen snapshot of protocol input
       │
       ▼
  Validator      ← reads raw; does not write back onto it
       │
       ▼
  Normalizer     ← maps raw → Resource (new object)
       │
       ▼
  Resource       ← canonical platform entity → SQLite

Incorrect:

  RawAgentCard → add normalized fields → save

Preserving an untouched raw card matters later for trust scoring,
auditing, dispute resolution, and reputation.

Tolerant by design: extra fields are retained; required-field enforcement
belongs in the validator (Sprint 1 Day 3), not in this model.
"""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class RawAgentCard(BaseModel):
    """Immutable parsed Agent Card JSON before normalization into a Resource."""

    model_config = ConfigDict(
        extra="allow",
        frozen=True,
    )

    name: str | None = None
    description: str | None = None
    # A2A Agent Card endpoint URL (maps to Resource.endpoint_url)
    url: str | None = None
    provider: dict[str, Any] | None = None
    capabilities: dict[str, Any] | None = None
    skills: list[Any] = Field(default_factory=list)
    # Auth shapes vary across A2A versions; keep flexible
    authentication: dict[str, Any] | list[Any] | None = None
    securitySchemes: dict[str, Any] | None = None
    defaultInputModes: list[str] | None = None
    defaultOutputModes: list[str] | None = None
    version: str | None = None
    protocolVersion: str | None = None

    @classmethod
    def from_json_dict(cls, payload: dict[str, Any]) -> RawAgentCard:
        """Build a frozen card from arbitrary JSON (extra keys preserved)."""
        return cls.model_validate(payload)
