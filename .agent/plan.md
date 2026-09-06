# Plan — F260 One world: mission → job → run

Branch: feature/f260-one-world, cut from `main` at b5cd6c20, the merge commit of
pull request 240 (F259). Rounds 1 to 5 are reviewed; 2, 3, 4 and 5 PASSED. T001
is CLOSED: the inventory, DECISION F260 D1 and D2, the three minting functions
and their four call sites are all on disk.

## Goal

One job model on disk. The classic store `<data_root>/jobs/<uuid>.json` and the
ping-pong store `<data_root>/task_jobs/<16hex>/job.json` become one record with
one id shape minted by one function per kind; a Run becomes the evidence case a
Job points at; `resolve_any_job_id`, the "TWO job stores" paragraph and every
which-store branch are deleted. Task slicing per T2_F260.md: T001 inventory and
id shape, T002 records and writers, T003 consumers, T004 the classic runner,
T005 the reachability test and the cluster deletion.

## Current Step

Open T002 with the LAYOUT, ruling first why the resolver is not in T001.
DECISION F260 D4 records that measurement. Then `data_paths` gains the one
spelling of DECISION F260 D1's layout — `job_dir`, `job_record_path`,
`job_evidence_dir` and `run_dir` — and `pingpong_job`'s two hand-built evidence
paths are built from it. Nothing moves on disk yet: the paths are the target
spelling every T002 writer will use.

## Next Steps

- The four remaining hand-built evidence paths — `job_evidence.py` twice,
  `repair_attest.py` and `do_cmd.py` — onto `data_paths.job_evidence_dir`, with
  a guard that no module outside `data_paths` spells that path again.
- The unified Job record and its writer under `jobs/<16hex>/job.json`, which
  moves `_persist_job` off `task_jobs/` and DELETES `pingpong_job._jobs_dir`.
  Finding R-0814 is resolved there, against the fix clause it already carries.
- The ONE resolver, in the same round group as that writer, because 40 of the
  42 job-taking call sites take a `UUID` today (DECISION F260 D4).
- Then `runs/<run_id>/`, T003 consumer by consumer, T004 the classic runner,
  T005 the reachability test and the cluster deletion, in that order.

## Risks

- D1 changes what `<data_root>/runs/` is keyed by, from job id to run id. Every
  reader of the old shape must move in the same commit as its writer, or a run
  log becomes unreadable between two commits.
- `job_record_path` names a path nothing writes yet. Its docstring says so and
  T002's writer round is what makes it live.
- The T005 cluster deletion is large and reversible in one direction only. It
  runs last, behind a reachability test green BEFORE the first `git rm`.
