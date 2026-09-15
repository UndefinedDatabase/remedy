── STEP T002/7 — F261 — ROUND 11 ──
Goal: Book round 10's PASS, register R-0902, record DECISION F261 D10, move the `job report`
and `do job-report` hints to `job show --full`, fold `job report`, delete `do job-report` and
name an unreadable job record, in four commits by applying four tables; append the Landed
lines; run the suite once.

Base commit: `25a97421`, on `feature/f261-cli-vocabulary-v2`. SESSION 3 of F261. Read AGENTS.md,
docs/agents/self_drive_protocol.md, and DECISIONs F261 D7 to D10 once C1 has landed D10.

THE FRAME RULE, per item 37 of §3, measured over the final bytes: NO LINE of this block is a run
of a single repeated character, and every box-drawing rule inside the STEP and SLICE header
lines is exactly two characters long.

ENVIRONMENT: `VAR=x cmd`, `env` and `export` are denied, so set environment in-process; `cp` is
denied, so copy with `shutil.copyfile`; bare `ruff` is denied, so use `python3 -m ruff check`.
Shell loops, `$(...)` and `$?` in a compound command are refused by form, so write such checks
as Python scripts under `.remedy-wt/f261r11w/`, and never name a script after a standard-library
module; a pipe into `tail` hides pytest's exit code. The editable install resolves `apps` and
`packages` to the PRIMARY checkout, so a pytest run inside a worktree goes through a runner
script that changes into the worktree, puts it first on `sys.path` and in `PYTHONPATH`, and
asserts `apps.cli.commands.job` loaded from inside it. Never call `run_job` or a runner yourself:
a job run started from inside a checkout creates a `remedy/job-*` branch in it.
`git branch --list 'remedy/job-*'` reads 16 lines now; keep it so.

## Bundle — the ordered commit sequence

C0a `.agent/authored/f261-r11.md`, the block file the delegating message names, by
    `shutil.copyfile`
C0b `.agent/last_block.md`, the same bytes
C1  THE RECORD, one commit: `.agent/plan.md` becomes slice PLAN11; slice RECORD11 is appended to
    `.agent/live_review.md` and slice DEC10 to `.agent/decisions.md`
C2  THE HINTS: copy `.remedy-wt/f261-block/f261-r11-hints.jsonl` to
    `.agent/authored/f261-r11-hints.jsonl` and apply it per THE TABLES, in one commit
C3  THE REPORT FOLD: the same with `f261-r11-report.jsonl`, in one commit
C4  THE DELETION OF `do job-report`: the same with `f261-r11-dojobreport.jsonl`, in one commit
C5  THE UNREADABLE RECORD: the same with `f261-r11-unreadable.jsonl`, in one commit
C6  THE LANDED LINES: slice LANDED11 is appended to `.agent/live_review.md`, in one commit
C7  `.agent/handoff.md`, the handback; then `git push origin feature/f261-cli-vocabulary-v2`

C1 is the FIRST SUBSTANTIVE COMMIT, per item 23 of §3. No pull request is created.

## Change — exactly these paths and no others

C0a to C1: `.agent/authored/f261-r11.md`, `.agent/last_block.md`, `.agent/plan.md`,
`.agent/live_review.md` and `.agent/decisions.md`. C2 to C5: each table's own carrier and the
paths G3 names. C6: `.agent/live_review.md`. C7: `.agent/handoff.md`.

## The appends

RECORD11, DEC10 and LANDED11 each begin with an empty line, and every target ends in a newline
at the commit before its append: an append is the file's bytes followed by the slice's bytes,
and nothing else.

## THE TABLES

