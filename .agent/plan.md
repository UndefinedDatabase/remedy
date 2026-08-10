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
Call evidence reaches both `do_cmd` flight-plan sites — the first through
`write_trace_jsonl`, the replan through `append_trace_jsonl`.
R29 is GATED; `LAST_REVIEWED_SHA` is 0c8932e3. R30 is in review: it makes
`compile_mission_plan` compose ONCE and hands that one composition to a
`mission_plan` recorder, so the mission manifest exists at the layer that owns
the bytes. R30 names no sink and touches no CLI — that is R31.
Open findings: R-0221, R-0239, R-0247, R-0256. R-0246 lands with R30.
No PR; one is created at CLOSURE.

## Next Steps
- R31: name the mission-plan sink. `plan_mission` owns the evidence dir, so it
  owns the traces list and appends to `<evidence_dir>/prompt_trace.jsonl`
  (APPEND, because a recompile is a second command against the same mission);
  `mission_cmd.py:187` passes the provider label; evidence tests plus the CLI
  wiring guard.
- Then the orchestrator prompt — `mission_cmd.py:362` into `run_mission`, then
  `gauntlet_runner.py:505`. Neither has a sink today either.
- R-0256 (compose once, not twice) needs a signature change on `plan_job_llm`
  and `run_intake`, so it is its own round.
- Then T004, `remedy stats cache` over actuals; then the integration gate
  (docs/agents/integration_gate.md); then closure
  (docs/roadmap/STATUS_closure_protocol.md), where the PR is created.

## Risks
- R-0221 stays open and will cost the integration gate phantom base-only
  failures.
- The reviewer prompt was the worst-ordered of the six sites and 1824 of 2048
  measured renders reorder, so T004's before/after number should quote its
  cacheable-prefix gain specifically.
