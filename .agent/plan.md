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
R37 is GATED; `LAST_REVIEWED_SHA` is c30b365e. R38 is a state-only round: it
records the R37 gate, resolves R-0261 and registers R-0262.
Open findings: R-0221, R-0239, R-0247, R-0256, R-0262.
No PR; one is created at CLOSURE.

## Next Steps
- R39 fixes R-0256, the next round and a SPLIT one: give `plan_job_llm`
  (`packages/orchestration/flight_plan.py`) and `run_intake`
  (`packages/orchestration/intake.py`) a keyword-only
  `composed: ComposedPrompt | None = None`, used as
  `composed.text if composed is not None else <the existing builder call>`.
  `ComposedPrompt` is already imported in both modules. In `run_intake` the
  expression MUST stay the argument inside the `try` (R-0257); in
  `plan_job_llm` it stays exactly where it is (R-0262 is not fixed there).
  Then pass `composed=` at the three `apps/cli/commands/do_cmd.py` call sites
  that already build one: the intake site, the flight-plan site (whose comment
  about the second composition goes stale and must be replaced) and the replan
  site. Two tests, one per module: build a ComposedPrompt with a sentinel,
  pass a DIFFERENT mission/facts to the function, assert the provider saw
  exactly `composed.text`. Red-proof each by reverting the function to its
  unconditional builder call — both branches are reachable from those tests.
  Prompt CONTENT must not change: digest `compose_*_prompt(...).text` for a
  fixed input before and after and show the two are equal.
- Then T004, `remedy stats cache` over actuals; then the integration gate
  (docs/agents/integration_gate.md); then closure
  (docs/roadmap/STATUS_closure_protocol.md), where the PR is created.

## Risks
- R-0221 stays open and will cost the integration gate phantom base-only
  failures.
- The reviewer prompt was the worst-ordered of the six sites and 1824 of 2048
  measured renders reorder, so T004's before/after number should quote its
  cacheable-prefix gain specifically.
