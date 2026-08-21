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
R18 CONTINUES T003 with the effect RUNNER: the loop that PERFORMS what R17's
driver decides. Effects become calls on an INJECTED host — connect, snapshot,
poll, schedule — so the reconnect, gap and fallback cycle runs headless under
the node-environment vitest against a recording host and a hand-fired clock.
That is the feature file's "fake job streaming into a headless client" at the
client-logic level, and it is what keeps R19's React hook thin enough to be
honest. R18 also fixes R-0624 by declining to report a status before the first
transport event resolves, records the R17 verdict, resolves R-0623 and
registers R-0625 and R-0626.

## Next Steps
1. R19 adds the thin React `useBrainStream` hook subscribing to the runner,
   the visible delayed badge and R-0626's rename; the badge is what finally
   renders the runner's view.
2. Then the integration gate before closure.

## Risks
- `npm run lint` in `apps/ui` is RED at base and is NOT a gate (R-0364):
  measured at `2c3abc5e` it exits 1 with 53 problems, every error a
  `Parsing error`, because that eslint config installs no TypeScript parser.
  That is R-0622, it routes to a paydown branch, and each new `.ts` file adds
  one more. `npm run typecheck` and `npx vitest run` both exit 0 there and ARE
  the gates. Repository-wide `ruff check .` is RED too and is not a gate; this
  round changes no Python.
- No React hook can be rendered by any gate this repository owns. R18 adds
  none: the runner is framework-free on purpose, so R19's hook has no branch
  left to get wrong. If that stops being true, the honest move is a jsdom
  dependency and its own round, never an untested hook.
- R-0624's fix lands here and its `Done:` paragraph is owed by R19, exactly as
  R17 left R-0623 to this round.
