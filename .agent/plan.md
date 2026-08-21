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
R4 discharges the prerequisite DECISION F008 D1 ruled. The cockpit server
instantiated `HTTPServer` bare and served one request at a time, so a single
long-lived SSE response would have blocked every other cockpit request for its
whole life. This round changes two lines to `ThreadingHTTPServer` and lands the
test that proves it: a `threading.Barrier` both requests must reach, which is a
fact about concurrency rather than a threshold about speed.

## Next Steps
1. R5 begins T001 proper: the stream endpoint, its 15 s heartbeat, 404 for an
   unknown job and 429 beyond the per-job connection cap, with seq read from
   the ledger position per DECISION F008 D1 and the framing golden as the
   contract test.
2. R6 builds T002: Last-Event-ID resume, gap-replay exactness and the
   forced-disconnect hammer whose transcript must byte-equal the ledger.
3. R7 onward builds T003 — the client hook, the fallback and the status
   states — and then the integration gate before closure.

## Risks
- Threading is live on a path every existing cockpit feature shares. The
  handler's three attributes are set once at construction and never mutated
  per request, so there is no shared-state race, but the state-reader four and
  the dashboard contract are the suites that would show a regression.
- 185 findings are open once R-0613 lands and none is a code defect of F008.
  Promoting R-0387's clause into the §3 checklist edits `docs/agents/**` and
  stays routed to the paydown branch with R-0403, R-0607, R-0608, R-0609,
  R-0611 and now R-0613.
