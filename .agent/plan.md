# Plan — F105 Cache-optimal prompt ordering

Branch: feature/f105-cache-optimal-prompt-ordering, cut from main at cfda4245
after PR #188 merged at the Open PR Gate. Build mode: one-session self-drive,
one delegated worker per round. Next finding ID: R-0242.

## Goal
Prompt assembly stops being ad hoc. Every prompt composes from REGISTERED
SEGMENTS ordered by stability — system and conventions first, task and steering
last — every call records a segment manifest (name, rank, hash) into evidence,
and `remedy stats cache` shows the cache-read share per role from actuals. Prompt
CONTENT does not change; only its composition.

## Current Step
T001 and T002 are DONE and gated. T003 counts its work in the MIGRATION ORDER of
`.agent/t003_inventory.md`, never in that file's catalogue "Site N" headings,
which number the same six builders differently (R-0241). Step 1,
`intake.py::_build_intake_prompt`, is COMPLETE: R11 moved its composition onto
the registry, R12 put its manifest into call evidence. R14 recorded the R13
gate, resolved R-0238 and registered R-0240 and R-0241; it migrated nothing,
because the combined block was over DECISION F105 D2's 240-line cap and D2's
remedy is a split. `LAST_REVIEWED_SHA` is 2d993ed9. Open findings: R-0221,
R-0240, R-0241. No PR exists; one is created at CLOSURE. The candidates file is
empty.

## Next Steps
- R15 gates R14 over `2d993ed9..HEAD`, then takes migration-order step 2,
  `mission_compiler.py::build_mission_prompt`, onto the registry under a new
  `tests/orchestration/test_mission_prompt_golden.py`, and lands DECISION
  F105 D4: the mission rules segment is cap-scoped, because
  `gauntlet_runner.py:506` varies `max_milestones`, so the byte-stable-prefix
  claim holds per cap value rather than per role.
- Then migration-order steps 3 to 6, ONE builder per round, each with its own
  golden: `flight_plan.py::_build_plan_prompt`,
  `orchestrator_loop.py::build_orchestrator_prompt`,
  `pingpong_loop.py::_build_builder_prompt`, and
  `pingpong_loop.py::_build_reviewer_prompt` last.
- Then T004, the `remedy stats cache` view over actuals, reporting "not
  reported" rather than zeros where a provider reports no cache figures.
- Then the integration gate (docs/agents/integration_gate.md), then closure
  (docs/roadmap/STATUS_closure_protocol.md), where the PR is created.

## Risks
- `build_mission_prompt` reaches NO call evidence today, and neither do steps 3
  and 4; each must thread `on_call` from its CLI caller first.
- Steps 3 and 4 interpolate caps and repo facts into their rules blocks, so
  those segments are cap-scoped rather than role-stable.
- R-0221 stays open and will cost the F105 integration gate phantom base-only
  failures.
