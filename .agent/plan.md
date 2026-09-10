# Plan — F275 One world completion, part three

Branch: feature/f275-one-world-completion-part-three, cut from `main` at
`a5bf894946ab6de053a4232109d6341a63533768`, the merge commit of pull request 246.

## Goal

Finish what F274 could not reach inside its own limit: the two carry-overs F260's Design
names, DECISION F260 D3, the prototype-cluster deletion itself, the atomic record flip that
T002 rules but does not perform, and the classic runner. Operator ruling amend0908-f275-finish
orders T001 PERFORMED, not prepared.

## Current Step

ROUND 22 deletes the LAST component of `.agent/f275_deletion_order.md` — the strongly
connected pair `provider_trust` and `provider_trust_verification` — with its handler, the
whole `provider` command group, six `ContractAction` members, four whole test files and two
documentation pages. `CLUSTER_MODULES` becomes the EMPTY tuple and T001's module list is
exhausted. DECISION F275 D11, committed before the first `git rm`, rules the three surviving
consumers that lose their outlet, and R-0866, R-0867 and R-0868 record what each one lost.

## Next Steps

1. DECISION F260 D3, the deletion paragraph, with R-0832's fix clause binding it. That round
   also discharges R-0843, R-0858, R-0859's closure test, R-0860, R-0864 and R-0868's
   scaffolding question, and retires the now-vacuous cluster map and order ratchets.
2. T002, the atomic record flip, alone, because every later commit's size depends on it.
3. T003, the classic runner, which T002's ruling is the prerequisite for.

## Risks

- The open set is 88 by distinct id at this round's base `5178df03`. Round 22 registers
  three and resolves none, taking it to 91. Four are High — R-0803, R-0804, R-0806 and
  R-0807 — all F273's rather than this feature's, per DECISION F272 D12.
- Worst on this round: a surviving module loses a safety check and nothing notices.
  `verify_provider_patch_material` genuinely does lose two of its seven checks, which
  R-0867 records; the reviewer measured that it has no production caller.
- The cluster map and order ratchets become VACUOUS the moment `CLUSTER_MODULES` empties.
  R-0868 records it with a fix clause; this round does not widen to retire them.
- The full suite runs SERIALLY in the PRIMARY checkout. A fresh worktree has no vitest.
