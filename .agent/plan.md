# Plan — F200 Daemon mode (remedy serve)

## Goal
`remedy serve` runs one supervisor per data root: it answers the cockpit's write door on a unix
socket, the command line sends `job stop`, `job pause`, `job unpause` and `job run` to it while it
runs, and it runs again after a restart the jobs it was running; direct mode stays fully supported
(docs/roadmap/features/T12_F200.md, amended by DECISIONs F200 D1, D4, D5, D7 and D8).

## Current Step
Session 3, round 13: book round 12 (PASS), append its prose slip, add F200's pass to the
consolidation record of `docs/agents/planner_reviewer_prompt.md`, which becomes the closure's
accepted head, then build the evidence job and the review package again at that head. The
open-findings count is 7 (`R-1117`, `R-1125`, `R-1127`, `R-1128`, `R-1129`, `R-1133`, `R-1137`,
all owned by F290).

## Next Steps
1. The closing round: book the evidence round, rotate the ledger, the STATUS line with the README
   sync and the queue's `consumed_by`, and the pull request, not merged.

## Risks
- Every command other than those four runs direct in both modes (DECISION F200 D4).
- Outside Linux a live process id alone marks a run as adopted (DECISION F200 D7).
- The STOP test drives a fixture run, not a real `remedy job run` (DECISION F200 D9).
