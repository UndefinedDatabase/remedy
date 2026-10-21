# Plan — F303 The face on the public API

## Goal
Everything the edition `remedy` needs is published under `/api/v1`, contract-tested, and nothing
outside the contract document is served; a steering note reaches a job through the API; and the
public API's verify, gate status and evidence bundle are offered as MCP tools behind an allowlist
closed by default (docs/roadmap/features/T12_F303.md; DECISIONs F303 D1 to D6).

## Current Step
Round 8 (session 2), the closure's evidence round again: book round 7, register R-1411, DECISION
F303 D6, and the evidence job `f303r8e1001` with a data root of its own, then the review package.

## Next Steps
1. Round 9, the closing round: the rotation, SU-072's consumed_by, the STATUS flip with the README
   sync, and the pull request, left unmerged.

## Risks
- The integrity check fails on High findings F303 does not own (DECISION F310 D7).
- The operator's live service writes the data root the guard watches (R-1411, owned by F307).
