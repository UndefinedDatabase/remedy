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
R44 is DONE and GATED-PENDING: the R43 gate record is on disk in
`.agent/live_review.md` (`LAST_REVIEWED_SHA` -> b0b2d12f), and T004 slice 0/2
landed — the ledger-reading half of `stats cost` now lives in
`_load_ledger_reports` in `apps/cli/commands/stats_ledger_cmd.py`, with no
behaviour change (tests/cli/test_stats_cost.py 33 passed; the mutation probe in
a disposable worktree failed 19 of those 33, so the helper is reached).
T001, T002 and T003 are DONE and gated. `.agent/t004_inventory.md` stays the
ground truth for T004 and DECISION F105 D14 answers its five open questions.
Open findings: R-0221, R-0239, R-0247, R-0262, R-0265, R-0266 — all six OPEN by
design, none touched this round. No PR; one is created at CLOSURE.

## Next Steps
- R45 = T004 slice 1/2: `remedy stats cache` beside `remedy stats cost` in
  `apps/cli/commands/stats_ledger_cmd.py`, reading through `_load_ledger_reports`
  rather than a second copy; plus its command-catalog entry and its own test
  module. Cache-read share per role from the ledger, `unmeasured` and never `0`
  where nothing was reported, and output that names the R-0266 limit instead of
  hiding it. Fixtures take the evidence-tree-backfilled shape
  (`tests/cli/test_stats_cost.py:121`).
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
