# Plan — F253 Headless API contract: the public HTTP API

## Goal
A machine client drives Remedy through a public, versioned HTTP API under `/api/v1`: it reads the
interface, the digest, the proof and what changed since a cursor, answers decisions, approves or
declines a result, submits orders and starts and follows runs, with a token whose policy the
operator writes and a ledger entry for every call (docs/roadmap/features/T12_F253.md, its
amendments, and DECISIONs F253 D1 to D23, which fix the order and the shape).

## Current Step
Session 6, round 26, the hardening stage's third and last repair round (DECISION F253 D23): book
round 25's verdict, resolve R-1210 and R-1207, register R-1216; a run's or an order's answer that
would read `lost` waits up to two seconds for its end to be written, and reads `ended` once it is.

## Next Steps
1. The acceptance audit repeated for the six statements that had gaps; a gap it finds keeps a
   finding with an owner, and the feature then closes PASS_WITH_RISKS naming it.
2. The closure sequence, which also settles the reserved namespace `apps/api`, whose docstring
   still says no HTTP API exists.

## Risks
- The installed `remedy` command on this machine runs the code of a stale job worktree (Q13);
  every test and gate of this loop runs from the checkout and is not affected.
- Client tokens live as plain text in `api/clients.json`, readable by its owner only, as the
  supervisor's own token does in `serve.token`; no command writes them yet (DECISION F253 D16).
- The cockpit's own routes take the token in the query and answer errors in another shape, and
  its server answers no write under `/api/v1`; they stay so until F303 moves the cockpit.
- A write runs its command as a child process, so each costs an interpreter start; one command
  runs per job at a time, and two supervisors on one data root are refused by the socket.
- An order or a run whose supervisor stops before it ends never gets its end written: once its
  process is gone it reads `lost`, with no exit code, after a wait of up to two seconds.
- Nothing limits how many orders run at once (DECISION F253 D15).
- Two orders with one key sent close together may both start, as two `remedy do` of one file
  may; the key's file holds the text of the last order sent with it (DECISION F253 D22).
- An apply with a push runs inside the 120-second ceiling of a write; a slow remote or a slow
  hook answers 500 `api_command_failed` while the apply may still have landed.
- What changed is read from file modification times; a clock set back on the server hides a
  change until the overlap covers it (DECISION F253 D4).
- A decline sent over HTTP reads "You (recorded as api)" in the job's ownership record, because
  the vocabulary of doors has no `api` yet (DECISION F253 D11).
- R-1216 (Medium) is open, owned by F253; R-1138, R-1139, R-1143, R-1149, R-1156, R-1157,
  R-1158, R-1162, R-1172, R-1176, R-1196 (Low) and R-1160 (Medium) by F297.
