# Plan — F303 The face on the public API

## Goal
Everything the edition `remedy` needs is published under `/api/v1`, contract-tested, and nothing
outside the contract document is served; a steering note reaches a job through the API; and the
public API's verify, gate status and evidence bundle are offered as MCP tools behind an allowlist
closed by default (docs/roadmap/features/T12_F303.md; DECISIONs F303 D1 to D5).

## Current Step
Round 5 (session 2): book round 4 and register R-1409, repair it, then the three MCP tools
(`mcp_tools.py`), the command `remedy client mcp --allow <tool>`, a real stdio session through
it, and the page `docs/system/mcp-server-v1.md` (DECISIONs F303 D4 (3) and D5).

## Next Steps
1. The closure: integration gate (the one full suite), evidence, acceptance; R-1329, R-1407,
   R-1408 and R-1409 resolved there.

## Risks
- `ui_server.py` and `command_catalog.py` have no headroom on the structure ledger.
- `client_interface.py` is 940 lines; it must stay under 1,000 (no ledger row).
- The integrity check fails on High findings F303 does not own (DECISION F310 D7).
