# Plan — F111 Diff-only repair

Branch: feature/f111-diff-only-repair, cut from main at 4e0b762e,
unmerged, no PR by design. Last reviewed SHA: 34319061 — R12's verdict
lives in the handoff (planner_reviewer_prompt.md §4.13 terminator).
Next free finding ID: R-0316. Open findings: 33 entering R13. None High.

## Goal
Repairs stop resending whole files: a repair round carries only the
failure-relevant hunks with a configurable context margin, the model
answers with a schema-enforced unified diff that is fence-checked and
applied strictly, and ANY hunk conflict discards the attempt whole
and falls back to today's full-file round with the reason recorded
(docs/roadmap/features/T2_F111.md).

## Current Step
R13 closes T002. R-0315 is settled by DECISION F111 D6: new-file
creation stays on the full-file path in v1 and the feature file is
amended to say so. `diff_repair_apply.apply_diff_repair` is the
apply-and-fallback seam — validate, fence-precheck, convert, apply,
and on any failure report mode `full_fallback` with a named
`fallback_reason`. It has NO call site yet.

## Next Steps
1. R14 — R-0313, the response-side blank-context normalisation. A
   blank context line stripped to "" makes an otherwise valid diff
   REJECT. It belongs in the response half, where the diff's own line
   structure is known, never in `_apply_hunks`, where a trailing ""
   from `split("\n")` would make the last hunk over-consume.
2. R15 — T003: wire `select_repair_hunks`,
   `changed_line_ranges_from_patch` and `apply_diff_repair` into
   `run_builder_bridge_loop`, emit mode and token evidence per repair
   round, add the fixture token comparison.
3. Integration gate, then closure.

## Risks
- The full suite is RED at the merge base with five known ids
  (R-0286): the integration gate compares base against branch.
- All-or-nothing rests entirely on source_apply's durable snapshot.
  `apply_diff_repair` adds no rollback of its own, so a snapshot
  regression is a fallback-correctness regression.
- A green suite over unreferenced modules is not a working feature.
  R15 is the round that makes F111 real.
