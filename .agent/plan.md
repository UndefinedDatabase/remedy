# Plan — F283 Machine contracts, part two: the refusal sweep, the JSON gap and the exit-code taxonomy

Branch: feature/f283-machine-contracts-part-two, cut from `main` at
`d0d40e89`, the merge commit of pull request 263 (F277's closure).

## Goal

Every CLI refusal answers a machine in the envelope, the
read-only-without-`supports_json` set becomes empty, and every exit code in use
is documented and asserted from the catalog
(`docs/roadmap/features/T2_F283.md`).

## Current Step

ROUND 5, R-1021. It books round 4's PASS, R-1020's `Done:` and R-1022's
registration, then moves the nineteen hand-caught `lookup_job_id` sites onto
`apps/cli/job_id_arg.py::resolve_job_id_or_fail`, one module per commit, so a
prefix two jobs share is refused as ambiguous at exit 2 everywhere instead of
as "no job matches" at exit 1. `resolve_job_id_or_fail` gains a payload
pass-through so `snapshot` and `test` keep the `job_id` key their JSON already
carried. A guard pins `lookup_job_id` to the two callers that handle the
ambiguous case themselves, and R-1022's two sentences are corrected.

## Next Steps

1. `_cmd_run_next_task_local`, the last eight print-then-exit pairs in
   `job.py`; ten tests monkeypatch it with a single-positional lambda and move
   in the same commit.
2. The four non-mechanical `job.py` sites: a loop of verification failures, a
   bare exit after a cost confirmation, two hand-rolled JSON objects.
3. The remaining groups largest first — `decision`, `brain`, `project`,
   `patch`, `do_cmd`, `grouped`, `test_cmds`, then the tail; `runtime_cmd.py`
   is its own round.
4. T001's catalog half, then T002's taxonomy and sweep.

## Risks

Twenty-five findings are open; R-1021 and R-1022 are this feature's own. The
refusal pairs outside `job.py` are several sessions of work, so the soft limit
of 7 sessions and 25 rounds is the number to watch.
