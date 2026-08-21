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
R5 closes this session. It registers R-0632, rules the open-count derivation as
DECISION F009 D10, records the R4 verdict, and rewrites the handback with the
number D10's rule produces. IT IS DECLARED AS A FIFTH ROUND AGAINST A STATED
FOUR-ROUND CAP: the reviewer found, while auditing the R4 handback, that three
authored texts this session each stated a different open-finding count and none
was derived by the only rule this repository has written down. A finding that
exists only in a session's chat is lost when that session ends, so persisting it
was worth one short round; taking on NEW work would not have been.

## Next Steps
1. R6 is the first BUILD round: T001's door — the POST route on `_RemedyHandler`
   dispatching `/api/jobs/<job_id>/commands`, the bearer plus X-Remedy-CSRF pair
   D2 rules, request-shape validation with typed errors naming the offending
   field, and BOTH halves of D3's constant-time comparison in one commit,
   compared as BYTES rather than as str, because `secrets.compare_digest` raises
   TypeError on a non-ASCII str and a query parameter is attacker-controlled.
   `import secrets` is already present, so D3 adds no import. Contract tests go
   in `tests/ui_server/test_command_channel.py` per D1.
2. R7 the catalog subset D4 rules and the rate limit D9 rules as a typed
   `ConfigKeySpec`; R8 the nonce store and audit record per D6, D7 and D8.
3. T003's effect table per D5, the plan-approval extraction landing as its own
   commit; then the integration gate, then closure.

## Risks
- R6 is the first round to touch `packages/orchestration/ui_server.py` on this
  branch and it changes a live authentication line. It is a SPLIT round and
  `tests/ui_server/test_live_state.py` already asserts the `invalid token`
  response the change must preserve.
- `npm run lint` in `apps/ui` is RED at base and is NOT a gate (R-0364), which is
  R-0622 and routes to a paydown branch.
