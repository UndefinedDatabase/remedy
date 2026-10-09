# Plan — F253 Headless API contract: the public HTTP API

## Goal
A machine client drives Remedy through a public, versioned HTTP API under `/api/v1`: it reads the
interface, the digest, the proof and what changed since a cursor, answers decisions, approves or
declines a result, submits orders and starts and follows runs, with a token whose policy the
operator writes and a ledger entry for every call (docs/roadmap/features/T12_F253.md, its
amendments, and DECISIONs F253 D1 to D27, which fix the order and the shape).

## Current Step
BLOCKED on operator question Q16 (R-1226): five early commit subjects carry slash-led route tokens
that the review package's metadata scan rejects, and rewording pushed history needs the operator's
leave (guardrail G2). Everything else of the closure is done: hardening, self-use run, a green full
suite, the consolidation pass and a green evidence run that failed only on those subjects.

## Next Steps
1. On the operator's leave: reword the five subjects as Q16 describes, then run the evidence job
   and the package again from the new accepted head.
2. The ledger rotation, the owner lines, the self-use entry's `consumed_by`, the STATUS line, the
   README and the pull request, left unmerged.

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
- R-1138, R-1139, R-1143, R-1149, R-1156, R-1157, R-1158, R-1162, R-1172, R-1176, R-1196,
  R-1219, R-1220, R-1225 (Low) and R-1160 (Medium) are open, all owned by F297; R-1226 (Medium),
  the closure blocker, is owned by F253.