Each carrier holds one JSON array per line. Their sha256 digests, to verify before copying:
`f261-r11-hints.jsonl` `806bdc26fc5d86bfb095bd1e1d055e2d48926076a629119ba00c2e7613246c84`,
`f261-r11-report.jsonl` `053333ac2c051359dd34aae59ef82f36673ef0f50879918c05ba3e4acedc124f`,
`f261-r11-dojobreport.jsonl` `6007bae3c4817bb42033d0edc04244bd98e7e434a79180b48b96bf70e9f915d2`,
`f261-r11-unreadable.jsonl` `5120264b78b0f51d5fd86c937e1747b9d8ee831d3c0edd2e787c28c5a16798ed`.
Apply the rows strictly
in file order, each against the tree as the previous rows left it, from the repository root:
`["edit", path, old, new, count]` opens the path with `encoding="utf-8", newline=""`, requires
the number of occurrences of `old` to equal `count` exactly, and replaces every occurrence with
`new`; `["delete", path]` removes the file; `["move", src, dst]` renames the file, whose target
must not exist; `["create", path, content]` writes `content` to a path that must not exist, with
the same encoding and newline setting. A count that differs or a target that exists is a STOP:
touch nothing further, commit nothing of that table, and hand back with the row and the reading.
Stage each commit with `git add -A` after its table and its carrier. The tables are the
reviewer's measured dry run of DECISION F261 D10: the hints table its CHOSEN FIRST, the report
table its CHOSEN SECOND, the `do job-report` table its CHOSEN THIRD, and the unreadable-record
table its CHOSEN FOURTH.

## SPEC S — the suite, once, after G6 and before C7

From the primary checkout's root, serially:
`python3 -B -m pytest -q -p no:randomly -p no:cacheprovider --tb=short -rfEs`, with `PYTHONPATH`,
`REMEDY_PROJECT` and `REMEDY_DATA_DIR` removed and `PYTHONDONTWRITEBYTECODE=1`, output under
`.remedy-wt/f261r11w/`. Report pytest's return code, the run's last output line, and every
distinct bad node, the text after a line-initial `FAILED ` or `ERROR ` up to the first ` - `.
Re-run each bad node alone, once, the same way, and report that return code beside it.

## Constraints

1. NO SLICE AND NO TABLE IS EDITED. Extract each slice as the bytes strictly between its
   `BEGIN <NAME>` and `END <NAME>` lines and verify its sha256 before use.
2. READ `.agent/STOP` before C0a, before C2 and before C7, with real exit codes. If it exists:
   finish a half-written commit, write the handoff, push, stop.
3. A red gate is a STOP: commit what is honestly finished, hand back with the raw output.
4. Scratch, runner scripts and your worktree live under `.remedy-wt/f261r11w/`, uncommitted; no
   `.py` file under `.agent/`. Under `.remedy-wt/` open only `.remedy-wt/f261-block/` and your
   own directory. `git worktree list` reads one row now; leave it so. Create no symlink.
5. Every commit stays under 500 insertions, read as the first column of `git show --numstat
   --format= <commit>` with git's default rename detection.
6. NEVER merge, open a pull request, force-push, rewrite history or delete a branch. No `remedy`.
   Write no `Done:` paragraph; the only `Landed:` lines are LANDED11's.
7. THE BLOCK'S OWN SIZE, measured on its final bytes: 313 lines TOTAL and 240 lines of PROSE,
   against the caps of 490 and 400.
8. GATE ORDER. G1 and G2 after C1; G3, G4 and G5 after C5; G6 after C6; then SPEC S, whose
   result is G7; G8 after C7 and the push, reported in the completion message only.
9. Every commit message ends with `Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>`, and
   no subject carries a leading-slash token or an absolute path.

## Done when — every gate run for real, its exit code recorded

G1 TRANSPORT. The sha256 of `.agent/authored/f261-r11.md` at C0a equals the digest the delegating
message gives, and `.agent/last_block.md` at C0b is byte-identical to it; the slices FOUND, each
matching its BEGIN-marker sha256; each committed carrier's sha256 equals its digest above.

