── STEP T002/1 — F261 — ROUND 5 ──
Goal: Book round 4's PASS, register R-0896 and R-0897, record DECISION F261 D4, and delete
`do promote` and its run-level library in two commits by applying two tables; run the suite once.

Base commit: `350fa353`, on `feature/f261-cli-vocabulary-v2`. SESSION 1 of F261. Read AGENTS.md,
docs/agents/self_drive_protocol.md, and DECISIONs F261 D1 to D4 once C1 has landed D4.

THE FRAME RULE, per item 37 of §3, measured over the final bytes: NO LINE of this block is a run
of a single repeated character, and every box-drawing rule inside the STEP and SLICE header
lines is exactly two characters long.

ENVIRONMENT: `VAR=x cmd`, `env` and `export` are denied, so set environment in-process; `cp` is
denied, so copy with `shutil.copyfile`; bare `ruff` is denied, so use `python3 -m ruff check`.
Shell loops, `$(...)` and `$?` in a compound command are refused by form, so write such checks
as Python scripts under `.remedy-wt/f261r5w/`; a pipe into `tail` hides pytest's exit code. The
editable install resolves `apps` and `packages` to the PRIMARY checkout, so a pytest run inside a
worktree goes through a runner script that changes into the worktree, puts it first on
`sys.path` and in `PYTHONPATH`, and asserts `apps.cli.command_catalog` loaded from inside it.

## Bundle — the ordered commit sequence

C0a `.agent/authored/f261-r5.md`, the block file the delegating message names, by
    `shutil.copyfile`
C0b `.agent/last_block.md`, the same bytes
C1  THE RECORD, one commit: `.agent/plan.md` becomes slice PLAN5; slice RECORD5 is appended to
    `.agent/live_review.md` and slice DEC4 to `.agent/decisions.md`; pair P268B is applied
C2  DELETION 1: copy `.remedy-wt/f261-block/f261-r5-delete-1.jsonl` to
    `.agent/authored/f261-r5-delete-1.jsonl` and apply it per THE TABLES, in one commit
C3  DELETION 2: the same with `f261-r5-delete-2.jsonl`, in one commit
C4  `.agent/handoff.md`, the handback; then `git push origin feature/f261-cli-vocabulary-v2`

C1 is the FIRST SUBSTANTIVE COMMIT, per item 23 of §3. No pull request is created.

## Change — exactly these paths and no others

C0a to C1: `.agent/authored/f261-r5.md`, `.agent/last_block.md`, `.agent/plan.md`,
`.agent/live_review.md`, `.agent/decisions.md` and `docs/roadmap/features/T2_F268.md`. C2 and C3: each table's own carrier and the paths G3 and G4
name. C4: `.agent/handoff.md`.

## The pair and the appends

P268B `docs/roadmap/features/T2_F268.md`: FROM slice P268B-FROM, which occurs exactly once there at
`350fa353`, TO slice ACC268B. The containment test printed `TO contains FROM: true`, so P268B is
APPEND-shaped and is proved by whole-file equality, with no FROM-zero count. RECORD5 and DEC4 each
begin with an empty line, and both targets end in a newline at `350fa353`: an append is the
file's bytes followed by the slice's bytes, and nothing else.

## THE TABLES

Each carrier holds one JSON array per line. The sha256 of `f261-r5-delete-1.jsonl` is
`65f89231984657f1a6651e908f6e8ca810be790cdae4d1bb6ae2eaa7efa81cf2` and that of `f261-r5-delete-2.jsonl` is
`84ba79bfd2420066c08ec937e30c059c14d6c397ce50567475972dd8f34ef37d`; verify each before copying. Apply the rows strictly
in file order, each against the tree as the previous rows left it, from the repository root:
`["edit", path, old, new, count]` opens the path with `encoding="utf-8", newline=""`, requires
the number of occurrences of `old` to equal `count` exactly, and replaces every occurrence with
`new`; `["delete", path]` removes the file; `["move", src, dst]` renames the file, whose target
must not exist; `["create", path, content]` writes `content` to a path that must not exist, with
the same encoding and newline setting. A count that differs or a target that exists is a STOP:
touch nothing further, commit nothing of that table, and hand back with the row and the reading.
Stage each commit with `git add -A` after its table and its carrier. The tables are the
reviewer's measured dry run of DECISION F261 D4: table 1 deletes the command `do promote`, its
hints and their tests and adds its id to `TestDeletedCommands`; table 2 deletes
`packages/orchestration/pingpong_promote.py`, its test file, the run's staged-snapshot writer and
the readers of the run's `promotion.json`.

