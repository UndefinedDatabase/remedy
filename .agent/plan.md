# Plan — F008 SSE event stream

Branch: feature/f008-sse-event-stream, cut from `main` at `7c03adfa`, the merge
commit of pull request #208. `.agent/live_review.md` is the source of truth for
the open set, for the next free finding id and for the round map; this file
repeats none of them.

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
R2 records the R1 verdict and repairs the red R1 was forbidden to touch. R1
claimed F008 correctly, but one line of `tests/docs/test_docs_consistency.py`
pinned F008 to the UNSTARTED marker, so the claim had to turn that suite red
while R1's own change set excluded every path under `tests/`. This round
replaces that pin with the invariant the workflow actually holds — exactly one
`[~]` entry exists and F008 is its holder — which is strictly stronger than
the sentence it retires. No production code is written here either.

## Next Steps
1. R3 inventories the ground the feature file's "How it fits" section names,
   MEASURED in the source rather than read off the feature file: whether
   ledger entries already carry a monotonic index, how the UI server serves a
   long-lived response and whether it is threaded, what the Part E envelope
   contract fixes, and how the existing state endpoint authenticates.
2. R4 records R3 and rules the stream's shape as a DECISION — threading, the
   heartbeat cadence, the max-connections guard and the fallback's contract —
   before any endpoint is written.
3. R5 onward builds T001, T002 and T003 in the feature file's own order.

## Risks
- The server-capability finding gates everything: the feature file's
  Orchestrator brief dispatches it first, and a stream built on an unthreaded
  stdlib server would block every other request the cockpit makes.
- 183 findings stay open and none is a code defect of F008. R1's red was a
  recurrence of R-0387, not a new id; promoting that finding's clause into the
  §3 checklist edits `docs/agents/**` and is routed to the paydown branch that
  already carries R-0403, R-0607, R-0608, R-0609 and R-0611.
