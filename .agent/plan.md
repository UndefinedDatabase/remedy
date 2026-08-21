# Plan — F009 The single write channel

Branch: feature/f009-single-write-channel, cut from `main` at the merge commit of
pull request #209, which R1 merges at the Open PR Gate. `.agent/live_review.md`
is the source of truth for the open set, the next free finding id and the round
map.

## Goal
Exactly ONE door for UI-initiated change: POST /api/jobs/{jid}/commands validates
against the UI command catalog, authenticates with a bearer token plus an
X-Remedy-CSRF double-submit, rate-limits per token and job, deduplicates by
client nonce, and ENQUEUES into the existing decision, approval and control
machinery without touching files, jobs or shells directly. Every other POST, PUT
and DELETE answers 405. DONE when the exposed commands round-trip through queue
effects on fixtures, replayed nonces are idempotent, unauthenticated and
cross-site attempts fail closed and are audited as rejected, and a route-walking
test plus an import guard prove no other mutating route exists.

## Current Step
R1 opens the feature. It merges pull request #209 at the Open PR Gate, claims
F009 in the roadmap ledger, resets this branch's review record while carrying the
open findings forward by script, records the F008 R36 verdict as that record's
first `Gate:` paragraph, registers the closure candidate F008 carried, resolves
R-0406 by dropping the stale next-free-id line the reset is the fix for, and
empties `.agent/candidates.md`.

## Next Steps
1. R2 the write-channel inventory, MEASURED in the source rather than read off
   the feature file: where the UI command catalog lives and which subset it
   exposes, how `_RemedyHandler` authenticates today, and which module owns each
   effect backend — the kill-switch control file, the decision queue and the
   approval consumption.
2. R3 records R2 and rules the channel's shape as a DECISION: the auth pair, the
   nonce replay window, the rate-limit configuration and the audit record fields.
3. R4 onward the built work, in the T001/T002/T003 order the feature file names.

## Risks
- `npm run lint` in `apps/ui` is RED at base and is NOT a gate (R-0364): that
  configuration installs no TypeScript parser, which is R-0622 and routes to a
  paydown branch.
