# F260 T001 — the measured inventory of jobs, runs and run evidence

> Written in F260 round 2 against `feature/f260-one-world` at `4b704705`. This
> branch has moved no file under `packages/`, `apps/` or `tests/`, so every
> reading below is also the reading at the branch base `b5cd6c20`.
>
> THIS FILE RULES NOTHING. It is the evidence DECISION F260 D1 and D2 are ruled
> from in round 3. Every path and symbol named here was resolved on disk and is
> cited as `file:line`; every count was produced by a command, not by reading.

## 1. Every on-disk area storing a job, a run, or a run's evidence

The round-2 block listed four areas and asked me to confirm or correct each.
Four are confirmed with two line-number corrections, and there is a FIFTH area
the list did not name.

| # | Path template | Keyed by | Writer | Readers |
|---|---|---|---|---|
| 1 | `<data_root>/jobs/<uuid>.json` | classic job id (UUID) | `storage.save_job` (packages/orchestration/storage.py:75) | `storage.load_job` (storage.py:83), `load_job_safe` (storage.py:100), `list_jobs` (storage.py:113), `list_jobs_safe` (storage.py:123) |
| 2 | `<data_root>/jobs/<16hex>/evidence/…` | ping-pong job id (16-hex) | `pingpong_job.job_evidence_dir` (pingpong_job.py:3050) and `_task_stream_dir` (pingpong_job.py:3560) | the evidence exporter; `stop_postmortem_dir` (pingpong_job.py:3101) |
| 3 | `<data_root>/task_jobs/<16hex>/job.json` | ping-pong job id (16-hex) | `pingpong_job._persist_job` (pingpong_job.py:381) | `pingpong_job.load_job_plan` (pingpong_job.py:394) |
| 4 | `<data_root>/runs/<job_id>/<32hex>.jsonl` | job id, EITHER shape | `run_log.RunLogWriter` (run_log.py:94) | `timeline.load_run_events` (timeline.py:68), `run_log.read_run_events` (run_log.py:184) |
| 5 | `<data_root>/pingpong_runs/<run_id>/` | RUN id (16-hex) | `pingpong_loop._persist_run` (pingpong_loop.py:4234) | `pingpong_loop.load_run` (pingpong_loop.py:4257), `list_runs` (pingpong_loop.py:4268) |

### Where I disagree with the block's list

- **`run_log.RunLogWriter` is at run_log.py:94, not run_log.py:114.** Line 114 is
  `root = runs_root if runs_root is not None else _runs_dir_default()` — the
  runs-root resolution inside `__init__`, which is the line that reaches
  `data_paths.runs_dir` (data_paths.py:78). The class statement is at 94 and the
  filename is built from `_run_id` at run_log.py:117.
- **`timeline.load_run_events` is at timeline.py:68, not timeline.py:75.** Line
  75 is `runs_dir = data_dir / "runs" / str(job_id)`, the path construction
  inside the function.
- **A FIFTH area exists and the list did not name it: `<data_root>/jobs/<16hex>/evidence/`.**
  `pingpong_job` uses TWO different "jobs directory" spellings. Its module-local
  `_jobs_dir()` (pingpong_job.py:374) returns `task_jobs_dir()`
  (pingpong_job.py:378), while `job_evidence_dir` (pingpong_job.py:3050) calls
  the IMPORTED `jobs_dir` (pingpong_job.py:3053) — the CLASSIC store's directory.
  So one ping-pong job writes its record under `task_jobs/<16hex>/job.json` and
  its evidence under `jobs/<16hex>/evidence/`, which is the classic store's root
  keyed by a non-classic id shape. `stop_postmortem_dir`'s own docstring
  (pingpong_job.py:3102) spells the result out: `jobs/<job_id>/evidence/stop_postmortems/<request_id>/`.
  The local name `_jobs_dir` shadowing the imported `jobs_dir` is what hides it.
  Measured uses: `_jobs_dir()` at pingpong_job.py:382, 395, 971, 1179, 2691 and
  2872; `jobs_dir()` at pingpong_job.py:3053 and 3567.
