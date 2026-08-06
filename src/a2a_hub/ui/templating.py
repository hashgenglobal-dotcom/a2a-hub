"""Jinja2 template helpers for the discovery UI."""

from __future__ import annotations

from pathlib import Path

from fastapi.templating import Jinja2Templates
from starlette.datastructures import URLPath

_TEMPLATES_DIR = Path(__file__).resolve().parent / "templates"

templates = Jinja2Templates(directory=str(_TEMPLATES_DIR))


def skill_label(skill: object) -> str:
    """Human-readable skill label for templates / tests."""
    if isinstance(skill, dict):
        value = skill.get("name") or skill.get("id") or skill
        return str(value)
    return str(skill)


# Expose helpers to Jinja
templates.env.globals["skill_label"] = skill_label


def resource_href(resource_id: str) -> str:
    """Build an href for a resource detail page (URN-safe)."""
    return str(URLPath(f"/resources/{resource_id}"))