G2 THE RECORD, at C1. `.agent/plan.md` is byte-identical to PLAN11, at most 50 lines, with
`^## Goal$` once and `^## Next Steps$` once. `.agent/live_review.md` equals its `25a97421` blob
followed by RECORD11, and `.agent/decisions.md` its `25a97421` blob followed by DEC10. Over
`.agent/live_review.md`: `^Gate: F\d+ R\d+ — ` reads 119 at `25a97421` and 120 at C1, with
`Gate: F261 R10 — ` once at C1; distinct `^- R-\d+ — ` ids 104 and 105, C1 minus base exactly
`R-0902`; distinct `^Done: R-\d+ — ` ids 6 and 6; the open set by distinct id 98 and 99.

G3 THE TABLES, at C2, C3, C4 and C5. `git diff --no-renames --name-only` from each commit's
parent prints exactly that commit's carrier and: at C2 `apps/cli/commands/job.py`, `docs/guides/simple-operator-quickstart-v0.md`, `docs/system/core-product-spine-v0.md`, `docs/system/first-fulfilled-job-demo-v0.md`, `docs/system/first-perfect-job-demo-v0.md`, `packages/orchestration/job_fulfillment.py`, `packages/orchestration/pingpong_job.py`, `packages/orchestration/run_report.py`, `tests/cli/test_advertised_commands.py`, `tests/cli/test_product_spine.py`, `tests/orchestration/test_job_fulfillment.py` and `tests/orchestration/test_job_task_runner.py`; at C3 `apps/cli/command_catalog.py`, `apps/cli/commands/job.py`, `tests/cli/test_job_report.py`, `tests/cli/test_job_show.py`, `tests/cli/test_open_decisions_view.py`, `tests/cli/test_product_spine.py`, `tests/orchestration/test_job_fulfillment.py` and `tests/test_command_catalog.py`; at C4
`apps/cli/command_catalog.py`, `apps/cli/commands/do_cmd.py`, `tests/orchestration/test_job_task_runner.py` and `tests/test_command_catalog.py`; at C5 `apps/cli/commands/job.py` and `tests/cli/test_job_show.py`. `git rev-parse <commit>:<object>` equals the dry run, for
`apps`, `tests`, `docs`, `scripts`, `packages` and `README.md` in that order: C2 `4e06b0ed28c3a08f312cdd4a6bbe88dcb6fee4f0`, `e4b1af405e2b95cbad939dec465ac9f0a83d1b39`, `cabe17706d0bf0a61c52009c99f89bc890f53d5b`, `68e16104807fd30c528b58559e4d7968d011ef48`, `d2d5b4c5295d80b66ac145b5c9359021c600c6ae`, `15b9e0e8fec9721c7c17a872cc8f1a2bed3a2952`;
C3 `379be2815bebf00b63e4302d4a44057c4d295fc8`, `28f65b1a22a6be435df61924b9d8be6c6368466c`, `cabe17706d0bf0a61c52009c99f89bc890f53d5b`, `68e16104807fd30c528b58559e4d7968d011ef48`, `d2d5b4c5295d80b66ac145b5c9359021c600c6ae`, `15b9e0e8fec9721c7c17a872cc8f1a2bed3a2952`; C4 `360ed791689a5e7bbdd69d314c709c13411d1997`, `6d6f49d1b4338896fe534a03273e683cf15890cf`, `cabe17706d0bf0a61c52009c99f89bc890f53d5b`, `68e16104807fd30c528b58559e4d7968d011ef48`, `d2d5b4c5295d80b66ac145b5c9359021c600c6ae`, `15b9e0e8fec9721c7c17a872cc8f1a2bed3a2952`; C5 `64404771eea09816b9ccb013f5e70e8945c6d434`, `b98818d2ff95fc49f0d33e69c614aab4c824b47e`, `cabe17706d0bf0a61c52009c99f89bc890f53d5b`, `68e16104807fd30c528b58559e4d7968d011ef48`, `d2d5b4c5295d80b66ac145b5c9359021c600c6ae`, `15b9e0e8fec9721c7c17a872cc8f1a2bed3a2952`. Report each commit's insertions per constraint 5.

