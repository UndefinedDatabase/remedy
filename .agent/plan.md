# Plan — F275 One world completion, part three

Branch: feature/f275-one-world-completion-part-three, cut from `main` at
`a5bf894946ab6de053a4232109d6341a63533768`, the merge commit of pull request 246.

## Goal

Finish what F274 could not reach inside its own limit: the two carry-overs F260's Design
names, DECISION F260 D3, the prototype-cluster deletion itself, the atomic record flip that
T002 rules but does not perform, and the classic runner. Operator ruling amend0908-f275-finish
orders T001 PERFORMED, not prepared.

## Current Step

ROUND 24 repairs the surviving surfaces that still offer a reader something this feature
deleted. `remedy mission run` advertises a second mode and three options no code path
honours; two `related=` tuples name commands that no longer exist; and the mission
run-loop page's Quick start gives an operator a `mission report` invocation that cannot
parse. The round lands the referential-closure test R-0859 asks for, with the mutation
colour that proves it bites, and books the round 23 verdict.

## Next Steps

1. Retire the cluster scaffolding R-0868 names — the deletion map, its two ratchets and
   the order file — repair F267's plan as the round 23 measurement re-states it, and
   banner the historical `Groups` table in `docs/system/architecture.md`.
2. T002, the atomic record flip, alone, because every later commit's size depends on it.
3. T003, the classic runner, which T002's ruling is the prerequisite for.

## Risks

- The open set is 92 by distinct id at this round's base `ea5f8128`, computed mechanically
  from the record. This round registers one and resolves one, leaving 92. Four are High —
  R-0803, R-0804, R-0806 and R-0807 — all F273's rather than this feature's, per DECISION
  F272 D12.
- Removing three advertised options is a user-visible narrowing of a SURVIVING command.
  DECISION F275 D14 rules it, and R-0871 records it; nothing is wired in to replace them.
- The advertisement guard `tests/cli/test_advertised_commands.py` is still blind to a
  whole-group deletion, which is R-0847 and is why this page survived four rounds of
  sweeps. Every remaining round sweeps the spaced form by hand.
