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

ROUND 35 lands the SECOND MEASUREMENT finding R-0832 asks for: a ratchet that records
EVENT-NAME couplings from deleted modules to surviving readers, which the retired import map
could not see. It measures 43 deleted modules, two event names they emitted and exactly one
dead coupling, `context_budget_optimized`. R-0832 STAYS OPEN: its second half — ruling how
each coupling is disposed of — belongs to the round that drafts DECISION F260 D3.

## Next Steps

1. DECISION F260 D3: name all 43 deleted modules and the feature that inherited each one,
   rule the disposal of every dead event coupling the round 35 ratchet reports, and delete
   what that ruling condemns. This discharges the second half of R-0832 and is the last
   thing T001 owes.
2. The flip DECISION F275 D17 sized, as the one declared-oversize commit AGENTS.md permits
   per feature, re-deriving the site set at its own base with the DECISION F272 D7
   descriptor probe rather than inheriting round 31's figures.
3. The resolver collapse DECISION F260 D5 places in T003 — `resolve_any_job_id`, the "TWO
   job stores" paragraph, every which-store branch and the absence test — with the classic
   store, which is the same commit range by that decision's own terms.
4. The closure sequence: the integration gate, the evidence job, a fresh review zip, the
   ledger rotation, the STATUS line and the PR.

## Risks

- Step 2 is the largest single commit this repository will take and it spends the one
  declared-oversize allowance AGENTS.md rations per feature. It needs its own session.
- The open set is 87 by distinct id at this round's base `df5d527f`. This round registers
  none and resolves none. Four are High — R-0803, R-0804, R-0806 and R-0807 — all F273's,
  per DECISION F272 D12.
