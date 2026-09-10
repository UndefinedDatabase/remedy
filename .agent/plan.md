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

ROUND 36 re-derives the T002 flip site set AT T003's OWN BASE, which DECISION F275 D17 orders
by name, and ENUMERATES it file by file into `.agent/f275_t003_flip_sites.md` so the flip
commit is applied from a committed list rather than from a fresh measurement. The same round
repairs the third and fourth instances of R-0870 — a docstring sentence falsified by a later
deletion, and a test whose name and docstring outlived the assertion they described. R-0870
STAYS OPEN until the reviewer's `Done:` text lands.

## Next Steps

1. The flip DECISION F275 D17 sized, applied from the round 36 enumeration, as the one
   declared-oversize commit AGENTS.md permits per feature, with the inseparability reason
   stated in the handback BEFORE review.
2. The resolver collapse DECISION F260 D5 places in T003 — `resolve_any_job_id`, the "TWO
   job stores" paragraph, every which-store branch and the absence test — with the classic
   store, which is the same commit range by that decision's own terms.
3. Amend DECISION F260 D3 by APPENDING a dated correction that names the nineteen deleted
   `apps/cli/commands/*_cmd.py` handler modules its mapping does not name, so the feature
   file's DONE condition "names every deleted module" is met on a reading rather than on an
   inference. D3's own landed text is NOT rewritten.
4. The closure sequence: the integration gate, the evidence job, a fresh review zip, the
   ledger rotation, the STATUS line and the PR.

## Risks

- Step 1 is the largest single commit this repository will take and it spends the one
  declared-oversize allowance AGENTS.md rations per feature.
- The open set is 87 by distinct id at this round's base `965ea50d`. This round registers
  none and resolves none. Four are High — R-0803, R-0804, R-0806 and R-0807 — all F273's,
  per DECISION F272 D12.
