# Product discovery protocol (Stage 1)

## Before asking anything
Harvest answers from: arguments, repo (README, docs, code, tests, seed data), assignment text, earlier replies. Fill the ledger first. Ask only about what remains.

## Requirements ledger

Maintain one table; each row has a status:
`Confirmed` (user said it or the repo proves it) | `Assumption` (your default, shown to the user) | `Unknown` | `Risk`.

Dimensions (critical ones marked *): purpose*, target audience*, personas*, business objectives, primary journeys*, functional requirements*, non-functional requirements, business rules*, roles and permissions*, constraints (deadline, stack, hosting, budget)*, integrations, expected workload, edge cases, definition of success*.

## Interview procedure (built-in)

1. Group open dimensions into rounds: (A) purpose, audience, success; (B) journeys and features; (C) rules, roles, data; (D) constraints, integrations, workload, edge cases.
2. One round at a time, at most 3 to 4 questions per round, via AskUserQuestion when available (2 to 4 concrete options each, your recommended option first, user can always type a custom answer). Ask in the user's language.
3. Questions must be answerable and decision-relevant. Prefer "Which of these?" over "Tell me about...". Do not ask for what you can assume safely; list the assumption instead.
4. After each round update the ledger. Compute remaining critical `Unknown`s.
5. **Stop** when no critical dimension is `Unknown` or when the round limit is reached (standard 5, hackathon 2, maintenance 1). Remaining unknowns become explicit assumptions or risks.
6. Present the **requirements summary** (max about 40 lines): purpose, users, MVP scope (in), non-goals (out), top journeys, key rules and roles, constraints, definition of success, then the ledger sections Assumptions / Unknowns / Risks. Ask the user to confirm and to decide the important open items. Record the decision in the ledger.

Question bank by dimension (pick, do not dump):
- Purpose: what problem, for whom, what happens today without this product?
- Audience: who uses it daily vs rarely; technical level; devices; language/locale.
- Journeys: the 3 things a user must be able to do on day one; what is the most frequent task?
- Rules: states and transitions of main entities; who can change what; validation limits; uniqueness; deletion vs archive.
- Roles: list roles; per role, what they can see/create/edit/delete; how users get accounts.
- Data: volume now and in 12 months; import/export; retention; personal data.
- Integrations: auth provider, email, payments, files, external APIs; credentials availability.
- Constraints: deadline, hosting, mandatory stack, browser support, accessibility requirements, offline.
- Success: how will we know it works (judges' criteria, KPIs, demo script)?
- Edge cases: empty data, concurrent edits, duplicate submissions, partial failures, large inputs.

Hackathon addition: read the assignment text and judging criteria; derive the MVP as "smallest set of journeys that satisfies every mandatory criterion"; list stretch items separately.

## Personas
Use 1 to 3 personas. Each: name and role, goals, frequent tasks, pain points, environment (device, expertise), success measure. Base them on stated audience, not invention; mark invented details as assumptions.

## Outputs
Fill `templates/prd.md`, `templates/user-journey.md`, `templates/acceptance-criteria.md`; personas go to `docs/USER_PERSONAS.md`. Acceptance criteria are numbered (AC-001...) in Given/When/Then form, each testable, each traced to a requirement ID (FR-xxx / NFR-xxx). Mark each AC `critical` if its failure breaks a primary journey.
