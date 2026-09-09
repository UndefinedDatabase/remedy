# Plan — F275 One world completion, part three

Branch: feature/f275-one-world-completion-part-three, cut from `main` at
`a5bf894946ab6de053a4232109d6341a63533768`, the merge commit of pull request 246.

## Goal

Finish what F274 could not reach inside its own limit: the two carry-overs F260's Design
names, DECISION F260 D3, the prototype-cluster deletion itself, the atomic record flip that
T002 rules but does not perform, and the classic runner. Operator ruling amend0908-f275-finish
orders T001 PERFORMED, not prepared.

## Current Step

ROUND 20 deletes the `worker_registry` module group — the module, its handler, the whole
`route-policy` command group, the three `worker.registry-*` commands, its cockpit section,
four `ContractAction` members and two documentation pages. DECISION F275 D9, committed
before the first `git rm`, rules that the surviving `token_economy.py` degrades FAIL-SAFE
rather than dying: no route spec resolves, so approval becomes unconditional and the R-0095
hard-safety floor holds by degradation. The round books round 19's PASS verdict and
registers R-0865.

## Next Steps

1. The `provider_trust` / `provider_trust_verification` pair, which is the last cycle and
   the last component of the deletion order.
2. DECISION F260 D3, the deletion paragraph, with R-0832's fix clause binding it and the
   open ids named among the ideas deleted rather than inherited. That round also discharges
   R-0843's widened sweep, R-0858's repair of F267 and R-0859's referential-closure test.
3. T002, the atomic record flip, alone, because every later commit's size depends on it.
4. T003, the classic runner, which T002's ruling is the prerequisite for.

## Risks

- The open set is 87 by distinct id at this round's base `0d18e58a`. Round 20 registers one,
  taking it to 88. Four are High — R-0803, R-0804, R-0806 and R-0807 — all F273's rather
  than this feature's, per DECISION F272 D12.
- Worst on this round: a surviving production module loses an approval-forcing invariant.
  The mutation red-proof is ordered in full and its STOP condition blocks the commit.
- R-0847 again: deleting a whole command group removes it from the advertised-command
  guard's `GROUPS`, so the guard goes blind exactly when the group's advertisements go
  dead. The sweep is read by hand, as its RAW list.
- The full suite is run SERIALLY: under `pytest -n auto` the `ui_server` command-channel
  tests race for a port.
