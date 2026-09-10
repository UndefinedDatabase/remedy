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

ROUND 38 does two things. It repairs the last surviving instance of R-0870's class, a
"Planned migration path" list that still names the deleted `approval` group and the deleted
`progress` command in the present tense, which the round 37 pair missed four lines below its
own span. And it enumerates the CLASSIC STORE SEAM — 821 calls of `save_job`, `load_job`,
`load_job_safe` and `resolve_job_id` across 152 files, 44 of them holding no enumerated
`.id` or `.name` site — which is the half of the flip DECISION F275 D17 gave no site list.
R-0870 STAYS OPEN until the reviewer's `Done:` text lands.

## Next Steps

1. Measure the last part of the flip remainder — the sites that treat a job id as a UUID
   rather than as a 16-hex string — and then a dated DECISION ruling the route on the
   complete figure, as T002's DECISION F275 D17 ruled it on the partial one.
2. The flip itself, applied from the round 36 enumeration and the round 38 seam list, as
   the one declared-oversize commit AGENTS.md permits per feature, with the inseparability
   reason stated in the handback BEFORE review.
3. The resolver collapse DECISION F260 D5 places in T003 — `resolve_any_job_id`, the "TWO
   job stores" paragraph, every which-store branch and the absence test — with the classic
   store, which is the same commit range by that decision's own terms.
4. The closure sequence: the integration gate, the evidence job, a fresh review zip, the
   ledger rotation, the STATUS line and the PR.

## Risks

- Step 2 is the largest single commit this repository will take and it spends the one
  declared-oversize allowance AGENTS.md rations per feature. Steps 1 and the round 38
  enumeration exist because that allowance can be spent once and the size it must cover
  was measured only in part.
- The open set is 87 by distinct id at this round's base `4921e117`. This round registers
  none and resolves none. Four are High — R-0803, R-0804, R-0806 and R-0807 — all F273's,
  per DECISION F272 D12.
