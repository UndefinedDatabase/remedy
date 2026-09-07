# Plan — F272 One world completion

Branch: feature/f272-one-world-completion. Rounds 1 to 30 PASSED except round 2 (premise
corrected by DECISION F272 D2) and round 21 (R-0824, repaired by round 22). T001, T002 and
T003 are COMPLETE; T004's remainder and T005 are F274's, split off in round 26 by DECISION
F272 D16.

## Goal

Close F272 at the self-consistent scope DECISION F272 D16 fixed. Every closure precondition
of `docs/roadmap/STATUS_closure_protocol.md` is now met: the integration gate ran in round
27 with zero branch-only failures, the self-use item was run in round 28 and its defects
registered in round 29, and round 30 rotated the ledger and built a READY_FOR_REVIEW package.

## Current Step

Round 31, the last round on this branch: the closure commit — the STATUS `[x]` line, the
README capability sync and SU-012's `consumed_by` in ONE commit, with the final handoff —
and then the pull request, which is NOT merged this session.

## Next Steps

1. The PR merges at the NEXT feature's start through the AGENTS.md Open PR Gate. That gap is
   the operator's manual-review window, and guardrail G1 forbids this session merging a PR
   it created.
2. Rule A5 then proposes F274, which sits directly after F272 by amend0906-split-placement
   and owns the atomic record flip and the cluster deletion.
3. F274's first slice is the DECISION F272 D7 raising-property probe and a ruling on the
   per-commit cap, NOT the flip itself.

## Risks

- Five open High findings — R-0803, R-0804, R-0806, R-0807 and R-0827 — all owned by F273,
  whose own Done clause covers "anything registered after 2026-09-06". DECISION F272 D17
  rules why the close names them rather than waiting.
- `remedy integrity check` passes while its `high_blockers_open` check is vacuous; that is
  the open R-0648 and the PR body states it.
