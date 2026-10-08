# Plan — F253 Headless API contract: the public HTTP API

## Goal
A machine client drives Remedy through a public, versioned HTTP API under `/api/v1`: it reads the
interface, the digest, the proof and what changed since a cursor, answers decisions, approves or
declines a result, submits orders and starts and follows runs, with a token whose policy the
operator writes and a ledger entry for every call (docs/roadmap/features/T12_F253.md, its
amendments, and DECISIONs F253 D1 to D21, which fix the order and the shape).

## Current Step
Session 5, round 24, the hardening stage's first repair round (DECISION F253 D21): book round
23's verdict, resolve R-1208, register R-1209 and the audit's six gaps R-1210 to R-1215, save the
audit; repair R-1209 and R-1212 to R-1215 with tests; state the writes' design in the feature
file for R-1211 and ask the operator (Q14).

## Next Steps
1. The second repair round: an order sent over HTTP carries a key, a resent order is refused
   naming the first, and F304's fifth path is driven over HTTP (R-1210, R-1207).
2. The audit repeated for the six statements that had gaps.
3. The closure sequence, which also settles the reserved namespace `apps/api`, whose docstring
   still says no HTTP API exists.

## Risks
- Round 25 is the soft limit of 25 rounds; the second repair round, the repeated audit and the
  closure need more, and the split-and-close default of amend0905-throughput applies there.
- The installed `remedy` command on this machine runs the code of a stale job worktree (Q13);
  every test and gate of this loop runs from the checkout and is not affected.
- Client tokens live as plain text in `api/clients.json`, readable by its owner only, as the
  supervisor's own token does in `serve.token`; no command writes them yet (DECISION F253 D16).
- The cockpit's own routes take the token in the query and answer errors in another shape, and
  its server answers no write under `/api/v1`; they stay so until F303 moves the cockpit.
- A write runs its command as a child process, so each costs an interpreter start; one command
  runs per job at a time, and two supervisors on one data root are refused by the socket.
- An order or a run whose supervisor stops before it ends never gets its end written: once its
  process is gone it reads `lost`, with no exit code.
- Nothing limits how many orders run at once (DECISION F253 D15).
- An apply with a push runs inside the 120-second ceiling of a write; a slow remote or a slow
  hook answers 500 `api_command_failed` while the apply may still have landed.
- What changed is read from file modification times; a clock set back on the server hides a
  change until the overlap covers it (DECISION F253 D4).
- A decline sent over HTTP reads "You (recorded as api)" in the job's ownership record, because
  the vocabulary of doors has no `api` yet (DECISION F253 D11).
- R-1209 to R-1215 (Low) are open, owned by F253; R-1207 and R-1138, R-1139, R-1143, R-1149,
  R-1156, R-1157, R-1158, R-1162, R-1172, R-1176, R-1196 (Low) and R-1160 (Medium) by F297.
