# F258 Round 1 — Seam Inventory

Measured against this branch at commit `fdb74bc2` (after C5, `.agent/context.md`
rewritten), the current tip when this file was written. Every claim below cites
a `file:line` and, where a count is involved, the exact command that produced
it. Six sections, per the block's SPEC.

## 1. The queue schema and its v1 contract

`packages/orchestration/self_use_queue.py`:

- `SELF_USE_QUEUE_SCHEMA_VERSION = 1` — `packages/orchestration/self_use_queue.py:57`.
- The id regex: `_ITEM_ID_RE = re.compile(r"^SU-\d{3}$")` — `packages/orchestration/self_use_queue.py:65`.
- The five allowed keys: `_ITEM_KEYS: tuple[str, ...] = ("id", "title", "why", "job_markdown", "consumed_by")` — `packages/orchestration/self_use_queue.py:69`.
- `SelfUseQueueEntry` (frozen dataclass) fields, in order: `id: str`, `title: str`, `why: str`, `job_markdown: str`, `consumed_by: str`, plus the derived `is_pending` property — `packages/orchestration/self_use_queue.py:83-95`.
- `def load_self_use_queue(path: Path | None = None) -> tuple[SelfUseQueueEntry, ...]` — `packages/orchestration/self_use_queue.py:109`.
- `def pending_self_use_items(path: Path | None = None) -> tuple[SelfUseQueueEntry, ...]` — `packages/orchestration/self_use_queue.py:178`.
- `def next_self_use_item(path: Path | None = None) -> SelfUseQueueEntry | None` — `packages/orchestration/self_use_queue.py:183`.

The exact validation code that would reject an unknown key today (e.g. a new
`provenance` field on a v2 item) — `packages/orchestration/self_use_queue.py:148-150`:

```
_require(tuple(sorted(raw)) == tuple(sorted(_ITEM_KEYS)),
         f"{queue_path}: items[{position}] must carry exactly the keys "
         f"{sorted(_ITEM_KEYS)}, found {sorted(raw)}")
```

This compares the SORTED key set of the raw item dict against the sorted
`_ITEM_KEYS` tuple for EQUALITY, not subset/superset — an item carrying a sixth
key such as `provenance`, however well-formed, fails this `_require` and the
whole `load_self_use_queue` call raises `SelfUseQueueError` before the entry is
ever constructed.

What a schema-version bump would need to touch for v2 to add a field (measured,
not designed): (a) `SELF_USE_QUEUE_SCHEMA_VERSION` at line 57 would move to `2`
or the version check at `packages/orchestration/self_use_queue.py:134-136` would
need to accept a set of versions rather than one exact value; (b) `_ITEM_KEYS`
at line 69 would need the new key added; (c) the per-item required-string loop
at `packages/orchestration/self_use_queue.py:151-155` (or a new equivalent
branch) would need to validate the new field; (d) `SelfUseQueueEntry` at
line 83-90 would need the new field added to the dataclass and to the
`SelfUseQueueEntry(...)` construction at `packages/orchestration/self_use_queue.py:164-170`;
(e) the shipped `scripts/self_use_queue.json`'s own `schema_version` value and
every existing item in it would need updating to stay loadable, since the
version check is an exact-match refusal, not a range.

## 2. The planner seam

`packages/orchestration/self_use_job.py`:

- `def write_self_use_job_file(entry: SelfUseQueueEntry, dest_dir: Path) -> Path` — `packages/orchestration/self_use_job.py:70`.
- `def plan_self_use_item(entry: SelfUseQueueEntry, dest_dir: Path, repo_path: str = ".") -> tuple[Path, object]` — `packages/orchestration/self_use_job.py:136-140`.
- `def plan_next_self_use_item(dest_dir: Path, repo_path: str = ".", queue_path: Path | None = None) -> tuple[SelfUseQueueEntry, Path, object]` — `packages/orchestration/self_use_job.py:152-156`.

`packages/orchestration/pingpong_job.py`'s `plan_job_from_file`:

- Signature: `def plan_job_from_file(job_file_path: str, repo_path: str = ".") -> JobPlan` — `packages/orchestration/pingpong_job.py:822`.
- What it requires as input: a `job_file_path` (str) that must exist on disk —
  if it does not, it persists and returns a `JobPlan` with `status=JOB_BLOCKED`
  and `error=f"job_file_not_found: {job_file_path}"` instead of raising
  (`packages/orchestration/pingpong_job.py:824-832`) — and a `repo_path` (str,
  default `"."`). When the file exists it reads the text and returns
  `parse_job_file(text, repo_path)` (`packages/orchestration/pingpong_job.py:833-834`).
- The exact shape of the `JobPlan` it returns: `@dataclass class JobPlan` at
  `packages/orchestration/pingpong_job.py:202-203`, with fields (in file order,
  `packages/orchestration/pingpong_job.py:205-234`): `job_id`, `job_file_sha256`,
  `repo_path`, `job_workspace_path`, `job_title`, `status`, `tasks: list[TaskEntry]`,
  `created_at`, `finished_at`, `error`, `target_guard: TargetGuard | None`,
  `repair_rounds_allowed`, `repair_rounds_source`, `execution_config: ExecutionConfig | None`,
  and the F006 isolation fields `isolation_mode` ("copy" default, or "worktree"),
  `worktree_branch`, `worktree_path`, `worktree_base_commit`, `worktree_head`,
  `worktree_cleanup_status`, plus `postmortem_path`, `postmortem_error`,
  `worktree_cleanup_error`, `result_diff_path`, `result_diff_sha256`.

## 3. The closure consumption point today — search for it and report the result

Commands run (both from the repo root, excluding test files by directory
scope — `tests/` was not included in either search path):

```
grep -rn "plan_next_self_use_item" --include="*.py" packages/ apps/
grep -rn "next_self_use_item" --include="*.py" packages/ apps/
```

Every line either command found:

- `packages/orchestration/self_use_job.py:21` — a docstring/comment line
  naming `plan_next_self_use_item(dest_dir, repo_path=".", queue_path=None)`.
- `packages/orchestration/self_use_job.py:48` — the import line
  `from packages.orchestration.self_use_queue import SelfUseQueueEntry, next_self_use_item`.
- `packages/orchestration/self_use_job.py:152` — the `def plan_next_self_use_item(` definition itself.
- `packages/orchestration/self_use_job.py:165` — `plan_next_self_use_item`'s own body calling `next_self_use_item(queue_path)`.
- `packages/orchestration/self_use_queue.py:25` — a docstring line naming `next_self_use_item(path=None) -> SelfUseQueueEntry | None`.
- `packages/orchestration/self_use_queue.py:41` — a docstring line referencing `next_self_use_item`.
- `packages/orchestration/self_use_queue.py:183` — the `def next_self_use_item(` definition itself.

ABSENCE, reported as measured: there is NO call site of either function
anywhere else in `packages/` or `apps/` — every hit above is either the
function's own definition, its own internal docstring/comment, or (for
`plan_next_self_use_item`) its one internal call of `next_self_use_item`. No
CLI command module, no closure script, no `apps/cli/commands/*.py` file and no
other `packages/orchestration/*.py` module calls either function. This is what
"no production caller at any closure point" means concretely: the composition
these two functions exist to start (queue → job file → `JobPlan`) is never
triggered by running code today.

`docs/roadmap/STATUS_closure_protocol.md` precondition 6's exact text
(`docs/roadmap/STATUS_closure_protocol.md:20-31`):

> 6. EXACTLY ONE SELF-USE ITEM IS CONSUMED BY THIS CLOSE (F257). The first
> pending item in `scripts/self_use_queue.json` — the one
> `packages.orchestration.self_use_queue.next_self_use_item` answers — has
> been planned through `packages.orchestration.self_use_job`, taken to the
> normal approval gate like any other job, and its `consumed_by` set to this
> feature's id in the closure commit. If the queue holds NO pending item the
> track is exhausted, not blocked: record `self-use NONE (queue exhausted)`
> in the handback and close normally, because an empty queue asks the
> operator to curate more rather than stopping a feature. Why this is a
> precondition and not an intention: "Remedy is used on Remedy" rots the
> moment it depends on someone remembering to do it, which is DECISION F257
> D2's CONSEQUENCE clause in as many words.

