# Plan — F283 Machine contracts, part two: the refusal sweep, the JSON gap and the exit-code taxonomy

Branch: feature/f283-machine-contracts-part-two, cut from `main` at
`d0d40e89`, the merge commit of pull request 263 (F277's closure).

## Goal

F277 left three machine-facing contracts declared and one of them half
applied. This feature finishes it: every CLI refusal answers a machine in the
envelope, the read-only-without-`supports_json` set becomes empty, and every
exit code in use is documented and asserted from the catalog
(`docs/roadmap/features/T2_F283.md`).

## Current Step

ROUND 1, THE CLAIM. It books F277 round 19's PASS and resolves R-1018, empties
`.agent/candidates.md`, re-heads the live review record, flips F283 to `[~]`,
and lands T001's first slice.

T001 SLICE A, measured on `apps/cli/commands/job.py` at `d0d40e89` by reading
the tree rather than the prose: 44 `sys.exit` sites, of which 40 are a single
stderr `print()` immediately before the exit. Twenty of those 40 sit in a
handler that ALREADY carries `json_output` — those are slice A and this round
migrates them onto `fail()`, threading nothing and changing no caller. The
other twenty have no flag in scope; the remaining 4 carry a loop or a
hand-rolled JSON branch. Both groups are named below.

## Next Steps

1. SLICE B — thread `json_output` into `_cmd_show_job`, `_cmd_create_job`,
   `_cmd_plan_job_local`, `_cmd_run_next_task_local` and `_refuse_budget_set`,
   then migrate their 20 sites. `job.show` and `job.run` declare
   `supports_json: True` in the catalog and answer failures in prose today,
   which is the gap T001 exists to close.
2. THE FOUR NON-MECHANICAL SITES of `job.py` — lines 1093 (a loop of printed
   verification failures), 1237 (a bare exit after a cost confirmation), 1629
   and 1649 (hand-rolled JSON objects that are not the envelope).
3. The remaining groups in the brief's order: `decision` (28 pairs), `brain`
   (24), `project` (22), `do_cmd` (13), `patch` (15), `grouped` (8),
   `test_cmds` (5), then the tail. `runtime_cmd.py` is its own round.
4. The catalog half of T001, then T002's taxonomy and sweep, which is the
   acceptance evidence for everything above it.

## Risks

Twenty-three findings are open after this round resolves R-1018, every one Low
or Medium. R-1019 is this feature's own and is fixed by slice B, not by slice A.
The 167 refusal pairs measured across the un-migrated modules are more than one
session's work, so the soft limit of 7 sessions and 25 rounds binds from here.
