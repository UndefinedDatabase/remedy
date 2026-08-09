# Plan — F105 Cache-optimal prompt ordering

Branch: feature/f105-cache-optimal-prompt-ordering, cut from main at cfda4245
after PR #188 (the F104 closure) merged at the Open PR Gate. Build mode:
one-session self-drive, one delegated worker per round. Next finding ID: R-0238.

## Goal
Prompt assembly stops being ad hoc. Every prompt composes from REGISTERED
SEGMENTS ordered by stability — system and conventions first, task and steering
last — every call records a segment manifest (name, rank, hash) into evidence,
and `remedy stats cache` shows the cache-read share per role from actuals. Prompt
CONTENT does not change; only its composition.

## Current Step
Session ended at its DECLARED THREE-ROUND CAP (R8 completion, R9, R10) with F105
work remaining — a clean ending under docs/agents/self_drive_protocol.md G7, not
a failure. T001 and T002 are DONE and reviewer-gated. R9 delivered
`.agent/t003_inventory.md`, the survey T003 migrates against. `LAST_REVIEWED_SHA`
is 9b50fafe. R-0229 through R-0235 are RESOLVED; R-0236 and R-0237 are FIXED
with `Landed:` lines the next gate converts. No PR exists; one is created at
CLOSURE. The candidates file is empty.

## Next Steps
- Gate R10 over `9b50fafe..HEAD` first: R10 ended a SESSION, not the branch, so
  its gate is owed (R-0233's correction to §4.13).
- Then T003 proper, ONE builder per round in the inventory's order, starting at
  `packages/orchestration/intake.py::_build_intake_prompt`: the content-equality
  golden lands FIRST, then composition moves to the registry, then the segment
  manifest reaches call evidence.
- Then the acceptance guard the feature file names: a test that greps direct
  string-assembly patterns in the builder modules, allowlist starting empty.
- Then T004, the `remedy stats cache` view over actuals, reporting "not
  reported" rather than zeros where a provider reports no cache figures.
- Then the integration gate (docs/agents/integration_gate.md), then closure
  (docs/roadmap/STATUS_closure_protocol.md), where the PR is created.

## Risks
- Four of the six builders never send the string they build: `run_structured_call`
  wraps it. A golden must state which string it pins, or a manifest will describe
  a strict prefix of the bytes actually sent.
- Three of the six reach no call evidence today; their rounds must thread
  `on_call` before a manifest can land anywhere.
- R-0221 stays open and will cost the F105 integration gate the same phantom
  base-only failures it cost F103 and F104.
- DECISION F105 D2 caps step blocks at 240 lines; the once-per-feature oversize
  exception is spent on `ea48ea89`.
