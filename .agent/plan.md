# Plan — F275 One world completion, part three

Branch: feature/f275-one-world-completion-part-three, cut from `main` at
`a5bf894946ab6de053a4232109d6341a63533768`, the merge commit of pull request 246.

## Goal

Finish what F274 could not reach inside its own limit: the two carry-overs F260's Design
names, DECISION F260 D3, the prototype-cluster deletion itself, the atomic record flip that
T002 rules but does not perform, and the classic runner. Operator ruling amend0908-f275-finish
orders T001 PERFORMED, not prepared.

## Current Step

ROUND 14 books round 13's PASS and one prose slip, registers R-0853 and R-0854, adds one
measured instance to the open finding R-0847 as a NOTE, and deletes the NINTH module group,
`packages/orchestration/local_model_advisor.py`, whole. This is a PRODUCTION round rather than
a deletion round: `orchestrator_brain.py` loses the adapter entry point, two private helpers,
the `advisor` dataclass field and the `advisor` key of the exported decision JSON;
`run_contract.py` loses two `ContractAction` members; and `orchestrator_cmd.py`, `grouped.py`
and `command_catalog.py` lose the `--use-local-advisor` path. Two enum members SURVIVE by
measurement rather than by omission.

## Next Steps

1. The `managed_builder_execution` component, which this round's regeneration makes the
   order file's first line. It is a SINGLE module.
2. The remaining components in the recorded order — every one a single module except the
   `provider_trust` / `provider_trust_verification` pair, which is the last cycle.
3. DECISION F260 D3, the deletion paragraph, with R-0832's fix clause binding it and R-0831,
   R-0840, R-0842, R-0844 through R-0846, R-0848, R-0849 and R-0851 through R-0854 named among
   the ideas deleted rather than inherited. That round also discharges R-0843's widened sweep.
4. T002, the atomic record flip, alone, because every later commit's size depends on its ruling.

## Risks

- The open set is 77 by distinct id at this round's base `16494bbd`; the ledger commit this
  block fixes as C2 registers two, taking it to 79. Four are High — R-0803, R-0804, R-0806 and
  R-0807 — all F273's rather than this feature's, per DECISION F272 D12.
- R-0847 stays OPEN and now holds a second face, measured at this round's dry run: a `GroupDef`
  left behind with no command and no handler passes every catalog guard at exit 0.
- The exported orchestrator decision JSON has NO test pinning its key set, so R-0854's contract
  change is invisible to the suite. That was measured by probe, not assumed.
- The full suite is run SERIALLY: under `pytest -n auto` the `ui_server` command-channel tests
  race for a port, and the vitest node needs `apps/ui/node_modules`.
