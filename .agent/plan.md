# Plan — F275 One world completion, part three

Branch: feature/f275-one-world-completion-part-three, cut from `main` at
`a5bf894946ab6de053a4232109d6341a63533768`, the merge commit of pull request 246.

## Goal

Finish what F274 could not reach inside its own limit: the two carry-overs F260's Design
names, DECISION F260 D3, the prototype-cluster deletion itself, the atomic record flip that
T002 rules but does not perform, and the classic runner. T001 runs FIRST, and its `git rm`
sequence is never started by a session that cannot finish it.

## Current Step

ROUND 1 claims F275 in the roadmap ledger, cuts the branch, re-points this file and
`.agent/context.md`, re-heads `.agent/live_review.md`, books F274's branch-terminating round
23 verdict into it, and records DECISION F275 D1 — which rules the first carry-over's
destination module, its measured definition partition and its staging. The round's code commit
lands the FIRST staged batch of `packages/orchestration/mission_readiness.py`, UNWIRED, so no
consumer moves and the tree is green at every commit boundary.

## Next Steps

1. The SECOND staged batch completes `mission_readiness.py`, still unwired, and lands the test
   file named after it.
2. The wiring round gives the CLI and the cockpit the carried readiness view, cuts the one
   surviving `packages/orchestration/ui_server.py` edge the deletion map records for
   `overnight_readiness`, and removes that line from the map in the SAME commit, which is what
   `tests/orchestration/test_cluster_deletion_map.py` requires of every cut.
3. DECISION F260 D3, the deletion paragraph, drafted with R-0832's fix clause binding it and
   R-0831 named among the ideas deleted rather than inherited.
4. The prototype-cluster deletion itself, bounded by the map's edges, one commit per module
   group, under the four measurements amend0906-triage-throughput names for a deletion round.

## Risks

- 65 findings are open by distinct id, four of them High — R-0803, R-0804, R-0806 and R-0807 —
  all F273's rather than this feature's, per DECISION F272 D12. The integrity gate's
  `high_blockers_open` check is WRONG about them, which is R-0648 and itself open.
- The first carry-over moves 655 lines of definitions, which exceeds the DECISION F104 D1 cap
  of 500 insertions for one commit, so it is staged across commits and the new module stays
  unwired until the last of them. This feature's single declared-oversize allowance is
  reserved for T002's atomic flip, which cannot be staged at all.
