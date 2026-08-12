# Plan — F111 Diff-only repair

Branch: feature/f111-diff-only-repair, cut from main at 4e0b762e, unmerged.
Last reviewed SHA: b1e5cc7e (R6 PASS). Next free finding ID: R-0307.
Open findings: 27, none above Medium.

## Goal
Repairs stop resending whole files: a repair round carries only the
failure-relevant hunks with a configurable context margin, the model answers
with a schema-enforced unified diff that is fence-checked and applied
strictly, and ANY hunk conflict discards the attempt whole and falls back to
today's full-file round with the reason recorded
(docs/roadmap/features/T2_F111.md).

## Current Step
T001 is COMPLETE and has NO CALL SITE. Both halves are on disk in
`packages/orchestration/`: the selector `select_repair_hunks`
(`diff_repair.py`) and its range source `changed_line_ranges_from_patch`,
which maps an applied `StructuredPatch` to the `{path: [[start, end], ...]}`
shape selection consumes by reading hunk headers through the one shared
parser `review_scope.parse_diff_line_ranges`. 30 tests in
`tests/orchestration/test_diff_repair.py`, mutation-proved at the R5 gate.
Nothing imports either function: `builder_bridge.py`, `repair_context.py`
and `pingpong_loop.py` are untouched, so the green suite is a seam, not a
working feature. Wiring is T003's job.

## Next Steps
1. T002 — versioned unified-diff response schema, a fence pre-check before
   any apply, and strict all-or-nothing apply with a recorded fallback to
   the full-file round, on the `builder_bridge` seam DECISION F111 D1
   selected (`run_builder_bridge_loop`, the real symbol name — see D2).
   Read `structured_patch.py` and the `apply_structured_patch` fence path
   before designing it.
2. T003 — wire `changed_line_ranges_from_patch` into
   `run_builder_bridge_loop`, which already holds each cycle's
   `BridgeResult` and therefore `parse_result.patch`, feed the ranges into
   `select_repair_hunks`, and emit mode and token evidence per repair round
   plus a fixture comparison recording both modes' token counts.
3. Integration gate, then closure.

## Risks
- The full suite is RED at the merge base with five known ids (R-0286): the
  integration gate compares base against branch, never absolute green.
- `review_scope._parse_diff` and `source_apply._apply_hunks` already exist and
  must be reused, never duplicated. `parse_diff_line_ranges` is the ONLY
  sanctioned reading of hunk headers outside `review_scope` itself.
