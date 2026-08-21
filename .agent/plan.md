# Plan — F009 The single write channel

Branch: feature/f009-single-write-channel, cut from `main` at `ce49348b`, the
merge commit of pull request #209. `.agent/live_review.md` is the source of truth
for the open set, the round map and the finding-id ceiling, which is derived with
`max` over its line-anchored entries rather than read from a header sentence.

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
R2 records the R1 verdict and inventories the ground this feature builds on: the
command catalog and whether a UI-exposed subset already exists, how the UI
server authenticates today, which module owns each effect backend the feature
names, where an event reaches the ledger the F008 stream reads, whether any nonce
or rate-limit machinery exists to reuse, and which test directory the contract
tests belong in. Every answer is MEASURED in the source and carried as a
`path:line` citation; an answer of "this does not exist" names the search that
established the absence.

## Next Steps
1. R3 records R2 and rules the channel's shape as a DECISION: the auth pair, the
   nonce replay window, the rate-limit configuration, the audit record's fields
   and the effect table for the initially exposed commands.
2. R4 onward the built work, in the T001/T002/T003 order the feature file's Task
   slicing names, gated on the SSE stream per its Orchestrator brief.
3. The integration gate before closure, then the closure round itself.

## Risks
- The feature file names `tests/ui_contract/test_command_channel.py` and no such
  directory exists; the repository has `tests/ui_contracts/`. R2 measures it and
  R3 rules it, rather than a builder guessing mid-round.
- `npm run lint` in `apps/ui` is RED at base and is NOT a gate (R-0364): that
  configuration installs no TypeScript parser, which is R-0622 and routes to a
  paydown branch.
