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
R6 records the R5 verdict and closes this session at its stated round cap. Both
prerequisites DECISION F008 D1 named are now landed and reviewed: the cockpit
server serves concurrent requests, and the events reader exposes each event's
ledger position as `seq`. No endpoint exists yet. This round writes no code.

## Next Steps
1. R7 begins T001's endpoint: `GET /api/jobs/<jid>/events/stream`, SSE framing
   with `seq` as the event id, a 15 s heartbeat comment frame, and 404 for an
   unknown job before any streaming starts. The route seam is a six-part path
   branch beside the existing `events-since` handler in `_RemedyHandler.do_GET`.
2. R8 adds the per-job connection cap answering 429 beyond it and the framing
   golden the feature file names as T001's contract test.
3. R9 onward builds T002 — Last-Event-ID resume and the forced-disconnect
   hammer whose transcript must byte-equal the ledger — then T003's client
   hook and fallback, then the integration gate before closure.

## Risks
- A streaming handler holds a socket open. Every test that opens one needs a
  hard timeout and a guaranteed close, or a hung test will cost a round; the
  barrier pattern R4 used is the model — assert a fact, never a duration.
- The 50-event cap in the reader bounds the RESPONSE, not the numbering, so
  T002's resume from an ancient cursor must page rather than assume one
  response covers the span.
- 185 findings are open and none is a code defect of F008. R-0403, R-0607,
  R-0608, R-0609, R-0611 and R-0613 stay routed to a paydown branch, together
  with promoting R-0387's and R-0573's fix clauses into the §3 checklist.
