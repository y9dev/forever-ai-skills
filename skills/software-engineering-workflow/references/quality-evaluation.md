# Quality evaluation (Stage 11)

Done by a fresh qa-engineer in CERTIFY mode. The implementer and orchestrator supply evidence paths but do not score.

## Distinguish these dimensions in the report
Product completeness (are all MVP requirements and journeys present), functional correctness, UX quality, visual quality, architecture quality, security, reliability, performance. Completeness and correctness are separate: a missing feature is incompleteness, a wrong behavior is incorrectness.

## Scoring model

| Category | Weight |
|----------|--------|
| Functional correctness (including completeness of MVP) | 25% |
| UX / Usability | 25% |
| Architecture / Maintainability | 20% |
| UI / Visual quality | 15% |
| Security / Reliability | 15% |

Score each 0 to 5 (halves allowed). `Weighted = sum(score/5 x weight) x 5`, giving a result on the same 0 to 5 scale. Thresholds: standard 3.8, hackathon 3.3, maintenance 3.5 (plus no regression against baseline). Every category score needs at least two evidence references.

## Anchors (use these, do not improvise)
**Functional:** 5 all ACs pass, critical journeys E2E green 3 runs, edge cases tested. 4 all critical ACs pass, minor ACs missing or untested. 3 critical journeys work, some important ACs fail. 2 a critical journey partly broken. 1 app starts but core flow fails. 0 does not run.
**UX:** 5 audits show no High, at most a few Low, journeys short and clear, all four states exist. 4 no High, some Medium friction. 3 completable journeys with several Medium or one High. 2 multiple High. 1 Critical unresolved. 0 unusable.
**Architecture:** 5 matches docs, clear boundaries, tests on core rules, no High review findings. 4 minor drift. 3 workable but duplication or leaky layers. 2 hard to change. 1 big tangles. 0 no structure.
**UI:** 5 consistent tokens, aligned, responsive at 3 widths, contrast passes. 4 small inconsistencies. 3 visible inconsistencies or one broken viewport. 2 many defects. 1 broken layouts. 0 unreadable.
**Security/Reliability:** 5 checklist covered with no open findings, validation and authz tested, graceful failures. 4 only Low open. 3 Medium open. 2 High open. 1 Critical open. 0 secrets leaked or no auth where needed.
If a level was `NOT RUN` (for example no browser), the related category is capped at 3 and the cap is stated.

## Blockers (any one means FAIL regardless of score)
1. Any critical functional test failing (critical AC, critical journey E2E, contract test for a critical endpoint).
2. Any critical user journey broken, shown by a failed E2E test or a manual run recorded with steps.
3. Any unresolved Critical UX finding.
4. Any unresolved Critical security vulnerability (High security findings also block unless the user explicitly accepted the risk in writing in chat; record the quote).
5. The application cannot be started or deployed as required (the run command from the README fails from a clean checkout, or the deployed target fails the primary journey).
6. Maintenance mode: any regression versus the recorded baseline.
7. A required quality-gate stage was skipped without user approval (for example Stage 9 with a UI).

## Certification procedure
1. Read PRD, ACs, state file, evidence index. 2. From a clean state, run the documented start command and the test suites; record outputs. 3. Re-run primary journeys by hand or via browser tools. 4. Check each blocker explicitly (yes/no with evidence). 5. Score categories with anchors. 6. Compute weighted score. 7. Verdict: `PASS` (no blockers and score at least threshold), `PASS WITH CONDITIONS` (no blockers, score at least threshold, High/Medium issues deferred with user acceptance), `FAIL`. 8. List remaining limitations and `NOT RUN` checks.
If the Agent tool is unavailable and certification runs inline, set `Independence: REDUCED` on the scorecard and say so in the report.

## Evidence
Acceptable: command + exit code + output excerpt; test file and test name; screenshot path; file:line; audit report ID. Not acceptable: "looks fine", "should work", the implementer's summary.

Evidence strength, strongest first: (1) E2E or integration run with exit code 0 and log excerpt; (2) unit test run log; (3) build, type-check or linter output; (4) static audit with file:line citations (`STATIC-CHECKED`). Claims about behavior need level 1 or 2 evidence to be `VERIFIED`; levels 3 and 4 alone support only claims about compilation or code structure. Any claim with no cited output or file:line is `UNVERIFIED`. In scorecards, a category scored 4 or 5 needs at least one level 1 or 2 reference.
