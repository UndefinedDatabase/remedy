# Plan — F253 Headless API contract: the public HTTP API

## Goal
A machine client drives Remedy through a public, versioned HTTP API under `/api/v1`: it reads the
interface, the digest, the proof and what changed since a cursor, answers decisions, approves or
declines a result and submits orders, with a token whose policy the operator writes and a ledger
entry for every call (docs/roadmap/features/T12_F253.md, its amendment of DECISION amend1007b D3,
and DECISIONs F253 D1 to D9, which fix the order and the shape).

## Current Step
Session 2, round 9: book round 8's verdict and register R-1192, R-1193 and R-1194, then repair
them: a path value is percent-decoded, the runner locks on the full job id, and the three
refusals of DECISION F253 D9 that had no guard each get a test.

## Next Steps
1. S4b: decline a result through `remedy job decline`, with its own DECISION.
2. S4c: approve an apply with its commit and push through `remedy job apply`, with its own
   DECISION.
3. S5: submit an order, created and then polled; two orders at once never corrupt a record.
4. S6b: client tokens carry the operator's policy (projects, largest limits, approval).
5. S7: F295's and F298's gate tests driven through HTTP alone; the page says how a client's test
   starts a supervisor.
6. The amend0930b-slow-cap hardening stage, then the closure sequence, which also settles the
   reserved namespace `apps/api`, whose docstring still says no HTTP API exists.

## Risks
- The cockpit's own routes take the token in the query and answer errors in another shape, and
  its server answers no write under `/api/v1`; they stay so until F303 moves the cockpit.
- A write runs its command as a child process, so each costs an interpreter start; one command
  runs per job at a time, and two supervisors on one data root are refused by the socket.
- What changed is read from file modification times; a clock set back on the server hides a
  change until the overlap covers it (DECISION F253 D4).
- The import-time data root changes what every test process sees before its first test; only the
  closure's one full suite reaches every module (DECISION F253 D8).
- R-1192 (Medium), R-1193 and R-1194 (Low) are owned by F253 and repaired this round. R-1160
  (Medium) and R-1138, R-1139, R-1143, R-1149, R-1156, R-1157, R-1158, R-1162, R-1172, R-1176
  (Low) stay open, owned by F297.
