
## DECISION F273 D2 (2026-09-19, reviewer, round 2) — one ledger row per provider call; the unified job path writes task and round events the teacher narrates; round 1's five reds repaired
CONTEXT: T2_F273.md T001 builds R-0807 and R-0812 as their finding text specifies. Measured by
research helpers and re-measured by the reviewer at `f32363e9`: `call_id_for_task_run` in
`packages/orchestration/token_ledger.py` keys one row per finalized task run (DECISION F103 D16), so
a task of two rounds and four provider calls leaves one builder row and no reviewer row, while each
`provider_attempts` entry of `provider_evidence.json` names its role and carries no usage of its
own. D16's own last sentence orders the switch "when a per-request evidence record exists". For
R-0812, `NARRATED_EVENTS` in `packages/orchestration/teacher_narration.py` holds the Stage 1 kinds;
`run_job` in `packages/orchestration/pingpong_job.py`, which both `remedy do` and `remedy job run`
reach, writes no task or round event, so a job with a budget narrates only `budget.tick` as
unrecognised and a job without one narrates nothing. `task_run_started`, `task_run_completed`,
`task_run_failed` and `task_run_noop` are still read by the timeline, trust report, brain and
cockpit and written only by the classic single pass in `apps/cli/commands/job.py`.
CHOSEN: (1) R-0807. Each `provider_attempts` entry gains `seq` (its 1-based position), `round`, and
the `usage` and `total_cost_usd` THAT call reported, copied verbatim and null where it reported
none, never a share of the task run's aggregate. A row is one attempt, keyed
`"<job_id>:<task_id>:<seq>"` by `call_id_for_provider_call`, through the live hook,
`backfill_ledger` and `verify_ledger` alike; an attempt is one real invocation, so a transport
retry is its own row. Evidence written before this carries no `seq` and keeps its one D16 row.
THE SUPERSEDE RULE: when a task run's per-call rows land, its old `"<job_id>:<task_id>"` row and
that row's segments are deleted in the same transaction, because both describe the same spend; no
schema migration, since a migration cannot know which old rows have per-call evidence on disk.
Segment rows attach to per-call rows only when the trace's roles match the calls' roles in order,
otherwise none is written. The D16 section of `docs/roadmap/features/T2_F103.md` gains a dated
note that its switch was made. R-0807's resolution also needs "a real run's row count equals its
call count", which no test may produce: it is read from the closure sequence's self-use run. (2)
R-0812. `run_job` writes, through one `RunLogWriter` per call opened at the first task,
`task_run_started` before a task's ping-pong, one `task_round_completed` per round with the
reviewer's verdict (a new kind; nothing existing fit), `task_run_completed` with outcome `pass`
after apply and commit, and `task_run_failed` naming the block on each of the six blocking exits,
all fail-soft like `_emit_budget_tick`. A stopped task writes no task terminal: `job_stopped`
closes the log, and readers then show the task as interrupted, which it is. The table gains
`task_round_completed`, `budget.tick`, `job_stopped` and `command.accepted`, and
`narrate_run_event` reads a field absent at top level from `metadata`, a top-level value winning.
`apps/ui/src/api/humanizeCatalog.ts` gains the new kind, as
`tests/ui_contracts/test_humanize_catalog.py` requires. (3) ROUND 1's REDS. The four
`tests/orchestration/test_config.py` tests that measure resolution with no `REMEDY_DATA_DIR` delete
the variable first; the walk test's docstring no longer names the deleted adapter class.
ALTERNATIVES: splitting a task run's aggregate across its calls, rejected by D16 and the F075
lesson; a numbered migration deleting old rows, rejected because it would drop history that has no
per-call evidence; keying rows by `finalized_calls`, rejected because it merges transport retries
that cost tokens; a `task_run_failed` for a stopped task, rejected because a stop is not a failure;
an event name built from a constant, rejected because the catalog test reads literal call sites.
REVERSE: restore `token_ledger.py`, `pingpong_evidence.py`, `pingpong_loop.py`, `pingpong_job.py`,
`teacher_narration.py`, `stats_ledger_cmd.py` and `humanizeCatalog.ts` from `f32363e9`, drop the
tests this round added or changed for (1) and (2) and the T2_F103.md note, keep (3), and delete
this paragraph.
