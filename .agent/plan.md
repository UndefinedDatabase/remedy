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
R27 makes the P3 contract mechanical and records the R26 verdict. An AST guard
pins the exact import set the door's own methods may make, names the applicator
and shell/filesystem modules they may never reach, admits `save_job` alone out of
storage because DECISION F009 D5's effect mapping names it, and carries both the
violation fixture the feature file's Acceptance demands and a test that stops the
guard from emptying its own scan under a rename.

## Next Steps
1. The route-walking 405 test proving every other mutating POST, PUT and DELETE
   answers 405 — the last piece of T003.
2. Then the integration gate, then closure.

## Risks
- `answer_source` is a two-valued field the escalation assumption log COUNTS.
  DECISION F009 D22 rules that this door must NOT pass its own source into it,
  the opposite of D20's rule for `request_stop`; a later round that generalises
  one to the other silently drops answers from both tallies.
- `npm run lint` in `apps/ui` is RED at base and is NOT a gate (R-0364), which
  is R-0622 and routes to a paydown branch.
