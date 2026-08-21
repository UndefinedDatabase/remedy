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
R25 records the R24 verdict and registers R-0629, a defect in the reviewer's
own R24 block: a red control asserted that its target line occurs once when it
occurs twice. It changes no code. T003's client side is now rules, driver,
runner-as-store and the real host, each proved under the node-environment
vitest.

## Next Steps
1. R26 adds the thin `useBrainStream` hook over the runner store and the
   visible delayed badge, gated by `npm run typecheck` and a
   `tests/ui_contracts/` source contract — the style this repository uses for
   every React component (R-0628). The hook must call the host's `close` on
   unmount, or a remounting cockpit leaks one EventSource per mount.
2. Then the integration gate before closure.

## Risks
- `npm run lint` in `apps/ui` is RED at base and is NOT a gate (R-0364): that
  config installs no TypeScript parser, which is R-0622 and routes to a
  paydown branch.
- The badge is a visual surface docs/ui/design_reference/ binds, with any
  deviation owed an assumption_log entry carrying a technical reason.
- Nothing wires the host to a real job yet: R26 is the first round in which
  the endpoint T001 built and the client T003 built meet.
