# Plan — F283 Machine contracts, part two: the refusal sweep, the JSON gap and the exit-code taxonomy

Branch: feature/f283-machine-contracts-part-two, cut from `main` at
`d0d40e89`, the merge commit of pull request 263 (F277's closure).

## Goal

Every CLI refusal answers a machine in the envelope, the
read-only-without-`supports_json` set becomes empty, and every exit code in use
is documented and asserted from the catalog
(`docs/roadmap/features/T2_F283.md`).

## Current Step

ROUND 3, R-1020's FIRST REPAIR. It books round 2's PASS, appends a CORRECTION
to R-1020 — the registration overstated the blast radius, counting
`require_job_plan` as an exiting helper when it raises — and lands the layer
the finding needs: `apps/cli/job_id_arg.py::resolve_job_id_or_fail`, which
catches what `lookup_job_id` raises and refuses through `fail()`.

THE ENVELOPE DOES NOT MOVE INTO `packages/`. `resolve_job_id` stays as it is
for callers with no failure path of their own and the `--json` callers move up;
pushing `fail()` down would make storage depend on a command's stdout shape.

`job.py`'s six call sites move this round and the strict xfail turns green with
its mark deleted in the same commit. Seventeen call sites remain in eight other
modules, so R-1020 stays OPEN and a second guard counts them.

## Next Steps

1. R-1020's remaining seventeen call sites: `patch` 7, `change` 3,
   `teacher_cmd` 2, then `contract_cmd`, `decision`, `job_context_cmd`,
   `job_stop_cmd` and `project` at one each.
2. `_cmd_run_next_task_local`, the last eight print-then-exit pairs in
   `job.py`; ten tests monkeypatch it with a single-positional lambda and move
   in the same commit.
3. The four non-mechanical `job.py` sites: a loop of verification failures, a
   bare exit after a cost confirmation, two hand-rolled JSON objects.
4. The remaining groups largest first — `decision` 28, `brain` 24, `project`
   22, `patch` 15, `do_cmd` 13, `grouped` 8, `test_cmds` 5, then the tail;
   `runtime_cmd.py` is its own round.
5. T001's catalog half, then T002's taxonomy and sweep.

## Risks

Twenty-four findings are open; R-1020 is this feature's own and is repaired for
one module of nine. The measured work left — 156 refusal pairs outside `job.py`
plus 17 resolver call sites — is several sessions, so the soft limit of 7
sessions and 25 rounds is the number to watch.
