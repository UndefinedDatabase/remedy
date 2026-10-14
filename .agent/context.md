# Context — F308 The run manifest survives a task split

## Active Branch
feature/f308-run-manifest-task-split, from `main` at `1622c16d7` (the merge commit of pull request
336, operator amendment amend1014-luna-mission-fixes).

## Scope
F308 (Tier 2), as `docs/roadmap/features/T2_F308.md` and DECISION F308 D1 state: the structural
steps into `packages/orchestration/run_task_list.py`, then the split record, the F7 check of
`build_run_manifest`, the task statuses and decoders that read the declared task list, and the
proof through the real split path. R-1252 is the finding it resolves.

## Do not touch
The manifest's hash chain, and the F7 refusal of an edit of the task list from outside. A
structural step changes no behaviour.

## Active assumptions
- A manifest written before F308 must stay byte-identical when read and written back.
- Every repair lands with a test that is red without it, proved by the reviewer's mutation; a
  structural step is proved by the unchanged tests.

## Constraints
- Every pytest run in a round is targeted; the closure runs the one full suite.
- A round touching `docs/roadmap/**` also gates `tests/docs/`.
- Per amend0930-test-load: no block, worker or reviewer sets `REMEDY_TEST_MAX_WORKERS`, passes a
  larger `-n`, or starts two test runs at once; mutation red-proofs are run by the reviewer only.
- Destructive verification runs only inside a disposable git worktree under `.remedy-wt/`.
- The functions and files on `docs/system/structure-ledger-v1.md` may not grow.

## Steps
The item-status table for each round lives in that round's handback, `.agent/handoff.md`.
