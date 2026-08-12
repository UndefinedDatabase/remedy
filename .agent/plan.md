# Plan — F111 Diff-only repair

Branch: feature/f111-diff-only-repair, cut from main at 4e0b762e.
Next free finding ID: R-0301. Last reviewed SHA: 4717ce8c (R3 PASS).
Open findings: 25, none above Medium.

## Goal
Repairs stop resending whole files: a repair round carries only the
failure-relevant hunks with a configurable context margin, the model answers
with a schema-enforced unified diff that is fence-checked and applied
strictly, and ANY hunk conflict discards the attempt whole and falls back to
today's full-file round with the reason recorded
(docs/roadmap/features/T2_F111.md).

## Current Step
R4 — persist the R3 gate and finding R-0300, then END THE SESSION cleanly at
its context limit. T001's helper `select_repair_hunks` is built, tested at 21
tests and mutation-proved, but has NO call site yet. DECISION F111 D1 is on
disk and the feature file is amended.

## Next Steps
1. R5 — close R-0300 with one test (empty file + non-empty range reports
   `out_of_bounds`), then WIRE T001. Settle this FIRST by reading code, never
   by assuming: `repair_context.build_repair_context(job_id, test_run_event,
   events)` carries `affected_files` (paths only), takes no repo_root and has
   no line ranges, so the ranges must come from elsewhere — most likely
   `review_scope._parse_diff` over the diff of the `source_patch_applied`
   event. Confirm that event actually carries a diff before designing.
2. T002 — versioned unified-diff response schema, fence pre-check before any
   apply, strict apply with an all-or-nothing conflict fallback, on the
   `builder_bridge` seam D1 selected.
3. T003 — mode and token evidence per repair round, plus a fixture comparison
   recording both modes' token counts.
4. Integration gate, then closure.

## Risks
- The full suite is RED at the merge base with five known ids (R-0286): the
  integration gate compares base against branch, never absolute green.
- `review_scope._parse_diff` and `source_apply._apply_hunks` already exist and
  must be reused, never duplicated.
