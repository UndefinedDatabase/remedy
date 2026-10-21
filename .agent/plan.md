# Plan — F303 The face on the public API

## Goal
Everything the edition `remedy` needs is published under `/api/v1`, contract-tested, and nothing
outside the contract document is served; a steering note reaches a job through the API; and the
public API's verify, gate status and evidence bundle are offered as MCP tools behind an allowlist
closed by default (docs/roadmap/features/T12_F303.md; DECISION F303 D1).

## Current Step
Round 1 (session 1): claim F303, book F060's round 7, the inventory, R-1329 moved here, the
contract section naming the socket's command door with its tests, and the logs route's order
proved through the route.

## Next Steps
1. Round 2: `POST /api/v1/jobs/{job}/note`, twinned with `remedy job steer`, and the story's
   `note_open` (T002, R-1329).
2. Rounds 3 and 4: the MCP facet — server, allowlist closed by default, three tools, page.
3. The closure: integration gate, evidence, acceptance.

## Risks
- `ui_server.py` has no headroom on the structure ledger; new logic goes into other modules.
- The integrity check fails on High findings F303 does not own (DECISION F310 D7).
