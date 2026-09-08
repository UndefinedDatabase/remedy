# Plan — F275 One world completion, part three

Branch: feature/f275-one-world-completion-part-three, cut from `main` at
`a5bf894946ab6de053a4232109d6341a63533768`, the merge commit of pull request 246.

## Goal

Finish what F274 could not reach inside its own limit: the two carry-overs F260's Design
names, DECISION F260 D3, the prototype-cluster deletion itself, the atomic record flip that
T002 rules but does not perform, and the classic runner. T001 runs FIRST, and its `git rm`
sequence is never started by a session that cannot finish it.

## Current Step

ROUND 2 books round 1's PASS verdict and its four reviewer-prose slips into the record, then
COMPLETES the first carry-over's code move: the second and last staged batch of
`packages/orchestration/mission_readiness.py`, which brings the carried set to all twenty-nine
definitions, and the test file named after that module. The module is STILL UNWIRED at the end
of this round — no consumer imports it and no cluster edge is cut yet — so every commit
boundary stays green.

## Next Steps

1. The wiring round gives the CLI and the cockpit the carried readiness view as
   `mission readiness`, cuts the one surviving `packages/orchestration/ui_server.py` edge the
   deletion map records for `overnight_readiness`, and removes that line from the map in the
   SAME commit, which is what `tests/orchestration/test_cluster_deletion_map.py` requires.
2. DECISION F260 D3, the deletion paragraph, drafted with R-0832's fix clause binding it and
   R-0831 named among the ideas deleted rather than inherited.
3. The prototype-cluster deletion itself, bounded by the map's edges, one commit per module
   group, under the four measurements amend0906-triage-throughput names for a deletion round.
   It is not started by a session that cannot finish it.

## Risks

- 65 findings are open by distinct id, four of them High — R-0803, R-0804, R-0806 and R-0807 —
  all F273's rather than this feature's, per DECISION F272 D12. The integrity gate's
  `high_blockers_open` check is WRONG about them, which is R-0648 and itself open.
- The carried module is dead code until the wiring round, by design and by DECISION F275 D1.
  That is the price of staying under the DECISION F104 D1 cap of 500 insertions per commit;
  this feature's single declared-oversize allowance is reserved for T002's atomic flip.
