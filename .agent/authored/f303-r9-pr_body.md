## F303 — The face on the public API: what the remedy edition needs

### What changed
- T001, the inventory: every capability the universe's edition `remedy` reads is mapped to a
  published route (`.agent/f303_inventory.md`). A test now proves the logs route answers one run's
  lines oldest first; the contract page names the one door served outside the public API, the
  socket's command door, and a test holds it to that door; the TCP port answers 404 on every method
  and every path outside `/api/v1`.
- T002, the steering note (R-1329): `POST /api/v1/jobs/{job}/note`, twinned with
  `remedy job steer`, which gains `--source`; the note is recorded with the new channel `api`, a
  client token steers only its own projects, and `PublicApiRoute` gains `positional_body`, a body
  key passed as the twin's positional argument and checked by the route guard. `job.steer` became a
  client operation (interface and API version 1.25), and the story's `note_open` reads whether a
  note would be accepted now. The `job.steer` catalog entry moved unchanged into
  `apps/cli/command_catalog_steer.py`, lowering `command_catalog.py` from 2314 to 2293 lines.
- The MCP facet (DECISION F253 D1): `packages/orchestration/mcp_server.py`, the stdio transport of
  the Model Context Protocol on the standard library alone, closed by default;
  `packages/orchestration/mcp_tools.py`, the tools `verify`, `gate_status` and `evidence_bundle`,
  each running its twin command as a child; and `remedy client mcp --allow <tool>`
  (`apps/cli/commands/client_mcp_cmd.py`). The page is `docs/system/mcp-server-v1.md`.

### Why
The roadmap's F303, narrowed by DECISION amend1016 D2 to the public API: everything the edition
needs is published and contract-tested, nothing outside the contract is served, a steering note
reaches a job through the API, and third-party orchestrators can use Remedy's gates over MCP
without adopting its loop.

### Key decisions (`.agent/decisions.md`)
- D1: the inventory, the command door kept and named, the logs order proved through the route.
- D2 and D3: the note route, its positional body key, the `api` channel and `note_open`.
- D4 and D5: the MCP server and its three tools run their twin commands; `client mcp` answers no
  `--json` envelope, because standard output is the protocol's channel.
- D6: the evidence run gets a data root of its own, because the operator's running service writes
  the real one while the data root guard watches it (R-1411, owned by F307).
- D7: the ledger rotation is skipped for the reason of DECISION F310 D8.

### How to review and test
- `python3 -m pytest -q tests/orchestration/test_mcp_server.py tests/orchestration/test_mcp_tools.py tests/cli/test_client_mcp_cmd.py`
- `python3 -m pytest -q tests/ui_server/test_public_api.py tests/cli/test_job_steer.py tests/orchestration/test_client_story.py`
- A real MCP session: `tests/cli/test_client_mcp_cmd.py` starts `remedy client mcp` as a child and
  verifies a real certificate through it.

### Verification (local; hosted CI is manual under operator amendment amend1011-manual-hosted-ci)
- The one full suite on `9595d5607`: `python3 -m pytest -n auto -q`, Python 3.10, exit 0,
  `23044 passed, 11 skipped, 1 warning in 349.69s` (`.agent/authored/f303-closure-suite.txt`).
- The evidence job `f303r8e1001` at `5727408e0926857a7f24363015c1ea96da6dc1a7`: 11116 passed,
  0 failed, 6 skipped; package `remedy-review-20261021-190053-READY_FOR_REVIEW.zip`, SHA-256
  `ceeee0c17538832f84c67beafeca5d53861c71a3713205efb27878d46e47d362`.
- Latest verdict: PASS (round 8); live review PASS_WITH_RISKS — the integrity check fails only on
  twelve High findings other features own (DECISION F310 D7).
- Findings: R-1329 (moved here from F307) and R-1407 to R-1410 resolved inside the feature; R-1411
  registered and owned by F307; open findings 88.

### Runtime actuals
- Two sessions, nine delegated rounds; reviewer on Claude Opus 5.5, workers on Claude Sonnet 5.5.
- The closure's self-use run SU-072: 4 provider calls, 670.9 seconds, never applied.
- Session token totals: not measured.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
