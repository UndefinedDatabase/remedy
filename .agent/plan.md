# Plan — F272 One world completion

Branch: feature/f272-one-world-completion. Round 1 PASSED. ROUND 2 FAILED its
gate: its production change is correct, but the reviewer's DECISION F272 D1
claimed only three test files observed it, and 24 do, so the tip went red at 207
tests. Round 3 is the repair.

## Goal

Finish what F260 began: a Job that carries MANY runs, every consumer on the
unified model, and the classic runner, its resolver and the prototype cluster
deleted. Task slicing per `docs/roadmap/features/T2_F272.md` — T001 the plural
run list and the run re-key, T002 the rest of the unified record, T003 the
eleven consumers, T004 the classic runner, T005 the reachability test and the
cluster deletion, which is never split.

## Current Step

Round 3 returns the tip to green WITHOUT reverting round 2. It registers finding
R-0818 before touching anything, sweeps the job-keyed run-log path out of the 24
files that hand-spell it, and appends DECISION F272 D2 correcting D1's
premise — the sentence that called three files the only observers — while
leaving D1's ruling, which the gates proved right about production code, intact.

## Next Steps

1. The name collapse DECISION F272 D1 places next: `pingpong_runs_dir` and
   `pingpong_run_dir` are DELETED in favour of `runs_dir` and `run_dir` at every
   call site, with no alias and no attic, per AGENTS.md "Replacing is deleting".
2. The rest of the unified record: the eleven administrative fields and the
   Mission extension (T002).
3. The eleven consumers named under Design in `T2_F260.md`, one per commit where
   the diff allows (T003).

## Risks

- The sweep is not a blind substitution: `"runs"` is still the correct spelling
  of the RUN store, which round 2 moved INTO `<data_root>/runs/<run_id>`. Only a
  path keyed by a JOB id changes, and the gate counts the job-keyed spellings to
  zero rather than counting the word.
- A test that reaches the path through a shared helper is fixed by the helper and
  must not be edited; two such files are deliberately outside the change set and
  must go green untouched.
