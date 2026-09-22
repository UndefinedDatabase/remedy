# Plan — F278 Durable writes & loud failures

Branch: feature/f278-durable-writes-loud-failures, cut from `main` at
`9817a927`, the merge commit of pull request 265 (F283's closure).

## Goal

One durable write in this repository, used everywhere, and no artifact that is
silently incomplete (`docs/roadmap/features/T2_F278.md`).

## Current Step

ROUND 3 books round 2's PASS and DECISION F278 D2, then migrates the three
boolean helpers — `real_test_execution`, `self_dogfood_execution` and
`token_economy` — onto `durable_write`, one module per commit, each deleting
its copy and its entry in the guard's set.

## Next Steps

1. T002, the last group: `dev_server`'s three helpers with
   `runtime_supervisor` and `runtime_cmd`, and the inline writers in
   `repository_snapshot` and `project_registry`; the guard's set ends empty.
2. T003, loud failures: BLE001 enabled with a frozen ignore list, the nine
   handlers in `stream_evidence.py` first, a `degradations` field on the
   stream artifact, and a reason on every remaining ignored site.
3. The closure sequence.

## Risks

A snapshot proof or a self-use request whose write fails now raises instead
of returning an artifact with no record on disk (DECISION F278 D2).