- **Area 4 is keyed by a job id of EITHER shape**, which I confirm and sharpen
  rather than correct — see item 5, where it decides the collision.

## 2. The two job records, field by field

Extracted with `ast` over the class bodies, not by grep.
`packages.core.models.Job` (packages/core/models.py:222) is a pydantic
`BaseModel` with **15** fields. `pingpong_job.JobPlan` (pingpong_job.py:288) is a
`@dataclass` with **56**. Exactly **four** field NAMES are shared, and no shared
name has the same type on both sides.

| Field | Classic `Job` | `JobPlan` | Same thing? |
|---|---|---|---|
| identity | `id: UUID` (packages/core/models.py:225) | `job_id: str` (pingpong_job.py:290) | YES — same concept, different id shape (item 3) |
| title | `name: str` (packages/core/models.py:226) | `job_title: str` (pingpong_job.py:294) | YES — different spelling of one concept |
| state | `state: RunState` (packages/core/models.py:231) | `status: str` (pingpong_job.py:295) | YES in role; `RunState` is an enum, `status` a bare string |
| tasks | `tasks: list[Task]` (packages/core/models.py:230) | `tasks: list[TaskEntry]` (pingpong_job.py:296) | SAME NAME, DIFFERENT ELEMENT TYPE |
| created | `created_at: datetime` (packages/core/models.py:229) | `created_at: str` (pingpong_job.py:297) | SAME NAME, DIFFERENT TYPE (`datetime` vs ISO string) |
| budgets | `budgets: JobBudgets \| None` (packages/core/models.py:239) | `budgets: dict \| None` (pingpong_job.py:355) | SAME NAME, DIFFERENT TYPE (model vs `model_dump` dict) |
| metadata | `metadata: dict[str, Any]` (packages/core/models.py:234) | `metadata: dict` (pingpong_job.py:367) | SAME NAME, same role |
| budget | `budget: Budget` (packages/core/models.py:233) | — | classic only, and distinct from `budgets` |
| mission | `mission: str \| None` (packages/core/models.py:227) | — | classic only |
| order text | `user_prompt: str \| None` (packages/core/models.py:228) | — | classic only |
| artifacts | `artifacts: list[Artifact]` (packages/core/models.py:232) | — | classic only |
| project | `project_id: str \| None` (packages/core/models.py:235) | — | classic only |
| intake | `intake: dict[str, Any] \| None` (packages/core/models.py:236) | — | classic only |
| flight plan | `flight_plan: dict[str, Any] \| None` (packages/core/models.py:237) | — | classic only |
| fences | `fences: JobFences \| None` (packages/core/models.py:238) | — | classic only |
| repo/workspace | — | `repo_path`, `job_workspace_path`, `isolation_mode`, `worktree_*` (7 fields) | JobPlan only |
| result diff | — | `result_diff_path`, `result_diff_sha256`, `result_diff_size_bytes`, `result_diff_error` | JobPlan only |
| stop episode | — | `stop_request_id`, `stop_reason`, `stop_source`, `stopped_at`, `stop_archive_ref`, `stop_postmortem_path`, `stop_error`, `stop_event_error` | JobPlan only |
| run manifest | — | `run_manifest_path/_error/_created_at/_required_v/_episodes`, `active_episode_id`, `episode_start_workspace_tree`, `input_snapshot`, `input_snapshot_error` | JobPlan only |
| handoff coverage | — | `root_changed_files`, `reviewed_task_files`, `unexpected_root_files`, `missing_root_files`, `handoff_coverage_verdict` | JobPlan only |

Measured set arithmetic: shared names = `budgets`, `created_at`, `metadata`,
`tasks` (4). Classic-only names = `artifacts`, `budget`, `fences`,
`flight_plan`, `id`, `intake`, `mission`, `name`, `project_id`, `state`,
`user_prompt` (11). The remaining 52 names exist only on `JobPlan`.

READING FOR D1, NOT A RULING: the classic record is the ADMINISTRATIVE one
(mission, project, fences, budgets, intake, flight plan) and `JobPlan` is the
EXECUTION one (workspace, worktree, stop episode, run manifest, result diff).
The overlap is four names, and each of the four would need a type decision.

