# Plan — F113 Local models for side roles

## Goal
Summaries stop costing API tokens: a named local endpoint serves the cheap-tier side roles only,
core roles are refused by F058's "core never local" rule, an endpoint that is down or a role that
fails its spot check falls back to the role's own model, and every call records its route and basis
(docs/roadmap/features/T3_F113.md; DECISION F113 D1).

## Current Step
Round 1 (session 1): claim F113, book F296's round 7, DECISION F113 D1 with the slice list, and
T001 + T002 — the endpoint table and probe, the side-role table and its refusal, the fallback, the
summary role's three call sites, the summary's route record, tests and the system page.

## Next Steps
1. T003a: the cost ledger records a side-role call with its basis.
2. T003b: the spot-check set, the flip, the dwell rule and the status line.
3. T003c: the end-to-end fixture and the page completed; then the closure sequence.

## Risks
- The open findings, R-1246 to R-1421, are owned by F314; F113 takes none of them.
