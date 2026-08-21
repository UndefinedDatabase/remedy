# Plan — F009 The single write channel

Branch: feature/f009-single-write-channel, cut from `main` at `ce49348b`, the
merge commit of pull request #209. `.agent/live_review.md` is the source of truth
for the open set, the round map and the finding-id ceiling.

## Goal
Exactly ONE door for UI-initiated change: POST /api/jobs/{jid}/commands validates
against the UI-exposed catalog subset, authenticates with a bearer token plus an
X-Remedy-CSRF double-submit, rate-limits per token and job, deduplicates by
client nonce, and ENQUEUES into the existing decision, approval and control
machinery without touching files, jobs or shells directly. Every other POST, PUT
and DELETE answers 405. DONE when the exposed commands round-trip through their
effects on fixtures, replayed nonces are idempotent, unauthenticated and
cross-site attempts fail closed and are audited as rejected, and a route-walking
test plus an import guard prove no other mutating route exists.

## Current Step
R10 lands the AUDIT half of T002 and leaves the nonce store to R11. DECISION F009
D14 rules the three halves D6 left open, `packages/common/secure_fs.py` gains the
append-only line writer this repository does not have, a new
`packages/orchestration/command_audit.py` writes the per-job record, and every
refusal the door already makes becomes an audited rejection. The round also
repairs R-0634 in the test file it is already touching.

## Next Steps
1. R11 the nonce store per D8 — create-only publication, a validated nonce
   character class, and a replay that returns the ORIGINAL body. Whether a replay
   spends rate budget is open and is ruled by that round.
2. T003's effect table per D5 — the round that finally retires the 501 seam —
   with the plan-approval extraction landing as its own commit.
3. Then the client wiring that sends both headers, the integration gate, and
   closure.

## Risks
- An audit write that fails must never turn a refusal into a 500; D14 rules that
  a failed write leaves the response it was recording unchanged.
- The audit runs before the job's control directory is known to exist, so the
  pre-credential path must never CREATE one — D14 rules that half too.
- `npm run lint` in `apps/ui` is RED at base and is NOT a gate (R-0364), which is
  R-0622 and routes to a paydown branch.
