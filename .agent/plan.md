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
R14 CLOSES T002 with the acceptance test the feature file calls its heart: a
client that keeps losing its connection reconnects with the id of the last
frame it kept, and its final transcript must BYTE-EQUAL the ledger's envelope
sequence — no duplicate, no gap, at every disconnect cadence from one drop per
frame to none at all. The hammer is a test-only round: T002's resume decision
landed at R13, so this round proves it rather than building it, and a mutation
control shows the hammer goes red when resume exactness is broken. R14 also
records the R13 verdict, registers R-0620 and widens R-0371.

## Next Steps
1. R15 begins T003: the `useBrainStream` client hook, EventSource with
   reconnect backoff, gap detection via seq discontinuity, and the status
   surface live | reconnecting | delayed.
2. R16 adds T003's polling fallback on the same hook interface and the
   fixture live-job end-to-end.
3. Then the integration gate before closure.

## Risks
- The hammer drives `_send_sse_stream` directly rather than over a socket, so
  it proves the resume CONTRACT and not the transport. The transport is
  covered separately by the framing golden and the drain tests.
- `resolve_sse_start` narrows a non-string `Last-Event-ID` to the cursor
  because `str(x or "")` reads an integer 0 as absent. Registered as R-0620;
  the HTTP path only ever passes strings, so it is latent.
- No open finding is a code defect of F008 reachable from the HTTP path.
  R-0403, R-0607 through R-0609, R-0611 and R-0613 through R-0620 stay routed
  to a paydown branch.
