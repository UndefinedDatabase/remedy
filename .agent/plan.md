# Plan — F253 Headless API contract: the public HTTP API

## Goal
A machine client drives Remedy through a public, versioned HTTP API under `/api/v1`: it reads the
interface, the digest, the proof and what changed since a cursor, answers decisions, approves or
declines a result and submits orders, with a token whose policy the operator writes and a ledger
entry for every call (docs/roadmap/features/T12_F253.md, its amendment of DECISION amend1007b D3,
and DECISIONs F253 D1 and D2, which fix the order and the shape).

## Current Step
Session 1, round 2: book round 1, register and repair R-1187, record DECISION F253 D2, and land
S2a — a line in `api/calls.jsonl` for every call under `/api/v1`, the route fields `twin_key` and
`query` with the refusal `api_query_invalid`, and `GET /api/v1/digest`, twinned with the `client`
object of `remedy status --json`.

## Next Steps
1. S2b: `GET /api/v1/jobs/<job>/proof`, with the twin's refusals and their HTTP statuses.
2. S3: what changed since a cursor the client holds.
3. S4: answer a decision, approve an apply with its commit and push, decline a result, through
   the F009 door.
4. S5: submit an order, created and then polled; two orders at once never corrupt a record.
5. S6: the supervisor serves the API on the localhost port the configuration names; client tokens
   carry the operator's policy.
6. S7: F295's and F298's gate tests driven through HTTP alone; the page says how a client's test
   starts a supervisor.
7. The amend0930b-slow-cap hardening stage, then the closure sequence, which also settles the
   reserved namespace `apps/api`, whose docstring still says no HTTP API exists.

## Risks
- The cockpit's own routes take the token in the query and answer errors in another shape; they
  stay as they are until F303 moves the cockpit onto the public API.
- F253 owns R-1187 (Low), repaired this round. R-1160 (Medium) and R-1138, R-1139, R-1143,
  R-1149, R-1156, R-1157, R-1158, R-1162, R-1172, R-1176 (Low) stay open, owned by F297.
