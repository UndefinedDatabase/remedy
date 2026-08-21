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
R28 records the R27 verdict and appends the F008 R27 instance to R-0629, a
defect in the reviewer's own R27 block: a destructive control's prose claimed
a byte string also occurs in a second file, where it occurs zero times. It
changes no code. T003's client is now complete as a unit — rules, driver,
runner-as-store, the real host, the composition seam and the React hook — and
every piece of it below React is proved under the node-environment vitest.

## Next Steps
1. R29 puts the delayed badge on a visible surface and wires the hook's deps
   to the endpoint T001 and T002 built: the first round in which this
   feature's server half and client half meet. It may also resolve R-0628,
   whose hook has now landed and been reviewed under its contract.
2. Then the integration gate before closure.

## Risks
- `npm run lint` in `apps/ui` is RED at base and is NOT a gate (R-0364): that
  config installs no TypeScript parser, which is R-0622 and routes to a
  paydown branch.
- The badge is a visual surface docs/ui/design_reference/ binds, with any
  deviation owed an assumption_log entry carrying a technical reason.
- The hook's RENDER behaviour stays unproved until a DOM environment exists:
  its contract gates its source, and the seam beneath it carries the logic.
