# A2A Hub

**The Universal Agent Control Plane.**

**Mission:** Make every AI resource discoverable, trustworthy, observable, and interoperable across the open Agent Internet.

---

## What This Is

A2A Hub is an open-source infrastructure project. It provides a unified control plane for discovering, verifying, monitoring, and governing AI resources across any platform, protocol, or organization.

This repository contains the MVP: a crawler, search index, and API for discovering A2A-compatible AI agents.

For the full product vision, see [`docs/strategy/VISION.md`](docs/strategy/VISION.md).

---

## Quick Start

```bash
git clone https://github.com/hashgenglobal-dotcom/a2a-hub.git
cd a2a-hub
pip install -e ".[dev]"
python -m a2a_hub crawl
python -m a2a_hub serve
```

Open http://localhost:8000 in a browser.

---

## Repository Map

| Path | Purpose |
|------|---------|
| [`docs/implementation/MVP_SPEC.md`](docs/implementation/MVP_SPEC.md) | **Start here.** Implementation contract for the MVP. |
| [`docs/implementation/SPRINT_01.md`](docs/implementation/SPRINT_01.md) | Sprint 1 plan with day-level tasks. |
| [`docs/architecture/ARCHITECTURE_MVP.md`](docs/architecture/ARCHITECTURE_MVP.md) | Current architecture (single process, SQLite). |
| [`docs/architecture/ARCHITECTURE_TARGET.md`](docs/architecture/ARCHITECTURE_TARGET.md) | Target architecture (Phase 2+). |
| [`docs/architecture/DOMAIN_MODEL_MVP.md`](docs/architecture/DOMAIN_MODEL_MVP.md) | Domain model for the MVP. |
| [`docs/architecture/DOMAIN_MODEL_TARGET.md`](docs/architecture/DOMAIN_MODEL_TARGET.md) | Domain model for the full platform. |
| [`docs/architecture/ENGINEERING_PRINCIPLES.md`](docs/architecture/ENGINEERING_PRINCIPLES.md) | Engineering principles and standards. |
| [`docs/strategy/VISION.md`](docs/strategy/VISION.md) | Product vision, mission, and business model. |
| [`docs/adr/`](docs/adr/) | Architecture Decision Records. |

---

## License

Apache 2.0. See [LICENSE](LICENSE).
