# F303 inventory — what the public API publishes, read at `2621bbe2e`

T001 of `docs/roadmap/features/T12_F303.md` (DECISION F303 D1 (1)). Read-only; nothing here is built.

## The route table
`PUBLIC_API_ROUTES` in `packages/orchestration/public_api_routes.py`, served by `_RemedyHandler` in
`packages/orchestration/ui_server.py` (the local socket) and by `_PublicApiHandler` in
`packages/orchestration/serve_daemon.py` (the TCP port, `/api/v1` only). `PUBLIC_API_VERSION` is
`1.24`. 21 routes:

| Method | Path | Twin |
|---|---|---|
| GET | `/api/v1/interface` | `client.interface` |
| GET | `/api/v1/execution` | `client.execution` |
| GET | `/api/v1/digest` | `status.run` |
| GET | `/api/v1/jobs/{job}/proof` | `change.proof` |
| GET | `/api/v1/changes` | `client.changes` |
| GET | `/api/v1/health` | `doctor.health` |
| POST | `/api/v1/jobs/{job}/decisions/{decision}` | `decision.resolve` |
| POST | `/api/v1/jobs/{job}/decline` | `job.decline` |
| POST | `/api/v1/jobs/{job}/stop` | `job.stop` |
| POST | `/api/v1/jobs/{job}/abandon` | `job.abandon` |
| POST | `/api/v1/orders/{order}/cancel` | `client.cancel-order` |
| POST | `/api/v1/jobs/{job}/apply` | `job.apply` |
| GET | `/api/v1/orders/{order}` | `client.order` |
| POST | `/api/v1/orders` | `client.order` |
| GET | `/api/v1/jobs/{job}/logs` | `doctor.logs` |
| GET | `/api/v1/jobs/{job}/story` | `client.story` |
| GET | `/api/v1/now` | `client.now` |
| GET | `/api/v1/jobs/{job}/insight` | `client.insight` |
| GET | `/api/v1/jobs/{job}/diff` | `client.diff` |
| GET | `/api/v1/jobs/{job}/run` | `client.run` |
| POST | `/api/v1/jobs/{job}/run` | `job.run` |

## The guards that exist
- An unpinned route fails: `test_every_route_is_pinned_by_name` (`tests/ui_server/test_public_api.py`).
- The contract page equals the code: `test_the_pages_generated_section_equals_the_rendering`, and
  `tests/orchestration/test_api_release_matrix.py` for the release matrix.
- The TCP port answers 404 `api_route_not_found` outside `/api/v1`: three paths in
  `tests/orchestration/test_serve_daemon.py`.

## The edition's inventory against the routes (`docs/roadmap/design/face-v1.md`)
Start an order, see runs, what one run does, the log, approve or decline, try again, answer a
question, what Remedy offers, is Remedy there, and what a change rests on: each has a published
route above. The steering note has none: finding R-1329, moved to F303 (round 2).

## Gaps this feature closes
1. The socket's command door, `POST /api/jobs/<job>/commands`, is served and the contract document
   does not name it (round 1).
2. The logs route's order is proved only below the route (round 1).
3. No route takes a steering note; the story's `note_open` is always false (round 2).
4. No MCP server exists (rounds 3 and 4). What each tool would wrap: verify,
   `verify_job_certificate` (`packages/orchestration/job_certificate_verify.py`); the evidence
   bundle, `build_job_certificate` with `collect_certificate_inputs`; gate status, no single
   command yet — `build_final_verifier_report` (`packages/orchestration/final_verifier.py`) is the
   nearest reader.

## Structure ledger
`ui_server.py` sits at its row (1826 lines, no headroom); `public_api.py` (920 lines) has no row
and must stay under 1,000; `public_api_routes.py` (435) and `public_api_writes.py` (270) have none.