## SPEC S — the suite, once, after G5 and before C4

From the primary checkout's root, serially:
`python3 -B -m pytest -q -p no:randomly -p no:cacheprovider --tb=short -rfEs`, with `PYTHONPATH`,
`REMEDY_PROJECT` and `REMEDY_DATA_DIR` removed and `PYTHONDONTWRITEBYTECODE=1`, output under
`.remedy-wt/f261r5w/`. Report pytest's return code, the run's last output line, and every
distinct bad node, the text after a line-initial `FAILED ` or `ERROR ` up to the first ` - `.

## Constraints

1. NO SLICE AND NO TABLE IS EDITED. Extract each slice as the bytes strictly between its
   `BEGIN <NAME>` and `END <NAME>` lines and verify its sha256 before use.
2. READ `.agent/STOP` before C0a, before C2 and before C4, with real exit codes. If it exists:
   finish a half-written commit, write the handoff, push, stop.
3. A red gate is a STOP: commit what is honestly finished, hand back with the raw output.
4. Scratch, runner scripts and your worktree live under `.remedy-wt/f261r5w/`, uncommitted; no
   `.py` file under `.agent/`. Under `.remedy-wt/` open only `.remedy-wt/f261-block/` and your
   own directory. `git worktree list` reads one row now; leave it so.
5. Every commit stays under 500 insertions by `git show --numstat`.
6. NEVER merge, open a pull request, force-push, rewrite history or delete a branch. No `remedy`.
   Write no `Done:` paragraph.
7. THE BLOCK'S OWN SIZE, measured on its final bytes: 237 lines TOTAL and 174 lines of PROSE,
   against the caps of 490 and 400.
8. GATE ORDER. G1 and G2 after C1; G3 after C2; G4 and G5 after C3; then SPEC S, whose result is
   G6; G7 after C4 and the push, reported in the completion message only.
9. Every commit message ends with `Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>`, and
   no subject carries a leading-slash token or an absolute path.

## Done when — every gate run for real, its exit code recorded

G1 TRANSPORT. The sha256 of `.agent/authored/f261-r5.md` at C0a equals the digest the delegating
message gives, and `.agent/last_block.md` at C0b is byte-identical to it; the slices FOUND, each
matching its BEGIN-marker sha256; each committed carrier's sha256 equals its digest above.

G2 THE RECORD, at C1. `.agent/plan.md` is byte-identical to PLAN5, at most 50 lines, with
`^## Goal$` once and `^## Next Steps$` once. `.agent/live_review.md` equals its `350fa353` blob
followed by RECORD5, `.agent/decisions.md` its `350fa353` blob followed by DEC4, and
`docs/roadmap/features/T2_F268.md` its `350fa353` blob with P268B's FROM replaced by its TO. Over
`.agent/live_review.md`: `^Gate: F\d+ R\d+ — ` reads 113 at `350fa353` and 114 at C1, with
`Gate: F261 R4 — ` once; distinct `^- R-\d+ — ` ids 98 and 100; distinct `^Done: R-\d+ — ` ids 4
and 4; the open set by distinct id 94 and 96, with C1 minus base exactly `R-0896` and `R-0897`
and base minus C1 empty.

G3 DELETION 1, at C2. `git diff --no-renames --name-only <C1> <C2>` prints exactly
`.agent/authored/f261-r5-delete-1.jsonl` and these: `apps/cli/command_catalog.py`, `apps/cli/commands/do_cmd.py`, `apps/cli/grouped.py`, `packages/orchestration/pingpong_loop.py`, `packages/orchestration/pingpong_promote.py`, `tests/cli/test_cli_ux.py`, `tests/cli/test_product_spine.py`, `tests/cli/test_task_input.py`, `tests/orchestration/test_pingpong_promote.py`, `tests/test_cli_execution_loop_closure.py` and `tests/test_command_catalog.py`. `git rev-parse <C2>:<dir>`
equals the dry run: `apps` `aaad9640abc468379001a6ff61bcea4be94aef04`,
`packages` `45f95bbc48dbc5e4884712c2fb9d7ff6154fb2a7`, `tests` `88dac13da3445963210dd1414998608d61100493`; `scripts` and `README.md` equal their objects at
`350fa353` and `docs` its object at C1.

