# Plan — F303 The face on the public API

## Goal
Everything the edition `remedy` needs is published under `/api/v1`, contract-tested, and nothing
outside the contract document is served; a steering note reaches a job through the API; and the
public API's verify, gate status and evidence bundle are offered as MCP tools behind an allowlist
closed by default (docs/roadmap/features/T12_F303.md; DECISIONs F303 D1 to D4).

## Current Step
Round 4 (session 1): book round 3 and register R-1407 and R-1408, repair both, and land the MCP
protocol core `packages/orchestration/mcp_server.py` with its tests (DECISION F303 D4 (1), (2)).

## Next Steps
1. Round 5: the three MCP tools, `remedy client mcp --allow`, the page, a real stdio session.
2. The closure: integration gate, evidence, acceptance; R-1329, R-1407, R-1408 resolved there.

## Risks
- `ui_server.py` and `command_catalog.py` have no headroom on the structure ledger.
- `client_interface.py` is 940 lines; it must stay under 1,000 (no ledger row).
- The integrity check fails on High findings F303 does not own (DECISION F310 D7).
