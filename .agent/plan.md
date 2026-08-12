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
`LAST_REVIEWED_SHA` is 5e55669d — R47 was GATED PASS and that record sits in
`.agent/live_review.md`. The operator removed `.agent/STOP` between sessions, so
work resumed at R48.
T001, T002, T003 and now T004 are all DONE. T004's view half is `remedy stats
cache` with its `--json` mode; T004's note half landed this round as
`docs/system/cache-optimal-prompt-ordering-v1.md`, backed by the measurement
module `tests/orchestration/test_prompt_cache_prefix.py`, and the feature file
carries a `## Built State` section. `.agent/t004_inventory.md` stays T004's
ground truth.
The provider-side cache-read share is UNMEASURED and the note says so: no
`ledger.sqlite` exists anywhere in this checkout, so there are no actuals.
Open findings: R-0221, R-0239, R-0247, R-0262, R-0265, R-0266 and R-0268 —
seven, all OPEN by design, none touched this round. The next free finding ID
stays R-0269: R48 registered nothing.

## Next Steps
1. The integration gate per `docs/agents/integration_gate.md`; R-0221 will
   attribute phantom base-only failures there — expected, not new.
2. Closure per `docs/roadmap/STATUS_closure_protocol.md`, where the evidence
   job, the FRESH review zip, the STATUS line and the PR all land.
3. PR #189 (`docs/amend0810-clerical` -> `main`), which the OPERATOR must
   resolve before F105's closure PR is cut.

## Risks
- PR #189 is open and is NOT from a `feature/*` branch, so the Open PR Gate
  makes it stop-and-report. It blocks no work here, but it blocks closure.
- R-0221 stays open and will cost the integration gate phantom base-only
  failures.
- R-0262, R-0265, R-0266 and R-0268 stay OPEN and out of scope for F105 by
  design; R-0268 belongs to the self-drive protocol, not prompt composition.
