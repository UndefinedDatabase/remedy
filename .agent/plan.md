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

ROUND 44 clears the tree the flip has to run over. A dry run of the flip found FORTY keyword
arguments passed to `Job(...)` and `Task(...)` that name no field on either model: pydantic
drops them silently, so forty test call sites have never done what they say, and four of them
make the flip's own rewrite produce `TaskEntry(title=..., title=...)`, which does not compile.
This round deletes 35, repoints the 5 that meant `user_prompt`, lands a source guard so the
class cannot return, and registers R-0875. DECISION F275 D25 carries the ruling and the two
mechanical rules the dry run had to learn: edits at `ast` columns are BYTE offsets, and the
flip must rewrite an import's MODULE PATH and not only the name it imports.

## Next Steps

1. THE FLIP, now that its target API exists (round 42), its record shapes are measured
   (round 43) and its tree is clean (this round). The dry run at `c0e9dd10` measured it at
   284 files and 4856 insertions once construction keywords are included, against DECISION
   F275 D21's 3771 changed lines — it is DECLARED at what the round itself measures, before
   review, as the one oversize commit AGENTS.md permits per feature. It also registers
   `Task.acceptance_checks`'s structured form as a finding naming the feature that owns
   acceptance criteria, per amend0908-f275-finish rule 4.
2. The resolver collapse DECISION F260 D5 places in T003 — `resolve_any_job_id`, the "TWO
   job stores" paragraph, every which-store branch and the absence test — with the classic
   store, which is the same commit range by that decision's own terms.
3. The closure sequence: the integration gate, the evidence job, a fresh review zip, the
   ledger rotation, the STATUS line and the PR.

## Risks

- Step 1 is the largest single commit this repository will take, and the dry run's 4856
  insertions is higher than every earlier estimate. The route is unchanged because AGENTS.md
  permits exactly one declared-oversize commit per feature and every alternative needs two.
- The open set is 86 by distinct id at this round's base `c0e9dd10` and 87 from C2, where
  R-0875 is registered. Four are High — R-0803, R-0804, R-0806 and R-0807 — all F273's, per
  DECISION F272 D12.
