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
R29 records the R28 verdict, amends R-0553 with the F008 R28 instance — a
handback that corrected an unmeasured universal and wrote a fresh one in the
same sentence — and puts the DELAYED badge on a visible surface. The pill now
reads the transport's status ahead of the dashboard's liveness, so a client on
the polling fallback says DELAYED rather than LIVE, this feature's own
acceptance condition. `streamStatus` is optional on both the pill and the panel
because no caller holds one until R30.

## Next Steps
1. R30 builds the real `BrainStreamHostDeps` factory over the endpoint T001 and
   T002 shipped, wires `useBrainStream` into `RemedyApp` and passes its status
   down to the badge: the round in which this feature's two halves meet.
2. Then the integration gate before closure.

## Risks
- `npm run lint` in `apps/ui` is RED at base and is NOT a gate (R-0364): that
  config installs no TypeScript parser, which is R-0622 and routes to a
  paydown branch.
- The badge reuses the pill's documented variant mechanism and an existing
  token, so no assumption_log entry is owed; DECISION F008 D2 in
  `.agent/decisions.md` records that reading and how to reverse it.
- The hook's RENDER behaviour stays unproved until a DOM environment exists:
  its contract gates its source, and the seam beneath it carries the logic.