## 3. Every id shape actually minted

| Shape | Length | Minting call site | What it names |
|---|---|---|---|
| `uuid4()` | 36-char canonical UUID | `packages/core/models.py:225` (`default_factory=uuid4`) | a classic Job |
| `uuid4().hex[:16]` | 16 hex | `pingpong_job.py:290` | a ping-pong Job (`JobPlan.job_id`) |
| `uuid4().hex` | 32 hex | `run_log.new_run_id` (run_log.py:41, minted at run_log.py:48) | one run-log session (the `.jsonl` stem) |
| `uuid4().hex[:16]` | 16 hex | `pingpong_loop.py:122` (`PingPongResult.run_id`) | a ping-pong RUN |
| `uuid4().hex` | 32 hex | `mission_state.py:404` | a Mission |
| `uuid4().hex[:16]` | 16 hex | `pingpong_job.py:2268` (`active_episode_id`) | one run episode of a job |
| `uuid4().hex[:16]` | 16 hex | `safe_points.new_request_id` (safe_points.py:153) | one stop request |

So THREE distinct shapes are in use — 36-char UUID, 32-hex and 16-hex — and the
16-hex shape names four different kinds of thing (job, run, episode, request).

### Every parse or validation path constraining an id

| Path | Line | Accepts | Rejects |
|---|---|---|---|
| `data_paths._SHORT_HEX_RE` | data_paths.py:150 | `[0-9a-fA-F]{4,32}` | anything non-hex, and any hex run longer than 32 |
| `resolve_job_id`, the `UUID(raw)` branch | data_paths.py:205 | a canonical UUID, or 32-hex | **a 16-hex ping-pong job id** |
| `resolve_job_id`, the prefix branch | data_paths.py:209 (guard), 213 | a hex prefix unique in the CLASSIC store | anything the classic store does not hold |
| `resolve_any_job_id` | data_paths.py:223; `UUID` at 250, `_SHORT_HEX_RE` at 254 | both stores, returns `str` | — |
| `_classic_job_id_matches` | data_paths.py:153 | `*.json` file stems under `jobs/` | a DIRECTORY under `jobs/`, so area 2 is invisible to it |
| `_task_job_id_matches` | data_paths.py:168 | directories under `task_jobs/` holding a `job.json` | a directory without `job.json` |
| `safe_points.validate_job_id` | safe_points.py:137, pattern `_ID_RE` at safe_points.py:66 | `^[A-Za-z0-9][A-Za-z0-9_-]{0,63}$` — 1-64 chars | path traversal; accepts ALL THREE shapes above |

PROBE (run, not reasoned): `UUID('a1b2c3d4e5f60718')` raises
`ValueError: badly formed hexadecimal UUID string`, while the 32-hex and
canonical forms parse. That single fact is why `resolve_job_id` can never
resolve a ping-pong job id, which is the defect the feature exists to remove.

SECOND PROBE, and it corrects an inference I nearly recorded: `RunLogWriter` is
annotated `job_id: UUID` (run_log.py:107) but performs no runtime check — it
calls `str(job_id)` at run_log.py:112. Constructing
`RunLogWriter('a1b2c3d4e5f60718', runs_root=<tmp>)` in an isolated temporary
directory created `a1b2c3d4e5f60718/e2ee1d4d7ea84a9289b46b48c964980a.jsonl`.
A 16-hex job id therefore DOES get a run-log directory under `runs/`.

The two run-log write paths differ on this point, and only one of them is
UUID-bound:

- `timeline.append_run_event` (timeline.py:49) coerces with
  `UUID(str(job_id))` at timeline.py:63, so it raises `ValueError` on a 16-hex
  job id. Its callers are the classic ones (`autorun.py:741`,
  `builder_bridge.py:546`, `do_run.py:653`, `event_persistence.py:62`,
  `event_replay.py:434`).
