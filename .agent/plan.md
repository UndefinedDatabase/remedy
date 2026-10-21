# Plan — F303 The face on the public API

## Goal
Everything the edition `remedy` needs is published under `/api/v1`, contract-tested, and nothing
outside the contract document is served; a steering note reaches a job through the API; and the
public API's verify, gate status and evidence bundle are offered as MCP tools behind an allowlist
closed by default (docs/roadmap/features/T12_F303.md; DECISIONs F303 D1 to D3).

## Current Step
Round 3 (session 1): book round 2, then the note route completed under DECISION F303 D3 — the
`api` channel, `job steer --source`, `job.steer` as a client operation, `positional_body` and its
guard, `POST /api/v1/jobs/{job}/note`, the story's `note_open`, tests and docs (T002, R-1329).

## Next Steps
1. Rounds 4 and 5: the MCP facet — server, allowlist closed by default, three tools, page.
2. The closure: integration gate, evidence, acceptance; R-1329 resolved there.

## Risks
- `ui_server.py` has no headroom on the structure ledger; new logic goes into other modules.
- `client_interface.py` is 934 lines; it must stay under 1,000 (no ledger row).
- The integrity check fails on High findings F303 does not own (DECISION F310 D7).