G4 THE SWEEP, at C5. `git grep -n -I -F -e '"job.report"' -e '"do.job-report"' -e _cmd_job_report
-e _cmd_job_run_report -e _cmd_do_job_report <C5> -- apps packages scripts tests docs README.md
':!docs/roadmap'` prints exactly two lines, the `DELETED` entries of `do.job-report` and
`job.report` in `tests/test_command_catalog.py`. `git grep -n -I -E
'remedy (job report|do job-report)\b|job-report' <C5> -- apps packages scripts docs README.md
':!docs/roadmap'` exits 1 and prints nothing. `python3 -m ruff check` over every `.py` path of
C2 to C5 exits 0.

G5 THE RED-PROOF, in `git worktree add --detach .remedy-wt/f261r11w/wt <C5's sha>`, each run
through the runner over `tests/cli/test_job_show.py`, `tests/test_command_catalog.py`,
`tests/cli/test_job_report.py`, `tests/cli/test_open_decisions_view.py`,
`tests/cli/test_product_spine.py`, `tests/orchestration/test_job_fulfillment.py` and
`tests/cli/test_advertised_commands.py` with `-rf --tb=no`. Mutation <n> is in the file its
line below names, replaces the bytes of slice MUT-<n>-FROM, whose count there must read 1, with
those of slice MUT-<n>-TO, and is restored with `git -C .remedy-wt/f261r11w/wt checkout --
<that file>`. (a) CONTROL: must exit 0. Each of (1) to (6) must exit 1 with the named node
among the failed nodes:
(1) `apps/cli/commands/job.py`, a `job.report` handler row:
`TestDeletedCommands::test_no_deleted_id_is_left_in_the_dispatch_table`;
(2) `apps/cli/commands/job.py`, every report final:
`TestANonTerminalRunGetsTheInterimReport::test_a_running_job_s_section_is_interim_with_the_banner`;
(3) `apps/cli/commands/job.py`, the status and report entries swapped:
`TestSections::test_full_prints_the_registered_sections_in_the_d4_order`;
(4) `packages/orchestration/pingpong_job.py`, the blocked hint naming `do job-report`:
`test_every_advertised_command_exists_in_the_catalog`;
(5) `apps/cli/commands/job.py`, `JobStoreError` uncaught:
`TestAnUnreadableJobRecord::test_job_show_names_the_unreadable_record_and_exits_one[bare]`;
(6) `apps/cli/commands/job.py`, the progress view dropped from the text:
`TestTheProgressView::test_the_text_is_the_progress_view_a_blank_line_and_the_markdown`.
Report each exit code, summary line and number of failed nodes; then
`git worktree remove --force .remedy-wt/f261r11w/wt` and read `git branch --list 'remedy/job-*'`.

G6 THE LANDED LINES, at C6. `.agent/live_review.md` equals its C5 blob followed by LANDED11, and
the path set of C6 is exactly `.agent/live_review.md`.

G7 THE SUITE, SPEC S at C6: must exit 0 with no bad node; report the last output line. A bad
node whose lone re-run exits 0 is reported as such with both readings, and is not a STOP; a bad
node whose lone re-run fails is.

G8 THE TREE, after C7 and the push. `git status --porcelain` prints `''`; C0a to C7 are
single-parent commits in that order on `25a97421`; `git rev-parse HEAD` equals
`git rev-parse origin/feature/f261-cli-vocabulary-v2`; `git worktree list` prints one row, and
`git branch --list 'remedy/job-*'` prints 16 lines.

## The handback, C7

`.agent/handoff.md` per `docs/agents/handback_template.md`, Session line
`SESSION 3 of feature F261 · round 11 · rounds so far 11`, with one sentence of context
self-assessment. `## Commits` lists C0a to C6, each row's `+/-` cell equal to constraint 5's
reading of that commit and its deletions column; C7's own numbers appear nowhere, per item 31 of
§3. `## Verification` gives G1 to G7 with real exit codes. It states the open findings at 99 by
distinct id, with the High ids R-0803, R-0804 and R-0807, and `Operator questions open: 0`. Its
`## Next` names, in order: Phase 1 rule 1; the reviewer's verdict on round 11 and the
resolutions of R-0901 and R-0902; the run-level promote words DECISION F261 D6 leaves.

