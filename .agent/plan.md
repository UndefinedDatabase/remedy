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
R13 begins T002 with the resume decision itself. `Last-Event-ID` names the last
frame a client ALREADY holds, so the span it missed starts one PAST it, while
the query cursor names the position to start AT; conflating the two yields a
duplicate or a gap, and the acceptance test forbids both. `resolve_sse_start`
holds that rule alone, the stream branch resolves both inputs before entering
the writer, and a header that is absent, blank or mangled falls back to the
cursor rather than refusing the stream. R13 also records the R12 verdict and
registers R-0619.

## Next Steps
1. R14 adds T002's forced-disconnect hammer: kill the connection mid-stream N
   times and require the client transcript to byte-equal the ledger's envelope
   sequence.
2. Then T003's client hook, backoff, gap detection and polling fallback, then
   the integration gate before closure.

## Risks
- The slot registry is process-global mutable state. Every test that acquires a
  slot clears it first and the release runs in a `finally`; if either
  discipline lapses, a leaked slot makes a later round's 429 test pass for the
  wrong reason.
- A `_RemedyHandler` built with `__new__` carries no `headers`, so every test
  driving `do_GET` into the stream branch must set it. R13 sets it in the
  shared `_dispatch` helper and in the one test that builds its own handler.
- No open finding is a code defect of F008. R-0403, R-0607 through R-0609,
  R-0611 and R-0613 through R-0619 stay routed to a paydown branch, with the
  fix clauses of R-0387 and R-0573 promoted into the §3 checklist.
