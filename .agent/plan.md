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
T001 and T002 are DONE and gated. T003 counts in the MIGRATION ORDER of
`.agent/t003_inventory.md`, never that file's catalogue "Site N" headings
(R-0241). Migration-order steps 1 (`intake.py::_build_intake_prompt`) and 2
(`mission_compiler.py::build_mission_prompt`) are COMPLETE and gated, each with
its own content-equality golden. DECISION F105 D5 ended the record-only stall:
the step block is counted once and capped at 400, so R16 carried a gate record
AND a migration in one block. `LAST_REVIEWED_SHA` is efd66b68. Open findings:
R-0221, R-0239, R-0242, R-0245, R-0246. No PR; one is created at CLOSURE.

## Next Steps
- R18 gates R17 FIRST — R17's own gate is owed — then takes migration-order
  step 3, `flight_plan.py::_build_plan_prompt`, which needs a `repo_facts`
  injection seam before its golden can be deterministic.
- Then migration-order steps 4 to 6, ONE builder per round, each with its own
  golden: `orchestrator_loop.py::build_orchestrator_prompt`, then
  `pingpong_loop.py`'s `_build_builder_prompt` and `_build_reviewer_prompt`.
- Fix R-0246 in the same round that next touches `mission_compiler.py`: the
  docstring's "byte for byte" sentence now reads as a claim about composition.
- The mission and plan manifests reach call evidence in their own later round:
  no production caller passes `on_call` to `plan_mission`
  (`apps/cli/commands/mission_cmd.py:187`,
  `packages/orchestration/gauntlet_runner.py:505`).
- Settle R-0242: whether intra-round commits are exempt from the AGENTS.md
  Commit Gate plan.md check, or the plan rewrite moves earlier in the block.
- Then T004, `remedy stats cache` over actuals; then the integration gate
  (docs/agents/integration_gate.md); then closure
  (docs/roadmap/STATUS_closure_protocol.md), where the PR is created.

## Risks
- R-0221 stays open and will cost the integration gate phantom base-only
  failures.
- Four of the six builders still reach no call evidence, so F105's every-role
  acceptance line is met for intake only.
