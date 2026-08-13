# Plan — F115 Prompt breakdown & cost report

Branch: feature/f115-prompt-cost-report, cut from main at 0d6c97aa after
PR #194 merged at the Open PR Gate. Last reviewed SHA: 19b59ccc (R4 PASS).
Next free finding ID: R-0324. Open findings: 3 — R-0320 (Low, carried
from F111), R-0322 (Medium, inherited suite red, not an F115 defect),
R-0323 (Low, reviewer gate arithmetic, no fix possible on disk).

## Goal
Costs stop being an opaque total: `remedy stats report` shows WHERE
tokens go — by segment kind, by role, by task class — plus a cost curve
and a prior-period comparison, as markdown and json, every number
traceable to a ledger row, and a period with missing data reported as
missing instead of interpolated (docs/roadmap/features/T2_F115.md).

## Current Step
R5 done — housekeeping only, no source or test file touched. R-0323 is
registered and the planner call site's shape is on disk as DECISION
F115 D2, so the next round orders its wiring from the record.

## Next Steps
1. The PLANNER call site, per DECISION F115 D2: build
   `compose_planner_prompt` in `llm_planner.py` over the two existing
   parts, thread the `ComposedPrompt` to `_record_plan_call` through an
   optional hook, and gate on byte-identity of the sent prompt FIRST.
2. T001 proper — persist the manifest, or a reference to it, alongside
   the ledger row, additively, with backfill tolerance: old rows render
   as "unattributed", never guessed.
3. T002 — aggregation queries plus the pure renderer, with goldens;
   follow `gauntlet_matrix.py` and `tests/cli/test_stats_cost.py:49-128`.
4. T003 — CLI, prior-period comparison, json schema; then the
   integration gate and closure.

## Risks
- The per-role breakdown has one bucket until `role` stops being
  hardcoded, and per-task-class has no source at all. Both are recorded
  in the feature file; F115 must report "no data", never a fake bucket.
- R-0322 will meet F115's integration gate as five pre-existing reds.

Fortschritt: 30 % (R1 ✅ · T001a ✅ · Reviewer-Site ✅ · Planner-Site · T001 · T002 · T003 offen) — Schätzung
