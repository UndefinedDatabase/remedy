# Plan — F275 One world completion, part three

Branch: feature/f275-one-world-completion-part-three, cut from `main` at
`a5bf894946ab6de053a4232109d6341a63533768`, the merge commit of pull request 246.

## Goal

Finish what F274 could not reach inside its own limit: the two carry-overs F260's Design
names, DECISION F260 D3, the prototype-cluster deletion itself, the atomic record flip that
T002 rules but does not perform, and the classic runner. Operator ruling amend0908-f275-finish
orders T001 PERFORMED, not prepared. T001 and T002 are DONE, and the classic runner's whole
command surface is gone as of round 34.

## Current Step

ROUND 47 lands the FIRST slice of the id-shape migration DECISION F275 D26 places before the
flip. `TaskExecutionContext.job_id` and `.task_id` become `str`, and the 34 construction
sites that fill them pass `str(...)` — a no-op once the flip lands, correct before it. The
reviewer measured the result at `013e5517`: the full suite reads 18371 passed, the base's
own figure, so the change moves no test in either direction. DECISION F275 D27 records the
scope and the two fields deliberately left for later.

## Next Steps

1. `PatchIntentSet.task_id`, MEASURED AND NOT YET SAFE. Widening it alongside this slice
   left four `tests/test_grouped_cli.py` tests failing with `Error: Job not found`, ONLY
   under full-suite ordering, against a base the reviewer measured fully green. The cause
   is undiagnosed and the next round diagnoses it before widening that field.
2. `Artifact.task_id`, the largest of the three at 84 construction sites. Widened alone it
   left 70 failures in four classes — an artifact lookup that compares the two spellings,
   three test assertions, and the ruff ceiling. Each is enumerated and none is unknown.
3. THE FLIP, once the id shape is one spelling, still as the one declared-oversize commit
   AGENTS.md permits per feature, declared with its inseparability reason before review.
4. The resolver collapse DECISION F260 D5 places in T003, with the classic store. Then the
   closure sequence: the integration gate, the evidence job, a fresh review zip, the ledger
   rotation, the STATUS line and the PR.

## Risks

- F275 stands at 47 rounds and 19 sessions against the operator's soft limit of 60 rounds
  and 20 sessions. The NEXT session is the twentieth and owes a scope report under
  amend0908-f275-finish rule 1, which also forbids the split-and-close default here.
- The open set is 86 by distinct id. Four are High — R-0803, R-0804, R-0806 and R-0807 —
  all F273's, per DECISION F272 D12.
