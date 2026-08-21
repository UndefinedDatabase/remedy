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
R15 PAYS DOWN T002's two authored defects rather than only recording them.
R-0620: `resolve_sse_start` guarded with `str(x or "")`, which reads the
integer 0 — the first ledger position — as an absent header; the guard becomes
an explicit None test and three tests pin the integer forms. R-0621: the
grown-ledger test started its second client from scratch, so the boundary its
name promised was never crossed by a resume; the hammer helper now accepts a
starting last-event-id and the test resumes across the growth. R15 also
records the R14 verdict and widens R-0371 a third time.

## Next Steps
1. R16 begins T003: the `useBrainStream` client hook, EventSource with
   reconnect backoff, gap detection via seq discontinuity, and the status
   surface live | reconnecting | delayed.
2. R17 adds T003's polling fallback on the same hook interface and the
   fixture live-job end-to-end.
3. Then the integration gate before closure.

## Risks
- The hammer drives `_send_sse_stream` directly rather than over a socket, so
  it proves the resume CONTRACT and not the transport. The transport stays
  covered by the framing golden and the drain tests.
- Repository-wide `ruff check .` is RED and is not a gate (R-0364), and
  `--preview` reports three pre-existing E306 in
  `packages/orchestration/ui_server.py`. Ruff is gated scoped to the touched
  files as a rule-code MULTISET, base against head, so a pre-existing finding
  is never read as a new one.
- No open finding is a code defect of F008 reachable from the HTTP path.
  R-0403, R-0607 through R-0609, R-0611 and R-0613 through R-0621 stay routed
  to a paydown branch, R-0620 and R-0621 being closed by this round's own
  commits.
