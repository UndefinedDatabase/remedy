# Plan — F008 SSE event stream

Branch: feature/f008-sse-event-stream, cut from `main` at `7c03adfa`, the merge
commit of pull request #208. `.agent/live_review.md` is the source of truth for
the open set, the next free finding id and the round map.

## Goal
A per-job SSE endpoint that streams the event ledger from a cursor — the
ledger's own monotonic seq carried and never renumbered, a 15 s heartbeat and
Last-Event-ID resume replaying exactly the missed span — plus a client hook
with reconnect backoff, gap detection and an honest polling fallback that
labels itself delayed. DONE when a fake job streams into a test client with
zero gaps across forced disconnects, the transcript byte-equals the ledger's
envelope sequence, the heartbeat holds cadence, and the fallback engages on a
disabled EventSource and recovers to live.

## Current Step
R27 lands `useBrainStream.ts`, the last piece of T003's client and the only
part of it React owns: it subscribes to the session R26 landed through
`useSyncExternalStore`, starts it in an effect and closes it in that effect's
cleanup, so a remounting cockpit cannot leak one EventSource per mount. It
keys the session on the job id alone and reads its dependency factory through
a ref, because a caller writing deps inline would otherwise tear the stream
down on every parent render. A new `tests/ui_contracts/` source contract gates
it, on comment-stripped source so a WHY comment cannot satisfy a guard.

## Next Steps
1. R28 puts the delayed badge on a visible surface and wires the hook's deps
   to the endpoint T001 and T002 built — the first round in which the server
   half and the client half of this feature meet.
2. Then the integration gate before closure.

## Risks
- `npm run lint` in `apps/ui` is RED at base and is NOT a gate (R-0364): that
  config installs no TypeScript parser, which is R-0622 and routes to a
  paydown branch.
- The badge is a visual surface docs/ui/design_reference/ binds, with any
  deviation owed an assumption_log entry carrying a technical reason.
- The hook's RENDER behaviour stays unproved until a DOM environment exists:
  the contract gates its source, and the session beneath it carries the logic.
