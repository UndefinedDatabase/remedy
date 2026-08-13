# Plan — F115 Prompt breakdown & cost report

Branch: feature/f115-prompt-cost-report, cut from main at 0d6c97aa after
PR #194 merged at the Open PR Gate. Last reviewed SHA: cc635159 (R2 PASS).
Next free finding ID: R-0323. Open findings: 3 — R-0320 (Low, carried
from F111), R-0321 (Low, fixed in R3, awaiting the reviewer's Done),
R-0322 (Medium, inherited suite red, not an F115 defect).

## Goal
Costs stop being an opaque total: `remedy stats report` shows WHERE
tokens go — by segment kind, by role, by task class — plus a cost curve
and a prior-period comparison, as markdown and json, every number
traceable to a ledger row, and a period with missing data reported as
missing instead of interpolated (docs/roadmap/features/T2_F115.md).

## Current Step
R3 done — housekeeping only. T001a wired the BUILDER call site through
`compose_builder_prompt` (DECISION F115 D1), proved the sent bytes
unchanged, and pinned it with a behaviour test plus an
`inspect.getsource` wiring guard whose red-proof really goes red.

## Next Steps
1. The reviewer call site. Decide first: its traced text is
   `_reviewer_effective_prompt(...)`, which appends the native-schema
   tail unconditionally in structured mode, so the manifest covers the
   composed BASE and `segment_manifest_chars < prompt_chars` records the
   gap — the F105 D3 precedent already covers this shape. Then the
   planner site at `apps/cli/commands/job.py:236`.
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

Fortschritt: 20 % (R1 ✅ · T001a ✅ · Reviewer-Site · T001 · T002 · T003 offen) — Schätzung