Stated plainly: this precondition names a MANUAL, BY-HAND STEP performed once
per session at closure, not a code hook. Its own wording is in the perfect
passive ("has been planned", "its `consumed_by` set ... in the closure
commit") describing something a session DID, and section 3's search above
confirms there is no function or script anywhere that performs this
planning/promotion/consumed_by-set sequence automatically — a human (or the
closing session acting as one) runs `plan_next_self_use_item`, takes the
result through the job path by hand, and edits `consumed_by` in the closure
commit itself.

## 4. The job execution path to "a real run"

`apps/cli/commands/job.py` — every subcommand between job creation and the
approval gate a self-use item's execution would pass through, in path order,
each with its catalog registration line in `apps/cli/command_catalog.py`:

1. Creation — `_cmd_create_job` at `apps/cli/commands/job.py:24`, catalog
   `command_id="job.create"` at `apps/cli/command_catalog.py:247`.
2. Repo-attach — `_cmd_attach_repo` at `apps/cli/commands/job.py:334`, catalog
   `command_id="job.attach-repo"` at `apps/cli/command_catalog.py:318`.
3. Permission setting — `_cmd_set_permission` at `apps/cli/commands/job.py:357`,
   catalog `command_id="job.permit"` at `apps/cli/command_catalog.py:327`.
4. The run-loop/run-cycles entry point — TWO exist and both were found:
   `_cmd_job_run_cycles` at `apps/cli/commands/job.py:646` (catalog
   `command_id="job.run"`, described "Run a job in bounded cycles", at
   `apps/cli/command_catalog.py:410`), and `_cmd_run_loop` at
   `apps/cli/commands/job.py:1027` (catalog `command_id="job.run-loop"`,
   "Run the contract-gated autonomy loop for a job", at
   `apps/cli/command_catalog.py:441`). There is also `_cmd_run_next_task_local`
   at `apps/cli/commands/job.py:402` (catalog `command_id="job.run-next"`,
   "Run the next pending task for a job", at `apps/cli/command_catalog.py:399`).

`packages/orchestration/job_promote.py`'s `promote_job` — the manual `--approve`
barrier: `def promote_job(job_id: str, target_repo: str = ".", *, approve: bool = False, dry_run: bool = False, test_command: str = "", skip_blocked: bool = False) -> JobPromotionResult` at
`packages/orchestration/job_promote.py:647`, whose own docstring states
"Without --approve, returns dry-run preview only. Never auto-promotes."
(`packages/orchestration/job_promote.py:658`). Its CLI surface is
`command_id="do.job-promote"` at `apps/cli/command_catalog.py:3317`, described
"Review and apply job workspace changes to target repo. Dry-run by default;
--approve applies." (`apps/cli/command_catalog.py:3320`), carrying the
`--approve` `ArgDef` at `apps/cli/command_catalog.py:3327`.

The worktree-isolation seam (F006) a self-use run would need for "an isolated
worktree": `JobPlan.isolation_mode: str = "copy"` with the comment
`# "worktree" | "copy"` at `packages/orchestration/pingpong_job.py:222`, and
the workspace-creation function `_create_job_workspace` at
`packages/orchestration/pingpong_job.py:859`, whose docstring states "For a
GIT target this is a job-owned WORKTREE" (`packages/orchestration/pingpong_job.py:860-866`).
The F006 marker comment "the job workspace IS a job-owned git worktree for a
git target" is at `packages/orchestration/pingpong_job.py:2146`.

## 5. The budget machinery for "a small dedicated budget"

The module and CLI surface that sets a per-job budget limit:
`_cmd_job_budget` at `apps/cli/commands/job.py:2125` (catalog
`command_id="job.budget"` at `apps/cli/command_catalog.py:384`, "Show budget
limits and current counters for a job (F018)"), which calls
`evaluate_budget` — `packages/orchestration/budget_guard.py:254` — imported at
`apps/cli/commands/job.py:2136` (`from packages.orchestration.budget_guard
import evaluate_budget`).

The F104 hard-enforcement module is `packages/orchestration/budget_guard.py`
itself — its module docstring opens "F104 adds a second, FORWARD-looking
evaluation next to the reactive one" at `packages/orchestration/budget_guard.py:6`.

The exact flag/field a caller sets to keep a self-use run small: `job.create`'s
`--max-cost-usd` `ArgDef`, documented inline as "Maximum cost in USD for this
job (F104 budget)" at `apps/cli/command_catalog.py:260` (the `job.create`
`CommandEntry` spans `apps/cli/command_catalog.py:246-264`; the other F018/F104
budget args on the same command — `--max-total-tokens`, `--max-provider-calls`,
`--max-wall-clock-minutes`, `--deadline` — sit alongside it at
`apps/cli/command_catalog.py:257-261`).

## 6. The finding ledger's own shape, for T003

Commands run against `.agent/live_review.md` on this branch (all from the repo
root):

```
grep -c "^- R-" .agent/live_review.md                                    → 317
grep -oE "^- (R-[0-9]+) — " .agent/live_review.md | sort -u | wc -l        → 317
grep -c "^Done: R-" .agent/live_review.md                                 → 57
grep -oE "^Done: (R-[0-9]+) — " .agent/live_review.md | sort -u | wc -l    → 55
```

317 distinct `^- R-\d+ — ` ids are registered (all 317 raw lines are already
distinct — no duplicate registration line exists). 57 raw `^Done: R-\d+` lines
exist but only 55 are DISTINCT ids — two ids each carry two `Done:` lines in
the record (the append-only record does not forbid a correction round writing
a second `Done:` line for the same id; this inventory does not chase which two,
since that is outside this round's scope). Open count on this reading: 317 − 55
= 262 ids that have been registered but never carry a `Done:` line.

One OPEN Medium finding's exact severity-and-status text, quoted verbatim from
its opening — `.agent/live_review.md`, the paragraph beginning at the line
`- R-0753 — Medium, THE DIGEST'S COST BASIS HAS THREE VALUES AND ONLY ONE OF
THEM IS REACHABLE IN PRODUCTION, BECAUSE THE PERSISTED ACTUALS RECORD CARRIES...`
— confirmed OPEN by `grep -c "^Done: R-0753" .agent/live_review.md` → `0`
(no match; `grep -c` reports the exit-1/zero-match count as `0`).

`tests/orchestration/test_self_use_queue.py` and
`tests/orchestration/test_self_use_job.py` are named as the fixture style
T001-T003's own tests should follow. One existing test function's name from
each, both class-scoped (neither file uses bare module-level `def test_`):

- `tests/orchestration/test_self_use_queue.py:70` —
  `class TestShippedQueueLoads` (`tests/orchestration/test_self_use_queue.py:67`)
  → `def test_shipped_queue_loads_with_at_least_one_item(self):`.
- `tests/orchestration/test_self_use_job.py:64` —
  `class TestWriteSelfUseJobFile` (`tests/orchestration/test_self_use_job.py:61`)
  → `def test_rendered_bytes_equal_the_curated_bytes(self, tmp_path: Path):`.

## Absences, summarized

- NO code caller of `plan_next_self_use_item` or `next_self_use_item` exists
  outside their own defining module and each other's internal use, searched
  with `grep -rn "plan_next_self_use_item" --include="*.py" packages/ apps/`
  and `grep -rn "next_self_use_item" --include="*.py" packages/ apps/` (both
  exclude `tests/` by not naming it in the search path).
- NO schema field named `provenance` exists on `SelfUseQueueEntry` or in
  `_ITEM_KEYS` today (`packages/orchestration/self_use_queue.py:69,83-90`) —
  confirmed by reading the full tuple and dataclass definitions directly, not
  by a text search that could miss a differently-spelled field.
- NO single run-loop entry point exists; the execution path has THREE
  candidate commands (`job.run`, `job.run-loop`, `job.run-next`), all found
  above — which one a self-use run would use is a T002 design question this
  inventory deliberately leaves open.
