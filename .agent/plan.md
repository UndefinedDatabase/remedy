# Plan — F200 Daemon mode (remedy serve)

## Goal
`remedy serve` runs one supervisor per data root: it answers the cockpit's write door on a unix
socket, the command line sends `job stop`, `job pause`, `job unpause` and `job run` to it while it
runs, and it runs again after a restart the jobs it was running; direct mode stays fully supported
(docs/roadmap/features/T12_F200.md, amended by DECISIONs F200 D1, D4, D5, D7 and D8).

## Current Step
Session 2, round 10, the closure sequence's first round: book round 9 (PASS), generate the
closure's self-use item into the empty queue and run it to its approval gate through the
`self_use` role, never applying it, with every reading saved under `.agent/selfuse_f200/`. The
reviewer's probe at `d9524de29` answered `SU-043`, the excused handler at
`apps/cli/commands/dev.py:133`. The open-findings count is 6 (`R-1117`, `R-1125`, `R-1127`,
`R-1128`, `R-1129`, `R-1133`, all owned by F290).

## Next Steps
1. Register any self-use run defect; land the item's change with its tests if it is sound.
2. The closure's one full suite, the evidence bundle and the review package.
3. The STATUS line and the pull request, not merged.

## Risks
- Every command other than those four runs direct in both modes (DECISION F200 D4).
- Outside Linux a live process id alone marks a run as adopted (DECISION F200 D7).
- The STOP test drives a fixture run, not a real `remedy job run` (DECISION F200 D9).
