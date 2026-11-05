# Architecture methodology (Stages 2 and 7)

## Principles
- Simplest design that satisfies actual requirements. Start as a **modular monolith**: one backend service, one database, one frontend build.
- Every added component (queue, cache, second service, ORM, state library) needs a written justification tied to a requirement or a measured problem. No justification: do not add.
- Respect the existing stack and conventions in maintenance mode; deviations need an ADR.
- Optimize for change: clear module boundaries, dependencies point inward (handlers -> services -> repositories), no business logic in handlers or components.

## Default stack when the user has no preference (record as an assumption)
- Backend: Go, standard `net/http` with a small router (or the project's existing one), `database/sql` with `pgx`, plain SQL migrations (e.g. golang-migrate or goose), structured logging via `log/slog`, config from env.
- Frontend: React + TypeScript + Vite, a data-fetching layer (TanStack Query or plain fetch hooks), a router, form validation (zod or similar), no global state library until needed.
- DB: PostgreSQL. REST + JSON. OpenAPI-style contract in `docs/API_CONTRACTS.md`.
- Auth: for MVP, session cookie (HttpOnly, SameSite=Lax) or JWT in HttpOnly cookie; password hashing with argon2id or bcrypt; role checks in a single middleware plus per-resource checks.
- Run: `docker compose` with db + app for local; single env example file.

## Evaluation checklist (answer each in `ARCHITECTURE.md`, one line)
Separation of concerns; modularity; coupling and cohesion; data model and constraints; API contracts; authn/authz; error handling; security boundaries; performance hotspots; deployment complexity; maintainability; scalability needed vs speculative.

## Document contents
- `ARCHITECTURE.md`: context (what and who), stack with reasons, module map and responsibilities, request flow for the primary journey, auth model, error model, config and deployment, testing approach, risks, out-of-scope scaling.
- `DATA_MODEL.md`: entities, columns with types, PK/FK, NOT NULL, UNIQUE, CHECK, indexes with the query each serves, enum/status transitions, soft vs hard delete, migration strategy, seed data.
- `API_CONTRACTS.md`: per endpoint method + path, auth/role, request schema with validation limits, response schema, error codes (one error envelope for all: `{ "error": { "code", "message", "fields" } }`), pagination, filtering, sorting conventions, idempotency where needed. The contract is the source of truth for frontend and backend; changes go through the orchestrator.
- `docs/adr/NNNN-title.md` from `templates/adr.md`: only for decisions that are costly to reverse or contested (stack, auth approach, data ownership, deployment).

## Pre-implementation review (independent)
Give the reviewer the PRD, acceptance criteria and architecture docs only. It must: challenge assumptions, flag unneeded complexity, propose at least one simpler alternative for each major component, check requirements coverage (every AC maps to a module and endpoint), check data model constraints, and check security boundaries. Findings in the standard format. You resolve Critical items before Stage 5.

## Stage 7 review focus
Coupling and layering violations; duplicated logic; leaky abstractions; premature abstractions; data-model drift from `DATA_MODEL.md`; API drift from `API_CONTRACTS.md`; transaction boundaries; error propagation; maintainability risks (god files, missing tests on core rules).
