# Plan — F278 Durable writes & loud failures

Branch: feature/f278-durable-writes-loud-failures, cut from `main` at
`9817a927`, the merge commit of pull request 265 (F283's closure).

## Goal

One durable write in this repository, used everywhere, and no artifact that is
silently incomplete (`docs/roadmap/features/T2_F278.md`).

## Current Step

ROUND 5 books round 4's PASS and DECISION F278 D4, then takes T003's first
slice: `stream_evidence.py`'s blind handlers are narrowed or recorded, and the
stream artifact gains `degradations`, both in `to_dict` and as
`stream_degraded` events.

## Next Steps

1. T003, the remaining blind handlers, module group by module group: each
   narrowed to the exception it expects or marked with a noqa reason.
2. T003, the last marking commit: BLE001 joins `select`, and the ratchet test
   freezes the count of excused handlers.
3. The closure sequence.

## Risks

About 257 handlers remain to be read, so the marking rounds are the bulk of
T003; a handler whose narrowing is not obvious is marked, never guessed.
