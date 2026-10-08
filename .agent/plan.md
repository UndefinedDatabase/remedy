# Plan — F253 Headless API contract: the public HTTP API

## Goal
A machine client drives Remedy through a public, versioned HTTP API under `/api/v1`: it reads the
interface, the digest, the proof and what changed since a cursor, answers decisions, approves or
declines a result and submits orders, with a token whose policy the operator writes and a ledger
entry for every call (docs/roadmap/features/T12_F253.md, its amendment of DECISION amend1007b D3,
and DECISIONs F253 D1 to D17, which fix the order and the shape).

## Current Step
Session 5, round 20, S6b-2 (DECISION F253 D17): book round 19's verdict; the budget decision's
predicate moves to `decision_queue`; a client token answers decisions, declines and applies only
for jobs of its projects, and a budget answer above its ceilings answers 403
`api_client_policy_refused`.

## Next Steps
1. S7: F295's and F298's gate tests driven through HTTP alone; the page says how a client's test
   starts a supervisor.
2. The amend0930b-slow-cap hardening stage, then the closure sequence, which also settles the
   reserved namespace `apps/api`, whose docstring still says no HTTP API exists.

## Risks
- The soft limit of 25 rounds is five rounds away; S7, the hardening stage and the closure may
  need more, and the split-and-close default of amend0905-throughput applies at round 25.
- Client tokens live as plain text in `api/clients.json`, readable by its owner only, as the
  supervisor's own token does in `serve.token`; no command writes them yet (DECISION F253 D16).
- The cockpit's own routes take the token in the query and answer errors in another shape, and
  its server answers no write under `/api/v1`; they stay so until F303 moves the cockpit.
- A write runs its command as a child process, so each costs an interpreter start; one command
  runs per job at a time, and two supervisors on one data root are refused by the socket.
- An order whose supervisor stops before it ends never gets its end written: once its process is
  gone it reads `lost`, with no exit code.
- Nothing limits how many orders run at once (DECISION F253 D15).
- An apply with a push runs inside the 120-second ceiling of a write; a slow remote or a slow
  hook answers 500 `api_command_failed` while the apply may still have landed.
- What changed is read from file modification times; a clock set back on the server hides a
  change until the overlap covers it (DECISION F253 D4).
- A decline sent over HTTP reads "You (recorded as api)" in the job's ownership record, because
  the vocabulary of doors has no `api` yet (DECISION F253 D11).
- No finding is owned by F253; R-1160 (Medium) and R-1138, R-1139, R-1143, R-1149, R-1156,
  R-1157, R-1158, R-1162, R-1172, R-1176, R-1196 (Low) stay open, owned by F297.
