# Testing strategy (Stages 6, 8, 9)

Use the project's existing tools first. Detect from manifests; do not install new tooling unless a gap is blocking and the user agrees to the dependency. Record every command and its outcome in `docs/evidence/qa-run-<n>.md` (command, exit code, summary). Anything not run is `NOT RUN: reason`.

## Level 1: static
| Check | Go | TypeScript/React |
|-------|----|------------------|
| Format | `gofmt -l .` (must print nothing) | `prettier --check` if configured |
| Lint | `go vet ./...`, `golangci-lint run` or `staticcheck ./...` if installed | `eslint .` if configured |
| Types | compiler | `tsc --noEmit` |
| Dependencies | `govulncheck ./...` if installed, else `go list -m -u all` | `npm audit --omit=dev` (or pnpm/yarn equivalent) |
| Secrets | `gitleaks detect` if installed; else grep for `AKIA`, `-----BEGIN`, `password\s*=`, `secret`, `token`, `.env` committed | same |
Level 1 is the entry gate: format/type/lint failures are fixed before Level 2 counts.

## Level 2: functional
- Unit tests for business rules and validation (table-driven in Go: `go test ./... -race -count=1`; Vitest/Jest for TS).
- Integration tests for repositories against a real PostgreSQL (docker compose service or testcontainers), including migrations up from empty, constraint violations, transaction rollbacks.
- API contract tests: for each endpoint in `API_CONTRACTS.md` test success, validation error (400/422), unauthenticated (401), forbidden (403), not found (404), and response shape and error envelope. Use `httptest` in Go.
- Frontend component tests for forms and tables with state variants (loading/empty/error) where logic exists.

## Level 3: E2E
Playwright preferred (`@playwright/test`), tests committed to the repo (`e2e/` or the existing folder), runnable with one command documented in the README. Cover: each critical journey end to end against a seeded database; login/logout and session expiry; authorization (each role sees and can do only its permitted things; direct URL to forbidden page); form submit success and each validation error; list filtering, sorting, pagination; server error and network failure (`page.route` to simulate 500/offline); double-submit; refresh mid-flow. Tests use roles/labels as locators (`getByRole`, `getByLabel`), not CSS paths. No sleeps; use auto-waiting assertions. Each test independent, with data created by API/seed.

## Level 4: browser UX verification
Purpose: look at the real UI. Not the same as E2E.
**Browser access ladder** (use the first available, record which):
1. Playwright MCP tools in your tool set.
2. Built-in browser pane tools (navigate, screenshot, read page, console, network).
3. Claude-in-Chrome tools.
4. Playwright scripts run via Bash (screenshots with `page.screenshot`, console via `page.on('console')`, network via `page.on('response')`, a11y via `@axe-core/playwright` if installed). Installing browsers/packages requires user consent.
5. None available: Level 4 is `NOT RUN`. Say so in the report, score UX with a confidence note, and ask the user to do a manual pass using the checklist below. Never fabricate visual findings from source code alone. You may still run a static pass over components (CSS-token contrast ratios, ARIA attributes and labels, semantic elements, loading/empty/error/disabled handling) and cite file:line; label those results `STATIC-CHECKED`, never `VERIFIED`, and they do not lift the Level 4 `NOT RUN` status or the category cap.

Checklist: every journey click-through; each screen at 360/768/1280 px; empty, loading (throttle), error states; keyboard-only pass of the primary journey; focus visibility; console errors and warnings (must be none unexpected); failed network requests; color contrast spot checks; zoom 200%. Screenshots go to `docs/evidence/screens/` with names `<journey>-<step>-<viewport>.png`.

## Test-writing rules
Tests written alongside the code by the implementer, but Level 3 journey tests and the contract tests are reviewed by qa-engineer. A test that cannot fail is worthless: for bug fixes show it failing before the fix. Never delete or weaken a test to get green; never `skip` without a tracked reason. Flaky test: find the cause, do not retry-loop it.

## Hackathon profile
L1 once per slice (fast commands only), L2 on rules and auth, L3 for each critical journey (at least 1 test per journey), L4 once before freeze and once before the demo. Seed script producing demo data is part of testing and the demo.

## Pass criteria (measurable)
L1: zero errors from format, types, lint. L2: all tests pass, race detector clean. L3: all critical journey tests pass 3 consecutive runs. L4: zero Critical/High findings, zero unexpected console errors on journeys.
