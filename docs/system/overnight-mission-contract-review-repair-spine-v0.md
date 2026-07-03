# Overnight Mission Contract + Review/Repair Spine v0 (Steps 1837-1876)

> **Status: SEMANTICS SUPERSEDED** — The overnight / time-of-day mechanics described here
> are explicitly deprecated by the roadmap (docs/roadmap/ROADMAP.md, Teil B).
> The underlying execution and approval concepts remain valid.

## Why this exists

This is the first hard **mission-contract spine** for Overnight Mode. A user gives Remedy a
mission/prompt; Remedy turns it into a **contract** and tracks it until the contract is fulfilled or
safely blocked. The user must never feel lost — Remedy explains what happened, what is still missing,
which review findings remain, and the next safe action.

> Workers execute. Remedy governs. **The Mission Contract decides whether work is done** — never from
> builder self-report.

This block does **not** pretend full overnight autonomy exists. It builds the contract loop +
readiness spine that future provider/Ollama/Claude/Pi/OpenCode adapters can plug into.

## Mission Contract concept

A `MissionContract` captures: the user goal (scrubbed summary), acceptance criteria, allowed/forbidden
actions, required gates, budgets (cycles/runtime/test-runs/tokens), autonomy level, and gate flags
(`require_clean_review`, `require_tests_green`, `require_proof_chain`,
`require_snapshot_before_apply`). Defaults are conservative: clean review required; tests/proof are
only required if explicitly set (real test execution does not exist yet, so those gates report
honestly as unavailable when set).

## Done criteria

A contract is **satisfied** only when ALL hold, from durable evidence:

- acceptance criteria are defined (else status `needs_user_acceptance_criteria`)
- the reviewer verdict is PASS with **zero open Blocker/High** findings (reviewer verdict beats
  builder self-report; a `Done:` marker is **not** `Resolved`)
- no open/blocked tasks remain
- no failing tests
- required gates pass (tests green / proof chain verified) — missing gates block satisfaction
- no open repair attempt

If none of these can produce a safe next action, the mission is `blocked`.

## Review findings as first-class blockers

The spine reads the live-review ledger via the existing safe parser (verdict + open
Blocker/High/Medium/Low counts — never raw finding text). Open Blocker/High **blocks** contract
satisfaction. `Done:` markers awaiting reviewer resolution do **not** count as resolved.

## Repair loop relationship

An open repair attempt (blocked/needs-review/failed) sets the mission to `repair_needed` and is a
blocker. The spine does not run repair — it points to the safe repair status/next action.

## Test / proof gate relationship

`require_tests_green` and `require_proof_chain` are evaluated from durable summaries
(progress-ledger test items, proof-chain `overall_status`). The spine never runs a test or builds a
patch; missing gates are reported as `missing_proofs`, not faked.

## User decision points

When acceptance criteria are missing, or a choice is needed, the mission enters `user_decision` /
`waiting_for_user` and the required action is flagged `user_decision_required`.

## Overnight readiness

`remedy overnight contract-readiness <job_id>` reports honestly: it always shows
`full_overnight_autonomy: false`, `worker_execution_available: false`, and
`real_test_execution_available: false` — because none of those exist yet.

## State machine (metadata only)

Phases: `plan`, `route`, `worker_wait`, `review`, `repair`, `test_gate`, `proof_gate`,
`user_decision`, `blocked`, `satisfied`. The spine decides what should happen next; it executes
nothing, runs no tests, applies no patches.

## Required next actions vs optional future ideas

The evaluation separates **required blockers** (needed to satisfy the current contract) from
**optional future ideas** (from the Feature Planner, surfaced only once the contract is satisfied).
They never mix.

## CLI

```
remedy overnight contract-create <job_id> [--user-goal ...] [--acceptance "a, b"] [--autonomy-level N] --json
remedy overnight contract-show <contract_id> --json
remedy overnight evaluate <contract_id> --json
remedy overnight next-action <contract_id> --json
remedy overnight cycles <contract_id> --json
remedy overnight contract-readiness <job_id> --json
remedy overnight integrity --json
```

`contract-create` and `evaluate` write safe metadata; the rest are read-only. None carry
`may_execute_commands`. (Note: `contract-readiness` is named to avoid colliding with the pre-existing
`overnight readiness` "bounded overnight prep" command.)

## What is not built yet / how adapters plug in later

- **No** Claude/Pi/OpenCode/Ollama/provider/cloud execution. Future worker adapters will execute the
  actual work; the contract spine already defines what "done" means for them to satisfy.
- **No** real test execution / snapshot-rollback proof yet (next block) — the gates are ready to
  consume them once they exist.
- **MemPalace** is an EXTERNAL long-term memory repository/tool that may later integrate as an
  adapter to store mission learnings. This block builds **no** internal memory / embeddings /
  vector DB.

## Anti-goals (explicit)

- No provider/Ollama/Claude/Pi/OpenCode/cloud/local execution; no network/browser/subprocess/shell.
- No worker execution, test run, apply/approve, git/PR automation, MCP, pricing sync.
- No fake overnight autonomy; no contract satisfied from builder self-report; no fake readiness.
- No internal MemPalace/embeddings/vector DB; no UI redesign.
