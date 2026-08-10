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
T001 and T002 are DONE and gated. T003's six migration sites are all migrated,
each under its own golden. R27 is GATED; `LAST_REVIEWED_SHA` is 73259d7a.
R28 is a SPLIT round: it records the R27 gate, resolves R-0255, registers
R-0256, and closes the last `do_cmd` evidence gap by adding
`append_trace_jsonl` beside `write_trace_jsonl` and wiring the replan site with
it — the per-job trace file must not be truncated by a second command.
Open findings: R-0221, R-0239, R-0246, R-0247, R-0256.
No PR; one is created at CLOSURE.

## Next Steps
- `on_call` for the mission and orchestrator prompts — `mission_cmd.py:187`,
  `mission_cmd.py:362`, `gauntlet_runner.py:505`. None has an evidence sink
  today, so each needs its sink named before it is wired.
- Fix R-0246 in the round that next touches `mission_compiler.py`.
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
