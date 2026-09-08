# Plan — F275 One world completion, part three

Branch: feature/f275-one-world-completion-part-three, cut from `main` at
`a5bf894946ab6de053a4232109d6341a63533768`, the merge commit of pull request 246.

## Goal

Finish what F274 could not reach inside its own limit: the two carry-overs F260's Design
names, DECISION F260 D3, the prototype-cluster deletion itself, the atomic record flip that
T002 rules but does not perform, and the classic runner. Operator ruling amend0908-f275-finish
orders T001 PERFORMED, not prepared.

## Current Step

ROUND 6 books round 5's PASS and performs THE FIRST `git rm` of this feature: the
`context_optimizer` module group — the module, its handler, its two catalog entries, the
`related` tuple naming one of them, its tests, its allowlist and cluster-map lines, and the
humanize-catalog entry for the event only that handler emitted. The deletion order file is
REGENERATED from the live graph rather than line-edited, because removing the module reorders
the condensation.

## Next Steps

1. The `review_bundle` group, the order file's new first line, in its own commit.
2. The remaining components in the recorded order, the multi-module ones as single commits
   because their members import each other.
3. DECISION F260 D3, the deletion paragraph, with R-0832's fix clause binding it and R-0831
   and R-0840 named among the ideas deleted rather than inherited.
4. T002, the atomic record flip, alone, because every later commit's size depends on its ruling.

## Risks

- 66 findings are open by distinct id, four of them High — R-0803, R-0804, R-0806 and R-0807 —
  all F273's rather than this feature's, per DECISION F272 D12.
- R-0832 records that the map measures IMPORT edges only, so a consumer coupled to the cluster
  by EVENT NAME is invisible to both the map and the deletion order. Round 6 measured that
  coupling for real: `tests/ui_contracts/test_humanize_catalog.py` pins the UI catalog's keys
  to the Python emitters, so every group whose module emits an event edits that catalog too.
- The full suite runs in the PRIMARY checkout: a fresh worktree may lack `apps/ui/node_modules`
  or a built `apps/ui/dist`, and both failure classes are the environment rather than the change.
