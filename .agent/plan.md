# Plan — F113 Local models for side roles

## Goal
Summaries stop costing API tokens: a named local endpoint serves the cheap-tier side roles only,
core roles are refused by F058's "core never local" rule, an endpoint that is down or a role that
fails its spot check falls back to the role's own model, and every call records its route and basis
(docs/roadmap/features/T3_F113.md; DECISIONs F113 D1 to D3).

## Current Step
Round 5 (session 1), the closure's evidence round: book round 4, save the evidence script, the
staging reclaim, the evidence job `f113r5e1001` and the review package.

## Next Steps
1. The closing round: the Built State, the rotation, SU-075's consumed_by, the STATUS flip with the
   README sync, and the pull request, left unmerged.

## Risks
- The open findings, R-1246 to R-1421, are owned by F314; F113 takes none of them.
