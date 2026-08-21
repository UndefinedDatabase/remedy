# Plan — F008 SSE event stream

Branch: feature/f008-sse-event-stream, cut from `main` at `7c03adfa`, the merge
commit of pull request #208. `.agent/live_review.md` is the source of truth for
the open set, the next free finding id and the round map; this file repeats
none of them.

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
R10 wires T001's reader to the route. `GET /api/jobs/<jid>/events/stream` is a
six-part path branch in `_RemedyHandler.do_GET`, `drain_sse_frames` writes the
generator's frames to the socket and ends the loop when the peer goes away, and
an unknown job answers 404 before one byte of stream. The server was already
threaded, so an open stream no longer blocks the rest of the cockpit.

## Next Steps
1. R11 adds the per-job connection cap answering 429 beyond it and the framing
   golden the feature file names as T001's contract test.
2. R12 onward builds T002 — Last-Event-ID resume, read from the header or the
   query, and the forced-disconnect hammer whose transcript must byte-equal the
   ledger.
3. Then T003's client hook, backoff, gap detection and polling fallback, then
   the integration gate before closure.

## Risks
- A streaming handler holds a socket open. The reader cannot observe a broken
  pipe from inside a `yield`, so the writer owns the flag its `should_continue`
  reads; if that flag is ever dropped, a departed peer leaks a thread that
  polls the ledger forever.
- No open finding is a code defect of F008. R-0403, R-0607, R-0608, R-0609,
  R-0611, R-0613, R-0614, R-0615 and R-0616 stay routed to a paydown branch,
  together with promoting the fix clauses of R-0387 and R-0573 into the §3
  checklist.