G4 DELETION 2, at C3. `git diff --no-renames --name-only <C2> <C3>` prints exactly
`.agent/authored/f261-r5-delete-2.jsonl` and these: `apps/cli/commands/do_cmd.py`, `packages/orchestration/job_evidence.py`, `packages/orchestration/pingpong_evidence.py`, `packages/orchestration/pingpong_loop.py`, `packages/orchestration/pingpong_promote.py`, `tests/cli/test_cli_ux.py`, `tests/orchestration/import_reachability_allowlist.txt`, `tests/orchestration/test_evidence_bundle.py`, `tests/orchestration/test_job_task_runner.py`, `tests/orchestration/test_pingpong_promote.py` and `tests/orchestration/test_repair_loop.py`. `git rev-parse <C3>:<dir>`
equals the dry run: `apps` `8bb7bd9b09e80234fea6165dad1bca1c157bb564`, `packages` `60db4fa8b3472661541025b5f4dfd28fc5c10423`, `tests`
`8e6ae952508ba8b68d7198fa1fb3f0925973aa40`; `scripts` and `README.md` equal their objects at `350fa353` and `docs` its object
at C1. `git grep -n -w -e _cmd_do_promote -e promote_run -e load_promotion -e load_artifacts -e
persist_artifacts -e pingpong_promote <C3> -- apps packages scripts tests docs ':!docs/roadmap'`
prints nothing, and `git grep -n -F do.promote <C3> -- apps packages scripts tests docs
':!docs/roadmap'` prints exactly the `DELETED` entry in `tests/test_command_catalog.py`.
`python3 -m ruff check` over every `.py` path of C2 and C3 exits 0.

G5 THE RED-PROOF, in `git worktree add --detach .remedy-wt/f261r5w/wt <C3's sha>`, each run
through the runner over `tests/test_command_catalog.py` with `-rf --tb=no`. (a) CONTROL: must
exit 0. (b) In `apps/cli/commands/do_cmd.py` the bytes
`    "do.repair-attest": lambda args: _cmd_do_repair_attest(`, whose count there must read 1,
become `    "do.promote": lambda args: None,` followed by a newline and those same bytes: must exit 1
with `TestDeletedCommands::test_no_deleted_id_is_left_in_the_dispatch_table` among the failed
nodes. Restore with `git -C .remedy-wt/f261r5w/wt checkout -- apps/cli/commands/do_cmd.py`.
(c) In `apps/cli/command_catalog.py` the bytes `command_id="job.apply",`, count 1, become
`command_id="do.promote",`: must exit 1 with
`TestDeletedCommands::test_no_deleted_id_is_left_in_the_catalog` among the failed nodes. Restore
the same way. Report each exit code, summary line and every failed node id; then
`git worktree remove .remedy-wt/f261r5w/wt`.

G6 THE SUITE, SPEC S at C3: must exit 0 with no bad node; report the last output line.

G7 THE TREE, after C4 and the push. `git status --porcelain` prints `''`; C0a to C4 are
single-parent commits in that order on `350fa353`; `git rev-parse HEAD` equals
`git rev-parse origin/feature/f261-cli-vocabulary-v2`; `git worktree list` prints one row.

## The handback, C4

`.agent/handoff.md` per `docs/agents/handback_template.md`, Session line
`SESSION 1 of feature F261 · round 5 · rounds so far 5`, with one sentence of context
self-assessment. `## Commits` lists C0a to C3, each row's `+/-` cell equal to
`git show --numstat` of that commit; C4's own numbers appear nowhere, per item 31 of §3.
`## Verification` gives G1 to G6 with real exit codes. It states the open findings at 96 by
distinct id, R-0896 owned by F261 and R-0897 owned by F268 among them, with the High ids R-0803,
R-0804, R-0806 and R-0807, and `Operator questions open: 1`. Its `## Next` names, in order:
Phase 1 rule 1; the reviewer's verdict on round 5; the rename of `job_promote.py` to
`job_apply.py`.

