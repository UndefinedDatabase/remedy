# Plan — F113 Local models for side roles

## Goal
Summaries stop costing API tokens: a named local endpoint serves the cheap-tier side roles only,
core roles are refused by F058's "core never local" rule, an endpoint that is down or a role that
fails its spot check falls back to the role's own model, and every call records its route and basis
(docs/roadmap/features/T3_F113.md; DECISIONs F113 D1 to D3).

## Current Step
Round 4 (session 1), the closure's integration-gate round: book round 3, T003c — the Acceptance held
on real runs in `tests/regression/test_f113_acceptance.py` — the checklist's consolidation pass, the
closure's self-use item run to its approval gate, and the feature's one full suite with its cost.

## Next Steps
1. The evidence bundle and the review package (or a repair round naming every bad node id).
2. The closing round: the Built State, the rotation, the STATUS line, the README and the pull request.

## Risks
- The open findings, R-1246 to R-1421, are owned by F314; F113 takes none of them.
