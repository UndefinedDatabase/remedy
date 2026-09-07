# Plan — F272 One world completion

Branch: feature/f272-one-world-completion. Rounds 1 to 26 PASSED except round 2 (premise
corrected by DECISION F272 D2) and round 21 (R-0824, repaired by round 22). T001, T002 and
T003 are COMPLETE; T004 is part-done and its remainder plus T005 are F274's, registered in
round 26 by DECISION F272 D16.

## Goal

Close F272 at the self-consistent scope DECISION F272 D16 fixed. Session 12 reached the
soft limit of 12 sessions, so the remaining work is the closure sequence of
`docs/roadmap/STATUS_closure_protocol.md` and no further building.

## Current Step

Round 27, two closure preconditions in one round: the feature file's Built State section,
which precondition 4 requires and which does not exist yet, and the dedicated
integration-gate round precondition 2 requires and which F272 has never run.

## Next Steps

1. The self-use round precondition 6 requires: the queue holds no pending item, so call
   `generate_and_append_if_empty` first, then plan it, run it, and register every string
   `describe_self_use_run_defects` returns as a normal R-id finding.
2. The evidence job and a FRESH review zip. Its `base_commit` is the FORK POINT
   `b18fad57`, never `git merge-base`, which differs on this branch and packages
   BLOCKED_EVIDENCE.
3. Ledger rotation by `scripts/rotate_live_review.py`, as its own commit, after the
   verdict bookings and before the STATUS flip.
4. The closure commit: the STATUS `[x]` line with the README capability sync in the SAME
   commit, then the PR. The PR is NOT merged this session.

## Risks

- Four open findings are High — R-0803, R-0804, R-0806 and R-0807 — all four booked to
  F273's T001 by the 2026-09-06 triage. The close is PASS_WITH_RISKS and names them.
- A failing review-zip build is a closure BLOCKER; the round that hits one stops.
- The base run's environment-coupled failures are a known class (R-0445); every one is
  attributed by direct evidence or the gate verdict is blocked.
