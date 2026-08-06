# A2A Hub — Target Architecture

**This document describes the Phase 2+ target architecture.**

For the current MVP architecture, see `ARCHITECTURE_MVP.md`.

---

## Overview

The target architecture is an event-driven, modular system built around the Resource Knowledge Graph. It is organized into four layers: Ingestion, Knowledge Graph, API, and Presentation.

```
┌─────────────────────────────────────────────────────────────────────┐
│                        PRESENTATION LAYER                            │
│  ┌─────────────────┐  ┌─────────────────┐  ┌──────────────────────┐  │
│  │  REST API       │  │  Resource       │  │  Enterprise          │  │
│  │  (FastAPI)      │  │  Profiles (Web) │  │  Dashboard (Gov UI)  │  │
│  └────────┬────────┘  └────────┬────────┘  └──────────┬───────────┘  │
└───────────┼────────────────────┼──────────────────────┼──────────────┘
            │                    │                      │
┌───────────┼────────────────────┼──────────────────────┼──────────────┐
│           ▼                    ▼                      ▼               │
│                     KNOWLEDGE GRAPH LAYER                             │
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │                    Resource Knowledge Graph                    │   │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────────┐ │   │
│  │  │Resources │  │ Orgs     │  │ Skills   │  │ Relationships│ │   │
│  │  └──────────┘  └──────────┘  └──────────┘  └──────────────┘ │   │
│  │                                                              │   │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────────┐ │   │
│  │  │ Health   │  │ Trust    │  │ Crawl    │  │ Events       │ │   │
│  │  │ Records  │  │ Records  │  │ Targets  │  │ (Audit Log)  │ │   │
│  │  └──────────┘  └──────────┘  └──────────┘  └──────────────┘ │   │
│  └──────────────────────────────────────────────────────────────┘   │
└───────────┬────────────────────┬──────────────────────┬──────────────┘
            │                    │                      │
┌───────────┼────────────────────┼──────────────────────┼──────────────┐
│           ▼                    ▼                      ▼               │
│                        INGESTION LAYER                               │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌────────────┐ │
│  │  Crawler    │  │  Parser     │  │  Embedder   │  │  Health    │ │
│  │  (aiohttp)  │  │  (pydantic) │  │  (MiniLM)   │  │  Checker   │ │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘  └─────┬──────┘ │
│         │                │                │               │        │
│  ┌──────┴──────┐  ┌──────┴──────┐  ┌──────┴──────┐  ┌────┴───────┐│
│  │  URL Queue  │  │  Validator  │  │  Indexer    │  │  Alert     ││
│  │  (SQLite)   │  │  (Schema)   │  │  (Writer)   │  │  Engine    ││
│  └─────────────┘  └─────────────┘  └─────────────┘  └────────────┘│
└─────────────────────────────────────────────────────────────────────┘
```

## Phase 2 Additions

- Embedder Service (all-MiniLM-L6-v2) for semantic search
- Health Checker Service for periodic liveness probes
- Identity Verification Service for cryptographic signature validation
- OAuth Broker for agent-to-agent authentication
- Staleness Manager for TTL-based re-crawling

## Phase 3 Additions

- Reputation System with multi-dimensional trust scoring
- Federation Protocol (ARDS-compliant)
- Platform Adapters (Google Agent Registry, Salesforce AgentExchange)
- Protocol Wrappers (expose as A2A Agent)

## Phase 4 Additions

- Enterprise Dashboard with governance and compliance
- Private registry for internal agent directories
- Analytics API for ecosystem intelligence
- Compliance reports and audit trails

## Storage Evolution

| Phase | Technology | Purpose |
|-------|-----------|---------|
| MVP | SQLite | Single file, zero infrastructure |
| Phase 2 | PostgreSQL + pgvector | Vector search, scale |
| Phase 2 | Redis | Cache, crawl queue |
| Phase 3 | Federation | Cross-registry interoperability |
