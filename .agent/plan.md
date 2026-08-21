# Plan — F008 SSE event stream

Branch: feature/f008-sse-event-stream, cut from `main` at `7c03adfa`, the merge
commit of pull request #208. `.agent/live_review.md` is the source of truth for
the open set, the next free finding id and the round map.

## Goal
A per-job SSE endpoint streaming the event ledger from a cursor — the ledger's
own monotonic seq carried and never renumbered, a 15 s heartbeat, Last-Event-ID
resume replaying exactly the missed span — plus a client hook with reconnect
backoff, gap detection and an honest polling fallback that labels itself
delayed. DONE when a fake job streams into a test client with zero gaps across
forced disconnects, the transcript byte-equals the ledger's envelope sequence,
the heartbeat holds cadence, and the fallback engages on a disabled EventSource
and recovers to live.

## Current Step
R36 CLOSES F008. It records the R35 verdict — PASS, with the evidence bundle and
the READY_FOR_REVIEW package re-verified from disk by the reviewer — makes the
one docs pin that hard-codes the claimed feature independent of it, then lands
the authored STATUS `[x]` line, the README sync and the closure-candidate
carrier in ONE commit and opens the pull request. That pull request is NOT
merged this session: it merges at the next feature's Open PR Gate.

## Next Steps
1. The next session starts at Phase 1: the `.agent/STOP` re-read, then the Open
   PR Gate, where this feature's pull request is the one to merge.
2. Rule A5 then proposes F009 — The single write channel — the first `[ ]` line
   this ledger carries top to bottom. That feature's first reviewed round
   registers or resolves the entry `.agent/candidates.md` carries.

## Risks
- `npm run lint` in `apps/ui` is RED at base and is NOT a gate (R-0364): that
  config installs no TypeScript parser, which is R-0622 and routes to a paydown
  branch.
