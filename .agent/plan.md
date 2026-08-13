# Plan — F115 Prompt breakdown & cost report

Branch: feature/f115-prompt-cost-report, cut from main at 0d6c97aa after
PR #194 merged at the Open PR Gate. Last reviewed SHA: 8601e276 (R3 PASS).
Next free finding ID: R-0323. Open findings: 2 — R-0320 (Low, carried
from F111), R-0322 (Medium, inherited suite red, not an F115 defect).
R-0321 was resolved at the R4 gate.

## Goal
Costs stop being an opaque total: `remedy stats report` shows WHERE
tokens go — by segment kind, by role, by task class — plus a cost curve
and a prior-period comparison, as markdown and json, every number
traceable to a ledger row, and a period with missing data reported as
missing instead of interpolated (docs/roadmap/features/T2_F115.md).

## Current Step
R4 done — the REVIEWER call site now composes through
`compose_reviewer_prompt` and hands the composition to its trace entry,
so reviewer traces carry a real segment manifest. The manifest covers
the composed BASE; the native-schema tail stays uncovered by design
(F105 D3), which `segment_manifest_chars < prompt_chars` records.

## Next Steps
1. The PLANNER call site (`apps/cli/commands/job.py:236`). It does NOT
   compose locally — the prompt arrives through `llm_planner` and
   `make_structured_planner` as `effective_prompt`, so the composition
   has to be threaded down from where it is built. Inspect that path
   before ordering the wiring.
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
