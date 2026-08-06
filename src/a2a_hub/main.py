"""CLI entry point: ``python -m a2a_hub crawl|serve``."""

from __future__ import annotations

import argparse
import logging
import sys

import uvicorn

from a2a_hub.api.app import create_app
from a2a_hub.config import Settings, get_settings
from a2a_hub.logging import setup_logging
from a2a_hub.store.database import Database

logger = logging.getLogger(__name__)


def cmd_crawl(settings: Settings) -> int:
    """Initialize storage for crawl. Fetch pipeline is Sprint 1 Day 2."""
    db = Database(settings.database_path)
    db.initialize()
    logger.info(
        "Crawl command ready — fetch/parse pipeline not implemented yet (Day 2)",
        extra={
            "fields": {
                "database_path": str(settings.database_path),
                "crawler_timeout_seconds": settings.crawler_timeout_seconds,
            }
        },
    )
    return 0


def cmd_serve(settings: Settings) -> int:
    """Serve the HTTP API (crawl is not started with the server — ADR-008)."""
    app = create_app(settings)
    logger.info(
        "Starting API server",
        extra={
            "fields": {
                "host": settings.host,
                "port": settings.port,
                "database_path": str(settings.database_path),
            }
        },
    )
    uvicorn.run(app, host=settings.host, port=settings.port, log_config=None)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="a2a-hub",
        description="A2A Hub — discover and index A2A-compatible AI resources",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("crawl", help="Run the crawl pipeline (CLI only; no background workers)")
    sub.add_parser("serve", help="Start the HTTP API and minimal UI server")

    return parser


def main(argv: list[str] | None = None) -> None:
    """Parse CLI args and dispatch to crawl or serve."""
    # Clear settings cache so tests/env changes are respected
    get_settings.cache_clear()
    settings = get_settings()
    setup_logging(settings.log_level)

    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "crawl":
        code = cmd_crawl(settings)
    elif args.command == "serve":
        code = cmd_serve(settings)
    else:
        parser.error(f"Unknown command: {args.command}")
        code = 2

    raise SystemExit(code)


if __name__ == "__main__":
    main(sys.argv[1:])
