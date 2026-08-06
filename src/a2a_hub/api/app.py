"""FastAPI application factory — public read-only Resource API."""

from __future__ import annotations

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from a2a_hub import __version__
from a2a_hub.api.routes import router
from a2a_hub.config import Settings, get_settings
from a2a_hub.store.database import Database


def create_app(settings: Settings | None = None) -> FastAPI:
    """Build the FastAPI application.

    Exposes ``GET /health``, ``GET /search``, ``GET /resources/{id}``.
    Crawl remains CLI-only (ADR-008). No auth (ADR-009).
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
    app.include_router(router)
    return app
