# Plan — F253 Headless API contract: the public HTTP API

## Goal
A machine client drives Remedy through a public, versioned HTTP API under `/api/v1`: it reads the
interface, the digest, the proof and what changed since a cursor, answers decisions, approves or
declines a result, submits orders and starts and follows runs, with a token whose policy the
operator writes and a ledger entry for every call (docs/roadmap/features/T12_F253.md, its
amendments, and DECISIONs F253 D1 to D33, which fix the order and the shape).

## Current Step
Round 38, the closing round on `feature/f253-public-http-api-v2`: book round 37 and R-1226's
resolution, rotate the ledger, accept F253 in STATUS with the README and the self-use queue, and
open the pull request, left unmerged.

## Next Steps
1. The next session's Open PR Gate merges F253's pull request after reading its hosted checks;
   round 38's verdict is booked in the next feature's first commit.
2. Rule A5: the next unchecked line, F299 — Acceptance checks on a repository that is not
   Remedy's own.

## Risks
- Client tokens live as plain text in a file under the data root, readable by its owner only;
  no command writes them yet (DECISION F253 D16).
- The cockpit's own routes take the token in the query and answer errors in another shape; they
  stay so until F303 moves the cockpit.
- Nothing limits how many orders run at once (DECISION F253 D15).
- R-1138, R-1139, R-1143, R-1149, R-1156, R-1157, R-1158, R-1162, R-1172, R-1176, R-1196,
  R-1219, R-1220, R-1225 (Low) and R-1160 (Medium) are open, all owned by F297.
