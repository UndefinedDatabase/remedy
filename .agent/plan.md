# Plan — F111 Diff-only repair

Branch: feature/f111-diff-only-repair, cut from main at 4e0b762e,
unmerged. Last reviewed SHA: 023e8d9d (R7 PASS). Next free finding
ID: R-0308. Open findings: 28, none above Medium.

## Goal
Repairs stop resending whole files: a repair round carries only the
failure-relevant hunks with a configurable context margin, the model
answers with a schema-enforced unified diff that is fence-checked and
applied strictly, and ANY hunk conflict discards the attempt whole
and falls back to today's full-file round with the reason recorded
(docs/roadmap/features/T2_F111.md).

## Current Step
T002 is HALF built and has NO CALL SITE. The response record landed
this round in `packages/orchestration/diff_repair_response.py`: the
versioned `{format, version, diff, files}` shape, its parse, a
validation that cross-checks the declared `files` list against the
paths the diff really touches, and `precheck_diff_repair_fences`,
the non-raising fence decision that rejects an out-of-fence path
BEFORE the applicator is called. `structured_patch.py` gained the
two helpers this reuses, `extract_json_object` and
`unsafe_path_issues`, so neither the JSON-wrapper reading nor the
path-safety rules exist twice. Nothing imports the new module: T001
and T002 are both seams, and T003 wires both.

## Next Steps
1. R9 — the apply half of T002: convert a validated response to a
   `StructuredPatch`, apply strictly through `apply_structured_patch`,
   and on ANY hunk conflict discard the attempt whole, record
   `fallback_reason`, and report mode `full_fallback` with the
   touched files byte-identical to their pre-attempt state.
2. T003 — wire `changed_line_ranges_from_patch` and the response
   channel into `run_builder_bridge_loop`, emit mode and token
   evidence per repair round, add the fixture token comparison.
3. Integration gate, then closure.

## Risks
- The full suite is RED at the merge base with five known ids
  (R-0286): the integration gate compares base against branch.
- `review_scope._parse_diff` and `source_apply._apply_hunks` already
  exist and must be reused, never duplicated. `parse_diff_line_ranges`
  is the ONLY sanctioned reading of hunk headers outside
  `review_scope` itself.
- A `files` list with more than one entry has no correct conversion
  yet: giving each path the whole diff text would apply every hunk to
  every file. R9 owns it.
