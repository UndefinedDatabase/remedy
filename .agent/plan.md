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
SESSION CLOSED at R43, cleanly and not against a STOP file. T001, T002 and T003
are DONE and gated. R42 is GATED PASS; `LAST_REVIEWED_SHA` is 1fc4c62c. T004 is
the only slice left and is now fully scoped: `.agent/t004_inventory.md` is its
ground truth and DECISION F105 D14 answers all five of its open questions.
Open findings: R-0221, R-0239, R-0247, R-0262, R-0265, R-0266.
No PR; one is created at CLOSURE.

## Next Steps
- T004 slice 1 under D14: `remedy stats cache` beside `remedy stats cost` in
  `apps/cli/commands/stats_ledger_cmd.py`, cache-read share per role read from
  the ledger, `unmeasured` and never `0` where nothing was reported, and output
  that names the R-0266 limit instead of hiding it. Fixtures take the
  evidence-tree-backfilled shape (`tests/cli/test_stats_cost.py:121`).
- Then the before/after comparison note in the feature's evidence, with honest
  numbers whatever they are (the feature file's T004 line).
- Then the integration gate (docs/agents/integration_gate.md); R-0221 will
  attribute phantom base-only failures there and that is expected, not new.
- Then closure (docs/roadmap/STATUS_closure_protocol.md), where the evidence
  job, the FRESH review zip, the STATUS line and the PR all land.

## Risks
- PR #189 (`docs/amend0810-clerical` -> `main`) is open and is NOT a `feature/*`
  branch, so the Open PR Gate makes it stop-and-report. It blocks no work on
  this branch but must be resolved by the operator before a NEW branch is cut.
- R-0221 stays open and will cost the integration gate phantom base-only
  failures.
- R-0262, R-0265 and R-0266 stay OPEN and out of scope for F105 by design.
