"""FastAPI application factory (Day 1 foundation)."""

from __future__ import annotations

from contextlib import asynccontextmanager
from collections.abc import AsyncIterator

from fastapi import FastAPI

from a2a_hub import __version__
from a2a_hub.config import Settings, get_settings
from a2a_hub.store.database import Database


def create_app(settings: Settings | None = None) -> FastAPI:
    """Build the FastAPI application.

    Day 1 exposes a health endpoint only. Search and resource routes
    arrive later in Sprint 1. Crawl remains CLI-only (ADR-008).
    """
    settings = settings or get_settings()

    @asynccontextmanager
    async def lifespan(app: FastAPI) -> AsyncIterator[None]:
        db = Database(settings.database_path)
        db.initialize()
        app.state.db = db
        yield

    app = FastAPI(
        title=settings.app_name,
        version=__version__,
        description="A2A Hub — Universal Agent Control Plane (MVP)",
        lifespan=lifespan,
    )
    app.state.settings = settings

    @app.get("/health")
    def health() -> dict[str, object]:
        """Liveness probe for the API process."""
        db: Database | None = getattr(app.state, "db", None)
        resources_count = 0
        if db is not None:
            with db.connect() as conn:
                row = conn.execute("SELECT COUNT(*) AS c FROM resources").fetchone()
                resources_count = int(row["c"]) if row else 0
        return {
            "status": "ok",
            "app": settings.app_name,
            "version": __version__,
            "resources_count": resources_count,
        }

    return app
