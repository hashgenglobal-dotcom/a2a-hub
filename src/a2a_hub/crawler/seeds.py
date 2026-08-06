"""Seed list loading — URLs live in config, not in crawler business logic."""

from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)

# Repo-relative default; override with Settings.seeds_path / A2A_HUB_SEEDS_PATH
DEFAULT_SEEDS_PATH = Path("config/seeds.json")


def _repo_root() -> Path:
    """Best-effort repository root (parent of ``src/`` when installed editable)."""
    # a2a_hub/crawler/seeds.py → parents[2] == repo root when using src layout
    here = Path(__file__).resolve()
    src_root = here.parents[2]  # .../src
    if src_root.name == "src":
        return src_root.parent
    return Path.cwd()


def resolve_seed_url(url: str, *, base_dir: Path | None = None) -> str:
    """Normalize seed URLs; resolve relative ``file:`` paths against repo root."""
    base = base_dir or _repo_root()
    if url.startswith("file:"):
        raw = url[len("file:") :]
        # Support file:/abs, file:///abs, and file:relative/path
        if raw.startswith("///"):
            path = Path(raw[2:])  # file:///tmp/x → /tmp/x
        elif raw.startswith("/") and not raw.startswith("//"):
            path = Path(raw)
        else:
            path = (base / raw.lstrip("/")).resolve()
        return path.as_uri()
    return url


def load_seed_urls(
    seeds_path: Path | None = None,
    *,
    include_disabled_public: bool = False,
    base_dir: Path | None = None,
) -> list[str]:
    """Load enabled seed URLs from a seeds.json configuration file."""
    path = seeds_path or DEFAULT_SEEDS_PATH
    if not path.is_absolute():
        path = (_repo_root() / path).resolve()

    if not path.exists():
        raise FileNotFoundError(f"Seeds file not found: {path}")

    payload: dict[str, Any] = json.loads(path.read_text(encoding="utf-8"))
    base = base_dir or _repo_root()
    urls: list[str] = []

    for entry in payload.get("seeds", []):
        url = str(entry["url"])
        urls.append(resolve_seed_url(url, base_dir=base))

    for entry in payload.get("public_seeds", []):
        enabled = bool(entry.get("enabled", False))
        if enabled or include_disabled_public:
            urls.append(resolve_seed_url(str(entry["url"]), base_dir=base))

    logger.info(
        "Loaded seed URLs",
        extra={"fields": {"count": len(urls), "seeds_path": str(path)}},
    )
    return urls
