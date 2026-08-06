"""HTTP JSON API route handlers — thin; repository owns query logic."""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, HTTPException, Query, Request
from fastapi.responses import JSONResponse, Response

from a2a_hub.api.deps import get_db
from a2a_hub.models.resource import Resource
from a2a_hub.store.repository import ResourceRepository
from a2a_hub.ui.views import render_resource_detail, wants_html

router = APIRouter()


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
def health(request: Request) -> dict[str, Any]:
    """Liveness / readiness probe with basic registry stats."""
    from a2a_hub import __version__

    db = get_db(request)
    try:
        with db.connect() as conn:
            row = conn.execute("SELECT COUNT(*) AS c FROM resources").fetchone()
            resources = int(row["c"]) if row else 0
        return {
            "status": "ok",
            "database": "connected",
            "resources": resources,
            "version": __version__,
        }
    except Exception:
        return {
            "status": "degraded",
            "database": "error",
            "resources": 0,
            "version": __version__,
        }


@router.get("/search")
def search_resources(
    request: Request,
    q: str = Query(default="", description="Keyword over name, description, skills"),
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
) -> dict[str, Any]:
    """Keyword discovery over indexed Resources (JSON)."""
    repo = ResourceRepository(get_db(request))
    matches, total = repo.search_resources(q, limit=limit, offset=offset)
    return {
        "results": [_search_item(r) for r in matches],
        "total": total,
        "limit": limit,
        "offset": offset,
        "q": q,
    }


@router.get("/resources/{resource_id:path}")
def get_resource(resource_id: str, request: Request) -> Response:
    """Resource detail — HTML for browsers, JSON for API clients."""
    if wants_html(request):
        return render_resource_detail(request, resource_id)

    repo = ResourceRepository(get_db(request))
    resource = repo.get_resource_by_id(resource_id)
    if resource is None:
        raise HTTPException(status_code=404, detail="Resource not found")
    return JSONResponse(_resource_detail(resource))
