# Plan — F113 Local models for side roles

## Goal
Summaries stop costing API tokens: a named local endpoint serves the cheap-tier side roles only,
core roles are refused by F058's "core never local" rule, an endpoint that is down or a role that
fails its spot check falls back to the role's own model, and every call records its route and basis
(docs/roadmap/features/T3_F113.md; DECISIONs F113 D1 to D3).

## Current Step
Round 3 (session 1): book round 2, DECISION F113 D3, and T003b — the summary role's frozen
spot-check set, the flip and its one-hour dwell, the route reading the flip, `remedy doctor
side-roles` with `--check`, the status lines, the tests and the page's quality-gate section.

## Next Steps
1. T003c: the end-to-end fixture of the Acceptance through a real run, and the page completed.
2. The closure sequence.

## Risks
- The open findings, R-1246 to R-1421, are owned by F314; F113 takes none of them.
