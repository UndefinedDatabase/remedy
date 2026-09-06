# Plan — F260 One world: mission → job → run

Branch: feature/f260-one-world, cut from `main` at b5cd6c20, the merge commit of
pull request 240 (F259). Rounds 1 and 2 are reviewed; round 2 PASSED and put the
measured inventory on disk as `.agent/f260_inventory.md`.

## Goal

One job model on disk. The classic store `<data_root>/jobs/<uuid>.json` and the
ping-pong store `<data_root>/task_jobs/<16hex>/job.json` become one record with
one id shape minted by one function; a Run becomes the evidence case a Job
points at; `resolve_any_job_id`, the "TWO job stores" paragraph and every
which-store branch are deleted. Task slicing per T2_F260.md: T001 inventory and
id shape, T002 records and writers, T003 consumers, T004 the classic runner,
T005 the reachability test and the cluster deletion.

## Current Step

Round 3 closes T001 by ruling DECISION F260 D1 (the record layout, and where a
Run's evidence lives) and D2 (the one id shape) from round 2's inventory, and
registers finding R-0814 — the split storage root that inventory measured, where
one ping-pong job files its record under `task_jobs/<16hex>/` and its evidence
under the classic store's `jobs/<16hex>/evidence/`. It changes no production
line; the code that implements the rulings is round 4.

## Next Steps

- T001 part 3: the one minting and resolving function, with its mutation
  red-proof, and every job-taking command moved onto it while both stores still
  exist.
- T002: the extended Mission record, the unified Job record under
  `jobs/<16hex>/`, and the run directory keyed by run id. R-0814 is fixed here,
  because the layout D1 rules is what removes the split root.
- T003 consumer by consumer, T004 the classic runner, T005 the reachability test
  and the cluster deletion, in that order.

## Risks

- D1 changes what `<data_root>/runs/` is keyed by, from job id to run id. Every
  reader of the old shape must move in the same commit as the writer, or a run
  log becomes unreadable between two commits.
- The T005 cluster deletion is large and reversible in one direction only. It
  runs last, behind a reachability test green BEFORE the first `git rm`.
