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
R23 lands the REAL host behind `BrainStreamHost`: an injected EventSource, a
snapshot read, a tail read and a scheduler, so the driver's effects reach a
transport. Every dependency is injected, so no DOM is involved. The module
COMPILES at this round and is not yet exercised: `npm run typecheck` is its
only gate here, and R24 brings its suite and its red controls. The round also
records the R22 verdict.

## Next Steps
1. R24 pins the adapter with its own vitest suite and three red controls —
   the malformed-frame guard, the close-before-reconnect and the polling
   cursor — and only then is the module proved rather than merely compiled.
2. R25 adds the thin `useBrainStream` hook and the visible delayed badge,
   gated by typecheck and a `tests/ui_contracts/` source contract, the style
   this repository uses for every React component (R-0628).
3. Then the integration gate before closure.

## Risks
- Untested code lands at R23 by design, one round ahead of its suite. The
  ordering is deliberate — AGENTS.md forbids one commit carrying a change and
  the tests that pin it — but until R24 the adapter's only evidence is that
  it typechecks, and no round may claim more for it than that.
- `npm run lint` in `apps/ui` is RED at base and is NOT a gate (R-0364): that
  config installs no TypeScript parser, which is R-0622.
- The adapter OWNS a socket: `close` sits on the object its factory returns
  rather than on `BrainStreamHost`, and R25's hook must call it on unmount.
