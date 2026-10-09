## What

F253 — Headless API contract: the public HTTP API. A program on the same machine drives Remedy
over versioned HTTP routes under `/api/v1`, answered by the supervisor `remedy serve` on
`127.0.0.1` beside its socket, through the request handler the cockpit already shares. The
contract page is `docs/system/public-http-api-v1.md`, and a test holds its route table equal to
the registry `PUBLIC_API_ROUTES` in `packages/orchestration/public_api.py`.

- **Reads.** `GET /api/v1/interface`, `GET /api/v1/digest`, `GET /api/v1/jobs/{job}/proof`,
  `GET /api/v1/changes` (what changed since a cursor the client holds, also as `remedy client
  changes --json`), `GET /api/v1/orders/{order}` and `GET /api/v1/jobs/{job}/run`.
- **Writes.** `POST /api/v1/jobs/{job}/decisions/{decision}`, `POST /api/v1/jobs/{job}/decline`,
  `POST /api/v1/jobs/{job}/apply`, `POST /api/v1/orders` and `POST /api/v1/jobs/{job}/run`. A write
  runs its command-line twin as a child process of the supervisor and answers that command's own
  envelope; an order and a run are started by the supervisor's launchers and followed to their end
  over their GET routes or `remedy client order` and `remedy client run`.
- **Tokens, policy and the ledger.** Every call needs a bearer token: the supervisor's own, or a
  client token from `api/clients.json` under the data root whose policy names its projects, its
  largest limits and whether it may apply; a call outside the policy is refused 403
  `api_client_policy_refused`. Every call writes one line to `api/calls.jsonl`.
- **The gate paths over HTTP alone.** `tests/orchestration/test_public_api_gate_paths.py` drives
  F295's gate path and F304's paths through a real supervisor on a scratch data root, over its
  port alone.
- The MCP facet and the shipped cockpit's migration moved to F303 (DECISIONs amend1007b D3 and
  F253 D1).

## Why

The operator's ruling of 2026-10-07 made this API the one bridge a client uses, with Luna as its
first client: a program needs real time and a contract it can test against, not a file mailbox.

## The branch

This pull request comes from `feature/f253-public-http-api-v2`, a copy of
`feature/f253-public-http-api` made with the operator's leave (DECISIONs F253 D32 and D33): every
commit keeps its original's tree, author, date and message, except that five early subjects name a
route in words instead of with a leading slash, which the review package's metadata scan read as a
local path (R-1226). The old branch stays untouched as the record; commit ids that `.agent/`
records name for the rounds before the copy are that branch's.

## Key decisions (in `.agent/decisions.md`)

- D1 to D5: the routes on the shared handler, one slice per round; the ledger line per call; the
  proof route; what changed since a cursor.
- D6, D16, D17: the supervisor's API port; client tokens and their policy.
- D9, D11, D12, D21, D30: a write runs its command-line twin; decline and apply over HTTP; the
  feature file's amendment on the F009 door, which the operator kept.
- D13 to D15, D18 to D20, D22, D23, D28: orders and runs started by the supervisor and followed to
  their end; two orders at once; a resent order with the same key refused while its mission runs.
- D7, D8, D10: the test suite's own data root, and the three stray practice records.
- D22, D24, D25, D31: the soft limit, the hardening stage and its two carried gaps.
- D26, D27: the closure suite's repairs. D32, D33: the reworded copy.

## How to review / test

- Read `docs/roadmap/features/T12_F253.md`'s Built State first, then
  `docs/system/public-http-api-v1.md`.
- `python3 -m pytest -q tests/ui_server/test_public_api.py tests/orchestration/test_public_api_gate_paths.py tests/orchestration/test_serve_runs.py tests/orchestration/test_api_clients.py tests/cli/test_golden_path.py`
- The closure suite transcript is `.agent/authored/f253-closure-suite.txt`: `22203 passed, 22
  skipped`, exit 0, 1143.17 CPU seconds, 1.5 percent more than F304's closure.

## Changed files (outside `.agent/`, fork point `1474a65ea` to this branch)

