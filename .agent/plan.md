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

ROUND 40 resolves R-0870 — every instance repaired across rounds 23, 36, 37, 38 and 39, and
both sweeps re-run by the reviewer against the committed tree — and records DECISION F275
D22: the flip carries a SECOND type pair, `Task` to `TaskEntry`, which no decision in this
chain has measured. The two share two field names of seven and twenty-three, and three
`Task` fields have no counterpart of the same meaning, one of them read at 35 sites.

## Next Steps

1. WIDEN `TaskEntry` with the fields DECISION F275 D22 names, in the shape F272's D5, D6
   and D7 staged a record collapse: widen first, because that half is green by construction
   and it shrinks the atomic commit that follows.
2. The flip itself, applied from the round 36 site enumeration, the round 38 seam list and
   the round 40 task-pair list, as the one declared-oversize commit AGENTS.md permits per
   feature, with the inseparability reason AND the real size stated in the handback BEFORE
   review.
3. The resolver collapse DECISION F260 D5 places in T003 — `resolve_any_job_id`, the "TWO
   job stores" paragraph, every which-store branch and the absence test — with the classic
   store, which is the same commit range by that decision's own terms.
4. The closure sequence: the integration gate, the evidence job, a fresh review zip, the
   ledger rotation, the STATUS line and the PR.

## Risks

- Step 2 is the largest single commit this repository will take, and each round that
  measures it has found it larger: DECISION F275 D17 sized it at 1766 changed lines, D21 at
  3771 across 263 files, and D22 adds a type pair worth 427 more across 111 files.
- The open set is 87 by distinct id at this round's base `6537ece6` and 86 after this round
  resolves R-0870. Four are High — R-0803, R-0804, R-0806 and R-0807 — all F273's, per
  DECISION F272 D12.
