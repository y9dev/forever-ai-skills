# Execution modes

Pick one mode in Step 0 and record it. Mode changes what is produced and how many agents run, never whether the quality gates exist.

## Stage matrix

`F` = full, `L` = lightweight (inline by orchestrator, short doc), `-` = skipped.

| Stage | Standard | Hackathon | Maintenance |
|-------|----------|-----------|-------------|
| 0 Discovery | F | L (30 min max) | F, plus baseline tests, mandatory |
| 1 Product | F, interview up to 5 rounds | L, up to 2 rounds, read assignment and judging criteria first | L, only the change being made; reproduce the bug |
| 2 Architecture | F + independent review | L, one `ARCHITECTURE.md` (stack, modules, tables, endpoints) + light review | only if the change touches structure; ADR for any deviation |
| 3 UX/IA | F | L, journeys + screen list + state matrix | only affected screens |
| 4 Design system | F | L, tokens + 6 components (button, input, table, card, dialog, toast) | reuse existing; extend minimally |
| 5 Plan | F | L, vertical slices ordered by demo value | task list for the change |
| 6 Implementation | F | F | F, smallest diff that solves it |
| 7 Review | each milestone | once at about 60% and once before freeze | once on the final diff |
| 8 QA | L1-L4 | L1, L2 on core logic, L3 on every critical journey, L4 once | before/after runs of relevant tests, plus regression E2E for the touched journey |
| 9 UX/UI audit | 3 auditors | 2 auditors (usability + merged ui/a11y) | 1 auditor on touched screens, if UI changed |
| 10 Perf/Security | F | security reviewer + auth/authorization/secrets/injection focus; perf only if visibly slow | security reviewer if the change touches auth, input, data access |
| 11 Gate | threshold 3.8 | threshold 3.3 | threshold 3.5, plus "no regressions vs baseline" |

Blockers (see `quality-evaluation.md`) apply identically in every mode.

## Documentation profiles

- **Standard:** all docs named in SKILL.md stages.
- **Hackathon:** `docs/PRD.md` (contains personas, journeys, acceptance criteria as sections), `docs/ARCHITECTURE.md` (contains data model, API contract, decisions as short ADR bullets), `docs/UX_SPECIFICATION.md` (contains IA and design tokens), `docs/QUALITY_SCORECARD.md`, `docs/WORKFLOW_STATE.md`. No separate ADR files unless a decision is contested.
- **Maintenance:** `docs/WORKFLOW_STATE.md` (includes baseline), a short change note in `docs/changes/<date>-<slug>.md` (problem, root cause or requirement, change, evidence), updates to any existing doc the change invalidates.

## Document sizing

Standard: each doc is short and decision-focused, about 300 to 500 words unless the content is a table or contract (API, data model). No filler sections; delete template sections that do not apply. Maintenance: for a change touching fewer than 5 files, record problem, change and evidence only in the change note and `docs/WORKFLOW_STATE.md`; create no other new docs. Hackathon: use the merged profile above.

## Hackathon timeboxes

Ask for the deadline once. Compute the budget from the absolute end time and record the planned clock times in the state file. Proportions of total time:

| Phase | Share |
|-------|-------|
| Stages 0-2 (assignment, MVP definition, minimal architecture) | 12% |
| Stages 3-5 (journeys, tokens, slice plan) | 8% |
| Stage 6 implementation | 45% |
| Stages 7-8 review and testing, stabilization | 15% |
| Stage 9-10 UX/UI audit, security pass, fixes | 10% |
| Deployment, demo data, pitch/README | 10% |

Rules:
1. **Walking skeleton first** (app boots, DB migrates, one round trip) within the first 25% of the time.
2. **Feature freeze at 75% of the time.** After freeze only fixes, tests, polish.
3. **Scope-cut ladder** when behind schedule: (1) drop nice-to-have screens, (2) simplify filters/sorting to one default, (3) replace custom UI with existing component, (4) hard-code seed data for non-core entities. Never cut: authentication if required by the assignment, the primary journey, the E2E test for the primary journey, the UX check, the security basics (no secrets in the repo, validation, authorization checks).
4. Fewer stops: present the requirements summary, MVP scope and the minimal architecture to the user in a single approval message (the Stage 1 and Stage 2 gates merge). The independent architecture review runs before that message so its outcome is included.
5. Report each scope cut to the user with a one-line reason; the user approves cuts that change the MVP definition.
6. Max 2 parallel implementation agents; each owns a vertical slice or a layer with a frozen API contract.
7. Keep a runnable, demoable build on the main branch at all times after the walking skeleton. Commit working states.
8. Deployment: use the target named in the assignment. Verify the deployed URL with the primary journey, not just a 200 on `/`.

## Maintenance mode flow

1. Reproduce or define the change precisely (failing test or exact steps).
2. Run the relevant existing tests and record the baseline.
3. Locate the root cause or insertion point; read neighbors for conventions.
4. Make the smallest coherent change. No drive-by refactors; list them as follow-ups instead.
5. Add or update a test that fails before and passes after.
6. Re-run the baseline set; any new failure is a regression and blocks.
7. Independent review of the diff (code-reviewer). Audit the UI only if UI changed.
8. Write the change note with evidence.
