# Plan — F275 One world completion, part three

Branch: feature/f275-one-world-completion-part-three, cut from `main` at
`a5bf894946ab6de053a4232109d6341a63533768`, the merge commit of pull request 246.

## Goal

Finish what F274 could not reach inside its own limit: the two carry-overs F260's Design
names, DECISION F260 D3, the prototype-cluster deletion itself, the atomic record flip that
T002 rules but does not perform, and the classic runner. Operator ruling amend0908-f275-finish
orders T001 PERFORMED, not prepared.

## Current Step

ROUND 9 books round 8's PASS, resolves R-0841, registers R-0843 and R-0844, and deletes the
FOURTH module group, `review_bundle` — the module, its ONE catalog entry `review.bundle`, the
one handler function inside `apps/cli/commands/review_cmd.py` that imports it, its two test
files, the two `docs/system/` pages whose subject it is, the string-keyed doctor probe no
import graph can see, and the surviving test call sites. The file `review_cmd.py`, the
`review` command group and its four other commands SURVIVE: they drive
`packages/orchestration/reviewer.py`, which is not on F260's Design list.

## Next Steps

1. The `dogfood_run` / `feature_planner` / `overnight_mission` / `progress_ledger` /
   `repair_loop_v2` / `self_repair_proposal` component, which this round's regeneration makes
   the order file's first line. Its six modules import each other, so DECISION F275 D2 makes
   the whole component one commit.
2. The remaining components in the recorded order, the multi-module ones as single commits
   because their members import each other.
3. DECISION F260 D3, the deletion paragraph, with R-0832's fix clause binding it and R-0831,
   R-0840, R-0842 and R-0844 named among the ideas deleted rather than inherited.
4. T002, the atomic record flip, alone, because every later commit's size depends on its ruling.

## Risks

- The open set is 68 by distinct id at this round's base `aae6d313`; the ledger commit this
  block fixes as C2 resolves R-0841 and registers R-0843 and R-0844, taking it to 69. Four are
  High — R-0803, R-0804, R-0806 and R-0807 — all F273's rather than this feature's, per
  DECISION F272 D12.
- R-0832 records that the map measures IMPORT edges only. `review_bundle` has NO line in
  `cluster_deletion_map.txt` and yet has a live importer: a STRING-keyed `importlib` probe in
  `apps/cli/commands/worker_facade_cmd.py`. An AST sweep sees none of it.
- The full suite is run SERIALLY. Under `pytest -n auto` the `ui_server` command-channel tests
  race for a server port and the vitest node needs `apps/ui/node_modules`.
