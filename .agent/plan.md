# Plan — F200 Daemon mode (remedy serve)

## Goal
`remedy serve` runs one supervisor per data root: it answers the cockpit's write door on a unix
socket, the command line sends `job stop`, `job pause`, `job unpause` and `job run` to it while it
runs, and it runs again after a restart the jobs it was running; direct mode stays fully supported
(docs/roadmap/features/T12_F200.md, amended by DECISIONs F200 D1, D4, D5, D7 and D8).

## Current Step
Session 3, round 14, the closing round: book round 13 (PASS; evidence job `f200r13e1001`, package
`remedy-review-20261001-153207-READY_FOR_REVIEW.zip` at the accepted head `f96507e80`), rotate the
ledger, accept F200 in STATUS with the README sync and `SU-043`'s `consumed_by`, push, and open the
pull request. F200 owns no open finding. The open-findings count is 7 (`R-1117`, `R-1125`,
`R-1127`, `R-1128`, `R-1129`, `R-1133`, `R-1137`, all owned by F290).

## Next Steps
1. The next session: Phase 1 rule 1 (`.agent/STOP`), then the Open PR Gate merges F200's pull
   request, then round 14's verdict is booked in the next feature's first commit, then Rule A5.

## Risks
- Every command other than those four runs direct in both modes (DECISION F200 D4).
- Outside Linux a live process id alone marks a run as adopted (DECISION F200 D7).
- The STOP test drives a fixture run, not a real `remedy job run` (DECISION F200 D9).
