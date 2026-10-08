# Plan — F253 Headless API contract: the public HTTP API

## Goal
A machine client drives Remedy through a public, versioned HTTP API under `/api/v1`: it reads the
interface, the digest, the proof and what changed since a cursor, answers decisions, approves or
declines a result and submits orders, with a token whose policy the operator writes and a ledger
entry for every call (docs/roadmap/features/T12_F253.md, its amendment of DECISION amend1007b D3,
and DECISIONs F253 D1 to D5, which fix the order and the shape).

## Current Step
Session 1, round 5: book round 4, register R-1189 and R-1190, record DECISION F253 D5, tell the
operator about the stray test records, and land S3b — `GET /api/v1/changes?since=<cursor>`
twinned with `remedy client changes --json`, with the first query key that takes a value; repair
R-1189 and R-1190 with their tests.

## Next Steps
1. S4: answer a decision, approve an apply with its commit and push, decline a result, through
   the F009 door.
2. S5: submit an order, created and then polled; two orders at once never corrupt a record.
3. S6: the supervisor serves the API on the localhost port the configuration names; client tokens
   carry the operator's policy.
4. S7: F295's and F298's gate tests driven through HTTP alone; the page says how a client's test
   starts a supervisor.
5. The amend0930b-slow-cap hardening stage, then the closure sequence, which also settles the
   reserved namespace `apps/api`, whose docstring still says no HTTP API exists.

## Risks
- The cockpit's own routes take the token in the query and answer errors in another shape; they
  stay as they are until F303 moves the cockpit onto the public API.
- A route's refusals are written beside its twin's handler rather than shared with it; equality
  tests against the command hold them together (DECISION F253 D3).
- What changed is read from file modification times; a clock set back on the server hides a
  change until the overlap covers it (DECISION F253 D4).
- F253 owns R-1189 and R-1190 (Low), repaired this round. R-1160 (Medium) and R-1138, R-1139,
  R-1143, R-1149, R-1156, R-1157, R-1158, R-1162, R-1172, R-1176 (Low) stay open, owned by F297.
