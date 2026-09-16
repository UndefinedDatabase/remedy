── STEP T002/4 — F261 — ROUND 8 ──
Goal: Book round 7's PASS, register R-0898 to R-0900, record DECISION F261 D7, and give `job show`
its `--json`, the findings of blocked tasks and the `--full` sections with `job permissions`
folded in, in three commits by applying three tables; mark R-0896 and R-0806 landed; run the
suite once.

Base commit: `22173331`, on `feature/f261-cli-vocabulary-v2`. SESSION 2 of F261. Read AGENTS.md,
docs/agents/self_drive_protocol.md, and DECISION F261 D7 once C1 has landed it.

THE FRAME RULE, per item 37 of §3, measured over the final bytes: NO LINE of this block is a run
of a single repeated character, and every box-drawing rule inside the STEP and SLICE header
lines is exactly two characters long.

ENVIRONMENT: `VAR=x cmd`, `env` and `export` are denied, so set environment in-process; `cp` is
denied, so copy with `shutil.copyfile`; bare `ruff` is denied, so use `python3 -m ruff check`.
Shell loops, `$(...)` and `$?` in a compound command are refused by form, so write such checks
as Python scripts under `.remedy-wt/f261r8w/`; a pipe into `tail` hides pytest's exit code. The
editable install resolves `apps` and `packages` to the PRIMARY checkout, so a pytest run inside a
worktree goes through a runner script that changes into the worktree, puts it first on
`sys.path` and in `PYTHONPATH`, and asserts `apps.cli.commands.job` loaded from inside it.
Never call `run_job` or a runner yourself: a job run started from inside a checkout creates a
`remedy/job-*` branch in it. `git branch --list 'remedy/job-*'` reads 16 lines now; keep it so.

## Bundle — the ordered commit sequence

C0a `.agent/authored/f261-r8.md`, the block file the delegating message names, by
    `shutil.copyfile`
C0b `.agent/last_block.md`, the same bytes
C1  THE RECORD, one commit: `.agent/plan.md` becomes slice PLAN8; slice RECORD8 is appended to
    `.agent/live_review.md` and slice DEC7 to `.agent/decisions.md`; pair P273 is applied
C2  `--json` AND THE FLAG GUARD: copy `.remedy-wt/f261-block/f261-r8-show-1.jsonl` to
    `.agent/authored/f261-r8-show-1.jsonl` and apply it per THE TABLES, in one commit
C3  THE FINDINGS OF BLOCKED TASKS: the same with `f261-r8-show-2.jsonl`, in one commit
C4  THE SECTIONS AND THE PERMISSIONS FOLD: the same with `f261-r8-show-3.jsonl`, in one commit
C5  THE LANDED LINES: slice LANDED8 is appended to `.agent/live_review.md`, in one commit
C6  `.agent/handoff.md`, the handback; then `git push origin feature/f261-cli-vocabulary-v2`

C1 is the FIRST SUBSTANTIVE COMMIT, per item 23 of §3. No pull request is created.

## Change — exactly these paths and no others

C0a to C1: `.agent/authored/f261-r8.md`, `.agent/last_block.md`, `.agent/plan.md`,
`.agent/live_review.md`, `.agent/decisions.md` and `docs/roadmap/features/T2_F273.md`. C2 to C4:
each table's own carrier and the paths G3 names. C5: `.agent/live_review.md`. C6:
`.agent/handoff.md`.

## The pair and the appends

P273 `docs/roadmap/features/T2_F273.md`: FROM slice P273-FROM, which occurs exactly once there at
`22173331`, TO slice ACC273. The containment test printed `TO contains FROM: true`, so
P273 is APPEND-shaped and is proved by whole-file equality, with no FROM-zero count. RECORD8,
DEC7 and LANDED8 each begin with an empty line, and every target ends in a newline at the commit
before its append: an append is the file's bytes followed by the slice's bytes, and nothing else.

## THE TABLES

