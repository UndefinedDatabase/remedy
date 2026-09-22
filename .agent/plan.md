# Plan — F278 Durable writes & loud failures

Branch: feature/f278-durable-writes-loud-failures, cut from `main` at
`9817a927`, the merge commit of pull request 265 (F283's closure).

## Goal

One durable write in this repository, used everywhere, and no artifact that is
silently incomplete (`docs/roadmap/features/T2_F278.md`).

## Current Step

ROUND 4 books round 3's PASS and DECISION F278 D3, then ends T002: the three
runtime helpers in `dev_server` are deleted and their callers in
`runtime_supervisor` and `runtime_cmd` import `durable_write`; the inline
writers in `repository_snapshot` and `project_registry` move onto it; the
guard's set is empty.

## Next Steps

1. T003, loud failures: BLE001 enabled with a frozen ignore list, the nine
   handlers in `stream_evidence.py` first, a `degradations` field on the
   stream artifact, and a reason on every remaining ignored site.
2. The closure sequence.

## Risks

A runtime record whose fsync fails now raises where it was suppressed; the
call sites that must not raise already carry their own `suppress`.
