# First Contributors Guide

Thank you for your interest in A2A Hub. This is an open-source infrastructure project, and contributions of all kinds are welcome.

---

## Ways to Contribute

### Engineering

| Area | Description | Good First Issue |
|------|-------------|-----------------|
| Agent adapters | Add support for new agent protocols (MCP, etc.) | Medium |
| Validation | Improve A2A schema validation coverage | Good first issue |
| Crawling | Add HTTP retry, concurrency, robots.txt | Medium |
| Search | Improve keyword search relevance | Good first issue |
| UI | Enhance the Jinja2 templates | Good first issue |
| Tests | Add test coverage for edge cases | Good first issue |

### Documentation

| Area | Description |
|------|-------------|
| Tutorials | Write "How to add your agent" guides |
| Examples | Add real Agent Card examples |
| API docs | Improve endpoint documentation |
| Architecture | Clarify design decisions |

### Research

| Area | Description |
|------|-------------|
| Trust model | What signals make agents trustworthy? |
| Discovery | How should agents find each other? |
| Federation | How should registries interoperate? |

### Community

| Area | Description |
|------|-------------|
| Submit agents | Point us to your Agent Card URL |
| Provide feedback | What's missing? What's broken? |
| Spread the word | Share with other agent builders |

---

## Getting Started

1. Read `docs/implementation/BUILD_SPEC.md` — the implementation contract
2. Read `docs/architecture/ARCHITECTURE_MVP.md` — understand the design
3. Check the issues labeled `good first issue`
4. Open a discussion if you have questions

## Pull Request Process

1. Open an issue first to discuss the change
2. Ensure tests pass: `pytest`
3. Update documentation if you change behavior
4. Keep PRs focused on one concern

## MVP Constraint

The MVP is frozen to 7 capabilities. If your PR adds a feature outside that scope, it will be deferred to Phase 2. See `BUILD_SPEC.md` for the exact scope.
