# Plan — F275 One world completion, part three

Branch: feature/f275-one-world-completion-part-three, cut from `main` at
`a5bf894946ab6de053a4232109d6341a63533768`, the merge commit of pull request 246.

## Goal

Finish what F274 could not reach inside its own limit: the two carry-overs F260's Design
names, DECISION F260 D3, the prototype-cluster deletion itself, the atomic record flip that
T002 rules but does not perform, and the classic runner. Operator ruling amend0908-f275-finish
orders T001 PERFORMED, not prepared.

## Current Step

ROUND 15 books round 14's PASS and one prose slip, registers R-0855 through R-0858, records
DECISION F275 D7 on the approval gate, sweeps the survivor state R-0855 names, and deletes the
TENTH module group, `packages/orchestration/managed_builder_execution.py`, whole. This is a
PRODUCTION round: `worker_facade_cmd.py` loses the template half of three user-facing
commands, `exec_guard.py` loses seven prose citations of the dying module, `run_contract.py`
loses fourteen `ContractAction` members, and the catalog loses the `execution` group with
seventeen commands.

## Next Steps

1. The `main_builder_adapter` component, which this round's regeneration moves from position
   four to position one of the order file. It takes the adapter half of the three `worker`
   commands this round halved.
2. The remaining components in the recorded order — each a single module except the
   `provider_trust` / `provider_trust_verification` pair, which is the last cycle.
3. DECISION F260 D3, the deletion paragraph, with R-0832's fix clause binding it and R-0831,
   R-0840, R-0842, R-0844 through R-0846, R-0848, R-0849 and R-0851 through R-0857 named among
   the ideas deleted rather than inherited. That round also discharges R-0843's widened sweep.
4. T002, the atomic record flip, alone, because every later commit's size depends on its
   ruling.

## Risks

- The open set is 79 by distinct id at this round's base `fadf4715`; the ledger commit this
  block fixes as C2 registers four, taking it to 83. Four are High — R-0803, R-0804, R-0806
  and R-0807 — all F273's rather than this feature's, per DECISION F272 D12.
- Deleting `remedy execution approve` deletes a HUMAN approval command. DECISION F275 D7 rules
  that this leaves no ungated path because the executor it gates dies in the same commit, and
  records the measurement behind it rather than asserting it.
- The full suite is run SERIALLY: under `pytest -n auto` the `ui_server` command-channel tests
  race for a port, and the vitest node needs `apps/ui/node_modules`.
