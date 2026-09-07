# Plan — F272 One world completion

Branch: feature/f272-one-world-completion. Rounds 1 to 28 PASSED except round 2 (premise
corrected by DECISION F272 D2) and round 21 (R-0824, repaired by round 22). T001, T002 and
T003 are COMPLETE; T004's remainder and T005 are F274's, split off in round 26 by DECISION
F272 D16.

## Goal

Close F272 at the self-consistent scope DECISION F272 D16 fixed. Session 12 reached the
soft limit of 12 sessions, so the remaining work is the closure sequence of
`docs/roadmap/STATUS_closure_protocol.md` and no further building.

## Current Step

Round 29: register the three defects round 28's self-use run surfaced and its describer
could not see — R-0826, R-0827, R-0828 — and rule closure precondition 1 as DECISION F272
D17, because five open High findings would otherwise deadlock every feature behind F273.
Nothing is repaired here; the findings are carried.

## Next Steps

1. The evidence job and a FRESH review zip. `base_commit` is the FORK POINT `b18fad57`,
   never `git merge-base`, which differs on this branch and packages BLOCKED_EVIDENCE.
2. Ledger rotation by `scripts/rotate_live_review.py`, as its own commit, after the verdict
   bookings and before the STATUS flip.
3. The closure commit: the STATUS `[x]` line, the README capability sync and SU-012's
   `consumed_by` in the SAME commit, then the PR. The PR is NOT merged this session.

## Risks

- Five open High findings — R-0803, R-0804, R-0806, R-0807 and the new R-0827. The close is
  PASS_WITH_RISKS and names every one with its owner; DECISION F272 D17 rules why that is
  the honest reading rather than a stop.
- `remedy integrity check` PASSES, but its `high_blockers_open` check reports "no open
  blocker/high findings" while five are open. That is the already-open R-0648, and the
  closure states it rather than leaning on it.
- A failing review-zip build is a closure BLOCKER; the round that hits one stops.
