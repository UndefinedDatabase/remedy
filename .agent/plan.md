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
R16 BEGINS T003 with the client-side RULES alone, as a pure module rather than
as a React hook. `apps/ui/vitest.config.ts` sets `environment: "node"` and
collects `src/**/*.test.ts`, and the app carries no jsdom and no testing
library, so nothing here can render a hook; `apps/ui/src/cockpitLogic.ts`
states that same precedent in its own header comment. A new pure module beside
the existing API client therefore holds the status surface live |
reconnecting | delayed, the Last-Event-ID resume position, seq gap detection
and the reconnect backoff schedule, with a test file pinning each. R16 also
records the R15 verdict, resolves R-0620 and R-0621, and registers R-0622.

## Next Steps
1. R17 wraps that module in the React `useBrainStream` hook, adds T003's
   polling fallback on the same interface and the fixture live-job
   end-to-end.
2. Then the integration gate before closure.

## Risks
- `npm run lint` in `apps/ui` is RED at base and is NOT a gate (R-0364):
  measured at `22dd8d31` it exits 1 with 49 problems, and every error is a
  `Parsing error` because that eslint configuration parses no TypeScript at
  all. That defect is R-0622 and routes to a paydown branch. `npm run
  typecheck` and `npx vitest run` both exit 0 at that same commit and ARE the
  gates this round runs.
- Repository-wide `ruff check .` is RED and is not a gate (R-0364). This round
  changes no Python, so it moves that reading in neither direction.
- No open finding is a code defect of F008 reachable from the HTTP path. The
  open set lives in `.agent/live_review.md` and this file does not repeat it;
  R-0620 and R-0621 leave it this round and R-0622 enters it.
