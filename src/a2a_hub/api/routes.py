"""HTTP route handlers — thin; repository owns query logic."""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, HTTPException, Query, Request

from a2a_hub.models.resource import Resource
from a2a_hub.store.database import Database
from a2a_hub.store.repository import ResourceRepository

router = APIRouter()


def _db(request: Request) -> Database:
    db = getattr(request.app.state, "db", None)
    if db is None:
        raise HTTPException(status_code=503, detail="Database not initialized")
    return db  # type: ignore[no-any-return]


def _search_item(resource: Resource) -> dict[str, Any]:
    return {
        "id": resource.id,
        "name": resource.name,
        "description": resource.description,
        "endpoint_url": resource.endpoint_url,
        "skills": resource.skills,
    }


def _resource_detail(resource: Resource) -> dict[str, Any]:
    return {
        "id": resource.id,
        "name": resource.name,
        "description": resource.description,
        "endpoint_url": resource.endpoint_url,
        "publisher": resource.publisher,
        "skills": resource.skills,
        "resource_type": resource.resource_type,
        "card_url": resource.card_url,
        "created_at": resource.created_at.isoformat(),
        "updated_at": resource.updated_at.isoformat(),
    }


@router.get("/health")
def health(request: Request) -> dict[str, str]:
    """Liveness probe (read-only)."""
    _ = _db(request)  # ensure app started cleanly
    return {"status": "ok"}


@router.get("/search")
def search_resources(
    request: Request,
    q: str = Query(default="", description="Keyword over name, description, skills"),
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
) -> dict[str, Any]:
    """Keyword discovery over indexed Resources."""
    repo = ResourceRepository(_db(request))
    matches, total = repo.search_resources(q, limit=limit, offset=offset)
    return {
        "results": [_search_item(r) for r in matches],
        "total": total,
        "limit": limit,
        "offset": offset,
        "q": q,
    }


@router.get("/resources/{resource_id:path}")
def get_resource(resource_id: str, request: Request) -> dict[str, Any]:
    """Return a complete Resource by stable id (URN path-safe)."""
    repo = ResourceRepository(_db(request))
    resource = repo.get_resource_by_id(resource_id)
    if resource is None:
        raise HTTPException(status_code=404, detail="Resource not found")
    return _resource_detail(resource)
