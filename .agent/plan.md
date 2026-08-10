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
R45 is DONE and GATED-PENDING: the R44 gate record is on disk in
`.agent/live_review.md` (`LAST_REVIEWED_SHA` -> ae1756f8), and T004 slice 1/2
landed — `remedy stats cache` renders the cache-read share per bucket through
`_load_ledger_reports`, with `unmeasured` for inputs nobody reported and
`undefined` for inputs reported as zero (DECISION F105 D15), and the R-0266
per-role limit named in the output. The catalog entry declares
supports_json=False and offers no --json arg, so no flag exists that does
nothing. tests/cli/test_stats_cost.py 39 passed (33 + 6 new). T001-T003 and
T004 slice 0/2 are DONE and gated; `.agent/t004_inventory.md` stays T004's
ground truth. Landed: R-0267. Open: R-0221, R-0239, R-0247, R-0262, R-0265,
R-0266 — all six OPEN by design, none touched. No PR; one is created at CLOSURE.

## Next Steps
- R46 = T004 slice 2/2: the `--json` mode for `stats cache` (payload version,
  the share as a number or as its reason word, and the same basis block
  `stats cost` carries), its catalog `--json` arg with supports_json=True, and
  its tests; plus the before/after comparison note in the feature's evidence
  with honest numbers whatever they are (the feature file's T004 line).
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
