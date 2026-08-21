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
R19 is a SMALL round that closes the record R18 left open and clears the last
naming defect out of T003's pure layer before a React file is added. It writes
the R18 verdict, resolves R-0624 — whose fix landed at `d3d5d1aa`, where the
runner declines to report a status until a transport event has resolved —
registers R-0627, and lands R-0626's rename of the driver's `opened` local to
`gapOpened`. No behaviour changes: the rename is proved neutral by the suite
staying at its count and by the snapshot branch still going red when forced.

## Next Steps
1. R20 adds the thin React `useBrainStream` hook over the runner and the
   visible delayed badge — the first surface that RENDERS the runner's view,
   and the round that must satisfy docs/ui/design_reference/ for the badge.
2. Then the integration gate before closure.

## Risks
- `npm run lint` in `apps/ui` is RED at base and is NOT a gate (R-0364):
  measured at `f484d47a` it exits 1 with 55 problems, every error a
  `Parsing error`, because that eslint config installs no TypeScript parser.
  That is R-0622, it routes to a paydown branch, and each new `.ts` file adds
  one more. `npm run typecheck` and `npx vitest run` both exit 0 there and ARE
  the gates. Repository-wide `ruff check .` is RED too and is not a gate; this
  round changes no Python.
- R20 is the round where a gate this repository owns stops covering the code:
  no React component can be rendered here. The runner is framework-free so the
  hook has almost no branch left to get wrong, but the BADGE is a visual
  surface and docs/ui/design_reference/ is binding for it, with any deviation
  owed an assumption_log entry carrying a technical reason. If the hook cannot
  be kept trivial, the honest move is a jsdom dependency and its own round.
- R-0626's fix lands here and its `Done:` paragraph is owed by R20, exactly as
  R18 left R-0624's resolution to this round.
