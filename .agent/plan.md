# Plan — F008 SSE event stream

Branch: feature/f008-sse-event-stream, cut from `main` at the merge commit of
pull request #208, which THIS round merged at the Open PR Gate.
`.agent/live_review.md` is the source of truth for the open set, for the next
free finding id and for the round map; this file repeats none of them.

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
R1 opens the feature. It merges pull request #208 at the Open PR Gate, claims
F008 in `docs/roadmap/STATUS.md`, resets `.agent/live_review.md` for the new
branch while carrying the open set forward by id, and records the F255 R21
verdict — the closing round of the previous branch, whose gate entry can only
be written by the next reviewed round. No production code is written here.

## Next Steps
1. R2 inventories the ground the feature file's "How it fits" section names,
   MEASURED in the source rather than read off the feature file: whether
   ledger entries already carry a monotonic index, how the UI server serves a
   long-lived response and whether it is threaded, what the Part E envelope
   contract fixes, and how the existing state endpoint authenticates.
2. R3 records R2 and rules the stream's shape as a DECISION — threading, the
   heartbeat cadence, the max-connections guard and the fallback's contract —
   before any endpoint is written.
3. R4 onward builds T001, T002 and T003 in the feature file's own order.

## Risks
- The server-capability finding gates everything: the feature file's
  Orchestrator brief dispatches it first, and a stream built on an unthreaded
  stdlib server would block every other request the cockpit makes.
- 183 findings are open at this reset and none is a code defect of F008.
  R-0403, R-0607, R-0608, R-0609 and R-0611 are routed to a paydown branch
  and are deliberately not fixed here.
