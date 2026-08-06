"""Adapt CrawlResult → RawAgentCard → validate → Resource (no DB)."""

from __future__ import annotations

import json
import logging
from typing import Any

from pydantic import BaseModel

from a2a_hub.models.agent_card import RawAgentCard
from a2a_hub.models.crawl import CrawlResult
from a2a_hub.models.resource import Resource
from a2a_hub.parser.normalizer import normalize_agent_card
from a2a_hub.parser.validator import ValidationResult, validate_agent_card

logger = logging.getLogger(__name__)


class AdaptOutcome(BaseModel):
    """Result of adapting one crawl result into a Resource (or skipping)."""

    card_url: str
    resource: Resource | None = None
    validation: ValidationResult | None = None
    parse_error: str | None = None
    skipped_reason: str | None = None

    @property
    def ok(self) -> bool:
        return self.resource is not None


def _parse_json_body(body: str) -> dict[str, Any] | str:
    """Return a dict on success, or an error string."""
    try:
        payload = json.loads(body)
    except json.JSONDecodeError as exc:
        return f"invalid_json: {exc}"
    if not isinstance(payload, dict):
        return "invalid_json: Agent Card root must be a JSON object"
    return payload


def adapt_crawl_result(crawl: CrawlResult) -> AdaptOutcome:
    """Parse → RawAgentCard → validate → normalize.

    Does not mutate crawl data or the RawAgentCard. Invalid cards do not raise.
    """
    card_url = crawl.url

    if crawl.error and crawl.response_body is None:
        return AdaptOutcome(
            card_url=card_url,
            skipped_reason=f"crawl_error: {crawl.error}",
        )

    if not crawl.response_body:
        return AdaptOutcome(
            card_url=card_url,
            skipped_reason="empty_response_body",
        )

    parsed = _parse_json_body(crawl.response_body)
    if isinstance(parsed, str):
        logger.warning(
            "Failed to parse Agent Card JSON",
            extra={"fields": {"url": card_url, "error": parsed}},
        )
        return AdaptOutcome(card_url=card_url, parse_error=parsed)

    card = RawAgentCard.from_json_dict(parsed)
    validation = validate_agent_card(card)

    for issue in validation.warnings:
        logger.info(
            "Agent Card validation warning",
            extra={
                "fields": {
                    "url": card_url,
                    "code": issue.code,
                    "field": issue.field,
                    "message": issue.message,
                }
            },
        )

    if not validation.is_valid:
        for issue in validation.errors:
            logger.warning(
                "Agent Card validation error",
                extra={
                    "fields": {
                        "url": card_url,
                        "code": issue.code,
                        "field": issue.field,
                        "message": issue.message,
                    }
                },
            )
        return AdaptOutcome(card_url=card_url, validation=validation)

    resource = normalize_agent_card(card, card_url=card_url)
    return AdaptOutcome(
        card_url=card_url,
        resource=resource,
        validation=validation,
    )
