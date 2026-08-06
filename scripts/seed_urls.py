#!/usr/bin/env python3
"""Seed URL loader for A2A Hub crawls.

Business logic must not hardcode seed URLs. Load them from ``config/seeds.json``
(or ``A2A_HUB_SEEDS_PATH``) via :func:`load_seed_urls`.

Local ``file:`` entries point at checked-in sample Agent Cards for deterministic
development and tests. Enable entries under ``public_seeds`` when real public
Agent Card URLs are available.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

# Allow ``python scripts/seed_urls.py`` without install
_REPO_ROOT = Path(__file__).resolve().parents[1]
if str(_REPO_ROOT / "src") not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT / "src"))

from a2a_hub.crawler.seeds import DEFAULT_SEEDS_PATH, load_seed_urls  # noqa: E402


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="List configured Agent Card seed URLs")
    parser.add_argument(
        "--seeds-path",
        type=Path,
        default=None,
        help=f"Path to seeds.json (default: {DEFAULT_SEEDS_PATH})",
    )
    parser.add_argument(
        "--include-disabled-public",
        action="store_true",
        help="Also print disabled public_seeds entries",
    )
    args = parser.parse_args(argv)

    urls = load_seed_urls(
        seeds_path=args.seeds_path,
        include_disabled_public=args.include_disabled_public,
    )
    for url in urls:
        print(url)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
