# Security

## Reporting Vulnerabilities

This project is in early MVP stage. If you discover a security issue, please open a GitHub issue with the label `security`.

## Scope

The MVP has no authentication, no rate limiting, and no user data. Security concerns are primarily:
- Malicious Agent Cards (mitigated by schema validation)
- Crawler behavior (respects standard HTTP semantics)
- Dependency vulnerabilities (monitored via standard tooling)
