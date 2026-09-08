# Plan — F275 One world completion, part three

Branch: feature/f275-one-world-completion-part-three, cut from `main` at
`a5bf894946ab6de053a4232109d6341a63533768`, the merge commit of pull request 246.

## Goal

Finish what F274 could not reach inside its own limit: the two carry-overs F260's Design
names, DECISION F260 D3, the prototype-cluster deletion itself, the atomic record flip that
T002 rules but does not perform, and the classic runner. Operator ruling amend0908-f275-finish
orders T001 PERFORMED, not prepared.

## Current Step

ROUND 10 books round 9's PASS, registers R-0845 and R-0846, and deletes the FIFTH module
group and the first that is a strongly connected COMPONENT: `dogfood_run`, `feature_planner`,
`overnight_mission`, `progress_ledger`, `repair_loop_v2` and `self_repair_proposal`, whole,
in ONE commit under DECISION F275 D2. With them go their five handler files, 38 catalog
entries, the `dogfood`, `progress` and `self-repair` groups, eleven test files, five doc
pages and the surviving call sites. `apps/cli/commands/worker_facade_cmd.py` SURVIVES and
loses the dogfood mode of `mission run`; `packages/orchestration/main_builder_adapter.py`
SURVIVES and loses its `remedy repair evaluate` next-action. Both losses are registered.

## Next Steps

1. The `builder_routing` / `candidate_quality` / `local_candidate_generator` /
   `model_route_tournament` component, which this round's regeneration makes the order
   file's first line. Its four modules import each other, so DECISION F275 D2 makes the
   whole component one commit.
2. The remaining components in the recorded order, the single-module ones as ordinary
   group commits and the two-module `provider_trust` pair as one.
3. DECISION F260 D3, the deletion paragraph, with R-0832's fix clause binding it and
   R-0831, R-0840, R-0842, R-0844, R-0845 and R-0846 named among the ideas deleted rather
   than inherited.
4. T002, the atomic record flip, alone, because every later commit's size depends on its ruling.

## Risks

- The open set is 69 by distinct id at this round's base `982d016b`; the ledger commit this
  block fixes as C2 registers R-0845 and R-0846, taking it to 71. Four are High — R-0803,
  R-0804, R-0806 and R-0807 — all F273's rather than this feature's, per DECISION F272 D12.
- The two carry-overs F260's Design orders before the first `git rm` ARE DONE: `mission
  readiness` landed in round 3 and `mission report` in round 4, and `Gate: F275 R4` records
  both. No carry-over work is owed by this round or any later one.
- `tests/test_grouped_cli.py` parametrises over the catalog, so 24 of this round's 381
  collected-id fall come from a file the deletion never names. A file-level reading of the
  fall cannot close; only the id-set difference can.
- The full suite is run SERIALLY. Under `pytest -n auto` the `ui_server` command-channel
  tests race for a server port and the vitest node needs `apps/ui/node_modules`.
