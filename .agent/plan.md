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
R26 lands `brainStreamSession.ts`, the composition seam T003 has been building
toward: it ties the host to the runner store — a knot neither half can tie, the
host dispatching into a runner that does not exist when the host is built — and
gives the React hook one object to hold, whose `close` stops the runner AND the
socket. Six vitest tests pin start, live, frame delivery, both halves of close
and the delayed fallback.

## Next Steps
1. R27 adds `useBrainStream.ts` over this seam and its `tests/ui_contracts/`
   source contract — the style every React component here is gated by
   (R-0628) — with the hook closing the session on unmount, or a remounting
   cockpit leaks one EventSource per mount.
2. R28 puts the delayed badge on a visible surface and wires the hook's deps
   to the endpoint T001 and T002 built.
3. Then the integration gate before closure.

## Risks
- `npm run lint` in `apps/ui` is RED at base and is NOT a gate (R-0364): that
  config installs no TypeScript parser, which is R-0622 and routes to a
  paydown branch.
- The badge is a visual surface docs/ui/design_reference/ binds, with any
  deviation owed an assumption_log entry carrying a technical reason.
- The hook's RENDER behaviour stays unproved until a DOM environment exists:
  its contract will gate its source, and this seam carries the logic beneath.
