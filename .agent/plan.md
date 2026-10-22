# Plan — F113 Local models for side roles

## Goal
Summaries stop costing API tokens: a named local endpoint serves the cheap-tier side roles only,
core roles are refused by F058's "core never local" rule, an endpoint that is down or a role that
fails its spot check falls back to the role's own model, and every call records its route and basis
(docs/roadmap/features/T3_F113.md; DECISIONs F113 D1 to D3).

## Current Step
Round 6 (session 1): the closing round — book round 5, the Built State, the ledger rotation, F113
accepted in STATUS with the README sync and SU-075's consumed_by, and the pull request, left
unmerged.

## Next Steps
1. The next session: Phase 1 rule 1, then the Open PR Gate merges F113's pull request, then the
   next feature's first commit books round 6's verdict, then Rule A5.

## Risks
- None of F113's own; the open findings, R-1246 to R-1421, are owned by F314.