Each carrier holds one JSON array per line. Their sha256 digests, to verify before copying:
`f261-r8-show-1.jsonl` `011479d6fa07a1fbb37e760db790334562cf5297243d4c7da3b1a183cf23190e`,
`f261-r8-show-2.jsonl` `b8134144d0ec1c953be1171392245c29678133b3552ef10dd7da5c107cb13169`,
`f261-r8-show-3.jsonl` `10d1c62056bcb60e99e9536742188d6e4b74f69eb05df984c55b40cb9f475b98`.
Apply the rows strictly
in file order, each against the tree as the previous rows left it, from the repository root:
`["edit", path, old, new, count]` opens the path with `encoding="utf-8", newline=""`, requires
the number of occurrences of `old` to equal `count` exactly, and replaces every occurrence with
`new`; `["delete", path]` removes the file; `["move", src, dst]` renames the file, whose target
must not exist; `["create", path, content]` writes `content` to a path that must not exist, with
the same encoding and newline setting. A count that differs or a target that exists is a STOP:
touch nothing further, commit nothing of that table, and hand back with the row and the reading.
Stage each commit with `git add -A` after its table and its carrier. The tables are the
reviewer's measured dry run of DECISION F261 D7: show-1 its CHOSEN FIRST, show-2 its CHOSEN
SECOND, and show-3 its CHOSEN THIRD and FOURTH.

## SPEC S — the suite, once, after G6 and before C6

From the primary checkout's root, serially:
`python3 -B -m pytest -q -p no:randomly -p no:cacheprovider --tb=short -rfEs`, with `PYTHONPATH`,
`REMEDY_PROJECT` and `REMEDY_DATA_DIR` removed and `PYTHONDONTWRITEBYTECODE=1`, output under
`.remedy-wt/f261r8w/`. Report pytest's return code, the run's last output line, and every
distinct bad node, the text after a line-initial `FAILED ` or `ERROR ` up to the first ` - `.
Re-run each bad node alone, once, the same way, and report that return code beside it.

## Constraints

1. NO SLICE AND NO TABLE IS EDITED. Extract each slice as the bytes strictly between its
   `BEGIN <NAME>` and `END <NAME>` lines and verify its sha256 before use.
2. READ `.agent/STOP` before C0a, before C2 and before C6, with real exit codes. If it exists:
   finish a half-written commit, write the handoff, push, stop.
3. A red gate is a STOP: commit what is honestly finished, hand back with the raw output.
4. Scratch, runner scripts and your worktree live under `.remedy-wt/f261r8w/`, uncommitted; no
   `.py` file under `.agent/`. Under `.remedy-wt/` open only `.remedy-wt/f261-block/` and your
   own directory. `git worktree list` reads one row now; leave it so. Create no symlink.
5. Every commit stays under 500 insertions, read as the first column of `git show --numstat
   --format= <commit>` with git's default rename detection.
6. NEVER merge, open a pull request, force-push, rewrite history or delete a branch. No `remedy`.
   Write no `Done:` paragraph.
7. THE BLOCK'S OWN SIZE, measured on its final bytes: 295 lines TOTAL and 216 lines of PROSE,
   against the caps of 490 and 400.
8. GATE ORDER. G1 and G2 after C1; G3 after C4; G4 and G5 after C4; G6 after C5; then SPEC S,
   whose result is G7; G8 after C6 and the push, reported in the completion message only.
9. Every commit message ends with `Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>`, and
   no subject carries a leading-slash token or an absolute path.

## Done when — every gate run for real, its exit code recorded

G1 TRANSPORT. The sha256 of `.agent/authored/f261-r8.md` at C0a equals the digest the delegating
message gives, and `.agent/last_block.md` at C0b is byte-identical to it; the slices FOUND, each
matching its BEGIN-marker sha256; each committed carrier's sha256 equals its digest above.

G2 THE RECORD, at C1. `.agent/plan.md` is byte-identical to PLAN8, at most 50 lines, with
`^## Goal$` once and `^## Next Steps$` once. `.agent/live_review.md` equals its `22173331` blob
followed by RECORD8, `.agent/decisions.md` its `22173331` blob followed by DEC7, and
`docs/roadmap/features/T2_F273.md` its `22173331` blob with P273's FROM replaced by its TO. Over
`.agent/live_review.md`: `^Gate: F\d+ R\d+ — ` reads 116 at `22173331` and 117 at C1, with
`Gate: F261 R7 — ` once at C1; distinct `^- R-\d+ — ` ids 100 and 103, C1 minus base exactly
`R-0898`, `R-0899` and `R-0900` and base minus C1 empty; distinct `^Done: R-\d+ — ` ids 4 and 4;
the open set by distinct id 96 and 99.

