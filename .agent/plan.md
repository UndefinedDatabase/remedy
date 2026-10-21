# Plan — F303 The face on the public API

## Goal
Everything the edition `remedy` needs is published under `/api/v1`, contract-tested, and nothing
outside the contract document is served; a steering note reaches a job through the API; and the
public API's verify, gate status and evidence bundle are offered as MCP tools behind an allowlist
closed by default (docs/roadmap/features/T12_F303.md; DECISIONs F303 D1 to D5).

## Current Step
Round 7 (session 2), the closure's evidence round: book round 6, resolve R-1329 and R-1407 to
R-1410, the evidence job `f303r7e1001` and the review package.

## Next Steps
1. Round 8, the closing round: the rotation, SU-072's consumed_by, the STATUS flip with the README
   sync, and the pull request, left unmerged.

## Risks
- The integrity check fails on High findings F303 does not own (DECISION F310 D7).
- The operator's live service writes the data root the suite's guard watches (Gate F303 R5).
