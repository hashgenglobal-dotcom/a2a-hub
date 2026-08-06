"""HTML discovery UI routes (Jinja2). Uses ResourceRepository — no duplicated search SQL."""

from __future__ import annotations

from urllib.parse import quote

from fastapi import APIRouter, HTTPException, Query, Request
from fastapi.responses import HTMLResponse

from a2a_hub.api.deps import get_db
from a2a_hub.store.repository import ResourceRepository
from a2a_hub.ui.templating import templates

ui_router = APIRouter(default_response_class=HTMLResponse)


def wants_html(request: Request) -> bool:
    """Prefer HTML when the client ranks text/html ahead of application/json."""
    accept = request.headers.get("accept", "")
    if not accept or accept == "*/*":
        return False
    html_pos = accept.find("text/html")
    if html_pos < 0:
        return False
    json_pos = accept.find("application/json")
    if json_pos < 0:
        return True
    return html_pos < json_pos


@ui_router.get("/", response_class=HTMLResponse)
def home(
    request: Request,
    q: str = Query(default=""),
    limit: int = Query(default=20, ge=1, le=100),
) -> HTMLResponse:
    """Search page — form GET ``/?q=``; results from repository keyword search."""
    repo = ResourceRepository(get_db(request))
    results: list[dict[str, object]] = []
    total = 0
    query = q.strip()
    if query:
        matches, total = repo.search_resources(query, limit=limit, offset=0)
        results = [
            {
                "id": quote(r.id, safe=""),
                "name": r.name,
                "description": r.description,
                "endpoint_url": r.endpoint_url,
                "skills": r.skills,
            }
            for r in matches
        ]

    return templates.TemplateResponse(
        request,
        "index.html",
        {
            "q": query,
            "results": results,
            "total": total,
        },
    )


def render_resource_detail(request: Request, resource_id: str) -> HTMLResponse:
    """Render resource detail HTML."""
    repo = ResourceRepository(get_db(request))
    resource = repo.get_resource_by_id(resource_id)
    if resource is None:
        raise HTTPException(status_code=404, detail="Resource not found")
    return templates.TemplateResponse(
        request,
        "resource.html",
        {"resource": resource, "q": request.query_params.get("q", "")},
    )
