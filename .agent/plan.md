# Plan — F303 The face on the public API

## Goal
Everything the edition `remedy` needs is published under `/api/v1`, contract-tested, and nothing
outside the contract document is served; a steering note reaches a job through the API; and the
public API's verify, gate status and evidence bundle are offered as MCP tools behind an allowlist
closed by default (docs/roadmap/features/T12_F303.md; DECISIONs F303 D1 and D2).

## Current Step
Round 2 (session 1): book round 1, the `job.steer` entry moved to its own catalog module, then
`POST /api/v1/jobs/{job}/note` with the `api` channel, `--source` and the story's `note_open`
(T002, R-1329, DECISION F303 D2).

## Next Steps
1. Rounds 3 and 4: the MCP facet — server, allowlist closed by default, three tools, page.
2. The closure: integration gate, evidence, acceptance; R-1329 resolved there.

## Risks
- `ui_server.py` has no headroom on the structure ledger; new logic goes into other modules.
- The integrity check fails on High findings F303 does not own (DECISION F310 D7).
