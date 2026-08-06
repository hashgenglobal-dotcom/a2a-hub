# Contributing

We welcome contributions. This is an open-source infrastructure project.

## Getting Started

1. Read `docs/implementation/MVP_SPEC.md` — it is the implementation contract.
2. Read `docs/architecture/ARCHITECTURE_MVP.md` — understand the single-process design.
3. Read the relevant ADRs in `docs/adr/` — understand why decisions were made.

## Pull Request Process

1. Open an issue first to discuss the change.
2. Ensure tests pass: `pytest`
3. Update documentation if you change behavior.
4. Keep PRs focused on one concern.

## Code Style

- Follow PEP 8.
- Use type hints everywhere.
- Write docstrings for public APIs.
- Keep functions small and testable.

## MVP Constraint

The MVP is frozen to 7 capabilities. If your PR adds a feature outside that scope, it will be deferred to Phase 2. See `docs/implementation/MVP_SPEC.md` for the exact scope.