- `pingpong_job` bypasses it and constructs the writer directly:
  `RunLogWriter(job.job_id, runs_root=runs_dir())` at pingpong_job.py:3165,
  inside `_append_job_stopped_event` (pingpong_job.py:3149), whose docstring
  names the target as `<data_root>/runs/<job_id>/<run>.jsonl`
  (pingpong_job.py:3152). `_job_stopped_event_exists` reads it back at
  pingpong_job.py:3200.

The other `RunLogWriter` constructions all pass a classic `job.id`:
`agent_loop.py:500`, `autonomy_loop.py:128`, `continue_from_node.py:123` and
`:136`, plus `safe_points.py:675`.

## 4. The consumers named under "Design" in `docs/roadmap/features/T2_F260.md`

Re-grepped at `4b704705`. The feature file's citations were taken 2026-09-05 and
this branch has moved no production file, so a mismatch is a defect of the
feature file.

| Consumer | Feature file says | Measured now | Citation resolves? |
|---|---|---|---|
| `packages/orchestration/orchestrator_loop.py` | imports `storage.load_job` (line 370) | `from packages.orchestration.storage import load_job` at orchestrator_loop.py:370; called at :375; two more importers at :1733 and :1925 | YES |
| `packages/orchestration/mission_state.py` | `Mission.job_links` | `job_links` at mission_state.py:189, serialized at :202, parsed at :227 | YES |
| `packages/orchestration/self_use_runner.py` | runs `pingpong_job.run_job` | `from packages.orchestration.pingpong_job import JOB_BLOCKED, JobPlan, run_job` at self_use_runner.py:53 | YES (no line was cited) |
| `packages/orchestration/self_use_job.py` | runs `plan_job_from_file` | imported at self_use_job.py:47, called at :147 | YES (no line was cited) |
| `packages/orchestration/gauntlet_runner.py` | `storage.load_job_safe(UUID(...))` (line 344) | import at gauntlet_runner.py:344; the call `load_job_safe(UUID(str(link.job_id)))` at :351 | YES — line 344 is the import, the call is 7 lines below |
| `packages/orchestration/bench_run.py` | grouped with gauntlet_runner as running "on the unified job run after this feature" | **NO job access of any kind.** The file is 84 lines; `storage`, `load_job`, `JobPlan`, `run_job` and `job_id` do not occur in it. Its only `data_paths` mentions are docstring lines 31 and 33 about data roots | **NO — see defect 1 below** |
| `apps/cli/commands/teach_cmd.py` | calls `resolve_any_job_id` (lines 56-66, 151) | import at teach_cmd.py:56, call at :66; second import at :151, second call at :166 | YES |
| `packages/orchestration/ui_server.py` | `_load_job` (line 232) tries `storage.load_job` then `pingpong_job.load_job_plan` | `def _load_job` at ui_server.py:232; `load_job_plan` imported at :256 and called at :257 | YES |
| `apps/cli/commands/job_context_cmd.py` | `resolve_job_id` + `storage.load_job` only (lines 219-223) | import at job_context_cmd.py:219; `load_job(resolve_job_id(job_id_str))` at :223 | YES |
| `packages/orchestration/decision_inbox.py` | "loads through `ui_server._load_job`" | the module LOADS NOTHING. `_load_job` occurs only in its docstring at decision_inbox.py:11. `build_decision_inbox` (decision_inbox.py:182) RECEIVES an already-loaded job; `ui_server.py:2773` imports it and `:2775` calls `build_decision_inbox(job, events)` | **PARTLY — see defect 2 below** |
| `packages/orchestration/checkpoints.py` | `pingpong_job.load_job_plan` (lines 242, 258) | imports at checkpoints.py:242 and :258; calls at :244 and :261 | YES |
| `apps/cli/commands/job_stop_cmd.py` | `load_job_plan` with a `_CoreJobAdapter` fallback onto `storage.load_job` | `_CoreJobAdapter` at job_stop_cmd.py:26; `_load_job` at :40 imports `load_job_plan` at :41 and calls it at :43; the fallback imports `load_job` at :50 and calls it at :52 | YES (no lines were cited) |

