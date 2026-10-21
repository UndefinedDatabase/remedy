# Plan — F303 The face on the public API

## Goal
Everything the edition `remedy` needs is published under `/api/v1`, contract-tested, and nothing
outside the contract document is served; a steering note reaches a job through the API; and the
public API's verify, gate status and evidence bundle are offered as MCP tools behind an allowlist
closed by default (docs/roadmap/features/T12_F303.md; DECISIONs F303 D1 to D7).

## Current Step
Round 9 (session 2), the closing round: book round 8, DECISION F303 D7 (no rotation), the Built
State's closure facts, the STATUS flip with the README sync and SU-072's consumed_by, and the pull
request, left unmerged.

## Next Steps
1. The next session: Phase 1 rule 1, then the Open PR Gate merges F303's pull request; Rule A5
   proposes the next feature (F307, Findings paydown v9).

## Risks
- The integrity check fails on High findings F303 does not own (DECISION F310 D7).
- The operator's live service writes the data root the guard watches (R-1411, owned by F307).
