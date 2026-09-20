
## DECISION F276 D7 (2026-09-20, reviewer, round 6) — the disk floor is a budget like every other, its probe is injected, it has no default, and the post-mortem says `disk_exhausted` while the stop keeps one vocabulary
CONTEXT: T004 of `docs/roadmap/features/T2_F276.md` orders `min_free_disk_bytes` on `JobBudgets`
with a config override, a `free_disk` limit in `budget_guard.evaluate_budget` behind an injectable
probe, a check at job start and at every safe point, the STOPPED path with post-mortem reason
`disk_exhausted`, and a `doctor` disk section. A research helper prototyped it and then rebased it
onto `caa9d073`; the reviewer re-applied, re-ran and re-proved it. Measuring first contradicted
three of that sentence's clauses, and each contradiction is settled below rather than worked
around.
CHOSEN: (1) THE CHECK IS ALREADY ONE CALL, NOT TWO. `run_job` defines `_stop_check` once and calls
it at four places — before the episode loop, at task dispatch, inside the ping-pong loop it is
handed to, and after the loop — and each reaches `safe_points.should_stop` and then
`evaluate_budget`. Putting the limit inside `evaluate_budget` therefore reaches job start and every
safe point at once, and no call site is added. A job refused at the pre-work check is persisted
STOPPED before `first_running_at` is stamped and before a workspace is acquired, which the tests
pin by reading both as empty. (2) `remedy job stop` NEVER STOPS A JOB — it writes one control file
and returns, as its own module docstring says — so "the STOPPED path it uses" is the runner's
`_stop_job`, which a budget stop already takes with `source="budget"`. The disk limit takes that
same path with `stop_reason` `budget_exhausted:min_free_disk_bytes`, one vocabulary for every
limit, while the POST-MORTEM's `terminal_status` and `FailureClass` read `disk_exhausted`, which is
where the acceptance line's word belongs and where an operator reads it. A second stop vocabulary
was the alternative and is rejected. (3) THE DEFAULT IS ABSENT. `resolve_job_budgets` returns None
when every field is None, and a non-None default would hand `run_contract.job_budget_limits` a
budget where there was none for EVERY job and start writing a `budget-ticks.jsonl` for every job
that writes none today. Measured for scale: one staging copy of this repository under T003's own
filters is 24161614 bytes, while the feature file's sampled copy on the operator's machine is 1
190.8 MB — two orders of magnitude apart for the same product, so Remedy does not guess what one
job needs. `remedy doctor core` prints "floor: not configured" and names the key. (4) The probe is
injected three ways: a module-level `FREE_DISK_PROBE` for the process, a `free_disk_probe`
parameter on `evaluate_budget` and `should_stop` for a call, and one reader,
`free_disk_bytes(probe=None)`, that both the guard and the doctor section use. The default probe
calls `shutil.disk_usage` on the nearest existing ancestor of the data root, because
`resolve_data_root` does not guarantee the path exists. No test touches the real filesystem and no
test is skipped for lack of disk. (5) The comparison is a FLOOR — `free < limit` — where every
other budget is a ceiling at `>=`, so a floor of N accepts exactly N; and the limit is FIRST in
`_LIMIT_ORDER`, so a job breaching both disk and tokens is reported as disk, because a token
ceiling can be raised and a full disk cannot. (6) `evaluate_budget` stays pure for every job
without a floor: the probe is called only inside `if budgets.min_free_disk_bytes is not None`, the
docstring's purity clause is narrowed rather than withdrawn, and a probe that raises becomes a
warning and never a stop. (7) Config-only, no CLI flag: the floor is a property of the machine, not
of an invocation, on the precedent `resolve_predictive_budget_config` already sets. (8)
`run_manifest._BUDGET_ALLOWED_KEYS` is DERIVED from `JobBudgets.model_fields` instead of being a
second hand-written spelling of them. The hand-written list has now failed twice — R-0225 for
`max_cost_usd`, and this slice's own first run, where a field the model accepted and the manifest
rejected left the job non-terminal with `run_manifest_write_failed`. The schema stays closed: a key
`JobBudgets` does not declare is still rejected. (9) `doctor core` reports free bytes, the
configured floor and whether it is met, and a configured floor that is not met makes `ready` false,
because a floor that does not block is not a floor; an unconfigured floor is met. (10) The T004
amendment is appended to the feature file, never rewritten, and its numerals name the commit they
were measured at.
ALTERNATIVES: adding call sites at job start and at each safe point as the feature file's wording
suggests, rejected under (1) because they exist; `disk_exhausted` as the stop reason, rejected
under (2); a non-zero default floor, rejected under (3); a CLI flag, rejected under (7); leaving
the manifest's key list hand-written, rejected under (8) after two failures.
REVERSE: restore `packages/core/models.py`, `packages/orchestration/config.py`,
`packages/orchestration/budget_resolution.py`, `packages/orchestration/budget_guard.py`,
`packages/orchestration/safe_points.py`, `packages/orchestration/failure_postmortem.py`,
`packages/orchestration/pingpong_job.py`, `packages/orchestration/run_manifest.py`,
`apps/cli/commands/worker_facade_cmd.py`, `docs/system/architecture.md`,
`docs/system/job-budget-enforcement-v0.md` and `docs/roadmap/features/T2_F276.md` from
`caa9d073`, delete `tests/orchestration/test_disk_floor.py` and the three lines this slice adds to
`tests/orchestration/test_failure_postmortem.py`, and delete this paragraph.
