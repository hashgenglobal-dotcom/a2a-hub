# Trust Layer Research

**Status:** Research — not implemented
**Phase:** Phase 2 candidate

---

## Research Questions

### 1. What makes developers trust an unknown agent?

Based on analogous systems (npm, PyPI, Docker Hub, mobile app stores):

| Signal | Source | Verifiability |
|--------|--------|---------------|
| Publisher identity | Domain ownership, org verification | High |
| Uptime history | Continuous health checks | High |
| Metadata completeness | Schema compliance | High |
| Version history | Changelog, semver | Medium |
| Security info | Auth schemes, encryption | Medium |
| Community feedback | Stars, reviews, usage | Low (gaming risk) |
| Code transparency | Open-source? | Medium |
| Task completion rate | End-to-end success | Low (requires integration) |

### 2. What evidence can be objectively measured?

| Metric | How | Reliability |
|--------|-----|-------------|
| Endpoint availability | HTTP health checks | High |
| Response time | Latency measurement | High |
| Schema compliance | A2A schema validation | High |
| Domain age | WHOIS data | Medium |
| HTTPS enforcement | TLS check | High |
| Card signature | Cryptographic verification | High |
| Update frequency | Git history, card changes | Medium |

### 3. What signals should never become hidden rankings?

- **Paid placement** — Never. Discovery is free.
- **Unverifiable reviews** — No "5-star" system without proof of usage.
- **Proprietary scoring** — Trust scores must be explainable and auditable.
- **Vendor preference** — No preferential treatment for partners.

---

## Proposed Trust Dimensions

| Dimension | Metrics | Phase |
|-----------|---------|-------|
| **Identity** | Domain ownership, signed card, org verification | Phase 2 |
| **Security** | HTTPS, OAuth, encryption, supported auth | Phase 2 |
| **Reliability** | Uptime, response time, SLA adherence | Phase 2 |
| **Compatibility** | A2A version, MCP support, OpenAPI, streaming | Phase 2 |
| **Community** | Stars, reviews, usage, dependents | Phase 3 |

---

## Guiding Principles

1. **Trust is earned, not claimed.** Every signal must be measurable.
2. **Transparency by default.** All trust signals are public and auditable.
3. **No black-box scoring.** Every trust score must be explainable.
4. **Open data.** The trust dataset is open-source, not proprietary.
5. **User choice.** Developers choose which signals matter to them.