── SLICE PLAN11 ── target `.agent/plan.md` ── FULL REPLACEMENT ──
BEGIN PLAN11 sha256=aa9072032f3b8257774dedfd177c3e82c6bb389961de5edc6bc28d75834bcbcc
# Plan — F261 CLI vocabulary v2 (rename & prune)

Branch: feature/f261-cli-vocabulary-v2, cut from `main` at
`7cdde89b5d0dc8ef1fb96980105870e956699873`, the merge commit of pull request 250.

## Goal

The catalog `apps/cli/command_catalog.py` equals DECISION amend0905-vocab D4: one name per
command, and every retired word deleted rather than aliased, per
`docs/roadmap/features/T2_F261.md`.

## Current Step

ROUND 11 finishes the read views of T002. It books round 10's PASS, registers R-0902 and
records DECISION F261 D10, then points the `job report` and `do job-report` hints at
`job show --full` with R-0901, folds `job report` into the `report` section, deletes
`do job-report`, and makes `job show` name an unreadable job record, one table per commit,
and appends the Landed lines of R-0901 and R-0902.

## Next Steps

1. The run-level promote words DECISION F261 D6 leaves, ruled by sense, with the kept-by-sense
   list DECISION amend0905-vocab D5 names written into the record and a test for the
   Acceptance grep of the retired word.
2. T003, the prune to D4, with R-0900; then T004.

## Risks

- 98 findings are open by distinct id before this round's record and 99 after it; three are
  High, R-0803, R-0804 and R-0807.
- `job show` prints JSON that the canary, `tests/cli/test_plan_approval.py` and
  `scripts/remedy_smoke.sh` parse, so every change to it only adds keys.
- `job show --full` builds every section, the run report's sources among them, so it is the
  slowest read of a job.
END PLAN11

── SLICE RECORD11 ── target `.agent/live_review.md` ── APPEND ──
BEGIN RECORD11 sha256=60772ac1112f972becb38bcea95982cd16c5f6b347ccaf234195b35efdd3d098

Gate: F261 R10 — the F261 round 10 entry. VERDICT PASS. Written by the planner and reviewer of session 38 after reading the committed range `a00c1624`..`25a97421` and re-deriving the readings below; the worker's report was evidence for none of them. It is booked here by the first commit of round 11 that writes the record, per operator amendment amend0827-process-diet rule 1. THE TRANSPORT: `.agent/authored/f261-r10.md` at `b20ed624` and `.agent/last_block.md` at `be0bd9f0` are byte-identical to the reviewer's scratch original, sha256 `79c6de8f519b85a4306a17cc7b78690808a625dd7f2bcefba4243abe26cd5a2e`, and the three tables committed at `836518f5`, `526de930` and `47d34a44` are byte-identical to the reviewer's. THE STATE: at `a3bac8e2` and again at `25a97421`, `.agent/plan.md` equals PLAN10 and `.agent/live_review.md` and `.agent/decisions.md` equal their `a00c1624` blobs followed by RECORD10 and DEC9. THE FOLDS: at `836518f5`, `526de930` and `47d34a44` the `apps`, `tests`, `docs`, `scripts`, `packages` and `README.md` objects equal the reviewer's dry-run commits of the tables, which had reproduced the research helper's trees exactly; each commit's `--no-renames` path set is the dry run's plus its carrier, and `git show --numstat` reads 93, 127 and 214 insertions. In the dry run's production diff each section builder computes what its deleted handler computed, with the handler's prints turned into returned lines, and the status section names the job by its full id. At `25a97421` the grep of `remedy job digest`, `summary` or `status` over `apps`, `packages`, `scripts`, `tests`, `docs` without `docs/roadmap`, and `README.md` exits 1 with no output. In the reviewer's dry run a full suite under `-n auto` without `tests/ui_server` read 3 failed and 17676 passed: `test_vitest_passes`, which fails for the worktree's missing UI build, and `test_the_huge_diff_parses_inside_the_recorded_perf_budget` and `TestAppStartsGreen::test_the_app_is_always_stopped`, of which a serial run of the first with the whole of `tests/orchestration/test_product_smoke.py` read 77 passed. Over `tests/cli/test_job_show.py`, `tests/test_command_catalog.py`, `tests/cli/test_job_digest_cli.py`, `tests/cli/test_open_decisions_view.py`, `tests/cli/test_product_spine.py`, `tests/orchestration/test_job_fulfillment.py` and `tests/cli/test_advertised_commands.py`, which passed 251 unmutated, restoring a `job.status` handler row failed 1 test, wrapping the digest in a key failed 2, a summary that is never live failed 1, printing the open decisions after the job line failed 1, swapping the summary and status registry entries failed 1, and dropping the status section's open decision count failed 3. The record slices applied on top of the dry run passed `tests/docs/` and the other files the reviewer ran among those that read the edited state files, apart from `test_vitest_passes`, at 779 passed. THE REVIEWER'S RUN in the primary checkout at `25a97421` of those seven files, `tests/cli/test_plan_approval.py`, `tests/cli/test_golden_path.py`, `tests/docs/`, `tests/ui_server/test_dashboard_contract.py`, `tests/orchestration/test_event_replay.py` and `tests/ui_contracts/test_decision_urgency_parity.py` read 740 passed, and `git branch --list 'remedy/job-*'` read 16 lines. The open set reads 98 by distinct id at `25a97421`.

