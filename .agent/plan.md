# Plan — F275 One world completion, part three

Branch: feature/f275-one-world-completion-part-three, cut from `main` at
`a5bf894946ab6de053a4232109d6341a63533768`, the merge commit of pull request 246.

## Goal

Finish what F274 could not reach inside its own limit: the two carry-overs F260's Design
names, DECISION F260 D3, the prototype-cluster deletion itself, the atomic record flip that
T002 rules but does not perform, and the classic runner. Everything the closure protocol asks
for is on disk: the Built State, the integration gate, the self-use run, the finding
re-assignment, the rotated ledger and a package that reaches READY_FOR_REVIEW.

## Current Step

CLOSURE ROUND B, the last round of this branch. Its bookkeeping commit books round 108's verdict.
Its closure commit then applies the STATUS `[x]` line authored from round 108's measured
values, the README capability sync, `SU-014`'s `consumed_by` set to `F275`, one closure
candidate, and the final handoff, in ONE commit, per the closure protocol's Rule A4 ordering;
then the pull request is opened and NOT merged.

## Next Steps

1. THE NEXT SESSION: Phase 1 rule 1 first, `.agent/STOP`; then the Open PR Gate merges this
   branch's pull request; then the closure candidate this commit records is registered or
   resolved by the first reviewed round; then Rule A5 claims the next feature.

## Risks

- The open findings stand at 89 by distinct id. Four are High — R-0803, R-0804, R-0806 and
  R-0807 — all F273's per DECISION F272 D12, and the integrity gate's `high_blockers_open`
  check does not see them, which is R-0648; so the close is PASS_WITH_RISKS.
- The closure commit is the last commit on the branch, so the docs gate its own STATUS and
  README edits must satisfy runs after it; the reviewer ran that gate against the same edits in
  a disposable worktree before authoring.
- A DRY-RUN PACKAGE IS IN THE ARCHIVE: `remedy-review-20260914-230148-READY_FOR_REVIEW.zip`
  was built from the reviewer's throwaway head `847335e2` and is NOT the closure package.
