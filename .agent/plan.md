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
T001 and T002 are DONE and gated. T003's MIGRATION ORDER
(`.agent/t003_inventory.md`, never that file's catalogue "Site N" headings —
R-0241) is COMPLETE: all six sites are migrated, each under its own golden.
R24 is GATED; `LAST_REVIEWED_SHA` is df32f595. R25 is the session terminator —
it records the R24 gate and registers R-0253 and R-0254, and starts no work.
Open findings: R-0221, R-0239, R-0246, R-0247, R-0253, R-0254.
No PR; one is created at CLOSURE.

## Next Steps
- R26 gates R25 (state only), then fixes R-0254 — production code, so SPLIT —
  and R-0253, whose fix is §4.9 plus a sixth D8 checklist item.
- ONE round wires `on_call` for the three sites lacking call evidence:
  `mission_cmd.py:362` (orchestrator), `mission_cmd.py:187` +
  `gauntlet_runner.py:505` (mission), `do_cmd.py:253` + `:2860` (plan).
- Fix R-0246 in the round that next touches `mission_compiler.py`.
- Then T004, `remedy stats cache` over actuals; then the integration gate
  (docs/agents/integration_gate.md); then closure
  (docs/roadmap/STATUS_closure_protocol.md), where the PR is created.

## Risks
- R-0221 stays open and will cost the integration gate phantom base-only
  failures.
- The reviewer prompt was the worst-ordered of the six sites and 1824 of 2048
  measured renders reorder, so T004's before/after number should quote its
  cacheable-prefix gain specifically.