**DEFECT 1 OF THE FEATURE FILE — `bench_run.py` is not a job-store consumer.**
The Design bullet reads "`gauntlet_runner.py` and `bench_run.py` — F075/F082;
`gauntlet_runner` loads jobs through `storage.load_job_safe(UUID(...))` (line
344); both run on the unified job run after this feature." The clause is true of
`gauntlet_runner.py` and unsupported for `bench_run.py`: that module is a pure
join over `bench_orders`, `gauntlet_runner.run_campaign`, `bench_dry_run` and
`bench_history` (its own docstring, bench_run.py:1-11) and names no job, no id
and no store. It reaches jobs only transitively through `run_campaign`. Reported,
not corrected — the feature file is not edited by this round except by C6.

**DEFECT 2 OF THE FEATURE FILE — the `decision_inbox.py` direction is inverted.**
"loads through `ui_server._load_job`" describes a call `decision_inbox` does not
make. `ui_server` loads the job and passes it in. The consequence for T003 is the
opposite of the one the bullet implies: `decision_inbox` needs no change of its
own once `ui_server._load_job` returns the unified record, provided the attribute
surface it reads is preserved.

## 5. The `runs/` collision, stated as a measurement

The feature file's "Goal & Done" says a Run "is the evidence-case folder that
today is `<data_root>/task_jobs/<16hex>/`" and that "The directory is renamed to
`runs/`" (docs/roadmap/features/T2_F260.md:21-23).

Measured:

- `data_paths.runs_dir` (data_paths.py:78) returns `<data_root>/runs`
  (data_paths.py:80).
- That directory is ALREADY WRITTEN, and by both kinds of job. `RunLogWriter`
  (run_log.py:94) creates the `job_dir` at run_log.py:116 and writes
  `<run_id>.jsonl` into it at run_log.py:117. Classic jobs reach it with a UUID
  (`agent_loop.py:500`, `autonomy_loop.py:128`); ping-pong jobs reach it with a
  16-hex id at `pingpong_job.py:3165`. `resolve_any_job_id`'s own docstring says
  the same thing (data_paths.py:229): "Both file their run logs the same way,
  under `<data_root>/runs/<job-id>/`".
- The directory keyed by a RUN id is a different one:
  `<data_root>/pingpong_runs/<run_id>/`, written by `pingpong_loop._persist_run`
  (pingpong_loop.py:4234) via `_pingpong_runs_dir` (pingpong_loop.py:4228,
  returning at :4231).

**PLAINLY: yes, the ordered rename lands on an occupied path.** `<data_root>/runs/`
exists in the code as a live, written area today, and `task_jobs/` cannot be
renamed onto it without merging two different kinds of content — one directory
per job holding `job.json`, and one directory per job holding run-log `.jsonl`
files — under one parent.

Two qualifications, so the ruling in round 3 is made on the exact shape:

1. **Entry-by-entry name collision is impossible TODAY, and becomes possible
   under D2.** Both areas are keyed by a job id, but a 16-hex `task_jobs/` entry
   can never equal a 36-char UUID `runs/` entry. It CAN equal a 16-hex `runs/`
   entry — and those already exist, because `pingpong_job.py:3165` writes them.
   So for a ping-pong job the rename collides at the entry level right now:
   `task_jobs/<16hex>/` and `runs/<16hex>/` are the same job, and merging them
   puts `job.json` beside that job's `.jsonl` run logs.
2. **The vocabulary makes the target wrong independently of the collision.** Both
   `task_jobs/` and `runs/` are keyed by JOB id, and F259's binding page gives a
   Job MANY runs. No job-keyed directory can express that, so renaming a
   job-keyed directory to `runs/` would give the plural name to a singular thing.

I could not list the live data root to corroborate this from the filesystem:
`ls -d /home/decodeux/Repos/remedy/.data` was refused by this session's sandbox.
The collision above is established from the WRITERS, which is the stronger
reading anyway — it holds for any data root, not just this machine's.

## What this file deliberately does not do

It rules nothing. DECISION F260 D1 (which classic fields move, and where a Run's
evidence lives), D2 (the one id shape) and the disposition of the five areas in
item 1 are round 3's first work. Nothing under `packages/`, `apps/` or `tests/`
was changed by the round that wrote this.
