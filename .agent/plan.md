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
R17 CONTINUES T003 with the transport ORCHESTRATION, still pure. R16 built the
rules a client holds; a new driver module says what it should DO next, as a
reducer returning effects as DATA — connect, wait, snapshot, poll — so the
reconnect schedule, the gap-to-snapshot-to-resume path and the polling
fallback are decided in code the node-environment vitest can run. Nothing
performs an effect yet: no EventSource, no timer, no fetch. R17 also pins the
backoff cap against a LITERAL (R-0623), records the R16 verdict and registers
R-0623 and R-0624.

## Next Steps
1. R18 adds the thin React `useBrainStream` hook interpreting the driver's
   effects, the visible delayed badge and the fixture live-job end-to-end;
   R-0624's fix lands there, with the badge that exposes it.
2. Then the integration gate before closure.

## Risks
- `npm run lint` in `apps/ui` is RED at base and is NOT a gate (R-0364):
  measured at `eb2e011c` it exits 1 with 51 problems, every error a
  `Parsing error`, because that eslint configuration installs no TypeScript
  parser. That is R-0622, it routes to a paydown branch, and each new `.ts`
  file adds one more such error. `npm run typecheck` and `npx vitest run`
  both exit 0 at that commit and ARE the gates.
- A React hook still cannot be rendered by any gate this repository owns, so
  R18's hook stays thin enough that typecheck plus the driver's tests cover
  it. If that stops being true, the honest move is a jsdom dependency and its
  own round, never an untested hook.
- Repository-wide `ruff check .` is RED and is not a gate (R-0364); this round
  changes no Python.
- No open finding is a code defect of F008 reachable from the HTTP path; the
  open set lives in `.agent/live_review.md`, not here. R-0623 and R-0624 both
  ENTER it this round, and R-0623's fix lands here too, so R18 resolves it.