G3 THE SHOW COMMITS, at C2, C3 and C4. `git diff --no-renames --name-only` from each commit's
parent prints exactly that commit's carrier and: at C2 `apps/cli/command_catalog.py`,
`packages/orchestration/orchestrator_brain.py`, `packages/orchestration/repair_request_builder.py`,
`packages/orchestration/self_dogfood_execution.py`, `tests/cli/test_advertised_commands.py` and
`tests/cli/test_job_show.py`; at C3 `apps/cli/command_catalog.py`, `apps/cli/commands/job.py`,
`packages/orchestration/pingpong_job.py` and `tests/cli/test_job_show.py`; at C4
`apps/cli/command_catalog.py`, `apps/cli/commands/job.py`, `docs/system/architecture.md`,
`packages/orchestration/brain_detail.py`, `tests/cli/test_job_show.py`, `tests/test_cli_main.py`
and `tests/test_command_catalog.py`. `git rev-parse <commit>:<dir>` equals the dry run: C2
`apps` `6a32ca216cc190667fe7b1f9e820e29a1cbc6ea4`, `packages` `66fcac08a584e67ca3a58a2b0b38e4cf0668982c`, `tests`
`6da54dc5daa809801c3e2f67b1ae83025bf73687`; C3 `apps` `cd096440309b99f46c9e20c66a62eba77ffa7256`, `packages`
`8ae6a584e763323ca50553a6a6a59a6fb715ba08`, `tests` `97fe2f2fc7f457be5cb77c8346b5cdaa3c3fdf4d`; C4 `apps`
`92dc18cc92bfadca14f92eca739feb89321faa0a`, `packages` `f614c5a23cbda685b1072e09f5f9b89341e6a79e`, `tests`
`6207c33baa1eb1cc2b5bf33b000972226a10477a`, `docs/system` `a2a587aab4c1f6bc716cc64968b72472e4d4de9c`. At each of those commits
`scripts` and `README.md` equal their objects at `22173331`, and `docs/roadmap` its object at
C1; at C2 and C3 `docs` equals its object at C1. Report each commit's insertions per constraint 5.

G4 THE SWEEP, at C4. `git grep -n -I -F -e job.permissions -e _cmd_show_permissions <C4> -- apps
packages scripts tests docs ':!docs/roadmap'` prints exactly one line, the `DELETED` entry
`"job.permissions",` in `tests/test_command_catalog.py`. `python3 -m ruff check` over every `.py`
path of C2, C3 and C4 exits 0.

G5 THE RED-PROOF, in `git worktree add --detach .remedy-wt/f261r8w/wt <C4's sha>`, each run
through the runner over `tests/cli/test_job_show.py`, `tests/cli/test_advertised_commands.py` and
`tests/test_command_catalog.py` with `-rf --tb=no`. Each mutation replaces bytes whose count in the
named file must read 1 and is restored afterwards with
`git -C .remedy-wt/f261r8w/wt checkout -- <that file>`. (a) CONTROL: must exit 0.
(b) `apps/cli/command_catalog.py`: the bytes of slice MUT-B-FROM become those of slice MUT-B-TO:
must exit 1 with `test_every_advertised_flag_is_declared_by_its_command` among the failed nodes.
(c) `packages/orchestration/pingpong_job.py`: `BLOCKED_TASK_FINDINGS_CAP = 10` becomes
`BLOCKED_TASK_FINDINGS_CAP = 11`: must exit 1 with
`TestBlockedTaskFindings::test_the_default_shows_ten_findings_and_names_the_overflow` failed.
(d) The same file: `last = rounds[-1]` becomes `last = rounds[0]`: must exit 1 with
`TestBlockedTaskFindings::test_only_the_last_round_of_the_blocked_task_appears` failed.
(e) `apps/cli/commands/job.py`: `except Exception as exc:  # noqa: BLE001` becomes
`except KeyError as exc:  # noqa: BLE001`: must exit 1 with
`TestSections::test_a_raising_section_becomes_section_failed_and_the_command_exits_zero` failed.
(f) The same file: `    "job.budget": lambda args: _cmd_job_budget(` becomes
`    "job.permissions": lambda args: None,` followed by a newline and those same bytes: must exit 1
with `TestDeletedCommands::test_no_deleted_id_is_left_in_the_dispatch_table` failed.
(g) The same file: `shown["blocked_task_findings"] = collect_blocked_task_findings(job, full=full)`
becomes `shown["blocked_task_findings"] = []`: must exit 1 with
`TestABlockedFakeRunShowsItsFindingText::test_the_persisted_finding_summary_appears_in_job_show`
failed. Report each exit code, summary line and number of failed nodes; then
`git worktree remove --force .remedy-wt/f261r8w/wt` and read `git branch --list 'remedy/job-*'`.

