"""A2A Agent Card parser: validate + normalize into Resources."""

from a2a_hub.parser.adapter import AdaptOutcome, adapt_crawl_result
from a2a_hub.parser.normalizer import normalize_agent_card
from a2a_hub.parser.validator import (
    ValidationIssue,
    ValidationResult,
    validate_agent_card,
)

__all__ = [
    "AdaptOutcome",
    "ValidationIssue",
    "ValidationResult",
    "adapt_crawl_result",
    "normalize_agent_card",
    "validate_agent_card",
]
