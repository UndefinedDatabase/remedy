# Plan — F260 One world: mission → job → run

Branch: feature/f260-one-world, cut from `main` at b5cd6c20, the merge commit of
pull request 240 (F259). Rounds 1 to 12 are reviewed and 2 to 12 PASSED. T001 is
CLOSED. T002 is open: the job record has MOVED, R-0814 is resolved, both
resolvers return `str`, and the ping-pong run store has one spelling on both the
production and the test side.

## Goal

One job model on disk. The classic store `<data_root>/jobs/<uuid>.json` and the
ping-pong store, now `<data_root>/jobs/<16hex>/job.json`, become one record with
one id shape minted by one function per kind; a Run becomes the evidence case a
Job points at; `resolve_any_job_id`, the "TWO job stores" paragraph and every
which-store branch are deleted. Task slicing per T2_F260.md: T001 inventory and
id shape, T002 records and writers, T003 consumers, T004 the classic runner,
T005 the reachability test and the cluster deletion.

## Current Step

ONE SPELLING FOR THE RUN-LOG STORE. `<data_root>/runs/<job_id>/` is spelled by
hand at nine sites in seven modules. A new `data_paths.run_log_dir` names the
live job-keyed directory, five base-only sites move onto the existing
`runs_dir`, and the four job-keyed sites move onto the new accessor. This is the
run-log twin of what rounds 11 and 12 did for the ping-pong run store, and it is
what turns DECISION F260 D1's re-key into a change to one function body.

## Next Steps

- The TEST side of the run-log spelling: the hand-built `tmp_path / "runs" /
  <job id>` paths across the suite, which this round deliberately leaves standing
  because they are what makes its own red-proof able to fail.
- THE RE-KEY ITSELF: `run_log_dir` and `pingpong_run_dir` collapse onto
  `run_dir`, keyed by RUN id, and `<data_root>/runs/` stops being keyed by job
  id — DECISION F260 D0 measured that collision and D1 rules the target.
- The unified record's own fields, and the Mission extension (order, contract,
  mission plan, job refs), which is the rest of T002.
- Then T003 consumer by consumer; T004 the classic runner, the classic store and
  the resolver collapse together (DECISION F260 D5); T005 the reachability test
  and the cluster deletion.

## Risks

- `<data_root>/runs/` is keyed by JOB id today and D1 keys it by RUN id. Every
  reader of the old shape moves in the same commit as its writer.
- `RunLogWriter.__init__` still joins the job id onto a runs BASE it is handed,
  so the layout has one more writer-side spelling than `data_paths` shows.
- The T005 cluster deletion is large and reversible in one direction only. It
  runs last, behind a reachability test green BEFORE the first `git rm`.
