# Plan — F111 Diff-only repair

Branch: feature/f111-diff-only-repair, cut from main at 4e0b762e.
Next free finding ID: R-0303. Last reviewed SHA: c9064b17 (R4 PASS).
Open findings: 26, none above Medium.

## Goal
Repairs stop resending whole files: a repair round carries only the
failure-relevant hunks with a configurable context margin, the model answers
with a schema-enforced unified diff that is fence-checked and applied
strictly, and ANY hunk conflict discards the attempt whole and falls back to
today's full-file round with the reason recorded
(docs/roadmap/features/T2_F111.md).

## Current Step
R5 landed T001's second half. The helper `select_repair_hunks`
(`packages/orchestration/diff_repair.py`) now has a RANGE SOURCE beside it:
`changed_line_ranges_from_patch` maps an applied `StructuredPatch` to the
`{path: [[start, end], ...]}` shape selection consumes, reading hunk headers
through the one shared parser `review_scope.parse_diff_line_ranges` — a new
public seam over the existing `_parse_diff`. R-0300 is closed by a test for a
zero-line file with a non-empty range. T001 therefore has BOTH its selector
and its range source, at 30 tests, and still has NO CALL SITE: nothing in
`builder_bridge.py`, `repair_context.py` or `pingpong_loop.py` imports either
function yet. A green suite here is not a working feature.

## Next Steps
1. T002 — versioned unified-diff response schema, fence pre-check before any
   apply, strict apply with an all-or-nothing conflict fallback, on the
   `builder_bridge` seam DECISION F111 D1 selected
   (`run_builder_bridge_loop`, the real symbol name — see D2).
2. T003 — wire `changed_line_ranges_from_patch` into
   `run_builder_bridge_loop`, which already holds each cycle's `BridgeResult`
   and therefore `parse_result.patch`, feed the ranges into
   `select_repair_hunks`, and emit mode and token evidence per repair round
   plus a fixture comparison recording both modes' token counts.
3. Integration gate, then closure.

## Risks
- The full suite is RED at the merge base with five known ids (R-0286): the
  integration gate compares base against branch, never absolute green.
- `review_scope._parse_diff` and `source_apply._apply_hunks` already exist and
  must be reused, never duplicated. `parse_diff_line_ranges` is the ONLY
  sanctioned reading of hunk headers outside `review_scope` itself.
- The R4 hypothesis that ranges come from the `source_patch_applied` event is
  FALSE and is deleted here; it is recorded as finding R-0302 and settled by
  DECISION F111 D3 in `docs/roadmap/features/T2_F111.md`.
