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
SESSION CLOSED at R46, by plan and NOT against a `.agent/STOP` file: no such
file exists and none was created. The BRANCH stays open.
`LAST_REVIEWED_SHA` is c7510403 — `.agent/live_review.md` carries the R45 gate
record and the R46 step line but NO R46 gate record, deliberately; the next
session gates R46 as an ordinary handback from base c7510403.
R46 is DONE: T004 slice 2/2 landed. `remedy stats cache --json` emits the share
as a number, or as `null` with `share_basis` naming which of the two absences
applies, alongside the formula and the R-0266 per-role limit; the catalog entry
now declares supports_json=True and carries a `--json` arg. The human table did
not change one byte. tests/cli/test_stats_cost.py 41 passed (39 + 2 new).
T001-T003 and BOTH T004 slices are DONE; `.agent/t004_inventory.md` stays
T004's ground truth. R-0267 was RESOLVED by the reviewer at R45. Open: R-0221,
R-0239, R-0247, R-0262, R-0265 and R-0266 — all six OPEN by design, none
touched. No PR exists; one is created at CLOSURE.

## Next Steps
- The T004 before/after comparison note in the feature's evidence, with honest
  numbers whatever they are (the feature file's T004 line).
- The integration gate per `docs/agents/integration_gate.md`; R-0221 will
  attribute phantom base-only failures there and that is expected, not new.
- Closure per `docs/roadmap/STATUS_closure_protocol.md`, where the evidence
  job, the FRESH review zip, the STATUS line and the PR all land.

## Risks
- PR #189 (`docs/amend0810-clerical` -> `main`) is open and is NOT a `feature/*`
  branch, so the Open PR Gate makes it stop-and-report. It blocks no work on
  this branch but must be resolved by the operator before F105's closure PR.
- R-0221 stays open and will cost the integration gate phantom base-only
  failures.
- R-0262, R-0265 and R-0266 stay OPEN and out of scope for F105 by design.
