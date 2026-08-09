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
(R-0241). Migration-order steps 1 (`intake.py`), 2 (`mission_compiler.py`) and
3 (`flight_plan.py`) are COMPLETE, each with its own content-equality golden;
step 3 also added the `project_facts` seam its golden needed.
`LAST_REVIEWED_SHA` is 70156f31 — R18's own gate is owed. Open findings:
R-0221, R-0239, R-0246, R-0247. No PR; one is created at CLOSURE.

## Next Steps
- R19 gates R18 FIRST, then takes migration-order step 4,
  `orchestrator_loop.py::build_orchestrator_system_prompt`.
- R19 also registers the Phase-0 gap the R17 gate records: the protocol gives
  no disposition for a tree a dead session left dirty. Not yet a DECISION.
- Then steps 5 and 6, ONE builder per round, each with its own golden:
  `pingpong_loop.py`'s `_build_builder_prompt` and `_build_reviewer_prompt`.
- Fix R-0246 in the same round that next touches `mission_compiler.py`: the
  docstring's "byte for byte" sentence now reads as a claim about composition.
- The mission and plan manifests reach call evidence in their own later round:
  no production caller passes `on_call` to `plan_mission`
  (`apps/cli/commands/mission_cmd.py:187`,
  `packages/orchestration/gauntlet_runner.py:505`) and none passes it to
  `plan_job_llm` (`apps/cli/commands/do_cmd.py:253` and `:2860`).
- Then T004, `remedy stats cache` over actuals; then the integration gate
  (docs/agents/integration_gate.md); then closure
  (docs/roadmap/STATUS_closure_protocol.md), where the PR is created.

## Risks
- R-0221 stays open and will cost the integration gate phantom base-only
  failures.
- Three of the six builders still reach no call evidence, so F105's every-role
  acceptance line is met for intake only.
