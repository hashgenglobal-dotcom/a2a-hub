# Announcement Drafts

---

## GitHub Discussion #1 — Announcement

**Title:** Introducing A2A Hub — Open Discovery Layer for AI Agents

**Category:** Announcements

**Body:**

A2A Hub v0.1.0 is live.

**The problem:** The A2A protocol defines *how* agents communicate — but not how developers find, evaluate, and discover them. Every integration requires a hand-copied URL. There is no cross-owner discovery layer.

**What A2A Hub does:** It crawls A2A Agent Cards from configured seed sources, validates and normalizes them into a canonical Resource registry, and exposes keyword search through API and web UI.

**What's in v0.1.0:**
- Agent Card crawling (async HTTP)
- Schema validation and normalization
- Resource registry (SQLite)
- Keyword search API (`GET /search`, `GET /resources/{id}`, `GET /health`)
- Minimal web UI
- Docker image

**Stack:** Python, FastAPI, SQLite, aiohttp, pydantic. Single process. Zero infrastructure.

**Roadmap:** Discovery → Trust → Federation → Universal Agent Control Plane

**We're looking for:**
- Feedback on the approach
- Reports of what's missing or broken
- Agents to index (point us to your Agent Card URL)
- Contributors who want to help build the trust layer

**Links:**
- GitHub: github.com/hashgenglobal-dotcom/a2a-hub
- Release: github.com/hashgenglobal-dotcom/a2a-hub/releases/tag/v0.1.0
- Docs: docs/implementation/BUILD_SPEC.md

---

## GitHub Discussion #2 — Ecosystem Conversation

**Title:** How should AI agents be discovered and trusted?

**Category:** Ideas

**Body:**

The A2A protocol solves *how* agents communicate. But a bigger question is still open: *how should agents find each other and establish trust?*

A2A Hub is our attempt at an answer — an open-source discovery layer. But we want to hear from the community before we go further.

**A few questions to start:**

1. **How do you currently discover AI agents?** Do you search GitHub, follow specific projects, rely on word of mouth?

2. **What metadata matters most?** When evaluating an agent, what do you need to know? Capabilities? Uptime? Publisher identity? Security?

3. **What trust signals would you require?** Before connecting your system to an unknown agent, what would you need to verify?

4. **Would you use a neutral discovery layer?** Or do you prefer platform-specific registries (Copilot Studio, Vertex AI, Bedrock)?

5. **What's missing from the current ecosystem?** What would make you excited about agent discovery?

No wrong answers. We're here to learn.

---

## LinkedIn Post

**Headline:** We built an open-source discovery layer for AI agents. Here's why.

**Body:**

The A2A protocol (25k+ GitHub stars, backed by Google, Microsoft, IBM) defines how AI agents communicate. But it doesn't define how they find each other.

That's the gap A2A Hub fills.

A2A Hub is an open-source discovery layer that crawls A2A Agent Cards, validates and normalizes them, and exposes search through API and web UI.

**Why open-source?** Because agent discovery shouldn't be owned by any single platform. The agent ecosystem needs a neutral layer — like DNS for the web, but for AI agents.

**Current state:** v0.1.0 MVP. Python, FastAPI, SQLite. Single process. Zero infrastructure. Apache 2.0.

**Roadmap:** Discovery → Trust → Federation → Universal Agent Control Plane

**We're looking for feedback from developers building AI agents.** What trust signals matter to you? How do you currently discover agents? What's missing?

GitHub: github.com/hashgenglobal-dotcom/a2a-hub

#AI #A2A #OpenSource #AgenticAI #Infrastructure

---

## X/Twitter Post

A2A Hub v0.1.0 is live.

The A2A protocol defines how agents communicate. We built the missing piece: how they find each other.

Open-source discovery layer for AI agents. Python, FastAPI, SQLite. Apache 2.0.

github.com/hashgenglobal-dotcom/a2a-hub

#A2A #AI #OpenSource

---

## Hacker News — Show HN

**Title:** Show HN: A2A Hub – Open-source discovery layer for AI agents

**Body:**

The A2A protocol (25k+ stars, backed by Google/Microsoft/IBM) defines how AI agents communicate via Agent Cards at `/.well-known/agent.json`. But it doesn't define how agents find each other.

A2A Hub fills that gap. It's an open-source discovery layer that:

1. Crawls A2A Agent Cards from seed URLs
2. Validates and normalizes them into a canonical Resource model
3. Exposes keyword search via API and web UI

**Stack:** Python, FastAPI, SQLite, aiohttp, pydantic. Single process. No Postgres, no Redis, no background workers.

**Why open-source?** Agent discovery shouldn't be owned by any single platform. The ecosystem needs a neutral layer.

**Current state:** v0.1.0 MVP. 46 tests passing. Docker image available. Apache 2.0.

**Roadmap:** Discovery → Trust → Federation → Universal Agent Control Plane

**We're looking for:**
- Feedback from developers building A2A agents
- Reports of what's missing or broken
- Contributors interested in the trust/verification layer

GitHub: github.com/hashgenglobal-dotcom/a2a-hub

---

## Reddit — r/MachineLearning

**Title:** [P] A2A Hub — Open-source discovery layer for A2A AI agents

**Body:**

The A2A protocol defines how agents communicate, but not how they find each other. I built an open-source discovery layer that crawls Agent Cards, validates them, and exposes search via API and web UI.

**Stack:** Python, FastAPI, SQLite. Single process. Apache 2.0.

**Looking for feedback from anyone building AI agents.** What trust signals would you need before connecting to an unknown agent?

GitHub: github.com/hashgenglobal-dotcom/a2a-hub

---

## Reddit — r/LocalLLaMA

**Title:** A2A Hub — Open-source agent discovery (for the agentic AI era)

**Body:**

With the rise of agentic AI, we're going to see thousands of independent agents — exactly like websites. But there's no Google for agents yet.

A2A Hub is an open-source discovery layer for A2A-compatible AI agents. It crawls Agent Cards, validates them, and makes them searchable.

**Stack:** Python, FastAPI, SQLite. Single process. Apache 2.0.

GitHub: github.com/hashgenglobal-dotcom/a2a-hub

---

## Outreach Template

**Subject:** A2A Hub — would your agent like to be discoverable?

**Body:**

Hi [Name],

I'm reaching out because I saw [project name] — it's doing interesting work with AI agents.

I'm building A2A Hub, an open-source discovery layer for A2A-compatible agents. It crawls Agent Cards, validates them, and makes them searchable via API and web UI.

I'd love to add [project name]'s agent to the index. If you have an Agent Card at `/.well-known/agent.json`, I can add it as a seed URL. If not, I'm happy to help set one up.

No promotion needed. Just want to make your agent discoverable.

GitHub: github.com/hashgenglobal-dotcom/a2a-hub

Thanks,
[Name]
