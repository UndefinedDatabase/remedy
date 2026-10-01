# Plan — F200 Daemon mode (remedy serve)

## Goal
`remedy serve` runs one supervisor per data root: it answers the cockpit's write door on a unix
socket, the command line sends `job stop`, `job pause`, `job unpause` and `job run` to it while it
runs, and it runs again after a restart the jobs it was running; direct mode stays fully supported
(docs/roadmap/features/T12_F200.md, amended by DECISIONs F200 D1, D4, D5, D7 and D8).

## Current Step
Session 2, round 8, the hardening stage's repair round: book round 7 (PASS) and R-1132's
resolution, register the acceptance audit's three gaps as R-1134, R-1135 and R-1136, record
DECISION F200 D9, save the audit's report as `.agent/f200_acceptance_audit.md`, and land the three
tests that close the gaps. The open-findings count is 9 (`R-1117`, `R-1125`, `R-1127`, `R-1128`,
`R-1129`, `R-1133`, owned by F290, and `R-1134`, `R-1135`, `R-1136`, owned by F200).

## Next Steps
1. The audit repeated for the three statements that had gaps, by a fresh auditor.
2. The feature file's Built State paragraph with the audit's counts, then the closure sequence.

## Risks
- Every command other than those four runs direct in both modes (DECISION F200 D4).
- Outside Linux a live process id alone marks a run as adopted (DECISION F200 D7).
- The STOP test drives a fixture run, not a real `remedy job run` (DECISION F200 D9).
