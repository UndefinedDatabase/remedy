# Plan — F115 Prompt breakdown & cost report

Branch: feature/f115-prompt-cost-report, cut from main at 0d6c97aa after
PR #194 merged at the Open PR Gate. Last reviewed SHA: a414c0c6 (R1 PASS).
Next free finding ID: R-0322. Open findings: 2 — R-0320 (Low, carried
forward from F111) and R-0321 (Low, an inventory miscount).

## Goal
Costs stop being an opaque total: `remedy stats report` shows WHERE
tokens go — by segment kind, by role, by task class — plus a cost curve
and a prior-period comparison, as markdown and json, every number
traceable to a ledger row, and a period with missing data reported as
missing instead of interpolated (docs/roadmap/features/T2_F115.md).

## Current Step
R2 (T001a) — make the premise true at the builder call site. The R1
inventory proved the segment manifest is EMPTY on live ping-pong data
because the builder, reviewer and planner trace entries never receive a
`composed_prompt` (DECISION F115 D1). This round wires the builder site
and pins the result with a test, with the sent bytes provably unchanged.

## Next Steps
1. R3 — the reviewer site, which needs a decision first: its traced text
   is wrapped by `_reviewer_effective_prompt` and is not always the
   composed text. Then the planner site in `apps/cli/commands/job.py`.
2. T001 proper — persist the manifest, or a reference to it, alongside
   the ledger row, additively, with backfill tolerance: old rows render
   as "unattributed", never guessed.
3. T002 — aggregation queries plus the pure renderer, with goldens over
   a fixture ledger; follow `gauntlet_matrix.py` and
   `tests/cli/test_stats_cost.py:49-128`.
4. T003 — CLI, prior-period comparison, json schema; then the
   integration gate and closure.

## Risks
- The per-role breakdown has one bucket until `role` stops being
  hardcoded, and per-task-class has no source at all. Both are recorded
  in the feature file; F115 must report "no data", never a fake bucket.
- Report generation must touch nothing (read-only, state snapshot equal).

Fortschritt: 15 % (R1 Inventar ✅ · T001a läuft · T001 · T002 · T003 offen) — Schätzung
