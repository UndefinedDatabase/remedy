# Plan — F036 Guided result tour

Branch: feature/f036-guided-result-tour, cut from `main` at `9dc2f2a7`, the
merge commit of pull request 290 (F035 Ownership ledger).

## Goal

"What did I get?" answered in a guided minute: at most eight stops built
from the job's own report, diff and Definition of Done, each tied to a real
place in the job, shown as an overlay in the browser and printed the same
way on the command line (`docs/roadmap/features/T5_F036.md`, DECISIONS
F036 D1 to D4).

## Current Step

ROUND 3: book round 2, record DECISION F036 D4, and land T002's second
half — `tour.json` versioned at every reported terminal, the `tour` section
of `job show --full` and `job show --tour`, and the fixture goldens.

## Next Steps

1. T003: the browser's read route for the tour, the overlay with its
   spotlight and navigation to each anchor, and the demo's tour.
2. The closure sequence.

## Risks

None open. Open findings: 0.
