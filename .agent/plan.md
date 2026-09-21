# Plan — F283 Machine contracts, part two: the refusal sweep, the JSON gap and the exit-code taxonomy

Branch: feature/f283-machine-contracts-part-two, cut from `main` at
`d0d40e89`, the merge commit of pull request 263 (F277's closure).

## Goal

Every CLI refusal answers a machine in the envelope, the
read-only-without-`supports_json` set becomes empty, and every exit code in use
is documented and asserted from the catalog
(`docs/roadmap/features/T2_F283.md`).

## Current Step

ROUND 4, R-1020's SECOND AND LAST REPAIR. It books round 3's PASS, corrects
the call-site count on the record — `decision.py` binds the exiting resolver
a second time as `_rji`, so twenty sites remained and not seventeen — and
registers R-1021.

It then moves all twenty onto `apps/cli/job_id_arg.py`, one module per commit,
largest first, under a guard that reads every import binding rather than one
name. `decision.list` and `decision.show` get the flag threaded into
`decision.py`'s `_load_job_events`; `job stop` answers in the envelope; the
ambiguous branch of the layer gets its first test. When the round ends no
module under `apps/cli/` calls the exiting resolver, and R-1020's `Done:` is
booked in the first commit of the round after the one that verifies it.

## Next Steps

1. R-1021: the nineteen `lookup_job_id` call sites that report an ambiguous
   prefix as matching nothing move onto `resolve_job_id_or_fail` — `brain` 11,
   `snapshot_cmds` 2, `test_cmds` 2, then `event`, `file`, `memory`, `project`.
2. `_cmd_run_next_task_local`, the last eight print-then-exit pairs in
   `job.py`; ten tests monkeypatch it with a single-positional lambda and move
   in the same commit.
3. The four non-mechanical `job.py` sites: a loop of verification failures, a
   bare exit after a cost confirmation, two hand-rolled JSON objects.
4. The remaining groups largest first — `decision`, `brain`, `project`,
   `patch`, `do_cmd`, `grouped`, `test_cmds`, then the tail; `runtime_cmd.py`
   is its own round.
5. T001's catalog half, then T002's taxonomy and sweep.

## Risks

Twenty-five findings are open; R-1020 and R-1021 are this feature's own. The
refusal pairs outside `job.py` are several sessions of work, so the soft limit
of 7 sessions and 25 rounds is the number to watch.
