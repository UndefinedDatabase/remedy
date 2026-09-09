# Plan — F275 One world completion, part three

Branch: feature/f275-one-world-completion-part-three, cut from `main` at
`a5bf894946ab6de053a4232109d6341a63533768`, the merge commit of pull request 246.

## Goal

Finish what F274 could not reach inside its own limit: the two carry-overs F260's Design
names, DECISION F260 D3, the prototype-cluster deletion itself, the atomic record flip that
T002 rules but does not perform, and the classic runner. Operator ruling amend0908-f275-finish
orders T001 PERFORMED, not prepared.

## Current Step

ROUND 11 books round 10's PASS and four prose slips, registers R-0847, R-0848 and R-0849,
closes F260's SECOND carry-over as a NOTE on R-0831 — the route-policy audit re-measured, a
finding update and never a rebuild — releases DECISION F274 D4's hold on the builder-routing
cockpit section as DECISION F275 D5, and deletes the SIXTH module group and the second that is
a strongly connected COMPONENT: `builder_routing`, `candidate_quality`,
`local_candidate_generator` and `model_route_tournament`, whole, in ONE commit under DECISION
F275 D2. With them go four handler files, 14 catalog entries, the `builder-routing`,
`candidate-quality`, `local-candidate` and `tournament` groups WHOLE, nine test files, five doc
pages and nine index rows. `apps/cli/commands/external_builder_cmd.py` SURVIVES and loses one
of its eight handlers; `packages/orchestration/worker_registry.py` SURVIVES and loses the
next-action it gave a local-candidate worker. Both losses are registered.

## Next Steps

1. The `execution_approval_policy` component, which this round's regeneration makes the order
   file's first line. It is a SINGLE module, so it is an ordinary group commit.
2. The remaining components in the recorded order — after this round every one is a single
   module except the `provider_trust` / `provider_trust_verification` pair, which is the last
   cycle in the cluster.
3. DECISION F260 D3, the deletion paragraph, with R-0832's fix clause binding it and R-0831,
   R-0840, R-0842, R-0844, R-0845, R-0846, R-0848 and R-0849 named among the ideas deleted
   rather than inherited.
4. T002, the atomic record flip, alone, because every later commit's size depends on its ruling.

## Risks

- The open set is 71 by distinct id at this round's base `cb89bbc3`; the ledger commit this
  block fixes as C2 registers three, taking it to 74. Four are High — R-0803, R-0804, R-0806
  and R-0807 — all F273's rather than this feature's, per DECISION F272 D12.
- R-0847 is a GATE defect, not only a code defect: `tests/cli/test_advertised_commands.py`
  cannot see an advertisement whose group has been deleted, so this round's four whole-group
  deletions widen a blind spot the same round registers. No later deletion round may rely on
  that guard to catch its own dead advertisements.
- The full suite is run SERIALLY: under `pytest -n auto` the `ui_server` command-channel tests
  race for a port, and the vitest node needs `apps/ui/node_modules`, absent from any worktree.
