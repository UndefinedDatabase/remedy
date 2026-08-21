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
R7 declares DECISION F009 D4's `UI_EXPOSED_COMMANDS` beside the catalog it
constrains and puts it in front of the door's seam: a command id outside the set
is refused with a typed 400 naming the `command` field, per DECISION F009 D12.
The 501 seam SURVIVES this round and is merely narrowed — only `job.stop` and
`decision.resolve` now reach it — because a command still has no effect to run
until D5's effect table lands. R7 also registers R-0633 against the R6 block.

## Next Steps
1. R8 the rate limit D9 rules as a typed `ConfigKeySpec` keyed by the pair
   (token fingerprint, job id), refusing with 429 rather than waiting, with the
   fingerprint helper D7 rules introduced where it is first used.
2. R9 the nonce store and the audit record per D6, D7 and D8, so that a replay
   returns the ORIGINAL body and a rejection is audited.
3. T003's effect table per D5 — the round that finally retires the 501 seam —
   with the plan-approval extraction landing as its own commit; then the client
   wiring that sends both headers, the integration gate, then closure.

## Risks
- `apps/cli/command_catalog.py` is 4824 lines and is imported by the whole CLI.
  This round adds one module-level name to it and edits no entry of `CATALOG`.
- `npm run lint` in `apps/ui` is RED at base and is NOT a gate (R-0364), which is
  R-0622 and routes to a paydown branch.
