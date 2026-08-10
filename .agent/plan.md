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
SESSION CLOSED against `.agent/STOP`. T001 and T002 are DONE and gated; T003's
six migration sites are all migrated. R39 is GATED PASS; `LAST_REVIEWED_SHA` is
c44a582c. R-0256 is HALF fixed: `run_intake` and `plan_job_llm` accept a
keyword-only `composed`, landed and gated, with no test on the new branch yet.
Open findings: R-0221, R-0239, R-0247, R-0256, R-0262, R-0263.
No PR; one is created at CLOSURE.

## Next Steps
- Resume by landing R39's two tests with `seen[0].startswith(composed.text)`,
  which fixes R-0263. Proved in a worktree at R39: 68 passed, and reverting
  either ternary red-proofs its own test.
- Then finish R-0256: pass `composed=` at the three
  `apps/cli/commands/do_cmd.py` sites that already build one — intake,
  flight-plan (whose comment about the second composition goes stale and must
  be replaced) and replan. The new keyword goes on its OWN line: the suite
  counts `on_call=make_flight_plan_call_recorder(` over the WHOLE file
  (tests/orchestration/test_prompt_trace.py, `== 2`).
- Then T004, `remedy stats cache` over actuals; then the integration gate
  (docs/agents/integration_gate.md); then closure
  (docs/roadmap/STATUS_closure_protocol.md), where the PR is created.

## Risks
- R-0221 stays open and will cost the integration gate phantom base-only
  failures.
- R-0262 stays OPEN and out of scope: it needs the composition moved inside the
  `try` in `plan_job_llm` AND at the CLI sites, pinned by a raising composer.
