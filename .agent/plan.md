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
R5 lands the second half of DECISION F008 D1. The cursor-based events reader
returned a cursor for the response but no position for the individual events,
so a caller had to infer each event's place in the ledger. This round exposes
that position as `seq` and pins it with tests that fail if it ever becomes a
per-response counter. Together with R4's threading change, both prerequisites
D1 named are now met and the stream endpoint itself is unblocked.

## Next Steps
1. R6 begins the endpoint: `GET /api/jobs/<jid>/events/stream`, SSE framing
   with `seq` as the event id, a 15 s heartbeat comment frame, and 404 for an
   unknown job before any streaming starts. The route seam is the six-part
   path branch beside the existing `events-since` handler.
2. R7 adds the per-job connection cap answering 429 beyond it, and the
   framing golden the feature file names as T001's contract test.
3. R8 onward builds T002 — Last-Event-ID resume and the forced-disconnect
   hammer — then T003's client hook, then the integration gate.

## Risks
- The 50-event response cap in the reader is bounded RESPONSE size, not
  bounded numbering; T002's resume from an ancient cursor must page rather
  than assume one response covers the span.
- 185 findings are open and none is a code defect of F008. Promoting
  R-0387's clause into the §3 checklist edits `docs/agents/**` and stays
  routed to the paydown branch with R-0403, R-0607, R-0608, R-0609, R-0611
  and R-0613.
