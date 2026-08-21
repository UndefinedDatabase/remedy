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
R8 registers R-0614, records the R6 and R7 verdicts, and re-issues the bundle
R7 halted on: T001's stream READER — the SSE frame builders, the safe
per-event envelope both event transports share, and the frame generator that
carries the ledger position as the event id and heartbeats while idle. R7
halted because one authored slice reached its worker with the escapes of two
byte-string literals doubled; those characters are corrected here and every
other byte of the bundle is unchanged.

## Next Steps
1. R9 wires the reader to the route: `GET /api/jobs/<jid>/events/stream` as a
   six-part path branch beside the existing `events-since` handler in
   `_RemedyHandler.do_GET`, the response writer that drains the generator into
   the socket, and 404 for an unknown job before one byte of stream.
2. R10 adds the per-job connection cap answering 429 beyond it and the framing
   golden the feature file names as T001's contract test.
3. R11 onward builds T002 — Last-Event-ID resume and the forced-disconnect
   hammer whose transcript must byte-equal the ledger — then T003's client
   hook and fallback, then the integration gate before closure.

## Risks
- A streaming handler holds a socket open. The reader takes `should_continue`
  from its caller, so R9's writer must bound the loop by the peer's
  disconnect, and no test may drive that route over a real socket without a
  hard timeout and a guaranteed close.
- No open finding is a code defect of F008. R-0403, R-0607, R-0608, R-0609,
  R-0611, R-0613 and R-0614 stay routed to a paydown branch, together with
  promoting the fix clauses of R-0387 and R-0573 into the §3 checklist.