- R-0902 — Medium, `job show` PRINTS A PYTHON TRACEBACK FOR A JOB WHOSE RECORD EXISTS AND CANNOT BE READ, AND ONCE `do job-report` IS DELETED IT IS THE ONLY COMMAND THAT READS A JOB'S RECORD. Raised by the planner and reviewer of session 38 while preparing F261 round 11, after searching the open set for `JobStoreError` and `Unreadable job record` under §3 item 30: no open finding describes it. THE DEFECT, read at `25a97421`: `require_job_plan` in `packages/orchestration/pingpong_job.py` raises `JobStoreError` for a record that exists and cannot be read and `JobNotFoundError` only for a missing one, and `_cmd_show_job` in `apps/cli/commands/job.py` catches only `JobNotFoundError`, while `apps/cli/commands/repair_cmd.py` catches both. The reviewer's research helper wrote `{not json` over a scratch job's record under a scratch data root and ran `job show` with the full id and with an eight-character prefix: each run exited 1 with empty stdout and a traceback ending in `JobStoreError: Unreadable job record for <id>`. The reviewer read the code and, in its own dry run of the repair, restored the single `except JobNotFoundError` and saw both cases of a test over an unreadable record fail. WHY MEDIUM: a damaged record reads as a crash of the read command rather than as a named error, on the command a user is told to run next. WHY F261's: the round that deletes `do job-report` makes `job show` its heir. FIX: `_cmd_show_job` catches `JobStoreError` beside `JobNotFoundError`, prints the error on stderr and exits 1, and a test runs `job show` with and without `--full` over an unreadable record. Owner: F261.
END RECORD11

── SLICE DEC10 ── target `.agent/decisions.md` ── APPEND ──
BEGIN DEC10 sha256=89a4fe178e80e2450528fb72deb7af196817fe9ad5c12bd67f4ad11b501032ac

## DECISION F261 D10 (2026-09-15, F261 round 11) — the deletion paragraph of `job report` with its `--final` and `--interim` forms and of `do job-report`, and the error an unreadable record names

CONTEXT. DECISION F261 D7 made the read views of a job sections of `job show --full` and left two questions to this fold: how the run report's `--final` and `--interim` forms sit in the `report` section, and whether `do job-report` joins that section or becomes a section of its own. DECISION amend0905-vocab D4 names the sections and names no section for `do job-report`. Measured by the reviewer's research helper at `a00c1624` and on round 10's dry-run trees, and re-read by the reviewer on this round's dry-run trees.

