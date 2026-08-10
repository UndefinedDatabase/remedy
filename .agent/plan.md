# Plan — F105 Cache-optimal prompt ordering

Branch: feature/f105-cache-optimal-prompt-ordering, cut from main at cfda4245
after PR #188 merged at the Open PR Gate. One-session self-drive, one delegated
worker per round. The next free finding ID lives in `.agent/live_review.md`
line 8 and is deliberately not duplicated here (R-0240's root cause).

## Goal
Prompt assembly stops being ad hoc. Every prompt composes from REGISTERED
SEGMENTS ordered by stability — system and conventions first, task and steering
last — every call records a segment manifest (name, rank, hash) into evidence,
and `remedy stats cache` shows the cache-read share per role from actuals.
Prompt CONTENT does not change; only its composition.

## Current Step
T001 and T002 are DONE and gated. T003's six migration sites are all migrated.
R38 is GATED; `LAST_REVIEWED_SHA` is 5ca4debd. R39 records that gate and takes
the first half of R-0256: `run_intake` and `plan_job_llm` accept a keyword-only
`composed` — C3, landed and gated. The two tests did NOT land; see BLOCKER.
R-0256 stays OPEN until R40.
Open findings: R-0221, R-0239, R-0247, R-0256, R-0262.
No PR; one is created at CLOSURE.

## Next Steps
- R40 finishes R-0256: pass `composed=` at the three
  `apps/cli/commands/do_cmd.py` sites that already build one — intake,
  flight-plan (whose comment about the second composition goes stale and must
  be replaced) and replan. The new keyword goes on its OWN line: the suite
  counts `on_call=make_flight_plan_call_recorder(` over the WHOLE file
  (tests/orchestration/test_prompt_trace.py, `== 2`).
- R40 also lands R39's two tests with `seen[0].startswith(composed.text)`:
  verified at R39 in a worktree — 68 passed, each ternary reverted red-proofs.
- Then T004, `remedy stats cache` over actuals: a per-role cache-read share
  from recorded call evidence, not estimates. Quote the flight-plan prompt's
  cacheable-prefix gain — it was the worst-ordered site.
- Then the integration gate (docs/agents/integration_gate.md), then closure
  (docs/roadmap/STATUS_closure_protocol.md), where the PR is created.

## BLOCKER (R39 C4, skipped)
The block's `assert seen == [composed.text]` is unsatisfiable for ANY
implementation: `run_structured_call` wraps the base prompt through
`build_schema_prompt`, appending ~1489 chars of schema instruction, so `call_fn`
never sees `composed.text` verbatim. Not committed, over a knowingly-red suite.

## Risks
- R-0221 stays open and will cost the integration gate phantom base-only
  failures.
- R-0262 stays OPEN and out of scope: it needs the composition moved inside the
  `try` in `plan_job_llm` AND at the CLI sites, pinned by a raising composer.
