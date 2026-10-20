# Plan — amend1020-orb-insight (operator docs round)

## Goal
Register F310, F311, F312 and F313 (REGISTERED THIN) before F078, from the operator's three lab
runs of 2026-10-20, with findings R-1369 to R-1371 and DECISION amend1020 D1. Docs only; the
loop builds the features afterwards.

## Current Step
Done: feature files, STATUS block (F310, F312, F311, F313), README counters, docs-suite pin 313,
findings, DECISION, handoff. Commit, push, PR, merge to main.

## Next Steps
- The operator starts the loop (`remedy-loop-feature`); Rule A5 proposes F310 first.
- F310's first round fills F310 D1 to D5 before any code.

## Risks
- The 9-minute job limit's origin (the task plan's suggested budgets) is read from the code, not
  yet from the job's record; F310's first round confirms it.