── SLICE PLAN5 ── target `.agent/plan.md` ── FULL REPLACEMENT ──
BEGIN PLAN5 sha256=a687db9ee013d705db67e5cfae0864bd12fa8649d227480f319599aa84c642c2
# Plan — F261 CLI vocabulary v2 (rename & prune)

Branch: feature/f261-cli-vocabulary-v2, cut from `main` at
`7cdde89b5d0dc8ef1fb96980105870e956699873`, the merge commit of pull request 250.

## Goal

The catalog `apps/cli/command_catalog.py` equals DECISION amend0905-vocab D4: one name per
command, and every retired word deleted rather than aliased, per
`docs/roadmap/features/T2_F261.md`.

## Current Step

ROUND 5 opens T002. It books round 4's PASS, registers R-0896 and R-0897, records DECISION
F261 D4, the deletion paragraph of `do promote` and of the run-level apply library only it
used, and deletes both in two commits, each applying a table the round saves under
`.agent/authored/` and the first adding `do.promote` to the deleted-command guard.

## Next Steps

1. The rename of `job_promote.py` to `job_apply.py` with its tests, then its identifiers and
   its output-visible words, keeping the evidence keys D4 names as history.
2. `job show --full` composing the read commands as sections, with the blocked-task findings
   R-0806 asks for and the fix R-0896 needs.
3. One commit per folded read command and `do job-report`, each adding its id to the guard.
4. The remaining run-level promote words; then T003, the prune to D4, and T004.

## Risks

- 94 findings are open by distinct id before this round's record and 96 after it; four are
  High, R-0803, R-0804, R-0806 and R-0807.
- `job show` prints JSON that the canary, `tests/cli/test_plan_approval.py` and
  `scripts/remedy_smoke.sh` parse, so its `--full` form only adds keys to that JSON.
- A run started without a job has no apply command after this round; R-0897 records it for
  F268.
END PLAN5

── SLICE RECORD5 ── target `.agent/live_review.md` ── APPEND ──
BEGIN RECORD5 sha256=449a1c25b7dedf8234c155821088badc52fcd8c2a82adbf472b2f05da143efe0

Gate: F261 R4 — the F261 round 4 entry. VERDICT PASS. Written by the planner and reviewer of session 36 after reading the committed range `b8f019de`..`350fa353` and re-deriving the readings below; the worker's report was evidence for none of them. It is booked here by the first commit of round 5 that writes the record, per operator amendment amend0827-process-diet rule 1. THE TRANSPORT: `.agent/authored/f261-r4.md` at `2ccc400b` and `.agent/last_block.md` at `71b078e7` are byte-identical to the reviewer's scratch original, sha256 `87b880f80856d3b1689949ddf050b7940e42a2338d00ca79f7c36732da922083`, and `.agent/authored/f261-r4-delete-1.jsonl` at `36eb4573` and `.agent/authored/f261-r4-delete-2.jsonl` at `40f449d1` are byte-identical to the reviewer's tables. THE STATE: at `bca20317` and again at `350fa353`, `.agent/plan.md` equals PLAN4 and `.agent/live_review.md` and `.agent/decisions.md` equal their `b8f019de` blobs followed by RECORD4 and DEC3. THE DELETIONS: at `36eb4573` and at `40f449d1` the `apps`, `tests`, `packages`, `scripts`, `docs` and `README.md` objects equal the reviewer's dry runs of table 1 and of tables 1 and 2, which had reproduced the research helper's trees `78d01e45` and `717b93f6` exactly; each commit's `--no-renames` path set is the dry run's plus its own carrier. In the reviewer's dry run a full suite under `-n auto` read 11 failed and 18243 passed against the helper's base control of 13 failed, every failure on both sides in `tests/ui_server` or `test_vitest_passes`, and a `do.plan` handler-table entry failed `TestDeletedCommands::test_no_deleted_id_is_left_in_the_dispatch_table` alone. THE REVIEWER'S RUN in the primary checkout at `350fa353` of `tests/test_command_catalog.py`, `tests/cli/test_scope_plan.py`, `tests/orchestration/test_stream_evidence_integration.py`, `tests/orchestration/test_f018_authority_integration.py`, `tests/orchestration/test_job_task_runner.py`, `tests/cli/test_advertised_commands.py`, `tests/cli/test_job_commands.py`, `tests/docs/`, `tests/ui_server/test_dashboard_contract.py` and `tests/cli/test_golden_path.py` read 924 passed. The open set reads 94 by distinct id at `350fa353`.

