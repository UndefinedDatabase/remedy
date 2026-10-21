# Plan — F303 The face on the public API

## Goal
Everything the edition `remedy` needs is published under `/api/v1`, contract-tested, and nothing
outside the contract document is served; a steering note reaches a job through the API; and the
public API's verify, gate status and evidence bundle are offered as MCP tools behind an allowlist
closed by default (docs/roadmap/features/T12_F303.md; DECISIONs F303 D1 and D2).

## Current Step
Round 2 (session 1) BLOCKED at C3. C1 (book round 1, DECISION F303 D2, the plan) and C2 (the
`job.steer` catalog entry moved to its own module) landed and pushed. C3 (the note route,
`--source`, the `api` channel, `note_open`) cannot proceed as DECISION F303 D2 (3) and block.md
literally specify: `POST /api/v1/jobs/{job}/note`'s body `(("task", "string"), ("text",
"string"))` fails `tests/ui_server/test_public_api.py::test_every_route_is_well_formed`, which
requires every non-flag string body key of an ordinary (non-`starts_order`/`starts_run`) write
route to equal an existing `--option` of its twin catalog command. `job.steer`'s `text` is a
required POSITIONAL CLI argument (`remedy job steer <job> <text> --task <task>`), not an option,
and nothing in DECISION F303 D2 or block.md's C3 touches that shape; changing it would break the
shipped CLI and the tests that already drive it positionally. Three candidate resolutions are in
`.agent/handoff.md`'s Deviations section, for an operator decision.

## Next Steps
1. Operator decision on the note route's body shape (see `.agent/handoff.md`), then C3 to C6 of
   this round, from a fresh block.
2. Rounds 3 and 4: the MCP facet — server, allowlist closed by default, three tools, page.
3. The closure: integration gate, evidence, acceptance; R-1329 resolved there.

## Risks
- `ui_server.py` has no headroom on the structure ledger; new logic goes into other modules.
- The integrity check fails on High findings F303 does not own (DECISION F310 D7).
