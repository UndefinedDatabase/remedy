# Plan — F008 SSE event stream

Branch: feature/f008-sse-event-stream, cut from `main` at `7c03adfa`, the merge
commit of pull request #208. `.agent/live_review.md` is the source of truth for
the open set, the next free finding id and the round map; this file repeats
none of them.

## Goal
A per-job SSE endpoint that streams the event ledger from a cursor — the
ledger's own monotonic seq carried and never renumbered, a 15 s heartbeat, and
Last-Event-ID resume replaying exactly the missed span — plus a client hook
with reconnect backoff, gap detection and an honest polling fallback that
labels itself delayed. DONE when a fake job streams into a test client with
zero gaps across forced disconnects, the client transcript byte-equals the
ledger's envelope sequence, the heartbeat holds cadence, and the fallback
engages on a disabled EventSource and recovers to live.

## Current Step
R20 makes the driver the single authority on what the client does next and
writes the record R19 left open. `start()` stops calling `host.connect`
itself and dispatches the opening event, so `perform` issues the effect the
driver chose — R-0627's fix. It is not a pure refactor: after the fallback has
engaged a restart now polls where it used to reopen a stream, so a new test
pins that. The round also writes the R19 verdict and resolves R-0626, whose
rename of the driver's gap local landed at `c1051495`.

## Next Steps
1. R21 adds the thin React `useBrainStream` hook over the runner and the
   visible delayed badge. Neither jsdom nor a testing library is installed, so
   R21 opens with that dependency decision and owns it.
2. Then the integration gate before closure.

## Risks
- `npm run lint` in `apps/ui` is RED at base and is NOT a gate (R-0364):
  measured at `1f10de78` it exits 1 with 55 problems, every error a
  `Parsing error`, because that eslint config installs no TypeScript parser.
  That is R-0622 and it routes to a paydown branch. `npm run typecheck` and
  `npx vitest run` both exit 0 there and ARE the gates. Repository-wide
  `ruff check .` is RED too and is not a gate; this round changes no Python.
- `noUnusedLocals` is on, so dropping the `resumeEventId` call orphans its
  import and turns typecheck red. R20 carries the import line for that reason:
  one indivisible edit, not scope drift.
- R21 is the round where a gate this repository owns stops covering the code:
  no React component can be rendered here today. The runner is framework-free
  so the hook has almost no branch left to get wrong, but the BADGE is a
  visual surface and docs/ui/design_reference/ is binding for it, any
  deviation owed an assumption_log entry with a technical reason.
- R-0627's fix lands here and its `Done:` paragraph is owed by R21, exactly as
  R19 left R-0626's resolution to this round.
