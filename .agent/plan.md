# Plan — F272 One world completion

Branch: feature/f272-one-world-completion, cut from `main` at
`b18fad576252f7f2739a5807b6408031da8fcde6`. Round 1 is reviewed and PASSED.

## Goal

Finish what F260 began: a Job that carries MANY runs, every consumer on the
unified model, and the classic runner, its resolver and the prototype cluster
deleted. Task slicing per `docs/roadmap/features/T2_F272.md` — T001 the plural
run list and the run re-key, T002 the rest of the unified record, T003 the
eleven consumers, T004 the classic runner, T005 the reachability test and the
cluster deletion, which is never split.

## Current Step

BLOCKED at `1d24b4a7`. Round 2 landed the re-key — the run log at
`<data_root>/job_logs/<job_id>`, the ping-pong run store at
`<data_root>/runs/<run_id>` — and swept the three test files its block named.
DECISION F272 D1's premise that those three are the only code observing the
change is FALSE BY MEASUREMENT: 22 test files hand-spell `<root>/runs/<job_id>`
and 205 tests are red, the canary `tests/cli/test_golden_path.py` among them
(42 passed at C3, 41 at C4). No production caller moved — all 74 readers and
35 writers resolve through `run_log_dir`, exactly as D1 says.

## Next Steps

1. Rule the widened sweep, then execute it: the 22 files and their failure
   counts are listed in `.agent/handoff.md`. It is mechanical — `"runs"`
   becomes `"job_logs"` wherever the join is keyed by JOB id — but it is far
   outside round 2's change set, so no worker may take it on its own authority.
2. The name collapse D1 places next: `pingpong_runs_dir` and `pingpong_run_dir`
   are DELETED in favour of `runs_dir` and `run_dir` at every call site.
3. The rest of the unified record (T002), then the eleven consumers (T003).

## Risks

- The branch tip is RED. Reverting C4 is the alternative to widening the
  sweep; both are re-rulings, and this round declined to choose either on its
  own authority.
- Old `.data` content becomes unreadable at this move. That is DECISION D-A
  working as ruled — no migration, no compatibility reader — not a regression.
