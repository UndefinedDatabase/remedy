# Plan — F275 One world completion, part three

Branch: feature/f275-one-world-completion-part-three, cut from `main` at
`a5bf894946ab6de053a4232109d6341a63533768`, the merge commit of pull request 246.

## Goal

Finish what F274 could not reach inside its own limit: the two carry-overs F260's Design
names, DECISION F260 D3, the prototype-cluster deletion itself, the atomic record flip that
T002 rules but does not perform, and the classic runner. Operator ruling amend0908-f275-finish
orders T001 PERFORMED, not prepared.

## Current Step

ROUND 13 books round 12's PASS and one prose slip, adds two measured instances to the open
finding R-0843 as a NOTE rather than minting a duplicate id, registers R-0852, and deletes the
EIGHTH module group: `packages/orchestration/external_builder_sandbox.py`, whole, in ONE commit.
Its handler file `apps/cli/commands/external_builder_cmd.py` dies WITH it rather than losing a
handler, because the one handler of the eight that did not drive the sandbox died in round 11.
Seven commands, the `external-builder` group WHOLE, two test files and two doc pages go too. No
survivor loses a call site and no cockpit section is involved.

## Next Steps

1. The `local_model_advisor` component, which this round's regeneration makes the order file's
   first line. It is a SINGLE module.
2. The remaining components in the recorded order — every one a single module except the
   `provider_trust` / `provider_trust_verification` pair, which is the last cycle.
3. DECISION F260 D3, the deletion paragraph, with R-0832's fix clause binding it and R-0831,
   R-0840, R-0842, R-0844 through R-0846, R-0848, R-0849, R-0851 and R-0852 named among the
   ideas deleted rather than inherited.
4. T002, the atomic record flip, alone, because every later commit's size depends on its ruling.

## Risks

- The open set is 76 by distinct id at this round's base `053a25a7`; the ledger commit this
  block fixes as C2 registers one, taking it to 77. Four are High — R-0803, R-0804, R-0806 and
  R-0807 — all F273's rather than this feature's, per DECISION F272 D12.
- R-0847 stays OPEN and binds every remaining deletion round: `test_advertised_commands.py`
  cannot see an advertisement whose group has been deleted, so a round that deletes a group
  WHOLE must sweep the spaced `remedy <group> <sub>` form by hand.
- R-0843 now holds three measured instances of one class — a docs page still naming a command
  or a page a deletion round removed. Every remaining deletion round should expect one.
- The full suite is run SERIALLY: under `pytest -n auto` the `ui_server` command-channel tests
  race for a port, and the vitest node needs `apps/ui/node_modules`.