CHOSEN, FIRST: THE HINTS MOVE FIRST. Every printed next step, docstring and doc page that named `remedy job report` or `remedy do job-report` names `remedy job show <id> --full`, keeping a `--json` the hint carried, in a commit ahead of the fold, so each later commit deletes a command no hint names: the status section's next safe action, whose two identical last branches become one, the next safe actions of `packages/orchestration/job_fulfillment.py`, the blocked-job hint `_suggest_next_command` returns in `packages/orchestration/pingpong_job.py`, and the quickstart guide, `docs/system/core-product-spine-v0.md`, `docs/system/first-fulfilled-job-demo-v0.md` and `docs/system/first-perfect-job-demo-v0.md`, whose step lists merge the two steps that now print one command and renumber the steps after them. R-0901's row is corrected in the same commit.

CHOSEN, SECOND: `job report`. Deleted: the catalog entry `job.report` with its comment, its handler-table row with its comment, `_cmd_job_report` and `_cmd_job_run_report`. THE HEIR is the `report` section, registered after `status`. Its data holds the keys of the former `--json` payload in their order, `fulfillment` when a fulfillment record exists, and then `run_report`, holding `mode`, `sources` and `markdown`. `mode` is `final` when the job's `cycle_terminal_status` is in `REPORTED_TERMINALS` of `packages/orchestration/long_run_executor.py` and `interim` for every other job; `sources` is the former `--final --json` document, built once by `build_report_sources` and passed through JSON with sorted keys and `str` for any other value; `markdown` is `render_report` over those sources in that mode, so an interim report opens with its snapshot banner. Its text is the former progress view, an empty line and the markdown. The refusal of `--final` for a job not at a reported terminal, with its `run_not_terminal` payload, is deleted with the flag: a job the section cannot call final is shown interim, under the banner that keeps a moving run from reading as a final account (R-0161). Like the command, the section writes no report file and changes no job.

CHOSEN, THIRD: `do job-report`. Deleted: the catalog entry `do.job-report`, its handler-table row and `_cmd_do_job_report`; it does not become a section. THE HEIR is `job show`, whose JSON already carries every stored field the command printed, `status`, `execution_config` and each task's `status` among them, and which resolves an id prefix the command did not and prints the findings of blocked tasks. No read command prints the derived keys and the text view of `export_job_report` and `format_job_report_text` any more; `job run` and `do job-resume` still print `export_job_report`'s document, and `job run` its text view too. The `related=` tuples that named `do.job-report` name `job.show`.

CHOSEN, FOURTH: AN UNREADABLE RECORD IS NAMED. `_cmd_show_job` catches `JobStoreError` beside `JobNotFoundError`, as `apps/cli/commands/repair_cmd.py` does, and prints `Error: Unreadable job record for <id>` with exit 1 instead of a traceback (R-0902).

CONSEQUENCE. `remedy job report`, with or without `--final` or `--interim`, and `remedy do job-report` exit with an argument error, and `job.report` and `do.job-report` join `TestDeletedCommands`. A test that pinned a deleted catalog entry, handler row, flag, refusal or unknown-id payload is deleted, and the refusal tests become tests that a non-terminal job's section is interim. The registry holds `permissions`, `fences`, `assumptions`, `digest`, `summary`, `status`, `report` and `dod`, every section D4 names, in its order. For the report, `job show --full` reads the job's STATUS mirror and run events, and an interim report carries the time it was rendered, so two calls differ. HOW TO REVERSE: revert the round's four table commits and delete this section.
END DEC10

── SLICE LANDED11 ── target `.agent/live_review.md` ── APPEND AT C6 ──
BEGIN LANDED11 sha256=abcf33bf9d9fc8f5835f471ba28b6ca0d69bfb825cb7463cbd4c3fe80be0d224

Landed: R-0901 — the `code_applied` row of the status-section table in `docs/system/first-perfect-job-demo-v0.md` gives `false`, the value that section prints for the demo job; landed by C2 of `.agent/authored/f261-r11.md`, which that block's Bundle orders before this line.

