"""Tolerant Agent Card validation. Never mutates RawAgentCard."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field, HttpUrl, ValidationError
from pydantic import TypeAdapter

from a2a_hub.models.agent_card import RawAgentCard

Severity = Literal["error", "warning"]


class ValidationIssue(BaseModel):
    """One validation finding."""

    severity: Severity
    code: str
    message: str
    field: str | None = None


class ValidationResult(BaseModel):
    """Outcome of validating an immutable RawAgentCard."""

    is_valid: bool
    issues: list[ValidationIssue] = Field(default_factory=list)
    card: RawAgentCard

    @property
    def errors(self) -> list[ValidationIssue]:
        return [i for i in self.issues if i.severity == "error"]

    @property
    def warnings(self) -> list[ValidationIssue]:
        return [i for i in self.issues if i.severity == "warning"]


_URL_ADAPTER: TypeAdapter[HttpUrl] = TypeAdapter(HttpUrl)


def _looks_like_url(value: str) -> bool:
    """Accept http(s) and file URLs used by local fixtures."""
    lowered = value.strip().lower()
    if lowered.startswith("file:"):
        return len(value.strip()) > 5
    try:
        _URL_ADAPTER.validate_python(value.strip())
        return True
    except ValidationError:
        return False


def validate_agent_card(card: RawAgentCard) -> ValidationResult:
    """Validate required fields; optional absences become warnings only.

    Required:
      - name (non-empty string)
      - url (endpoint URL on the Agent Card)

    Optional (warn if missing): description, skills, capabilities, provider/metadata.
    """
    issues: list[ValidationIssue] = []

    name = (card.name or "").strip() if isinstance(card.name, str) else ""
    if not name:
        issues.append(
            ValidationIssue(
                severity="error",
                code="missing_name",
                message="Agent name is required",
                field="name",
            )
        )

    endpoint = (card.url or "").strip() if isinstance(card.url, str) else ""
    if not endpoint:
        issues.append(
            ValidationIssue(
                severity="error",
                code="missing_endpoint_url",
                message="Endpoint URL (Agent Card 'url') is required",
                field="url",
            )
        )
    elif not _looks_like_url(endpoint):
        issues.append(
            ValidationIssue(
                severity="error",
                code="invalid_endpoint_url",
                message=f"Endpoint URL is not a valid URL: {endpoint!r}",
                field="url",
            )
        )

    description = ""
    if isinstance(card.description, str):
        description = card.description.strip()
    if not description:
        issues.append(
            ValidationIssue(
                severity="warning",
                code="missing_description",
                message="Description is optional but recommended",
                field="description",
            )
        )

    if not card.skills:
        issues.append(
            ValidationIssue(
                severity="warning",
                code="missing_skills",
                message="Skills are optional but recommended",
                field="skills",
            )
        )

    if not card.capabilities:
        issues.append(
            ValidationIssue(
                severity="warning",
                code="missing_capabilities",
                message="Capabilities are optional but recommended",
                field="capabilities",
            )
        )

    if not card.provider:
        issues.append(
            ValidationIssue(
                severity="warning",
                code="missing_provider",
                message="Provider/metadata is optional but recommended",
                field="provider",
            )
        )

    is_valid = not any(i.severity == "error" for i in issues)
    return ValidationResult(is_valid=is_valid, issues=issues, card=card)