| Path | + | - |
|---|--:|--:|
| `README.md` | 12 | 2 |
| `apps/api/__init__.py` | 0 | 15 |
| `apps/cli/client_interface.py` | 39 | 4 |
| `apps/cli/command_catalog.py` | 60 | 0 |
| `apps/cli/commands/client_cmd.py` | 105 | 2 |
| `apps/cli/commands/decision.py` | 3 | 1 |
| `apps/cli/commands/do_cmd.py` | 7 | 2 |
| `apps/cli/commands/serve_cmd.py` | 4 | 0 |
| `docs/README.md` | 2 | 0 |
| `docs/agents/planner_reviewer_prompt.md` | 15 | 0 |
| `docs/guides/environment.md` | 1 | 0 |
| `docs/guides/exit-codes.md` | 2 | 0 |
| `docs/roadmap/STATUS.md` | 1 | 1 |
| `docs/roadmap/features/T12_F253.md` | 52 | 0 |
| `docs/roadmap/features/T12_F303.md` | 6 | 0 |
| `docs/system/architecture.md` | 1 | 1 |
| `docs/system/machine-client-contract-v1.md` | 70 | 2 |
| `docs/system/public-http-api-v1.md` | 255 | 0 |
| `docs/system/serve-daemon-v1.md` | 8 | 0 |
| `packages/orchestration/api_clients.py` | 197 | 0 |
| `packages/orchestration/client_changes.py` | 278 | 0 |
| `packages/orchestration/client_digest.py` | 38 | 14 |
| `packages/orchestration/config.py` | 10 | 0 |
| `packages/orchestration/data_paths.py` | 3 | 0 |
| `packages/orchestration/decision_queue.py` | 7 | 0 |
| `packages/orchestration/public_api.py` | 1136 | 0 |
| `packages/orchestration/serve_daemon.py` | 157 | 10 |
| `packages/orchestration/serve_paths.py` | 13 | 0 |
| `packages/orchestration/serve_runs.py` | 429 | 17 |
| `packages/orchestration/ui_server.py` | 177 | 1 |
| `scripts/remedy_smoke.sh` | 0 | 1 |
| `scripts/self_use_queue.json` | 8 | 0 |
| `tests/cli/test_client_changes_cmd.py` | 107 | 0 |
| `tests/cli/test_client_interface.py` | 39 | 2 |
| `tests/cli/test_client_order_cmd.py` | 204 | 0 |
| `tests/cli/test_client_run_cmd.py` | 124 | 0 |
| `tests/cli/test_job_decline.py` | 14 | 0 |
| `tests/cli/test_serve_cmd.py` | 1 | 0 |
| `tests/conftest.py` | 41 | 16 |
| `tests/orchestration/import_reachability_allowlist.txt` | 3 | 0 |
| `tests/orchestration/test_api_clients.py` | 217 | 0 |
| `tests/orchestration/test_client_changes.py` | 246 | 0 |
| `tests/orchestration/test_client_digest.py` | 60 | 0 |
| `tests/orchestration/test_decision_queue.py` | 17 | 0 |
| `tests/orchestration/test_public_api_gate_paths.py` | 439 | 0 |
| `tests/orchestration/test_serve_daemon.py` | 863 | 7 |
| `tests/orchestration/test_serve_paths.py` | 2 | 0 |
| `tests/orchestration/test_serve_runs.py` | 541 | 0 |
| `tests/test_data_root_isolation.py` | 48 | 1 |
| `tests/test_reserved_namespaces.py` | 0 | 1 |
| `tests/ui_server/test_command_channel.py` | 27 | 3 |
| `tests/ui_server/test_public_api.py` | 2255 | 0 |

## Verdict and evidence

- Latest live review verdict: PASS (round 37); F253 accepted PASS_WITH_RISKS, the risks being the
  open findings below.
- The hardening stage (SLOW MODE): 32 statements audited, 23 with a proving test at once, 3 moved
  to F303, 6 gaps; ten gaps in all over the repeated audits, eight repaired with a test proved by
  mutation, and two carried to F297 (R-1219, R-1220).
- Evidence job `f253r37e1001`, package `remedy-review-20261009-134321-READY_FOR_REVIEW.zip`,
  SHA-256 `c3c31dda428e52aee4fe4e7980db88adcf3dfc3e72c10272a0b613894ce66944`, archived at
  `/home/decodeux/Repos/remedy-history/zips`, accepted head `04ee857ca`.
- Resolved on this branch: R-1187 to R-1195, R-1197 to R-1218, R-1221 to R-1224 and R-1226.
- Open findings: 15, all owned by F297, Findings paydown v7: R-1160 (Medium) and R-1138, R-1139,
  R-1143, R-1149, R-1156, R-1157, R-1158, R-1162, R-1172, R-1176, R-1196, R-1219, R-1220 and
  R-1225 (Low).

## Runtime actuals

- Rounds: 38, in 7 sessions, on 2026-10-08 and 2026-10-09; the operator let the feature run past
  the soft limit of 25 rounds (DECISION F253 D31).
- Models: the workers' commit trailers name Claude Sonnet 5.5 and Claude Sonnet 5; the seventh
  session's reviewer ran on Claude Opus 5.5. The closure's self-use job SU-050 ran on `claude-cli`
  / `claude-sonnet-4-6`: 2 provider calls, 16,334 tokens, a measured $0.96, completed with the
  reviewer's verdict pass, never applied.
- Tokens and cost of the sessions themselves: not measured.
- Full-suite runs: three, in rounds 32, 33 and 37; the first found two red nodes, which round 33
  repaired, and the third was taken again on the reworded copy after an operator commit on the
  branch.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