Landed: R-0902 — `job show` names a job record that exists and cannot be read, printing `Error: Unreadable job record for <id>` and exiting 1, and `tests/cli/test_job_show.py::TestAnUnreadableJobRecord` holds that with and without `--full`; landed by C5 of `.agent/authored/f261-r11.md`, which that block's Bundle orders before this line.
END LANDED11

── SLICE MUT-1-FROM ── G5 (1) only ── never a file ──
BEGIN MUT-1-FROM sha256=9489ee8832c4a185bac13752680fe3080f85e39ca8e9549c661b18e925664c3b
    "job.fulfill": lambda args: _cmd_job_fulfill(
END MUT-1-FROM

── SLICE MUT-1-TO ── G5 (1) only ── never a file ──
BEGIN MUT-1-TO sha256=30b327c084b4e23d788b4bb93a6c8fbd6241ba720709c19f51434c43d2801e98
    "job.report": lambda args: None,
    "job.fulfill": lambda args: _cmd_job_fulfill(
END MUT-1-TO

── SLICE MUT-2-FROM ── G5 (2) only ── never a file ──
BEGIN MUT-2-FROM sha256=2592c4adc78bcdb057d6e05c60926b243f9d586b99236a68d24405e5c33b53b6
    mode = MODE_FINAL if terminal in REPORTED_TERMINALS else MODE_INTERIM
END MUT-2-FROM

── SLICE MUT-2-TO ── G5 (2) only ── never a file ──
BEGIN MUT-2-TO sha256=794a47efb031d8a95baac4e0ae78f38efaba8f9b48d8009c5d7ad680a4588a35
    mode = MODE_FINAL
END MUT-2-TO

── SLICE MUT-3-FROM ── G5 (3) only ── never a file ──
BEGIN MUT-3-FROM sha256=bb8b394998204f3856086fa98022a2432d3874e5d8adc352fe3dd9bb848ef279
    ("status", _status_section),
    ("report", _report_section),
END MUT-3-FROM

── SLICE MUT-3-TO ── G5 (3) only ── never a file ──
BEGIN MUT-3-TO sha256=977ef7215c7b8be29792410a08c6c6f8c492d7c9d24194fd913ecc230acae16e
    ("report", _report_section),
    ("status", _status_section),
END MUT-3-TO

── SLICE MUT-4-FROM ── G5 (4) only ── never a file ──
BEGIN MUT-4-FROM sha256=52ec8857603f52c44c9d666b7812c14a11542f7b1e066b8d333a29a909246a08
        return f"remedy job show {job.job_id} --full"
END MUT-4-FROM

── SLICE MUT-4-TO ── G5 (4) only ── never a file ──
BEGIN MUT-4-TO sha256=5151f3cc6312af87cafc090bac742d86d7f3d639867e593084d84c3f1c29ea36
        return f"remedy do job-report {job.job_id}"
END MUT-4-TO

── SLICE MUT-5-FROM ── G5 (5) only ── never a file ──
BEGIN MUT-5-FROM sha256=4c1e284cf0bf0dfe102fda7aa6ad082a3d13db0dd8c0032831981bdc59373480
    except (JobNotFoundError, JobStoreError) as exc:
END MUT-5-FROM

── SLICE MUT-5-TO ── G5 (5) only ── never a file ──
BEGIN MUT-5-TO sha256=2b5d5c6e6f6d12791caaf6a4f2fcd6a3288604c94460c6498659beda44d0318e
    except JobNotFoundError as exc:
END MUT-5-TO

── SLICE MUT-6-FROM ── G5 (6) only ── never a file ──
BEGIN MUT-6-FROM sha256=65e4eac45830842e547fa3248466a1262cdf8dab6fcb5d7fb057c90f562cfe93
    lines.append("")
    lines.extend(markdown.splitlines())
END MUT-6-FROM

── SLICE MUT-6-TO ── G5 (6) only ── never a file ──
BEGIN MUT-6-TO sha256=852f500ded29f3d13a0b7fad41ea9bbf55f1f5a040f89ad2d6105d9dcf02acb7
    lines = [""]
    lines.extend(markdown.splitlines())
END MUT-6-TO
