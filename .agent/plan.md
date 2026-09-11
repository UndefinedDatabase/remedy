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

ROUND 49 repairs `R-0876`, which round 48's id-shape widen landed and its worker declared.
The generator wrapped two construction keywords in `str(...)` whose value can be `None`, so
an artifact produced by orchestration rather than by a task recorded the string `"None"`
instead of the absence `packages/core/models.py` documents — a truthy value no lookup
matches. Both sites move the `str(...)` inside the conditional's true branch, and both gain
a test that goes red without the fix on `assert 'None' is None`. The round 48 FAIL verdict
is booked here.

## Next Steps

1. RE-RUN THE FLIP DRY RUN against a tree whose id shape is one spelling, and re-classify
   the residue `.agent/f275_t003_flip_residue.md` records at 2714 failures. The 256
   hexadecimal-UUID and 369 model-validation failures should be gone; what remains is the
   transform rules section 3 of that artefact enumerates.
2. THE FLIP, still as the one declared-oversize commit AGENTS.md permits per feature,
   declared with its inseparability reason before review.
3. The resolver collapse DECISION F260 D5 places in T003, with the classic store.
4. The closure sequence: the integration gate, the evidence job, a fresh review zip, the
   ledger rotation, the STATUS line and the PR.

## Risks

- F275 stands at 49 rounds and 19 sessions against the operator's soft limit of 60 rounds
  and 20 sessions. The NEXT session is the twentieth and owes a scope report under
  amend0908-f275-finish rule 1, which also forbids the split-and-close default here.
- A mechanical wrap applied to a construction keyword is only safe where the value cannot
  be `None`. `R-0876` is that class; the flip's own transform wraps nothing, but its
  `**`-splat rule will face the same question.
- The open set is 87 by distinct id once this round registers `R-0876`. Four are High —
  R-0803, R-0804, R-0806 and R-0807 — all F273's, per DECISION F272 D12.
