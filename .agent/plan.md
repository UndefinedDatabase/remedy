# Plan — F111 Diff-only repair

Branch: feature/f111-diff-only-repair, cut from main at 4e0b762e.
Next free finding ID: R-0300. Last reviewed SHA: 5d8d8c56 (R2 PASS).

## Goal
Repairs stop resending whole files: a repair round carries only the
failure-relevant hunks with a configurable context margin, the model answers
with a schema-enforced unified diff that is fence-checked and applied
strictly, and ANY hunk conflict discards the attempt whole and falls back to
today's full-file round with the reason recorded
(docs/roadmap/features/T2_F111.md).

## Current Step
R3 — persist the R2 gate and findings R-0298 and R-0299, then fix R-0299 by
giving the omissions record a distinct `out_of_bounds` reason. T001's helper
`select_repair_hunks` exists and is tested but has NO call site yet; wiring
is the next round's work, deliberately separated so a green gate is never
mistaken for a working feature.

## Next Steps
1. R4 — wire the selected hunks into the repair payload. OPEN QUESTION the
   next session must settle FIRST, by reading code and not by assuming:
   `repair_context.build_repair_context(job_id, test_run_event, events)`
   carries `affected_files` (paths only), takes no repo_root and has no line
   ranges, so the hunk ranges must come from somewhere else — most likely
   `review_scope._parse_diff` over the diff of the `source_patch_applied`
   event. Confirm the event actually carries a diff before designing.
2. T002 — versioned unified-diff response schema, fence pre-check before any
   apply, strict apply with an all-or-nothing conflict fallback, on the
   `builder_bridge` seam DECISION F111 D1 selected.
3. T003 — mode and token evidence per repair round, plus a fixture
   comparison recording both modes' token counts.
4. Integration gate, then closure.

## Risks
- The full suite is RED at the merge base with five known ids (R-0286), so
  the integration gate compares base against branch, never absolute green.
- `review_scope._parse_diff` and `source_apply._apply_hunks` already exist
  and must be reused, never duplicated.
