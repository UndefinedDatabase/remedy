# Plan — F275 One world completion, part three

Branch: feature/f275-one-world-completion-part-three, cut from `main` at
`a5bf894946ab6de053a4232109d6341a63533768`, the merge commit of pull request 246.

## Goal

Finish what F274 could not reach inside its own limit: the two carry-overs F260's Design
names, DECISION F260 D3, the prototype-cluster deletion itself, the atomic record flip that
T002 rules but does not perform, and the classic runner. Operator ruling amend0908-f275-finish
orders T001 PERFORMED, not prepared.

## Current Step

ROUND 19 deletes the `overnight_readiness` module group, the first line of the regenerated
deletion order. It takes the WHOLE `overnight` command group with it — the GroupDef, the
three remaining read-only commands, the handler file round 18 left alive, and two test
files — because `mission_readiness.py` has carried the same capability since rounds 1 and 2
and `remedy mission readiness` and `remedy mission report` already serve every reader. It
also books round 18's PASS verdict and registers R-0864.

## Next Steps

1. `worker_registry`, the next component of the order file.
2. Then the `provider_trust` / `provider_trust_verification` pair, which is the last cycle
   and the last component.
3. DECISION F260 D3, the deletion paragraph, with R-0832's fix clause binding it and the
   open ids named among the ideas deleted rather than inherited. That round also discharges
   R-0843's widened sweep, R-0858's repair of F267 and R-0859's referential-closure test.
4. T002, the atomic record flip, alone, because every later commit's size depends on it.

## Risks

- The open set is 86 by distinct id at this round's base `c878073e`. Round 19 registers one,
  taking it to 87. Four are High — R-0803, R-0804, R-0806 and R-0807 — all F273's rather
  than this feature's, per DECISION F272 D12.
- R-0847 is worst on this round: deleting a whole command group removes it from the
  advertised-command guard's `GROUPS`, so the guard goes blind exactly when the group's
  advertisements go dead. The sweep is read by hand, as its RAW list.
- The full suite is run SERIALLY: under `pytest -n auto` the `ui_server` command-channel
  tests race for a port, and the vitest node needs `apps/ui/node_modules`.