- R-0896 — Medium, PRINTED NEXT-STEP HINTS TELL THE USER TO RUN `remedy job show <id> --json`, WHICH EXITS 2 BECAUSE `job show` DECLARES NO `--json`. Raised by the planner and reviewer of session 36 while preparing F261 round 5, after searching the open set for the defect under §3 item 30: no open finding describes it. THE DEFECT, read at `350fa353`: `get_command("job.show").args` holds only `job_id`, and `main` in `apps/cli/grouped.py` prints "Unrecognized arguments" and exits 2 when parsing leaves unknown arguments; `git grep -n "job show .*--json"` over `apps`, `packages`, `scripts`, `docs/system` and `docs/guides` prints 20 lines, in `packages/orchestration/repair_loop.py`, `packages/orchestration/test_execution_service.py`, `packages/orchestration/run_contract.py`, `packages/orchestration/do_run.py`, `packages/orchestration/mission_readiness.py` and `docs/guides/do-run-v1.md`, most of them `next_safe_action` or recovery strings a user copies. `tests/cli/test_advertised_commands.py` resolves a hint's group and subcommand and not its flags, so it passes. WHY MEDIUM: the command a failure tells the user to run next fails too. WHY F261's: T002 builds `job show --full`, where the command's output forms are settled. FIX: T002 either gives `job show` the `--json` those hints name or rewrites every hint to a form the command accepts, and extends the advertised-commands test to reject a flag the named command does not declare. Owner: F261.

- R-0897 — Medium, ONCE `do promote` IS DELETED A RUN STARTED WITHOUT A JOB HAS NO COMMAND THAT APPLIES ITS REVIEWED CHANGES. Raised by the planner and reviewer of session 36 while preparing F261 round 5, after searching the open set under §3 item 30: no open finding describes it. THE DEFECT, read at `350fa353`: `_cmd_do` in `apps/cli/commands/do_cmd.py` sends a run with `--builder` or `--reviewer` to `_cmd_do_pingpong`, whose `run_pingpong` call passes no `job_id`; `do promote` applied such a run by its run id through `packages/orchestration/pingpong_promote.py`, and `job apply` takes a job id and applies only a completed job whose tasks each carry an applied manifest. DECISION F261 D4 deletes `do promote` because renaming it into `job apply` would change a surviving command. WHY MEDIUM: a user who runs `remedy do run --builder <provider>` gets a reviewed staged result and no CLI word that writes it to the target; the result branch and diff survive for a manual apply. WHY F268's: F268's `remedy do <order>` makes every run a job and gives `--apply` as `job apply --approve`, which is where a run without a job stops existing. FIX: every run F268's entry starts belongs to a job that `job apply` accepts, and a test applies a fake-provider run started from `remedy do`. Owner: F268.
END RECORD5

── SLICE DEC4 ── target `.agent/decisions.md` ── APPEND ──
BEGIN DEC4 sha256=504b47846121f9230e618423c52b36d391207cc692af358381614b01a59e80b2

## DECISION F261 D4 (2026-09-15, F261 round 5) — the deletion paragraph of `do promote` and of the run-level apply library only it used, and the order and evidence limits of the rest of T002

CONTEXT. DECISION amend0905-vocab D5 makes `apply` replace `promote`, naming `do promote` and `do job-promote` as becoming `job apply`, and DECISION F261 D1 put `do promote` into T002. `do job-promote` became `job apply` in round 2. `do promote` cannot follow it: `_cmd_do_promote` in `apps/cli/commands/do_cmd.py` takes a RUN id and calls `promote_run` in `packages/orchestration/pingpong_promote.py`, which checks the run's own staged snapshot, while `job apply` takes a JOB id and applies through `promote_job` in `packages/orchestration/job_promote.py` with job-level gates, and neither module imports the other. Renaming the one into the other would change what a surviving command does.

