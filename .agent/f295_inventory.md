# F295 claim inventory — what the machine-client path answers at `9a8431ea9`

Measured by the reviewer of F295's first session on 2026-10-06, on `main` at `9a8431ea9`, with
the script `.agent/authored/f295-r1-measure.py`: a scratch git repository holding `README.md`,
`hello.py` and `order.md` (one line, "Add a docstring to hello in hello.py."), and a scratch data
root set through `REMEDY_DATA_DIR`. Every command ran as `python3 -m apps.cli.main ...` from the
scratch repository. DECISION F295 D1 turns these readings into the slice order.

## `remedy do <path>.md`
- `do order.md --plan-only --no-llm --json --no-ui --yes` — exit 0. The order planned is the text
  `order.md`: the one task reads "Deliver order.md" with the deliverable `order.md`, and the
  contract's one criterion reads "The mission goal is met in full: order.md". The file's content
  is never read.
- `do missing.md` with the same flags, where no such file exists — exit 0, the same shape for the
  text `missing.md`. Nothing refuses a path that does not exist.
- Gap: T001 in full.

## `remedy status --json`
- Keys: `ok`, `schema_version`, `project`, `scope`, `jobs`, `decisions_open`, `runtime` and
  `stops_pending`; `runtime_warning`, `degraded` and `skipped_files` appear only when they apply.
- `jobs` groups the jobs by state; each entry carries `job_id`, `short_id`, `name` and `state`.
- There is no mission, no cost, no list of the open decisions (only the count `decisions_open`),
  no mark on a job that waits for apply, and no word on whether a supervisor answers. A job whose
  `do` walk ran and stopped before apply is listed only as `completed`.
- Gap: T002 in full.

## The `decision` group
- `decision list <job> --json` — exit 0, keys `ok`, `schema_version`, `version`, `job_id` and
  `decisions`. Each decision is exported by `export_decision_json` in
  `packages/orchestration/decision_queue.py` with `id`, `type`, `status`, `severity`, `source`,
  `related_node_id`, `related_intent_id`, `related_file`, `safe_summary`, `next_actions`,
  `created_at`, `resolved_at`, `payload`, `evidence_refs`, `outcomes` and `evidence_status`. No
  field is named for a question or for a documented default.
- `decision resolve` takes `--reason`, `--answer`, `--as-mission` and `--json`. Hunk decisions are
  recorded by a separate command, `patch approve-hunks`.
- `DECISION_TYPES` in the same module names `patch_approval`, `stop_reason`, `test_failure`,
  `token_budget`, `worker_approval`, `memory_review`, `revert_missing`, `task_plan_approval`,
  `task_decision`, `proposal` and `replan_proposal`.
- Gap: T003 measures which of these a run can raise and makes each answerable with `--json`.

## `--yes` on a pipe
- `do "Add a docstring to hello in hello.py." --json --no-ui --yes --no-llm --builder-provider
  fake --reviewer-provider fake --max-cost-usd 1`, its stdin an open pipe nobody wrote to — exit
  0; the steps read init done, study skipped, plan done, shape done, run done, ui skipped and apply
  stopped, and `stopped_before_apply` is true. The run did not block, so this path read no line
  from stdin.
- `cost.cost_usd` read `null`, because the fake providers report no price; the roles read two
  builder calls and two reviewer calls.
- `apps/cli/cost_preview_confirm.py` refuses a stdin that is not a terminal unless `--yes` is
  given (exit 2, `confirmation_required`). It is called by `remedy job rerun` and by
  `_cmd_job_run_cycles` in `apps/cli/commands/job.py`; `remedy do` does not call it.
- Gap: no test pins that this path never reads stdin (T003).