G6 THE LANDED LINES, at C5. `.agent/live_review.md` equals its C4 blob followed by LANDED8;
`^Landed: R-0896 — ` and `^Landed: R-0806 — ` each occur once among the lines C5 adds; the open
set reads 99 by distinct id, equal as a set to C4's.

G7 THE SUITE, SPEC S at C5: must exit 0 with no bad node; report the last output line.

G8 THE TREE, after C6 and the push. `git status --porcelain` prints `''`; C0a to C6 are
single-parent commits in that order on `22173331`; `git rev-parse HEAD` equals
`git rev-parse origin/feature/f261-cli-vocabulary-v2`; `git worktree list` prints one row, and
`git branch --list 'remedy/job-*'` prints 16 lines.

## The handback, C6

`.agent/handoff.md` per `docs/agents/handback_template.md`, Session line
`SESSION 2 of feature F261 · round 8 · rounds so far 8`, with one sentence of context
self-assessment. `## Commits` lists C0a to C5, each row's `+/-` cell equal to constraint 5's
reading of that commit and its deletions column; C6's own numbers appear nowhere, per item 31 of
§3. `## Verification` gives G1 to G7 with real exit codes. It states the open findings at 99 by
distinct id, with the High ids R-0803, R-0804, R-0806 and R-0807 and with R-0896 and R-0806
landed, and `Operator questions open: 0`. Its `## Next` names, in order: Phase 1 rule 1; the
reviewer's verdict on round 8; the folds of `job assumptions`, `job fences` and `job dod`.

── SLICE PLAN8 ── target `.agent/plan.md` ── FULL REPLACEMENT ──
BEGIN PLAN8 sha256=77721d550611aadc57b8c7471612b19c8e99792787dce5c70ed696b0234ca4f7
# Plan — F261 CLI vocabulary v2 (rename & prune)

Branch: feature/f261-cli-vocabulary-v2, cut from `main` at
`7cdde89b5d0dc8ef1fb96980105870e956699873`, the merge commit of pull request 250.

## Goal

The catalog `apps/cli/command_catalog.py` equals DECISION amend0905-vocab D4: one name per
command, and every retired word deleted rather than aliased, per
`docs/roadmap/features/T2_F261.md`.

## Current Step

ROUND 8 continues T002. It books round 7's PASS, registers R-0898, R-0899 and R-0900 and
records DECISION F261 D7. Then, in three commits, `job show` takes the `--json` its hints name
and a guard checks every advertised flag (R-0896), prints the last-round findings of blocked
tasks with a `--full` overflow (R-0806), and gains the `--full` sections with `job permissions`
folded in as the first; a last record commit marks R-0896 and R-0806 landed.

## Next Steps

1. The folds of `job assumptions`, `job fences` and `job dod` into sections of `job show --full`,
   one command per commit, each adding its id to the deleted-command guard.
2. The folds of `job summary`, `job digest`, `job status` and `job report`, then `do job-report`,
   the same way.
3. The run-level promote words DECISION F261 D6 leaves, ruled by sense, with the kept-by-sense
   list DECISION amend0905-vocab D5 names written into the record and a test for the
   Acceptance grep of the retired word.
4. T003, the prune to D4, with R-0900; then T004.

## Risks

- 96 findings are open by distinct id before this round's record and 99 after it; four are
  High, R-0803, R-0804, R-0806 and R-0807.
- `job show` prints JSON that the canary, `tests/cli/test_plan_approval.py` and
  `scripts/remedy_smoke.sh` parse, so every change to it only adds keys.
- `job fences` refuses a job whose repository was never attached with `job attach-repo`; its
  section reports that as an error envelope rather than an exit.
END PLAN8

── SLICE RECORD8 ── target `.agent/live_review.md` ── APPEND ──
BEGIN RECORD8 sha256=1b65d9217e07dba5dd611922665f6f696eae18a88728798afa44d82b29b76847

