# Security and performance checklist (Stage 10; reused in Stages 2, 6, 7)

Prioritize real, exploitable risk over theory. Each finding: severity, location, exploit scenario, fix. Severity: **Critical** = unauthenticated or cross-tenant data access, RCE, auth bypass, committed live secret; **High** = authenticated privilege escalation, injection, sensitive data exposure; **Medium** = missing hardening with limited exploitability; **Low** = defense in depth.

## Security (check by reading code AND probing the running app where possible)
**Authentication**
- Passwords hashed (argon2id/bcrypt), never logged; login errors do not reveal which field was wrong; lockout or rate limit on login; session cookie `HttpOnly`, `Secure` in prod, `SameSite`; session/JWT expiry and logout invalidation; JWT secret from env, algorithm pinned.
**Authorization**
- Every endpoint has an explicit auth requirement. Role checks server-side, not only hidden buttons. Object-level checks: user A cannot read/update/delete user B's record by changing an ID (IDOR). Test each role against each endpoint.
**Input and injection**
- SQL only via parameters (`$1`), no string concatenation, including `ORDER BY`/column names (allowlist them). Request body size limits; validation of types, lengths, enums on the server. No `dangerouslySetInnerHTML` with user data; output encoding; no `eval`/shell with user input; path traversal on file names.
**CSRF/CORS**
- Cookie auth: CSRF protection (SameSite + token or custom header). CORS allowlist, not `*` with credentials.
**Secrets and config**
- No secrets in the repo or git history, `.env` ignored, `.env.example` has placeholders, frontend bundle contains no private keys, debug mode off in prod.
**Files**
- Upload type/size limits, random server-side names, not served from an executable path, content-type checks.
**Errors and leakage**
- No stack traces or SQL errors in responses; consistent error envelope; logs without PII/passwords/tokens; user enumeration avoided.
**Rate limiting and abuse**
- Login, signup, password reset, expensive search/export endpoints limited.
**Transport and headers**
- HTTPS in prod; security headers (`X-Content-Type-Options`, `Content-Security-Policy` where feasible, `Referrer-Policy`).
**Dependencies**
- `govulncheck`, `npm audit` results triaged: reachable vulnerabilities in prod deps are High.
**Go specifics**
- Goroutine/data races (`-race`), unchecked errors, `http.Server` timeouts set, `context` cancellation passed to DB calls, `defer rows.Close()`, transaction rollback on error.
**React specifics**
- Tokens not in localStorage if avoidable; route guards are UX only, server enforces; sanitized rendering of user content.

Probing rules: only against the local or user-provided test instance; never against third-party systems; never run destructive tests on data you did not seed. If probing is not possible, mark items `CODE-REVIEW ONLY`.

## Reliability
Graceful handling of DB down/timeouts; idempotent or guarded double-submit; migrations re-runnable and ordered; health endpoint; startup fails fast on bad config; graceful shutdown; backup/restore note for deployment.

## Performance (measure first)
- Frontend: production build size (`vite build` output; flag any single chunk over about 500 kB gzip-uncompressed warning), route-level code splitting if large, unnecessary re-renders only if the profiler/UX shows lag, image sizes.
- Backend/DB: list endpoints paginated with a maximum page size; N+1 detection (count queries per request in logs for list pages); indexes for filter/sort columns shown by `EXPLAIN` on realistic data (seed 10k to 100k rows if the workload justifies); response time of primary journey endpoints (p95 under 300 ms locally for typical reads is a reasonable target unless the PRD says otherwise).
- Network: request waterfalls, duplicate fetches, missing caching headers for static assets.
Do not optimize without a measurement showing a user-visible or requirement-relevant problem. Record measurement method and numbers.

## Output
Findings in the standard format plus a coverage table: each checklist group with `checked (how)`, `code-review only`, or `NOT RUN`.
