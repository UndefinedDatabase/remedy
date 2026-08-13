# Plan — F115 Prompt breakdown & cost report

Branch: feature/f115-prompt-cost-report, cut from main after PR #194
(F111 closure) merged at the Open PR Gate. Last reviewed SHA: none yet,
R1 is the first round. Next free finding ID: R-0321. Open findings: 1
(R-0320, Low, carried forward from F111 — not an F115 defect).

## Goal
Costs stop being an opaque total: `remedy stats report` shows WHERE
tokens go — by segment kind, by role, by task class — plus a cost curve
and a prior-period comparison, as markdown and json, every number
traceable to a ledger row, and a period with missing data reported as
missing instead of interpolated (docs/roadmap/features/T2_F115.md).

## Current Step
R1 — claim F115, reset the round state, and inventory the CURRENT shape
of the token ledger and the prompt-segment registry before any code is
written. The feature file demands that inspection first: F115 is
aggregation and presentation only, so the join it needs must be found
in what exists, not invented.

## Next Steps
1. T001 — persist the segment manifest, or a reference to it, alongside
   the ledger row, additively, with backfill tolerance: old rows render
   as "unattributed", never guessed.
2. T002 — aggregation queries plus the pure renderer, with goldens over
   a fixture ledger covering mixed roles, mixed task classes, missing
   manifests and unpriced calls.
3. T003 — the CLI, the prior-period comparison and the json schema; an
   empty prior period reads "no comparison data", not zeros.
4. Integration gate, then closure per STATUS_closure_protocol.md.

## Risks
- The join may not exist yet. If the ledger writer stores no manifest
  reference at all, T001 grows and the R1 inventory must say so plainly.
- Report generation must touch nothing (read-only, state snapshot equal);
  an aggregation path that writes is an acceptance failure, not a nit.

Fortschritt: 5 % (R1 Inventar läuft · T001 · T002 · T003 offen) — Schätzung
