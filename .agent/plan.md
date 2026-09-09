# Plan — F275 One world completion, part three

Branch: feature/f275-one-world-completion-part-three, cut from `main` at
`a5bf894946ab6de053a4232109d6341a63533768`, the merge commit of pull request 246.

## Goal

Finish what F274 could not reach inside its own limit: the two carry-overs F260's Design
names, DECISION F260 D3, the prototype-cluster deletion itself, the atomic record flip that
T002 rules but does not perform, and the classic runner. Operator ruling amend0908-f275-finish
orders T001 PERFORMED, not prepared.

## Current Step

ROUND 12 books round 11's PASS and two prose slips, registers R-0850 and R-0851, records
DECISION F275 D6 — that F275's "Do not touch" protects the APPROVAL GATE F017 owns and not
`execution_approval_policy.py`, which F260's own Design section lists for deletion — and deletes
the SEVENTH module group: `packages/orchestration/execution_approval_policy.py`, whole, in ONE
commit. With it go its 1197-line test file, its doc page, six `approval.policy-*` commands and
the `approval` group WHOLE. `apps/cli/commands/worker_facade_cmd.py` SURVIVES and loses six of
its eleven handlers; `_cmd_doctor_core` SURVIVES and loses one diagnostic probe, so
`remedy doctor` is untouched. The command loss is registered as R-0851.

## Next Steps

1. The `external_builder_sandbox` component, which this round's regeneration makes the order
   file's first line. It is a SINGLE module, and round 11 already measured that
   `apps/cli/commands/external_builder_cmd.py` holds seven handlers driving it, so that file
   dies with it rather than losing one handler as it did in round 11.
2. The remaining components in the recorded order — every one a single module except the
   `provider_trust` / `provider_trust_verification` pair, which is the last cycle.
3. DECISION F260 D3, the deletion paragraph, with R-0832's fix clause binding it and R-0831,
   R-0840, R-0842, R-0844 through R-0846, R-0848, R-0849 and R-0851 named among the ideas
   deleted rather than inherited.
4. T002, the atomic record flip, alone, because every later commit's size depends on its ruling.

## Risks

- The open set is 74 by distinct id at this round's base `21c90fe5`; the ledger commit this
  block fixes as C2 registers two, taking it to 76. Four are High — R-0803, R-0804, R-0806 and
  R-0807 — all F273's rather than this feature's, per DECISION F272 D12.
- R-0847 stays OPEN and binds every remaining deletion round: `test_advertised_commands.py`
  cannot see an advertisement whose group has been deleted, so a round that deletes a group
  WHOLE must sweep the spaced `remedy <group> <sub>` form by hand. This round swept it and
  found zero.
- The full suite is run SERIALLY: under `pytest -n auto` the `ui_server` command-channel tests
  race for a port, and the vitest node needs `apps/ui/node_modules`.