WHAT IS DELETED, measured at `350fa353` by the reviewer's research helper with an `ast` import check and `git grep`, and re-read by the reviewer in the dry-run trees of the round. In the first commit: the catalog entry `do.promote`, its handler-table entry and `_cmd_do_promote`; the `do promote` steps of `_QUICK_START` in `apps/cli/grouped.py`, the promote lines of `_print_text_report`, the promote keys and shell-flow steps of `_build_next_commands` in `packages/orchestration/pingpong_loop.py`, and the hint in `pingpong_promote.py`; `PingPongResult.original_repo_arg`, whose only reader was that hint; the tests that asserted them; and `do.promote` added to `TestDeletedCommands`. In the second commit: `packages/orchestration/pingpong_promote.py` whole, because every name in it was reachable only from `_cmd_do_promote` or fed a reader that dies with it, together with `tests/orchestration/test_pingpong_promote.py` and its reachability-allowlist line; the writer of the run's staged snapshot in `pingpong_loop.py`, whose only reader was `load_artifacts`; the readers of the run's `promotion.json` in `do report`, `export_evidence` and `job evidence`; and `build_evidence_bundle`'s promotion parameter with the bundle's `promotion.json`, its manifest section and the readiness keys `promotion_performed`, `promotion_status` and `promoted` only it filled.

THE HEIRS. Applying reviewed changes to a target belongs to `job apply`; its dry-run preview, approval barrier, post-apply test command and hash and path checks already exist in `job_promote.py`. The copy-paste apply hints and the apply step of a run started from `remedy do` belong to F268, whose `--apply` is `job apply --approve`. The run's `promotion.json`, its staged snapshot and their readers have no heir.

CHOSEN, FIRST: THE VALIDATORS ARE UNTOUCHED, AND SO ARE TWO EVIDENCE WORDS. `scripts/build_review_manifest.py`, `scripts/build_observability_index.py`, `packages/orchestration/final_verifier.py` and `packages/orchestration/commit_execution_gate.py` read none of what this round deletes. For the rest of T002, `promote_ready` in `commit_execution_gate.json` and the recommended-action strings of `final_verifier.py` keep the word `promote`: the manifest's closed schema reads the first from every existing package, and its reproducibility check regenerates the second and requires equality, so renaming either would fail every accepted package, which D5's own clause "where a rename does not break an accepted evidence chain" excludes.

CHOSEN, SECOND: THE ORDER OF T002. After this round: the module and test-file rename of `job_promote.py` to `job_apply.py`, its identifiers, and its output-visible words in separate commits under the insertion cap; then `job show --full`, which only adds keys to the JSON `job show` prints because the canary, `tests/cli/test_plan_approval.py` and `scripts/remedy_smoke.sh` parse it; then one commit per read command folded into it, `do job-report` among them; then the run-level promote words that remain. Which report variants `--full` carries, how a section that exits today reports inside it, and whether `job show` gains `--json` for R-0896 are ruled in the round that builds `--full`.

CONSEQUENCE. A bare `remedy do promote` becomes a `do run` goal, as D1's fifth ruling accepts, and `remedy do promote <run-id>` exits with an argument error; a run started without a job has no apply command, which R-0897 records for F268. `do run --json` loses its promote keys, `do report` its promotion lines, and evidence bundles their `promotion.json`; run directories already on disk keep files nothing reads. HOW TO REVERSE: restore the command and the module from the parent of the round's first deletion commit, and delete this section and the registrations it names.
END DEC4

── SLICE P268B-FROM ── target `docs/roadmap/features/T2_F268.md` ── FROM OF P268B ──
BEGIN P268B-FROM sha256=2dec9e87412e30fd7d88c71b2cf208da91f5c23898a6daf10bc071bd25472b69
- R-0892 carries a resolution line: a provider run through this feature's flow exports an
  evidence package that passes the required-artifact check of
  `scripts/build_review_manifest.py`, and a test builds one from a fake-provider run.
END P268B-FROM

── SLICE ACC268B ── target `docs/roadmap/features/T2_F268.md` ── TO OF P268B ──
BEGIN ACC268B sha256=4db01827a15a2478b6751ac1f98a498bd9ff62eaec13d02b07799cf9af3ebb27
- R-0892 carries a resolution line: a provider run through this feature's flow exports an
  evidence package that passes the required-artifact check of
  `scripts/build_review_manifest.py`, and a test builds one from a fake-provider run.
- R-0897 carries a resolution line: every run this feature's entry starts belongs to a job
  that `job apply` accepts, and a test applies a fake-provider run started from `remedy do`.
END ACC268B
