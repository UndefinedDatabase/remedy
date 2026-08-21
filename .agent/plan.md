# Plan — F009 The single write channel

Branch: feature/f009-single-write-channel, cut from `main` at `ce49348b`, the
merge commit of pull request #209. `.agent/live_review.md` is the source of truth
for the open set, the round map and the finding-id ceiling, which is derived with
`max` over its line-anchored entries.

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
R4 registers R-0631 against the reviewer's own R3 gate design and records the R3
verdict. It writes no code: this session ends here at its stated four-round cap,
and the build opens the next one with DECISIONS F009 D1 through D9 already ruled.

## Next Steps
1. R5 lands T001's door: the POST route on `_RemedyHandler` dispatching
   `/api/jobs/<job_id>/commands`, the bearer plus X-Remedy-CSRF pair D2 rules,
   the request-shape validation with typed errors naming the offending field,
   and BOTH halves of D3's constant-time comparison in one commit — the existing
   GET check at the `token != self.server_token` line and the new POST check —
   compared as BYTES rather than as str, because `secrets.compare_digest` raises
   TypeError on a non-ASCII str and a query parameter is attacker-controlled.
   `import secrets` is already present, so D3 adds no import. Contract tests go
   in `tests/ui_server/test_command_channel.py` per D1.
2. R6 the catalog subset D4 rules and the rate limit D9 rules as a typed
   `ConfigKeySpec`; R7 the nonce store and audit record per D6, D7 and D8.
3. T003's effect table per D5, the plan-approval extraction landing as its own
   commit; then the integration gate, then closure.

## Risks
- R5 is the first round to touch `packages/orchestration/ui_server.py` on this
  branch and it changes a live authentication line. It is a SPLIT round, the
  `tests/ui_server/` suite gates it, and `tests/ui_server/test_live_state.py`
  already asserts the `invalid token` response the change must preserve.
- `npm run lint` in `apps/ui` is RED at base and is NOT a gate (R-0364), which is
  R-0622 and routes to a paydown branch.
