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

ROUND 46 books round 45's PASS verdict and the resolution of R-0875, and records what a DRY
RUN of the flip measured at `978046fe`. Applied as a mechanical `ast` transformation the flip
produces a parseable tree that collects 18394 tests with zero collection errors, and the suite
then reads 2714 failed, 15551 passed and 106 errors. The failures classify into six classes,
and the largest that no decision has ruled is the ID SHAPE: `Job.id` and `Task.id` are
`uuid.UUID` while the unified record spells both `str`, and that type reaches `Artifact`,
`TaskExecutionContext` and `PatchIntentSet` — three models no artefact of this feature
enumerates. DECISION F275 D26 records the finding and the route.

## Next Steps

1. THE ID-SHAPE MIGRATION, as its own commit or commits before the flip, on the pattern
   DECISION F275 D22 and D23 set: measure the sites, then widen. It is the prerequisite the
   flip's three enumerations each recorded as a bound and never sized.
2. THE FOUR TRANSFORM RULES the dry run added to DECISION F275 D25's two, all in
   `.agent/f275_t003_flip_residue.md` section 3: the seam's own imports move with the seam,
   a mixed import is SPLIT rather than moved, the type imports move their MODULE PATH, and a
   construction whose keywords arrive through a `**` splat is invisible to a keyword rewrite.
3. THE FLIP, once the classes above are gone from the dry run's residue, still as the one
   declared-oversize commit AGENTS.md permits per feature, declared with its inseparability
   reason before review.
4. The resolver collapse DECISION F260 D5 places in T003, with the classic store. Then the
   closure sequence: the integration gate, the evidence job, a fresh review zip, the ledger
   rotation, the STATUS line and the PR.

## Risks

- F275 stands at 46 rounds and 19 sessions against the operator's soft limit of 60 rounds and
  20 sessions. The NEXT session is the twentieth and owes a scope report under
  amend0908-f275-finish rule 1; that rule also forbids the split-and-close default here.
- The open set is 86 by distinct id once this round books `Done: R-0875`. Four are High —
  R-0803, R-0804, R-0806 and R-0807 — all F273's, per DECISION F272 D12.