Gate: F261 R7 — the F261 round 7 entry. VERDICT PASS. Written by the planner and reviewer of session 37 after reading the committed range `8b07c95b`..`22173331` and re-deriving the readings below; the worker's report was evidence for none of them. It is booked here by the first commit of round 8 that writes the record, per operator amendment amend0827-process-diet rule 1. THE TRANSPORT: `.agent/authored/f261-r7.md` at `82f2f088` and `.agent/last_block.md` at `ab225280` are byte-identical to the reviewer's scratch original, sha256 `b3aba0b5f49dae402c943a75bb806675477743918f7ea2bb3abd8cbf9379f6e9`, and the four tables committed at `a8ac671a`, `0e7e2182`, `cc56e9e4` and `c7d8f7a6` are byte-identical to the reviewer's. THE STATE: at `9984586e` and again at `22173331`, `.agent/plan.md` equals PLAN7 and `.agent/live_review.md` and `.agent/decisions.md` equal their `8b07c95b` blobs followed by RECORD7 and DEC6. THE WORDS: at `a8ac671a`, `0e7e2182`, `cc56e9e4` and `c7d8f7a6` the `apps`, `packages`, `tests`, `scripts`, `docs` and `README.md` objects equal the reviewer's dry-run commits of the tables, which had reproduced the research helper's trees exactly; each commit's `--no-renames` path set is the dry run's plus its carrier, and `git show --numstat` reads 90, 54, 174 and 25 insertions. In the dry run the `.py` lines the three words tables change reduce, with names, strings and comments blanked, to the token skeletons of the lines they replace, except five prose lines that gained a word; and no new status value, reason code, key, directory or prefix occurred outside `.agent/` at `8b07c95b`. At `c7d8f7a6` the grep of the old status values, reason codes, key, directory, prefix and helper names exits 1 with no output, the case-insensitive `promot` grep over `job_apply.py` and its four test files prints only the guard's own assertion, and the grep of the old record test names over `tests/orchestration` exits 1. In the reviewer's dry run a full suite under `-n auto` without `tests/ui_server` read 1 failed, `test_vitest_passes`, and 17664 passed; over the four test files, which passed 172 unmutated, reverting the `applied` status failed 25 tests, and reverting the `job_apply_records` directory, the `job_apply_id` key, the `Job apply record: ` text or the `--skip-blocked` help failed 1 each. THE REVIEWER'S RUN in the primary checkout at `22173331` of the four test files, `tests/test_command_catalog.py`, `tests/docs/`, `tests/cli/test_advertised_commands.py`, `tests/ui_server/test_dashboard_contract.py` and `tests/cli/test_golden_path.py` read 629 passed. The open set reads 96 by distinct id at `22173331`.

- R-0898 — Medium, `job summary`, `job status` AND `job report` COUNT A TASK AS DONE ONLY WHEN ITS STATUS READS `completed`, SO A JOB FINISHED BY THE JOB RUNNER READS `0/N done` HOWEVER MANY OF ITS TASKS PASSED. Raised by the planner and reviewer of session 37 while preparing F261 round 8, after searching the open set for `done_count` and the `completed` comparison under §3 item 30: no open finding describes it. THE DEFECT, measured at `22173331`: `_cmd_job_summary`, `_cmd_job_status` and `_cmd_job_report` in `apps/cli/commands/job.py` each count as done the tasks whose status equals `"completed"`, and `all_tasks_done` in `packages/orchestration/job_fulfillment.py` makes the same comparison; the job runner in `packages/orchestration/pingpong_job.py` marks a finished task `passed` or `applied_to_job_workspace`, while `RunState.COMPLETED` is written to a task only by `job_fulfillment.py`, `mission_state.py`, `task_runner.py` and `worker_queue.py`. The reviewer saved, under a scratch data root, a job in state `completed` whose two tasks read `applied_to_job_workspace` and `passed`, and ran the three commands with `--json`: each printed `done_count` 0 and `pending_count` 0 for `task_count` 2. WHY MEDIUM: the view described as the truth contract prints a finished job as having done nothing. WHY F273's: F261 folds these views into `job show --full` without changing what they compute, per its Do-not-touch. FIX: one done predicate over both task vocabularies, used by the three views and by `all_tasks_done`, and a test over a job whose tasks passed and were applied. Owner: F273.

