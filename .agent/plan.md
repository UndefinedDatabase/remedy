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
R12 records the R11 verdict, registers R-0618, and closes this session at its
round cap. This round writes no code. T001 is COMPLETE and reviewed as of R11:
the frame builders and the shared envelope, the frame generator that carries
the ledger position as the SSE event id and heartbeats while idle, the
six-part route, the socket writer that ends the loop when the peer goes away,
404 before one byte of stream, the per-job slot cap answering 429, and the
framing golden that pins the wire bytes.

## Next Steps
1. R13 begins T002: Last-Event-ID resume, read from the request header and
   falling back to the query cursor, replaying exactly the missed span from the
   ledger — which IS the buffer, so there is no in-memory ring to lose.
2. R14 adds T002's forced-disconnect hammer: kill the connection mid-stream N
   times and require the client transcript to byte-equal the ledger's envelope
   sequence.
3. Then T003's client hook, backoff, gap detection and polling fallback, then
   the integration gate before closure.

## Risks
- The slot registry is process-global mutable state. Every test that acquires a
  slot clears it first, and the release runs in a `finally`; if either
  discipline lapses, a leaked slot makes a later round's 429 test pass for the
  wrong reason.
- No open finding is a code defect of F008. R-0403, R-0607, R-0608, R-0609,
  R-0611, R-0613, R-0614, R-0615, R-0616, R-0617 and R-0618 stay routed to a
  paydown branch, together with promoting the fix clauses of R-0387 and R-0573
  into the §3 checklist.
