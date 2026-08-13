# Plan — F115 Prompt breakdown & cost report

Branch: feature/f115-prompt-cost-report, cut from main at 0d6c97aa after
PR #194 merged. Last reviewed SHA: 139b5c48 (R6 PASS). Next free finding
ID: R-0327. Open findings: 6 — R-0320 (Low, from F111), R-0322 (Medium,
inherited suite red), R-0323 + R-0324 (Low, reviewer arithmetic),
R-0325 + R-0326 (Low, R6 authoring defects, fixed this round, awaiting
the reviewer's resolution text).

## Goal
Costs stop being an opaque total: `remedy stats report` shows WHERE
tokens go — by segment kind, by role, by task class — plus a cost curve
and a prior-period comparison, as markdown and json, every number
traceable to a ledger row, and a period with missing data reported as
missing instead of interpolated (docs/roadmap/features/T2_F115.md).

## Current Step
R7 cleared the two R6 authoring defects and put the T001 persistence
facts on disk in `.agent/f115_inventory.md`: a ledger row is one
finalized task run, a manifest is one provider call, so T001 has a
one-to-many mapping to decide before it writes anything.

## Next Steps
1. T001 — decide the manifest-to-row mapping from the R7 inventory
   (aggregate column vs trace reference vs per-call table), record it as
   a DECISION, then persist additively with backfill tolerance: old rows
   render "unattributed", never guessed.
2. T002 — aggregation queries plus the pure renderer, with goldens;
   follow `gauntlet_matrix.py` and `tests/cli/test_stats_cost.py:49-128`.
3. T003 — CLI, prior-period comparison, json schema.
4. Integration gate (docs/agents/integration_gate.md), then closure.

## Risks
- Per-role has one bucket until `role` stops being hardcoded, and
  per-task-class has no source at all: report "no data", never a bucket.
- R-0322 will meet F115's integration gate as five pre-existing reds.

Fortschritt: 45 % (R1 ✅ · T001a ✅ · alle drei Call-Sites ✅ · T001-Shape ✅ · T001 · T002 · T003 offen) — Schätzung
