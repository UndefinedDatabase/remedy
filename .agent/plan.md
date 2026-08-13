# Plan — F115 Prompt breakdown & cost report

Branch: feature/f115-prompt-cost-report, cut from main at 0d6c97aa after
PR #194 merged. Last reviewed SHA: 1422b01f (R5 PASS). Next free finding
ID: R-0325. Open findings: 4 — R-0320 (Low, from F111), R-0322 (Medium,
inherited suite red), R-0323 + R-0324 (Low, reviewer arithmetic).

## Goal
Costs stop being an opaque total: `remedy stats report` shows WHERE
tokens go — by segment kind, by role, by task class — plus a cost curve
and a prior-period comparison, as markdown and json, every number
traceable to a ledger row, and a period with missing data reported as
missing instead of interpolated (docs/roadmap/features/T2_F115.md).

## Current Step
R6 wired the PLANNER call site per DECISION F115 D3: composed from two
ranked segments, handed to the trace entry through an optional hook,
sent bytes pinned unchanged. All three call sites are now wired.

## Next Steps
1. T001 proper — persist the manifest, or a reference to it, alongside
   the ledger row, additively, with backfill tolerance: old rows render
   as "unattributed", never guessed.
2. T002 — aggregation queries plus the pure renderer, with goldens;
   follow `gauntlet_matrix.py` and `tests/cli/test_stats_cost.py:49-128`.
3. T003 — CLI, prior-period comparison, json schema.
4. Integration gate (docs/agents/integration_gate.md), then closure.

## Risks
- Per-role has one bucket until `role` stops being hardcoded, and
  per-task-class has no source at all: report "no data", never a bucket.
- R-0322 will meet F115's integration gate as five pre-existing reds.

Fortschritt: 40 % (R1 ✅ · T001a ✅ · alle drei Call-Sites ✅ · T001 · T002 · T003 offen) — Schätzung
