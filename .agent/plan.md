# Plan — F260 One world: mission → job → run

Branch: feature/f260-one-world, cut from `main` at b5cd6c20, the merge commit of
pull request 240 (F259). Rounds 1 to 6 are reviewed; 2 through 6 PASSED. T001 is
CLOSED. T002 is open: `data_paths` now holds the one spelling of DECISION F260
D1's layout, and DECISION F260 D4 records why the resolver waits for the store.

## Goal

One job model on disk. The classic store `<data_root>/jobs/<uuid>.json` and the
ping-pong store `<data_root>/task_jobs/<16hex>/job.json` become one record with
one id shape minted by one function per kind; a Run becomes the evidence case a
Job points at; `resolve_any_job_id`, the "TWO job stores" paragraph and every
which-store branch are deleted. Task slicing per T2_F260.md: T001 inventory and
id shape, T002 records and writers, T003 consumers, T004 the classic runner,
T005 the reachability test and the cluster deletion.

## Current Step

Finish the layout consolidation. The four remaining hand-built
`jobs_dir() / <id> / "evidence"` expressions — two in `job_evidence.py`, one in
`repair_attest.py`, one in `do_cmd.py` — move onto
`data_paths.job_evidence_dir`, and the round-6 guard widens from one module to
the whole set that owns a job's evidence. `checkpoints.py` and `storage.py` keep
their `jobs_dir` calls: they name the CLASSIC store, which T004 deletes.

## Next Steps

- The unified Job record and its writer under `jobs/<16hex>/job.json`, moving
  `_persist_job` and `load_job_plan` off `task_jobs/` and DELETING
  `pingpong_job._jobs_dir`. Finding R-0814 is resolved there, against the fix
  clause it already carries.
- The ONE resolver, in the same round group as that writer, because 40 of the
  42 job-taking call sites take a `UUID` today (DECISION F260 D4).
- Then `runs/<run_id>/` keyed by run id, T003 consumer by consumer, T004 the
  classic runner, T005 the reachability test and the cluster deletion.

## Risks

- D1 changes what `<data_root>/runs/` is keyed by, from job id to run id. Every
  reader of the old shape must move in the same commit as its writer, or a run
  log becomes unreadable between two commits.
- `job_record_path` names a path nothing writes yet; its docstring says so and
  the writer round is what makes it live.
- The T005 cluster deletion is large and reversible in one direction only. It
  runs last, behind a reachability test green BEFORE the first `git rm`.
