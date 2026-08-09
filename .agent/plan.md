# Plan — F105 Cache-optimal prompt ordering

Branch: feature/f105-cache-optimal-prompt-ordering, cut from main at cfda4245
after PR #188 merged at the Open PR Gate. Build mode: one-session self-drive,
one delegated worker per round. Next finding ID: R-0240.

## Goal
Prompt assembly stops being ad hoc. Every prompt composes from REGISTERED
SEGMENTS ordered by stability — system and conventions first, task and steering
last — every call records a segment manifest (name, rank, hash) into evidence,
and `remedy stats cache` shows the cache-read share per role from actuals. Prompt
CONTENT does not change; only its composition.

## Current Step
The session ended at its DECLARED THREE-ROUND CAP (R11, R12, R13) with F105 work
remaining — a clean ending under docs/agents/self_drive_protocol.md G7, not a
failure. T001 and T002 are DONE and gated. T003 SITE 1 is COMPLETE: R11 moved
`_build_intake_prompt` onto the registry under
`tests/orchestration/test_intake_prompt_golden.py`, and R12 put its manifest
into call evidence and settled DECISION F105 D3. `LAST_REVIEWED_SHA` is
927bfdad. Open findings: R-0221, R-0238 and R-0239. No PR exists; one is created
at CLOSURE. The candidates file is empty.

## Next Steps
- Gate R13 over `927bfdad..HEAD` first: R13 ended a SESSION, not the branch, so
  its gate is owed (R-0233's correction to §4.13).
- Then T003 sites 2-6 in `.agent/t003_inventory.md`'s order, ONE builder per
  round, each with its own golden, starting at
  `packages/orchestration/mission_compiler.py::build_mission_prompt`.
- Then T004, the `remedy stats cache` view over actuals, reporting "not
  reported" rather than zeros where a provider reports no cache figures.
- Then the integration gate (docs/agents/integration_gate.md), then closure
  (docs/roadmap/STATUS_closure_protocol.md), where the PR is created.

## Risks
- Sites 3, 5 and 6 reach no call evidence today; each must thread `on_call` from
  its CLI caller before a manifest can land anywhere.
- Sites 5 and 6 interpolate caps and repo facts into their rules blocks, so
  those segments are not byte-stable per role without a split.
- R-0221 stays open and will cost the F105 integration gate phantom base-only
  failures.
