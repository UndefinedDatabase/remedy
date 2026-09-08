# Plan — F275 One world completion, part three

Branch: feature/f275-one-world-completion-part-three, cut from `main` at
`a5bf894946ab6de053a4232109d6341a63533768`, the merge commit of pull request 246.

## Goal

Finish what F274 could not reach inside its own limit: the two carry-overs F260's Design
names, DECISION F260 D3, the prototype-cluster deletion itself, the atomic record flip that
T002 rules but does not perform, and the classic runner. Operator ruling amend0908-f275-finish
orders T001 PERFORMED, not prepared.

## Current Step

ROUND 5 books round 4's PASS, confirms R-0831's measurement still holds, and writes the
DELETION ORDER operator RULE 2 requires before the first `git rm`, with a ratchet holding it
against the live import graph. The cluster's internal graph is CYCLIC, so the atomic unit is
the strongly connected component — fifteen of them over twenty-four modules — which DECISION
F275 D2 rules and records. No production file is touched and nothing is deleted.

## Next Steps

1. The FIRST module groups, in the recorded order, one commit each: `context_optimizer`, then
   `review_bundle`. Each commit takes the module, its handler, its catalog entries, its
   cockpit section, its tests and its map lines together, and leaves the tree green.
2. The remaining thirteen components in the recorded order, the three multi-module ones deleted
   as single commits because their members import each other.
3. DECISION F260 D3, the deletion paragraph, with R-0832's fix clause binding it and R-0831 and
   R-0840 named among the ideas deleted rather than inherited.
4. T002, the atomic record flip, alone, because every later commit's size depends on its ruling.

## Risks

- 66 findings are open by distinct id, four of them High — R-0803, R-0804, R-0806 and R-0807 —
  all F273's rather than this feature's, per DECISION F272 D12.
- R-0832 records that the map measures IMPORT edges only, so a consumer coupled to the cluster
  by EVENT NAME is invisible to both the map and the deletion order. The order is a safe
  sequence for imports and is not a completeness claim about couplings.
- The full suite must be run in the PRIMARY checkout: a fresh worktree has no
  `apps/ui/node_modules`, so `test_test_runner.py`'s vitest node fails there for the
  environment rather than for the change.
