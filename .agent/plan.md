# Plan — F272 One world completion

Branch: feature/f272-one-world-completion. Rounds 1 to 27 PASSED except round 2 (premise
corrected by DECISION F272 D2) and round 21 (R-0824, repaired by round 22). T001, T002 and
T003 are COMPLETE; T004's remainder and T005 are F274's, split off in round 26 by DECISION
F272 D16.

## Goal

Close F272 at the self-consistent scope DECISION F272 D16 fixed. Session 12 reached the
soft limit of 12 sessions, so the remaining work is the closure sequence of
`docs/roadmap/STATUS_closure_protocol.md` and no further building.

## Current Step

Round 28, closure precondition 6: the self-use item. The queue holds no pending item, so
`generate_and_append_if_empty` supplies one from its ledger tier, and the round plans it
and RUNS it to the approval gate under the product's own provider. The defects the run
reports are carried to the next round in the handback, because only reviewer-authored text
registers a finding.

## Next Steps

1. Register every string `describe_self_use_run_defects` returned, in reviewer-authored
   text, starting at the next free id `R-0826`. An empty tuple means nothing to register.
2. The evidence job and a FRESH review zip. Its `base_commit` is the FORK POINT
   `b18fad57`, never `git merge-base`, which differs on this branch and packages
   BLOCKED_EVIDENCE.
3. Ledger rotation by `scripts/rotate_live_review.py`, as its own commit, after the verdict
   bookings and before the STATUS flip.
4. The closure commit: the STATUS `[x]` line, the README capability sync and SU-012's
   `consumed_by` in the SAME commit, then the PR. The PR is NOT merged this session.

## Risks

- Four open findings are High — R-0803, R-0804, R-0806 and R-0807 — all four booked to
  F273's T001 by the 2026-09-06 triage. The close is PASS_WITH_RISKS and names them.
- A failing review-zip build is a closure BLOCKER; the round that hits one stops.
- Precondition 2 is MET: round 27's integration gate found zero branch-only failures, with
  all 126 base-only ids attributed and a repaired control re-running them green.