- R-0899 — Medium, SECTION 3 OF `scripts/remedy_smoke.sh` READS A `state` KEY THAT `job show` DOES NOT PRINT, SO ITS PLANNED-STATE CHECK FAILS WHENEVER THE SCRIPT REACHES IT. Raised by the planner and reviewer of session 37 while preparing F261 round 8, after searching the open set for the script and the key under §3 item 30: no open finding describes it. THE DEFECT, read at `22173331`: after `remedy job create --task-type`, the script parses the output of `remedy job show` and exits 1 unless `job.get('state', '')` equals `planned`; `_export_job` in `packages/orchestration/pingpong_job.py`, which `job show` prints, writes the job's state under the key `status` and writes no key `state`. The reviewer read the code and did not run the script. WHY MEDIUM: the product smoke cannot pass its own job-creation check, so that gate reads red for a working job and proves nothing about it. WHY F273's: it is a one-key repair in a script no F261 slice owns. FIX: read `status`, and a test that runs the section's parser against the `job show` output of a created job. Owner: F273.

- R-0900 — Medium, PRINTED NEXT STEPS NAME `remedy do --continue <job-id>`, A FORM THE CLI REJECTS, AND `docs/system/architecture.md` DOCUMENTS `remedy brain <job_id>` LINES THE `brain` GROUP HAS NO COMMAND FOR. Raised by the planner and reviewer of session 37 while preparing F261 round 8, whose advertised-flag check reads only hints that name a group and a subcommand, after searching the open set under §3 item 30: no open finding describes it. THE DEFECT, read at `22173331`: `packages/orchestration/do_continue.py` sets `next_safe_action` to `remedy do --continue {job_id} --json` and, for more than one approved intent, to `remedy do --continue {job_id} --intent-id <id> --json`, while the catalog's continuation command is `do continue <job_id>`; `docs/guides/do-continue-v1.md` is titled with the same form; and `docs/system/architecture.md` lists `remedy brain <job_id>` and `remedy brain <job_id> --json`, while every `brain` command takes a subcommand. `tests/cli/test_advertised_commands.py` resolves a group-only match against the group list alone, so every one of these lines passes it. WHY MEDIUM: the continuation a blocked cycle recommends exits 2, the R-0896 shape. WHY F261's: T003 deletes `do continue` and repoints its hints, and T004 re-derives the documented command lines. FIX: each such line names a command the catalog carries, and a test covers the group-only form. Owner: F261.
END RECORD8

── SLICE DEC7 ── target `.agent/decisions.md` ── APPEND ──
BEGIN DEC7 sha256=50174a6bd1c9a14c3073ba74c8cda51621b1acae8835402962f31dc81e0eea93

## DECISION F261 D7 (2026-09-15, F261 round 8) — `job show` takes `--json` and `--full`, prints the findings of blocked tasks and carries the read views as sections; the deletion paragraph of `job permissions`

CONTEXT. DECISION amend0905-vocab D4 binds `job show <id> [--full]` and makes permissions, fences, assumptions, digest, summary, status, report and dod sections of `--full` rather than commands. DECISION F261 D4 ordered `--full` next and left its shape to the round that builds it; R-0806 asks `job show` for the findings of blocked tasks, and R-0896 for the `job show --json` that printed hints name. Measured at `22173331` by the reviewer's research helper and re-read by the reviewer on the dry-run trees: `job show` prints `_export_job` as one JSON document, which `tests/cli/test_golden_path.py`, `tests/cli/test_plan_approval.py` and `scripts/remedy_smoke.sh` parse whole, and prints its intake block on stderr.

CHOSEN, FIRST: `--json`. `job show` declares `--json`, and its output is the same JSON with or without it, rather than every hint losing the flag: nineteen next-step hints, one of them in `docs/guides/do-run-v1.md`, name the flag a user copies. `tests/cli/test_advertised_commands.py` now holds every `--flag` after a `remedy <group> <sub>` hint against the flags that command declares; the three `patch approve ... --json` hints it found lose the flag, which `patch approve` never declared. A group-only hint names no command and is not flag-checked; the defects of that form are R-0900.

CHOSEN, SECOND: THE FINDINGS OF BLOCKED TASKS. After every key it carried, the JSON gains `blocked_task_findings`: for each blocked task in task order, its run id, the number of its run's last round, that round's reviewer findings with `id`, `severity`, `file` and `summary` copied verbatim, at most ten of them, and their total and the number omitted. `summary` is the title R-0806 names, because the run record has no other. `--full` omits none. The shown findings also print on stderr beside the intake block. The reader never raises: a task without a readable run shows none.

