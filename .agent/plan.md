# Plan — F275 One world completion, part three

Branch: feature/f275-one-world-completion-part-three, cut from `main` at
`a5bf894946ab6de053a4232109d6341a63533768`, the merge commit of pull request 246.

## Goal

Finish what F274 could not reach inside its own limit: the two carry-overs F260's Design
names, DECISION F260 D3, the prototype-cluster deletion itself, the atomic record flip that
T002 rules but does not perform, and the classic runner. Operator ruling amend0908-f275-finish
orders T001 PERFORMED, not prepared.

## Current Step

ROUND 16 books round 15's PASS, five prose slips and the resolution of R-0855, registers R-0859
and R-0860, and deletes the ELEVENTH module group,
`packages/orchestration/main_builder_adapter.py`, whole. This is a PRODUCTION round: the
`builder` group and its ten commands go, six `ContractAction` members go, and
`worker_facade_cmd.py` loses three of its five commands — `worker doctor`, `worker add` and
`worker disable` — which R-0857's fix clause orders deleted whole rather than narrowed a second
time.

## Next Steps

1. The `overnight_executor` component, which this round's regeneration makes the order file's
   first line. It is a SINGLE module.
2. The remaining components in the recorded order — `worker_registry`, then
   `overnight_readiness`, then the `provider_trust` / `provider_trust_verification` pair, which
   is the last cycle.
3. DECISION F260 D3, the deletion paragraph, with R-0832's fix clause binding it and R-0831,
   R-0840, R-0842, R-0844 through R-0846, R-0848, R-0849 and R-0851 through R-0860 named among
   the ideas deleted rather than inherited. That round also discharges R-0843's widened sweep
   and R-0858's repair of F267.
4. T002, the atomic record flip, alone, because every later commit's size depends on its
   ruling.

## Risks

- The open set is 83 by distinct id at this round's base `38e03d2f`; the ledger commit this
  block fixes as C2 registers two and resolves one, taking it to 84. Four are High — R-0803,
  R-0804, R-0806 and R-0807 — all F273's rather than this feature's, per DECISION F272 D12.
- This round removes three USER-FACING commands and a documented step from the core product
  spine. R-0860 records the loss and its inheritor; no stub, shim or alias replaces them.
- The full suite is run SERIALLY: under `pytest -n auto` the `ui_server` command-channel tests
  race for a port, and the vitest node needs `apps/ui/node_modules`.
