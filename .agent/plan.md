# Plan — F008 SSE event stream

Branch: feature/f008-sse-event-stream, cut from `main` at `7c03adfa`, the merge
commit of pull request #208. `.agent/live_review.md` is the source of truth for
the open set, the next free finding id and the round map.

## Goal
A per-job SSE endpoint that streams the event ledger from a cursor — the
ledger's own monotonic seq carried and never renumbered, a 15 s heartbeat and
Last-Event-ID resume replaying exactly the missed span — plus a client hook
with reconnect backoff, gap detection and an honest polling fallback that
labels itself delayed. DONE when a fake job streams into a test client with
zero gaps across forced disconnects, the transcript byte-equals the ledger's
envelope sequence, the heartbeat holds cadence, and the fallback engages on a
disabled EventSource and recovers to live.

## Current Step
R24 pins the stream host R23 landed: twelve tests over an injected source, an
injected snapshot read, an injected tail read and an injected scheduler, plus
three red controls — the malformed-frame guard, the close-before-reconnect and
the polling cursor. Only with this round is the adapter proved rather than
merely compiled. The round also records the R23 verdict.

## Next Steps
1. R25 adds the thin `useBrainStream` hook and the visible delayed badge,
   gated by typecheck and a `tests/ui_contracts/` source contract, the style
   this repository uses for every React component (R-0628).
2. Then the integration gate before closure.

## Risks
- The adapter OWNS a socket: `close` sits on the object its factory returns
  rather than on `BrainStreamHost`, so R25's hook must call it on unmount or
  a remounting cockpit leaks one EventSource per mount.
- `npm run lint` in `apps/ui` is RED at base and is NOT a gate (R-0364): that
  config installs no TypeScript parser, which is R-0622 and routes to a
  paydown branch.
- The badge remains a visual surface docs/ui/design_reference/ binds, with any
  deviation owed an assumption_log entry carrying a technical reason.
