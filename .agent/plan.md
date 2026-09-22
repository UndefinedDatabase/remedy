# Plan — F278 Durable writes & loud failures

Branch: feature/f278-durable-writes-loud-failures, cut from `main` at
`9817a927`, the merge commit of pull request 265 (F283's closure).

## Goal

One durable write in this repository, used everywhere, and no artifact that is
silently incomplete (`docs/roadmap/features/T2_F278.md`).

## Current Step

ROUND 2 books round 1's PASS and DECISION F278 D1, then lands T002's guard as
a ratchet and the first two migrations: `pingpong_job.atomic_write_text`
with its three importers, and `proposed_tasks._atomic_write`, each deleted in
the commit that moves its callers onto `durable_write`.

## Next Steps

1. T002, the boolean helpers: `real_test_execution`, `self_dogfood_execution`
   and `token_economy`, each keeping its call sites' boolean contract.
2. T002, `dev_server`'s three helpers with `runtime_supervisor` and
   `runtime_cmd`, and the inline writers in `repository_snapshot` and
   `project_registry`; the ratchet's set ends empty.
3. T003, loud failures: BLE001 enabled with a frozen ignore list, the nine
   handlers in `stream_evidence.py` first, a `degradations` field on the
   stream artifact, and a reason on every remaining ignored site.
4. The closure sequence.

## Risks

The directory fsync adds one system call per record written; the job,
checkpoint and mission records are small and written once per cycle.
