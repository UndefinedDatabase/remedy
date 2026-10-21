# Plan — F303 The face on the public API

## Goal
Everything the edition `remedy` needs is published under `/api/v1`, contract-tested, and nothing
outside the contract document is served; a steering note reaches a job through the API; and the
public API's verify, gate status and evidence bundle are offered as MCP tools behind an allowlist
closed by default (docs/roadmap/features/T12_F303.md; DECISIONs F303 D1 to D5).

## Current Step
Round 6 (session 2), the closure's integration gate: book round 5 and register R-1410, the
self-use run, R-1410's test, the Built State, the consolidation pass, and the one full suite.

## Next Steps
1. Round 7: book round 6, resolve R-1329 and R-1407 to R-1410, the evidence bundle and the review
   package (or a repair round naming every bad node id, if the suite is red).
2. Round 8: the STATUS line, the README and the pull request.

## Risks
- The integrity check fails on High findings F303 does not own (DECISION F310 D7).
- The operator's live service writes the data root the suite's guard watches (Gate F303 R5).
