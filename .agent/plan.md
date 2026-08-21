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
R3 discharges the findings order the feature file's Orchestrator brief
dispatches first. Both preconditions were MEASURED in the source and both
contradict a prediction the feature file carried: the UI server is not threaded,
so a long-lived response would block every other request; and `LedgerEvent`
carries no seq, the enumeration position being consumed into a hash and
discarded. This round registers that spec defect as R-0612, amends the feature
file with the measured state and rules the consequence as DECISION F008 D1.

## Next Steps
1. R4 makes the UI server threaded and proves it behaviourally — a slow
   request must stop blocking a concurrent one — as its own commit with its
   own tests. DECISION F008 D1 makes this a prerequisite of T001, not a part
   of it, because it is production code on a path every cockpit feature uses.
2. R5 builds T001 proper: the stream endpoint, the heartbeat, 404 and 429,
   and the framing golden, with seq read from the ledger position.
3. R6 onward builds T002 and T003 in the feature file's own order.

## Risks
- Making the server threaded touches a path every existing UI feature shares,
  so R4's blast radius is wider than its diff: the state-reader four and the
  dashboard contract are the suites that would show it.
- 184 findings are open once R-0612 lands and none is a code defect of F008.
  Promoting R-0387's clause into the §3 checklist edits `docs/agents/**` and
  stays routed to the paydown branch with R-0403, R-0607, R-0608, R-0609 and
  R-0611.
