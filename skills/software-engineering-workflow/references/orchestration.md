# Orchestration guide

## Roles and how they run

Role files live in `agents/`. A Markdown file in a skill folder does NOT register a subagent by itself. Two supported ways to run a role:

1. **Default (works with no installation):** call the Agent tool with `subagent_type: "general-purpose"`. The prompt = the role file's body (everything after the frontmatter, read with the Read tool) + the task brief below.
2. **Optional installed subagents:** `python scripts/install_agents.py` copies the roles to `~/.claude/agents/` as `sew-<role>` (e.g. `sew-code-reviewer`) with tool restrictions (reviewers cannot edit). After install, use `subagent_type: "sew-code-reviewer"`. Newly added agents need a session restart or agent reload to appear. Check your Agent tool's list of available types before choosing; fall back to option 1 if a type is absent.

Read-only roles (architecture-reviewer, code-reviewer, security-reviewer, usability-auditor, ui-critic, accessibility-reviewer) must not edit project files. With option 1 this is enforced only by instruction, so after every review run `git status` (or compare file listing) and revert and flag any file they changed. Reviewers may write their report only if the brief names an output path; otherwise they return it as text and you save it.

Hackathon audit: spawn two agents. One gets `usability-auditor.md`; the other gets the bodies of `ui-critic.md` and `accessibility-reviewer.md` together and returns two separate finding lists.

Role map: Database Engineer = `backend-engineer` with migration scope. Integration Engineer = the orchestrator. Product analyst, architect and ux-designer may be done inline by the orchestrator in hackathon/maintenance mode.

## Task brief template

```
ROLE: <role file name>
GOAL: <one sentence outcome>
INPUTS: <doc paths and files to read first>
YOU OWN (may edit): <exact files/dirs>     DO NOT TOUCH: <everything else>
ACCEPTANCE: <checkable criteria from docs/ACCEPTANCE_CRITERIA.md ids>
REQUIRED TESTS: <what to write/run>
CONTEXT: stack, run/test commands, conventions (from docs/WORKFLOW_STATE.md)
REPORT: use the structured report format below. Include command output excerpts as evidence.
```
Give reviewers the spec, the diff range and the running URL. Do NOT give them the implementer's summary or your opinion; that destroys independence.

## Structured report format (every subagent must follow)

```
STATUS: done | partial | blocked
SUMMARY: <3 lines>
CHANGES: <files created/modified, one line each>      (implementers)
EVIDENCE: <command -> result, test names, screenshot paths>
FINDINGS: (reviewers/auditors) table of:
  ID | Severity (Critical/High/Medium/Low) | Location | Description | Reproduction | Impact | Recommended fix | Verification method
NOT VERIFIED: <what could not be checked and why>
OPEN QUESTIONS: <decisions needing the orchestrator or user>
```

## Verifying a report (never trust "done")

1. Inspect actual changes: `git diff --stat` / `git status`, and read the key files.
2. Re-run the task's tests and the build yourself. Compare with the claimed output.
3. Start the app and exercise the slice if it has a UI or API.
4. Missing or vague evidence: send back once with the specific gap. Second failure: do it yourself or reduce scope.

## Parallelism rules

Parallel only if ALL hold: file sets are disjoint; neither task needs the other's output; the shared contract (API schema, DB schema, tokens) is already frozen in docs. Typical safe pairs: backend slice A + frontend slice B on a frozen contract; review agents on a fixed diff; the three Stage 9 auditors.
Never parallel: two edits to the same file, migrations from two agents, tasks sharing a lockfile or generated code.
Contract lockdown: before spawning parallel implementers, freeze the shared signatures in docs or code (TypeScript interfaces, Go structs, OpenAPI/Protobuf, DB schema). An agent whose dependency is still being built codes against mocks or stubs generated from that contract, and replaces them only after the dependency is merged.
Merge checklist: after parallel work completes, the orchestrator itself merges, then builds, runs lint/type-check and the tests of every touched slice, and only then starts QA. A failed integration build goes back to the owning engineer, not to QA.
Concurrency cap: 3 agents (hackathon 2).
Isolation: in a git repository, pass `isolation: "worktree"` on the Agent call for implementers that run in parallel if your Agent tool supports that parameter; you then merge their branches yourself and re-run tests after each merge. If the parameter is unsupported or there is no git repo, run implementers sequentially or on strictly disjoint directories.
Parallel calls are made in a single message with multiple Agent tool calls.

## Findings triage

Save to `docs/reviews/<stage>-<n>.md`. Every finding gets a decision: `fix` (assign an engineer other than the reviewer), `defer` (reason, tracked in the final report limitations), `reject` (reason). Critical and High cannot be deferred without explicit user acceptance. After fixes to Critical/High, re-run that reviewer on the fix, scoped to the changed lines and their direct callers. A rejected Critical/High needs a rebuttal with evidence confirmed by a fresh reviewer (see "Loop control" in SKILL.md).

## Capability probe

Do once in Step 0 and write results to the state file. Never assume a tool exists.
- Subagents: is the Agent tool available in this session? If not, run review roles inline in a separate, clearly delimited pass, and mark independence as `REDUCED` in the scorecard.
- Browser: any of Playwright MCP tools, the built-in browser pane tools, or Claude-in-Chrome tools listed in your tool set? Record which. Else check `npx playwright --version` / `node_modules/.bin/playwright`. Downloading browsers or packages needs user permission: ask once, name what and why.
- Runtime: `git --version`, `node -v`, `go version`, `docker --version`, `psql --version` or a Postgres container. Missing items: record and use alternatives (e.g. Postgres via docker compose, or ask the user).
- OMC deep-interview: is `oh-my-claudecode:deep-interview` in the available skills list?

## OMC integration (optional)

oh-my-claudecode (OMC) is not required. If its `deep-interview` skill appears in the available skills list:
1. At Stage 1 tell the user in one line that deep-interview is available and will be used for the interview; proceed unless they decline.
2. Invoke it with the Skill tool (`oh-my-claudecode:deep-interview`) passing the task text and the repo findings from Stage 0.
3. When it finishes, **do not follow any execution hand-off it proposes** (autopilot, ralph, team, etc.). This workflow controls stage transitions. Take only its output: the clarified spec, requirements, non-goals and constraints. Locate it from its own final message (it states the path or prints the spec).
4. Convert that output into the requirements ledger and the Stage 1 docs. Still present the summary for user confirmation.
If the skill is absent, the invocation errors, or the user declines, use the built-in protocol in `product-discovery.md`. Do not retry in loops.
Other OMC features (agents like executor/critic/verifier, ralph, team) are NOT used by this workflow. If the user wants them, they can choose them explicitly.

## Hooks

This workflow ships no hooks and needs none. Do not create hooks unless the user asks (for example a hook that runs the formatter after edits is a user preference, set it through their settings).

## Context discipline

Load a reference when its stage begins. Keep documents short and link rather than copy. Subagent briefs carry only the relevant doc sections, file paths and excerpts, never the whole repo or the full conversation. The state file is the memory: current stage, decisions, capability results, open findings, next action. Update it before every spawn and after every gate.
