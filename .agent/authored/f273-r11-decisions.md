
## DECISION F273 D11 (2026-09-19, reviewer, round 11) — a job's snapshot keeps tracked ignored files, `job run` refuses an unresumable workspace, the self-use runner passes the role config's models, a passed or applied task is done, and a job's budgets reach its run contract
CONTEXT: R-0974, R-0913, R-0890, R-0898 and R-0935 each needed a choice between routes their texts
allow, taken in the round that lands the patch (amend0917-throughput rule 3). Measured by research
helpers and re-measured by the reviewer's dry run at `e707b52e`: `write_tree` in
`packages/orchestration/worktrees.py` adds into an empty temporary index, and its twin
`write_tree_for_path` has no caller; `resume_job_plan`'s two refusals have no production caller;
the self-use runner passes provider names only; `job show --full`'s summary, status and report
sections count only `completed` while the job runner writes `passed` and `applied`; and
`build_default_run_contract` and `_reconcile_budget_fields` read the persisted budgets dict as
attributes, so a job's F018 limits never reach its contract.
CHOSEN: (1) R-0974. The snapshot's temporary index is seeded with `git read-tree HEAD` before
`git add -A`, and the dead `write_tree_for_path` is deleted. (2) R-0913, the Acceptance line's
first branch. The two refusals are one function, `job_resume_refusal`, which `resume_job_plan`
raises and `remedy job run` prints before `run_job` runs, leaving the record untouched; other
callers of `run_job` create fresh jobs and are not changed. (3) R-0890, the runner half only. A role
whose provider the runner takes from the role config also takes that config's model and effort
unless the caller passed them; `run_job`'s own defaults are unchanged. (4) R-0898. One predicate,
`task_is_done`, over `TASK_DONE_STATUSES` — `passed`, `applied` and `completed` — owned by
`pingpong_job.py`, is used by the three views and by `run_job_fulfill`; skipped and split tasks
did no work and are not done. The resume preview keeps its own rule, because the runner steps past
skipped tasks too. (5) R-0935. `job_budget_limits` validates the persisted dict into `JobBudgets`,
and both contract readers use it. The finding's question is answered by measurement: once the
contract reads the budgets, a `job budget set` of `max_tokens` or `max_runtime_seconds` would be
put back silently by the next `ensure_contract`, so that command now refuses those two fields when
the job carries the overlapping F018 limit, naming the `job run` flag that sets it. Without the
limit the write holds.
ALTERNATIVES: routing R-0913 through `_acquire_job_workspace`, rejected because it would mark the
job blocked instead of leaving the record untouched; `run_job` defaulting to the role config's
model, rejected because it would pair a role's model with a provider given by flag; letting the
reconcile overwrite a set value and documenting it, rejected as a command that silently does not
hold.
REVERSE: restore `worktrees.py`, `pingpong_job.py`, `apps/cli/commands/do_cmd.py`,
`self_use_runner.py`, `apps/cli/commands/job.py`, `job_fulfillment.py` and `run_contract.py` from
`e707b52e`, drop the tests this round added, and delete this paragraph.
