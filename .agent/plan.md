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
R22 records the R21 verdict and registers R-0628, which retires the claim that
T003 is blocked until a DOM environment can be installed. It changes no code:
the ordering that finding fixes is what the next two rounds execute.

## Next Steps
1. R23 builds the REAL host behind `BrainStreamHost` — an injected
   EventSource, a snapshot read, a tail read and a scheduler — the piece the
   hook cannot exist without, proved under the node-environment vitest with
   no DOM at all.
2. R24 adds the thin `useBrainStream` hook over the runner store and the
   visible delayed badge, gated by `npm run typecheck` and a
   `tests/ui_contracts/` source contract — the style this repository already
   uses for every React component.
3. Then the integration gate before closure.

## Risks
- `npm run lint` in `apps/ui` is RED at base and is NOT a gate (R-0364): it
  exits 1 because that eslint config installs no TypeScript parser, which is
  R-0622 and routes to a paydown branch. `npm run typecheck` and
  `npx vitest run` both exit 0 and ARE the gates.
- The adapter R23 adds owns a socket, so a leak is the failure mode to fear:
  `close` belongs on the object its factory returns rather than on
  `BrainStreamHost`, and R24's hook must call it on unmount.
- The badge remains a visual surface docs/ui/design_reference/ binds, with any
  deviation owed an assumption_log entry carrying a technical reason.
