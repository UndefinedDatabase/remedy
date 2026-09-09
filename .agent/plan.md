# Plan — F275 One world completion, part three

Branch: feature/f275-one-world-completion-part-three, cut from `main` at
`a5bf894946ab6de053a4232109d6341a63533768`, the merge commit of pull request 246.

## Goal

Finish what F274 could not reach inside its own limit: the two carry-overs F260's Design
names, DECISION F260 D3, the prototype-cluster deletion itself, the atomic record flip that
T002 rules but does not perform, and the classic runner. Operator ruling amend0908-f275-finish
orders T001 PERFORMED, not prepared.

## Current Step

ROUND 17 is a REPAIR round. Round 16's gate G4 went red because three operator-facing sections
of `docs/guides/simple-operator-quickstart-v0.md` still advertised `worker doctor`, `worker
add` and `worker disable` after the commit that deleted them; the reviewer's change set never
named that file. This round books round 16's FAIL verdict, registers R-0861 and sweeps every
surviving advertisement across three documentation pages, replacing the core product spine's
worker section with the deliberate-absence note AGENTS.md requires.

## Next Steps

1. The `overnight_executor` component, the order file's first line. It is a SINGLE module.
2. The remaining components in the recorded order — `worker_registry`, then
   `overnight_readiness`, then the `provider_trust` / `provider_trust_verification` pair,
   which is the last cycle.
3. DECISION F260 D3, the deletion paragraph, with R-0832's fix clause binding it and R-0831,
   R-0840, R-0842, R-0844 through R-0846, R-0848, R-0849 and R-0851 through R-0861 named among
   the ideas deleted rather than inherited. That round also discharges R-0843's widened sweep,
   R-0858's repair of F267 and R-0859's referential-closure test.
4. T002, the atomic record flip, alone, because every later commit's size depends on its
   ruling.

## Risks

- The open set is 84 by distinct id at this round's base `12dd60ad`; the ledger commit this
  block fixes as C2 registers one, taking it to 85. Four are High — R-0803, R-0804, R-0806 and
  R-0807 — all F273's rather than this feature's, per DECISION F272 D12.
- The advertised-commands guard did NOT catch these three sections, which is R-0847's blindness
  measured a third time. Until R-0847 is fixed, every deletion round of this feature runs the
  token sweep by hand and reads its RAW list, not only its stripped count.
- The full suite is run SERIALLY: under `pytest -n auto` the `ui_server` command-channel tests
  race for a port, and the vitest node needs `apps/ui/node_modules`.
