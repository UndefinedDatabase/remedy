
## DECISION F276 D3 (2026-09-20, reviewer, round 2) — reclaim addresses `job_workspaces` alone; `workspaces`, `runs` and `job_logs` are durable because live readers depend on them, and a class is a reclaim policy
CONTEXT: T002 of `docs/roadmap/features/T2_F276.md` orders a preview-first `remedy data reclaim`
whose `--apply` "deletes only the exact paths the preview named" and "refuses any workspace whose
job is not terminal". A research helper prototyped it in its own worktree against the branch tip
`96fd8f9c`; the reviewer re-applied that work, ran it and red-proved it. Building it exposed a
question the feature file does not answer: T001 calls `workspaces`, `runs` and `job_logs`
ephemeral, and all three hold data that outlives the job whose id names them. The helper measured
the readers; the reviewer confirmed each by reading the source at `96fd8f9c`, and measured the
yield with the command T001 built.
CHOSEN: (1) `workspaces`, `runs` and `job_logs` move to `DURABLE_CLASSES`, each carrying the reader
that keeps it: `workspaces/<job>` holds the `repository_snapshots/` and `apply_records/` that
`repository_snapshot._snapshot_dir` and `_apply_record_dir` write and `snapshot_cmds.py:118` reads,
which the catalog's own `snapshot.list-applies` description calls "durable apply records for a
job"; `runs/<run_id>` holds the `result.json`, `prompt_trace.jsonl` and `prompt_trace_summary.json`
that `job_evidence.py` reads for jobs that are ALREADY terminal, and the `result.json` and
`result.diff` `worktree_resume.py` reads; `job_logs/<job>` is the event trail the timeline, the
trust report, the cockpit and `pingpong_job` read. Two ephemeral classes remain, `job_workspaces`
and `review_staging.*`, and exactly one has reclaim candidates. (2) A CLASS IS A RECLAIM POLICY,
not a claim about how long a directory lives. Reclaim's safety comes from addressing whole DIRECT
CHILDREN of a class directory; a subtree rule that reached inside a mixed directory to separate
scratch from evidence would give that up, so a mixed directory stays durable until a later slice
can split it, and age-based retention of the three kept classes is F166's. (3) The narrowing costs
almost nothing, measured by `data usage --json` on the operator's root at `96fd8f9c`: of
923560682122 bytes, `job_workspaces` holds 922931683643 — 99.93 per cent — against `runs`
144775616, `workspaces` 39580459 and `job_logs` 17575775. (4) Terminal means `completed`, `failed`
or `cancelled`, declared as `pingpong_job.JOB_TERMINAL_STATES` beside the `JOB_*` constants and
read through `job_is_terminal`; `blocked`, `stopped`, `paused`, `planned`, `running` and `pending`
keep their scratch, because `JOB_STOPPED`'s own docstring says a stopped job "keeps its pending
work and resumes at the first pending task" and `job resume` is a live command. `status_cmd`'s
private `_TERMINAL` set is routed through the same function so the vocabulary has one spelling.
(5) `review_staging.*` stays ephemeral and is REFUSED by reclaim, because no job owns it and no age
rule exists; its registry entry says so rather than promising a reclaim nothing performs. (6) A
refusal the operator asked for exits 0; `delete_failed` — a deletion attempted and failed — exits
1, pinned in both directions by tests, the failing case made real with an unwritable parent rather
than a patched call. (7) The round is five code commits, none over 500 insertions. The alternative
was one 507-line commit declared oversize; a declared oversize has to mean the change cannot be
split, the helper's slice probe proved it can, so the allowance is not spent. The split's whole
cost is two docstring rewordings in `data_reclaim.py` so that the module never names a command the
catalog does not yet carry — `tests/cli/test_advertised_commands.py` forbids the module's prose
landing before the catalog entry and `tests/orchestration/test_dead_command_check.py` forbids the
catalog entry landing before a naming test, and those two guards together are what bracket the
order.
ALTERNATIVES: keeping the three classes ephemeral and refusing them inside reclaim, rejected
because `data usage` would then report 923 GB of "ephemeral" bytes an operator cannot reclaim, and
the report is the thing that must be honest; a subtree rule deleting a workspace's checkout while
keeping its snapshots and apply records, rejected under (2) and for 0.004 per cent of the bytes;
deleting a stopped job's scratch, rejected because `job resume` reads it; declaring the oversize
commit, rejected under (7).
REVERSE: restore `packages/orchestration/data_paths.py`, `packages/orchestration/data_footprint.py`,
`packages/orchestration/pingpong_job.py`, `apps/cli/commands/status_cmd.py`,
`apps/cli/commands/data_cmd.py`, `apps/cli/command_catalog.py`, `docs/system/architecture.md` and
`tests/cli/test_data_cmd.py` from `96fd8f9c`, delete `packages/orchestration/data_reclaim.py`,
`tests/orchestration/test_data_reclaim.py` and their allowlist line, delete the AMENDMENT paragraph
this decision appended to `docs/roadmap/features/T2_F276.md`, and delete this paragraph.
