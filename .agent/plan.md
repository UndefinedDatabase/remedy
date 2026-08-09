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
T001 and T002 are DONE and reviewer-gated. R10 is gated PASS and R-0236 and
R-0237 are RESOLVED, so R-0221 is the only open finding. R11 migrates T003 SITE
1 — `packages/orchestration/intake.py::_build_intake_prompt` — to the registry
under `tests/orchestration/test_intake_prompt_golden.py`. Composition only: the
manifest reaches call evidence in R12, split off so each diff is one reviewable
idea. `.agent/t003_inventory.md` holds the survey and the migration order. No PR
exists; one is created at CLOSURE. The candidates file is empty.

## Next Steps
- R12: the intake segment manifest into call evidence through the existing
  `_record_intake_call` recorder at `apps/cli/commands/do_cmd.py:206`, plus the
  schema-tail decision the inventory defers.
- Then sites 2-6 in the inventory's order, ONE builder per round, each golden.
- Then the acceptance guard: a test that greps direct string-assembly patterns
  in the builder modules, allowlist starting empty.
- Then T004, the `remedy stats cache` view over actuals, reporting "not
  reported" rather than zeros where a provider reports no cache figures.
- Then the integration gate (docs/agents/integration_gate.md), then closure
  (docs/roadmap/STATUS_closure_protocol.md), where the PR is created.

## Risks
- Four of the six builders never send the string they build: `run_structured_call`
  wraps it, so a manifest ignoring the schema tail describes a strict prefix.
- Three of the six reach no call evidence today; those rounds thread `on_call`
  first.
- R-0221 stays open and will cost the F105 integration gate phantom base-only
  failures.
- DECISION F105 D2 caps step blocks at 240 lines; the once-per-feature oversize
  exception is spent on `ea48ea89`.
