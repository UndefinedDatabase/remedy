# Plan — F113 Local models for side roles

## Goal
Summaries stop costing API tokens: a named local endpoint serves the cheap-tier side roles only,
core roles are refused by F058's "core never local" rule, an endpoint that is down or a role that
fails its spot check falls back to the role's own model, and every call records its route and basis
(docs/roadmap/features/T3_F113.md; DECISIONs F113 D1 and D2).

## Current Step
Round 2 (session 1): book round 1, DECISION F113 D2, and T003a — `side_role_calls.json` per task
run from the run's routed summaries, its own ledger table with the basis `local_zero`, the export's
call beside the tier outcomes, the tests and the page's ledger section.

## Next Steps
1. T003b: the spot-check set, the flip, the dwell rule and the status line.
2. T003c: the end-to-end fixture and the page completed; then the closure sequence.

## Risks
- The open findings, R-1246 to R-1421, are owned by F314; F113 takes none of them.
