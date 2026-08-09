# Plan — F105 Cache-optimal prompt ordering

Branch: feature/f105-cache-optimal-prompt-ordering, cut from main at cfda4245
after PR #188 merged at the Open PR Gate. Build mode: one-session self-drive,
one delegated worker per round. Next finding ID: R-0244.

## Goal
Prompt assembly stops being ad hoc. Every prompt composes from REGISTERED
SEGMENTS ordered by stability — system and conventions first, task and steering
last — every call records a segment manifest (name, rank, hash) into evidence,
and `remedy stats cache` shows the cache-read share per role from actuals. Prompt
CONTENT does not change; only its composition.

## Current Step
T001 and T002 are DONE and gated. T003 counts in the MIGRATION ORDER of
`.agent/t003_inventory.md`, never that file's catalogue "Site N" headings, which
number the same six builders differently (R-0241). Step 1,
`intake.py::_build_intake_prompt`, is COMPLETE. R14 and R15 were both RECORD
rounds: R14 recorded the R13 gate, R15 recorded the R14 gate, and neither
migrated a builder, because the combined gate-plus-migration block does not fit
DECISION F105 D2's 240-line cap. That recurrence is registered as R-0243 and is
the branch's ⚠️ momentum condition. `LAST_REVIEWED_SHA` is 73e159b7. Open
findings: R-0221, R-0239, R-0242, R-0243. No PR; one is created at CLOSURE. The
candidates file is empty.

## Next Steps
- R16 gates R15 over `73e159b7..HEAD`, then takes migration-order step 2,
  `mission_compiler.py::build_mission_prompt`, onto the registry under a new
  `tests/orchestration/test_mission_prompt_golden.py`, with a mutation red-proof
  in a disposable worktree that the golden really catches a content change.
- Settle R-0243 FIRST, before authoring R16's block: without a cap change or an
  exemption, R16 splits the same way and the branch keeps spending rounds on
  record-keeping.
- Land DECISION F105 D4: the mission rules segment is cap-scoped, because
  `gauntlet_runner.py:506` varies `max_milestones`, so the byte-stable-prefix
  claim holds per cap value rather than per role. A byte-preserving split is
  impossible — the interpolations sit mid-list, the delimiter is a blank line —
  so the scope is made visible instead.
- Then migration-order steps 3 to 6, ONE builder per round, each with its own
  golden: `flight_plan.py::_build_plan_prompt`,
  `orchestrator_loop.py::build_orchestrator_prompt`, then
  `pingpong_loop.py`'s `_build_builder_prompt` and `_build_reviewer_prompt`.
- Settle R-0242: whether intra-round commits are exempt from the AGENTS.md
  Commit Gate's plan.md check, or the plan rewrite moves earlier in the block.
- Then T004, `remedy stats cache` over actuals; then the integration gate
  (docs/agents/integration_gate.md); then closure
  (docs/roadmap/STATUS_closure_protocol.md), where the PR is created.

## Risks
- `build_mission_prompt` reaches NO call evidence today, and neither do steps 3
  and 4; each must thread `on_call` from its CLI caller first, so F105's
  every-role acceptance line is not yet met for the mission role.
- R-0221 stays open and will cost the integration gate phantom base-only
  failures.