CHOSEN, THIRD: THE SECTIONS. With `--full` the JSON also gains `sections`, whose keys follow D4's order and hold only the views folded so far, each `{"ok": true, "data": ...}` or `{"ok": false, "error": {"code": ..., "message": ...}}`. A view that raises becomes the code `section_failed`, and `job show --full` exits 0 for every job that exists. Each view's former text prints on stderr under its own heading. The registry is `_SHOW_SECTIONS` in `apps/cli/commands/job.py`, and each fold adds one entry. A view whose former command exited non-zero for a job it could not describe, `job fences` for a job without an attached repository among them, reports that as an error envelope with its own code when it folds.

CHOSEN, FOURTH: THE DELETION OF `job permissions`. Deleted: the catalog entry `job.permissions`, its handler-table row and `_cmd_show_permissions`. `job.permissions` joins `TestDeletedCommands` and leaves `TestRequiredCommands`, `job permit` relates to `job show`, and the blocker hint of `packages/orchestration/brain_detail.py` and the permissions paragraph of `docs/system/architecture.md` name `remedy job show <id> --full`. THE HEIR is the `permissions` section: its data is the rows `effective_permissions` returns, and its text is the former command's.

CONSEQUENCE. `job show` gains one key by default and two with `--full`, and every parser of it keeps working. `remedy job permissions <id>` exits with an argument error. The remaining views fold one per commit in later rounds, each with its own deletion paragraph; whether `do job-report` joins the `report` section or becomes a section of its own is ruled when it folds. HOW TO REVERSE: revert the round's three table commits and delete this section.
END DEC7

── SLICE P273-FROM ── target `docs/roadmap/features/T2_F273.md` ── FROM OF P273 ──
BEGIN P273-FROM sha256=12a68827ef6563e070221a34747c2d36e96a7674b52e09566b11244f725032b3
- R-0890 carries a resolution line naming the test that proves an unflagged self-use run
  records the role config's builder and reviewer model.
END P273-FROM

── SLICE ACC273 ── target `docs/roadmap/features/T2_F273.md` ── TO OF P273 ──
BEGIN ACC273 sha256=2103e972ce9303e858656440d8ca563d077899494a0c768ee19252087baba257
- R-0890 carries a resolution line naming the test that proves an unflagged self-use run
  records the role config's builder and reviewer model.
- R-0898 carries a resolution line naming the test that proves a job whose tasks passed and
  were applied reads them as done in the job's summary, status and report views.
- R-0899 carries a resolution line naming the test that runs the job-creation check of
  `scripts/remedy_smoke.sh` against the `job show` output of a created job.
END ACC273

── SLICE LANDED8 ── target `.agent/live_review.md` ── APPEND AT C5 ──
BEGIN LANDED8 sha256=da87ce51cada40db44656a356aaf0c8ec45b767728ced72b532055f82634ac11

Landed: R-0896 — `job show` declares `--json`, and `tests/cli/test_advertised_commands.py` now fails for a flag that a `remedy <group> <sub>` hint passes and that command does not declare; landed by C2 of `.agent/authored/f261-r8.md`, which that block's Bundle orders before this line.

Landed: R-0806 — `job show` prints the last-round reviewer findings of every blocked task, ten by default and all of them with `--full`, and `tests/cli/test_job_show.py` finds a blocked fake-provider run's persisted finding text in its output; landed by C3 of `.agent/authored/f261-r8.md`, which that block's Bundle orders before this line.
END LANDED8

── SLICE MUT-B-FROM ── G5 (b) only, never a file ──
BEGIN MUT-B-FROM sha256=fa2da571dcd9ed3082fe15fb3e218b18b423c9be5bde291ae5a566d27ee30d67
            _JSON_OPT,
        ),
        supports_json=True,
        related=("job.list", "brain.graph"),
END MUT-B-FROM

── SLICE MUT-B-TO ── G5 (b) only, never a file ──
BEGIN MUT-B-TO sha256=44b2185ed1b7547619ea8c5d94fc76b0ab31cd50d804ea8641268e405237a8b6
        ),
        supports_json=True,
        related=("job.list", "brain.graph"),
END MUT-B-TO
