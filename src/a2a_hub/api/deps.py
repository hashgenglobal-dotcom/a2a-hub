"""Shared FastAPI request dependencies."""

from __future__ import annotations

from fastapi import HTTPException, Request

from a2a_hub.store.database import Database


def get_db(request: Request) -> Database:
    """Return the app SQLite database or 503 if not initialized."""
    db = getattr(request.app.state, "db", None)
    if db is None:
        raise HTTPException(status_code=503, detail="Database not initialized")
    return db  # type: ignore[no-any-return]
