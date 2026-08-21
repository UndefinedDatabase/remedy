# Plan — F008 SSE event stream

Branch: feature/f008-sse-event-stream, cut from `main` at `7c03adfa`, the merge
commit of pull request #208. `.agent/live_review.md` is the source of truth for
the open set, the next free finding id and the round map.

## Goal
A per-job SSE endpoint streaming the event ledger from a cursor — the ledger's
own monotonic seq carried and never renumbered, a 15 s heartbeat, Last-Event-ID
resume replaying exactly the missed span — plus a client hook with reconnect
backoff, gap detection and an honest polling fallback that labels itself
delayed. DONE when a fake job streams into a test client with zero gaps across
forced disconnects, the transcript byte-equals the ledger's envelope sequence,
the heartbeat holds cadence, and the fallback engages on a disabled EventSource
and recovers to live.

## Current Step
R31 records the R30 verdict — PASS, every gate re-run by the reviewer out of the
committed blobs — and builds the real `BrainStreamHostDeps` factory over the
endpoint T001 and T002 shipped: `createBrainStreamHostDeps`, the cursor
arithmetic that makes a resume replay nothing and skip nothing, and the readers
for the events-since envelope, each gated by its own vitest tests. The factory
takes its environment INJECTED, so no global is read yet.

## Next Steps
1. R32 binds that environment to the browser's EventSource, fetch and timer,
   wires `useBrainStream` into `RemedyApp` over the new factory and passes its
   status down to the badge R29 built — the round in which this feature's two
   halves meet.
2. Then the integration gate before closure.

## Risks
- `npm run lint` in `apps/ui` is RED at base and is NOT a gate (R-0364): that
  config installs no TypeScript parser, which is R-0622 and routes to a
  paydown branch.
- The wiring round touches `RemedyApp.tsx`, the one file every cockpit surface
  renders through, so its blast radius is wider than any round since R4.
- The hook's RENDER behaviour stays unproved until a DOM environment exists:
  its contract gates its source, and the seam beneath it carries the logic.
