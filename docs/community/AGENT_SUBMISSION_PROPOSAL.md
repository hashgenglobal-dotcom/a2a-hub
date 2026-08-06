# Agent Submission Proposal

**Status:** Proposal — not implemented
**Phase:** Post-MVP (Phase 2 candidate)

---

## Problem

Currently, A2A Hub discovers agents through configured seed URLs. This works for known agents but does not scale. Agent owners have no way to submit their agent for indexing.

## Proposed Flow

```
Agent owner submits:
  - Agent Card URL
  - Name
  - Description
  - Capabilities
  - Documentation URL
        │
        ▼
Validation:
  - Is the URL reachable?
  - Does it return a valid Agent Card?
  - Is the card already indexed?
        │
        ▼
Queue for crawl → Indexed → Listed in search results
```

## Endpoint

```
POST /api/v1/submit
{
  "card_url": "https://example.com/.well-known/agent.json",
  "contact_email": "owner@example.com"  // optional, for notifications
}
```

## Requirements

- Rate limiting (prevent abuse)
- CAPTCHA or proof-of-work (prevent automated spam)
- Email verification (optional, for ownership claims)
- Re-submission window (prevent rapid re-submissions)

## Not in This Proposal

- Authentication (Phase 2+)
- OAuth broker (Phase 3)
- Reputation system (Phase 3)
- Paid listings (never — open-source core)

## Open Questions

1. Should submissions be public or require review?
2. Should there be a submission API or only a web form?
3. How do we handle malicious submissions?
4. Should submissions be immediately indexed or queued for review?
