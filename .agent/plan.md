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
R21 turns the runner into a STORE: `subscribe` plus a view whose object
identity is stable across calls that change nothing. That pair is exactly what
React's `useSyncExternalStore` requires, and it is the last piece of T003
provable under the node-environment vitest. The round also writes the R20
verdict and resolves R-0627, whose fix — the driver as the single author of a
`connect` — landed at `732091d9`.

## Next Steps
1. R22 adds the thin React `useBrainStream` hook over this store and the
   visible delayed badge. IT IS BLOCKED until a session can install a DOM
   environment: no jsdom, happy-dom or testing library is present and the
   R21 session's command guard denied the npm commands that would add one.
2. Then the integration gate before closure.

## Risks
- `npm run lint` in `apps/ui` is RED at base and is NOT a gate (R-0364):
  measured at `b97fb0b7` it exits 1 with 55 problems, every error a
  `Parsing error`, because that eslint config installs no TypeScript parser.
  That is R-0622 and it routes to a paydown branch. `npm run typecheck` and
  `npx vitest run` both exit 0 there and ARE the gates. Repository-wide
  `ruff check .` is RED too and is not a gate; this round changes no Python.
- A store that returns a fresh view object on every call sends
  `useSyncExternalStore` into an endless re-render. Identity stability is
  therefore a CONTRACT of this seam and not an optimisation, and R21 pins it
  with its own test and its own red control.
- The badge remains a visual surface docs/ui/design_reference/ binds, with any
  deviation owed an assumption_log entry carrying a technical reason. R22
  owns that, together with the dependency decision it cannot avoid.
