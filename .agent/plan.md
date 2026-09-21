# Plan — F283 Machine contracts, part two: the refusal sweep, the JSON gap and the exit-code taxonomy

Branch: feature/f283-machine-contracts-part-two, cut from `main` at
`d0d40e89`, the merge commit of pull request 263 (F277's closure).

## Goal

Every CLI refusal answers a machine in the envelope, the
read-only-without-`supports_json` set becomes empty, and every exit code in use
is documented and asserted from the catalog
(`docs/roadmap/features/T2_F283.md`).

## Current Step

ROUND 2, T001 SLICE B PART ONE. It books round 1's PASS, registers R-1020, and
migrates the eleven refusal sites of `apps/cli/commands/job.py` outside
`job run`. `_cmd_show_job` and `_refuse_budget_set` serve commands declaring
`supports_json: True`, so the flag is THREADED into both; `_cmd_create_job` has
no catalog entry and no dispatch lambda and `job.plan` declares
`supports_json: False`, so those ten sites migrate with `json_output=False`.

R-1020 IS WHAT THIS ROUND LEARNED. Threading is not enough: for 52 of the
catalog's 111 `supports_json` commands the refusal that fires is in a shared
EXITING helper under `packages/` — `resolve_job_id`, `_exit_ambiguous` or
`require_job_plan` — which prints prose and exits before the handler's own
failure path. `job show --json` on a bad id still writes prose with the flag
threaded. A `strict` xfail pins it, so the repair has a red-to-green target.

## Next Steps

1. ROUND 3 — R-1020's repair, which the reviewer rules comes BEFORE any further
   group migration: the three helpers gain a non-exiting form or take the
   caller's `json_output`, the ambiguous-prefix message gets its shape
   decision, and the xfail flips green with its mark deleted in that commit.
2. `_cmd_run_next_task_local`, the last eight sites in `job.py`; ten tests
   monkeypatch it with a single-positional lambda and move in the same commit.
3. The four non-mechanical `job.py` sites: a loop of verification failures, a
   bare exit after a cost confirmation, two hand-rolled JSON objects.
4. The remaining groups largest first — `decision` 28, `brain` 24, `project`
   22, `patch` 15, `do_cmd` 13, `grouped` 8, `test_cmds` 5, then the tail;
   `runtime_cmd.py` is its own round.
5. T001's catalog half, then T002's taxonomy and sweep.

## Risks

Twenty-four findings are open after this round registers R-1020, and R-1020 is
the one that changes the plan: it puts the Acceptance criterion out of reach of
a pure `apps/cli` sweep, and it is this feature's own. The 167 refusal pairs
across the un-migrated modules were already more than one session's work.
