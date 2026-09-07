# Plan — F272 One world completion

Branch: feature/f272-one-world-completion. Rounds 1 to 29 PASSED except round 2 (premise
corrected by DECISION F272 D2) and round 21 (R-0824, repaired by round 22). T001, T002 and
T003 are COMPLETE; T004's remainder and T005 are F274's, split off in round 26 by DECISION
F272 D16.

## Goal

Close F272 at the self-consistent scope DECISION F272 D16 fixed. Session 12 reached the soft
limit of 12 sessions, so the remaining work is the closure sequence of
`docs/roadmap/STATUS_closure_protocol.md` and no further building.

## Current Step

Round 30: rotate the ledger, then build the evidence job and a FRESH review zip from a clean
tree at the last content commit. The rotation runs after the verdict booking and before the
STATUS flip, as amend0905-throughput requires, and before the zip so the package carries the
rotated ledger. `base_commit` is the FORK POINT `b18fad57`, proved equal-count before use.

## Next Steps

1. THE CLOSURE COMMIT, and it is the last one on this branch: the STATUS `[x]` line, the
   README capability sync and SU-012's `consumed_by` set to `F272`, all in ONE commit, from
   the values this round's handback records. Then the pull request.
2. The PR is NOT merged this session. It merges at the next feature's start via the Open PR
   Gate, which is the operator's manual-review window.
3. F274 owns the atomic record flip and the cluster deletion. None of that work starts here.

## Risks

- Five open High findings — R-0803, R-0804, R-0806, R-0807 and R-0827. The close is
  PASS_WITH_RISKS and names every one with its owner; DECISION F272 D17 rules why.
- `remedy integrity check` PASSES while its `high_blockers_open` check reports "no open
  blocker/high findings" and five are open. That is the already-open R-0648, and the closure
  states it rather than leaning on it.
- A failing review-zip build is a closure BLOCKER; the round that hits one stops and hands
  back rather than adjusting a field to make the package go READY.
