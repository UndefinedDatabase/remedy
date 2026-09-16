── STEP T003/7 — F261 — ROUND 19 ──
Goal: Book round 18's PASS and its prose slip, register R-0911 and R-0912 for F273, record
DECISION F261 D18, rename `do report` into the new `run` group and delete `do evidence`, in two
commits by applying two tables; run the suite once.

Base commit: `ac87bcc4`, on `feature/f261-cli-vocabulary-v2`. SESSION 4 of F261. Read AGENTS.md,
docs/agents/self_drive_protocol.md, `.agent/f261_t003_inventory.md`, and DECISION F261 D18 once
C1 has landed it.

THE FRAME RULE, per item 37 of §3, measured over the final bytes: NO LINE of this block that is two or
more characters long is a run of a single repeated character, and every box-drawing rule inside the STEP and SLICE header
lines is exactly two characters long.

ENVIRONMENT: `VAR=x cmd`, `env` and `export` are denied, so set environment in-process; `cp` is
denied, so copy with `shutil.copyfile`; bare `ruff` is denied, so use `python3 -m ruff check`.
Shell loops, `$(...)` and `$?` in a compound command are refused by form, so write such checks
as Python scripts under `.remedy-wt/f261r19w/`, and never name a script after a standard-library
module; a pipe into `tail` hides pytest's exit code. The editable install resolves `apps` and
`packages` to the PRIMARY checkout, so a pytest run inside a worktree goes through a runner
script that changes into the worktree, puts it first on `sys.path` and in `PYTHONPATH`, and
asserts `apps.cli.grouped` loaded from inside it. Never call `run_job` or a runner yourself: a
job run started from inside a checkout creates a `remedy/job-*` branch in it.
`git branch --list 'remedy/job-*'` reads 16 lines now; keep it so. While a deletion is staged
but not committed, `test_every_enumerated_path_exists_in_this_repo` fails; run no suite then.

## Bundle — the ordered commit sequence

C0a `.agent/authored/f261-r19.md`, the block file the delegating message names, by
    `shutil.copyfile`
C0b `.agent/last_block.md`, the same bytes
C1  THE RECORD, one commit: `.agent/plan.md` becomes slice PLAN19; slice RECORD19 is appended to
    `.agent/live_review.md`, slice DEC18 to `.agent/decisions.md` and slice SLIP19 to
    `.agent/prose_slips.md`; in `docs/roadmap/features/T2_F273.md` the bytes of slice P273-FROM
    are replaced by those of slice P273-TO
C2  THE RUN GROUP: copy `.remedy-wt/f261-block/f261-r19-run.jsonl` to
    `.agent/authored/f261-r19-run.jsonl` and apply it per THE TABLES, in one commit
C3  `do evidence`: the same with `f261-r19-evidence.jsonl`, in one commit
C4  `.agent/handoff.md`, the handback; then `git push origin feature/f261-cli-vocabulary-v2`

C1 is the FIRST SUBSTANTIVE COMMIT, per item 23 of §3. No pull request is created.

## Change — exactly these paths and no others

C0a to C1: `.agent/authored/f261-r19.md`, `.agent/last_block.md`, `.agent/plan.md`,
`.agent/live_review.md`, `.agent/decisions.md`, `.agent/prose_slips.md` and
`docs/roadmap/features/T2_F273.md`. C2 and C3: each table's own carrier and the paths G3 names.
C4: `.agent/handoff.md`.

## The appends and the pair

RECORD19, DEC18 and SLIP19 each begin with an empty line, and their targets end in a
newline at `ac87bcc4`: an append is the file's bytes followed by the slice's bytes, and nothing
else. The pair P273: TO contains FROM: false, so it is a REWRITE; P273-FROM occurs once
in `docs/roadmap/features/T2_F273.md` at `ac87bcc4`, and at C1 P273-FROM occurs 0 times and
P273-TO once.

## THE TABLES

Each carrier holds one JSON array per line. Their sha256 digests, to verify before copying:
`f261-r19-run.jsonl` `0e6d26ecb22e8429982cacbf26409d1152be18f3437e08e2c5b9c53914368cd2` and
`f261-r19-evidence.jsonl` `af19a5585abbe883e6a683756967d76cd427db08475ab860fd5362477cc2e68f`.
Apply the rows strictly
in file order, each against the tree as the previous rows left it, from the repository root:
`["edit", path, old, new, count]` opens the path with `encoding="utf-8", newline=""`, requires
the number of occurrences of `old` to equal `count` exactly, and replaces every occurrence with
`new`; `["delete", path]` removes the file; `["move", src, dst]` renames the file, whose target
must not exist; `["create", path, content]` writes `content` to a path that must not exist, with
the same encoding and newline setting. A count that differs or a target that exists is a STOP:
touch nothing further, commit nothing of that table, and hand back with the row and the reading.
Stage each commit with `git add -A` after its table and its carrier. The tables are the
reviewer's measured dry run of DECISION F261 D18, applied on top of C1's record: the run table
its CHOSEN FIRST and the evidence table its CHOSEN SECOND.

## SPEC S — the suite, once, after G5 and before C4

From the primary checkout's root, serially:
`python3 -B -m pytest -q -p no:randomly -p no:cacheprovider --tb=short -rfEs`, with `PYTHONPATH`,
`REMEDY_PROJECT` and `REMEDY_DATA_DIR` removed and `PYTHONDONTWRITEBYTECODE=1`, output under
`.remedy-wt/f261r19w/`. Report pytest's return code, the run's last output line, and every
distinct bad node, the text after a line-initial `FAILED ` or `ERROR ` up to the first ` - `.
Re-run each bad node alone, once, the same way, and report that return code beside it.

## Constraints

1. NO SLICE AND NO TABLE IS EDITED. Extract each slice as the bytes strictly between its
   `BEGIN <NAME>` and `END <NAME>` lines and verify its sha256 before use.
2. READ `.agent/STOP` before C0a, before C2 and before C4, with real exit codes. If it exists:
   finish a half-written commit, write the handoff, push, stop.
3. A red gate is a STOP: commit what is honestly finished, hand back with the raw output.
4. Scratch, runner scripts and your worktree live under `.remedy-wt/f261r19w/`, uncommitted; no
   `.py` file under `.agent/`. Under `.remedy-wt/` open only `.remedy-wt/f261-block/` and your
   own directory. `git worktree list` reads one row now; leave it so. Create no symlink.
5. Every commit stays under 500 insertions, read as the first column of `git show --numstat
   --format= <commit>` with git's default rename detection.
6. NEVER merge, open a pull request, force-push, rewrite history or delete a branch. No `remedy`.
   Write no `Done:` paragraph and no `Landed:` line.
7. THE BLOCK'S OWN SIZE, measured on its final bytes: 396 lines TOTAL and 262 lines of PROSE,
   against the caps of 490 and 400, where PROSE is every line that is not a line of slice CONTENT — the
   `BEGIN` and `END` marker lines count as prose.
8. GATE ORDER. G1 and G2 after C1; G3, G4 and G5 after C3; then SPEC S, whose result is G6; G7
   after C4 and the push, reported in the completion message only.
9. Every commit message ends with `Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>`, and
   no subject carries a leading-slash token or an absolute path.

## Done when — every gate run for real, its exit code recorded

G1 TRANSPORT. The sha256 of `.agent/authored/f261-r19.md` at C0a equals the digest the delegating
message gives, and `.agent/last_block.md` at C0b is byte-identical to it; the slices FOUND, each
matching its BEGIN-marker sha256; each committed carrier's sha256 equals its digest above.

G2 THE RECORD, at C1. `.agent/plan.md` is byte-identical to PLAN19, at most 50 lines, with
`^## Goal$` once and `^## Next Steps$` once. `.agent/live_review.md` equals its `ac87bcc4` blob
followed by RECORD19, `.agent/decisions.md` its `ac87bcc4` blob followed by DEC18, and
`.agent/prose_slips.md` its `ac87bcc4` blob followed by SLIP19.
`docs/roadmap/features/T2_F273.md` equals its `ac87bcc4` blob with the pair P273 applied, with
the counts The appends and the pair give. Over `.agent/live_review.md`: `^Gate: F\d+ R\d+ — `
reads 127 at `ac87bcc4` and 128 at C1, with `Gate: F261 R18 — ` once at C1; distinct
`^- R-\d+ — ` ids 113 and 115, C1 minus base exactly `R-0911` and `R-0912`; distinct `^Done: R-\d+ — ` ids 8
and 8; the open set by distinct id 105 and 107. `python3 -m pytest tests/docs/ -q` exits 0 at C1.

G3 THE TABLES, at C2 and C3. `git diff --no-renames --name-only` from each commit's parent
prints exactly that commit's carrier and: at C2 `README.md`, `apps/cli/command_catalog.py`, `apps/cli/commands/do_cmd.py`, `apps/cli/grouped.py`, `packages/orchestration/pingpong_loop.py`, `tests/cli/test_cli_ux.py`, `tests/cli/test_product_spine.py`, `tests/cli/test_task_input.py`, `tests/orchestration/test_pingpong_cli.py`, `tests/test_cli_execution_loop_closure.py` and `tests/test_command_catalog.py`; at C3 `apps/cli/command_catalog.py`, `apps/cli/commands/do_cmd.py`, `tests/orchestration/test_evidence_bundle.py` and `tests/test_command_catalog.py`.
`git rev-parse <commit>:<object>` equals the reviewer's dry run, which applied C1's
record before the tables, for `apps`, `tests`, `docs`, `scripts`, `packages` and `README.md` in
that order: C2 `5b305ea84eb80e8857976cdabb638a9d99167526`, `aec267237992e3a9a02f1d1de0f6003d609b2796`, `07f12816d94a6f09495945fd43380a8735a46b55`, `208d836b3d5d6532fe9354d9455ab71c67639ed2`, `6bf22116f83610bc347af00a8aa86d8210526a9c`, `666769d2b1a77cdb2ccdffc841f84f64d3eabdf8`; C3 `e3cf5879f00c5fff5632d3e873572c5d053ba4e7`, `d51c09d12ebbab33ac525b9fde9bad21c8077910`, `07f12816d94a6f09495945fd43380a8735a46b55`, `208d836b3d5d6532fe9354d9455ab71c67639ed2`, `6bf22116f83610bc347af00a8aa86d8210526a9c`, `666769d2b1a77cdb2ccdffc841f84f64d3eabdf8`.
Report each commit's insertions per constraint 5.

G4 THE SWEEP, at C3. `git grep -n -I -E 'remedy do report|_cmd_do_report|_cmd_do_evidence'
<C3> -- apps packages scripts tests docs README.md AGENTS.md .claude ':!docs/roadmap'` exits 1
and prints nothing; at `ac87bcc4` the same command exits 0 and names 7 files.
`python3 -m ruff check` over every `.py` path of C2 and C3 that still exists at C3 exits 0.

G5 THE RED-PROOF, in `git worktree add --detach .remedy-wt/f261r19w/wt <C3's sha>`, each run
through the runner over `tests/test_command_catalog.py`, `tests/cli/test_cli_ux.py`,
`tests/test_grouped_cli.py`, `tests/orchestration/test_import_reachability.py` and
`tests/cli/test_advertised_commands.py` with `-rf --tb=no`. Mutation <n> is in the file its line
below names, replaces the bytes of slice MUT-<n>-FROM, whose count there must read 1, with those
of slice MUT-<n>-TO, and is restored with `git -C .remedy-wt/f261r19w/wt checkout -- <that
file>`. (a) CONTROL: must exit 0. Each of (1) to (8) must exit 1 with the named node among the
failed nodes:
(1) `apps/cli/command_catalog.py`, the `run` group removed:
`TestGroupDefIntegrity::test_all_groups_still_in_catalog`; (2) the same file, `run.show` removed
while its handler row stays: `TestGroupDefIntegrity::test_run_group_holds_exactly_show_and_list`;
(3) `apps/cli/commands/do_cmd.py`, `run.show`'s handler row removed while its catalog entry
stays: `TestGroupDefIntegrity::test_run_commands_have_handlers`; (4)
`packages/orchestration/pingpong_loop.py`, the old `do report` hint restored:
`test_every_advertised_command_exists_in_the_catalog`; (5) `apps/cli/command_catalog.py`,
`do.report` put back: `TestRenamedCommands::test_no_old_id_is_left_in_the_catalog`; (6) the same
file, `do.evidence` put back: `TestDeletedCommands::test_no_deleted_id_is_left_in_the_catalog`;
(7) `apps/cli/commands/do_cmd.py`, `run list --json` printing other bytes:
`TestRunList::test_no_flag_prints_list_runs_verbatim`; (8) the same file, `run list` dropping the
`--limit` the catalog attached: `TestRunList::test_limit_flag_is_honoured`.
Report each exit code, summary line and number of failed nodes; then
`git worktree remove --force .remedy-wt/f261r19w/wt` and read `git branch --list 'remedy/job-*'`.

G6 THE SUITE, SPEC S at C3: must exit 0 with no bad node; report the last output line. A bad
node whose lone re-run exits 0 is reported as such with both readings, and is not a STOP; a bad
node whose lone re-run fails is.

G7 THE TREE, after C4 and the push. `git status --porcelain` prints `''`; C0a to C4 are
single-parent commits in that order on `ac87bcc4`; `git rev-parse HEAD` equals
`git rev-parse origin/feature/f261-cli-vocabulary-v2`; `git worktree list` prints one row, and
`git branch --list 'remedy/job-*'` prints 16 lines.

## The handback, C4

`.agent/handoff.md` per `docs/agents/handback_template.md`, Session line
`SESSION 4 of feature F261 · round 19 · rounds so far 19`, with one sentence of context
self-assessment. `## Commits` lists C0a to C3, each row's `+/-` cell equal to constraint 5's
reading of that commit and its deletions column; C4's own numbers appear nowhere, per item 31 of
§3. `## Verification` gives G1 to G6 with real exit codes. It states the open findings at 107 by
distinct id, with the High ids R-0803, R-0804 and R-0807, and `Operator questions open: 0`. Its
`## Next` names, in order: Phase 1 rule 1; the reviewer's verdict on round 19; `do
repair-attest`, `do job-resume` and `do replan`, as the inventory proposes.

── SLICE PLAN19 ── target `.agent/plan.md` ── FULL REPLACEMENT ──
BEGIN PLAN19 sha256=40498c55e959f0b03f6393297305b24425799cfe2fd002567f3d9654bd7b460b
# Plan — F261 CLI vocabulary v2 (rename & prune)

Branch: feature/f261-cli-vocabulary-v2, cut from `main` at
`7cdde89b5d0dc8ef1fb96980105870e956699873`, the merge commit of pull request 250.

## Goal

The catalog `apps/cli/command_catalog.py` equals DECISION amend0905-vocab D4: one name per
command, and every retired word deleted rather than aliased, per
`docs/roadmap/features/T2_F261.md`.

## Current Step

ROUND 19 continues T003. It books round 18's PASS and a prose slip, registers R-0911 and R-0912
for F273 and records DECISION F261 D18, then renames `do report` into the new `run` group as
`run show <id>` and `run list`, and deletes `do evidence`, one table per commit.

## Next Steps

1. `do repair-attest`, `do job-resume` and `do replan`, as `.agent/f261_t003_inventory.md`
   proposes, then the `do continue` hints with the command and `do_continue.py`, with R-0900.
2. The rest of T003 in the inventory's order, each round re-measured before it is authored,
   with R-0767 and R-0894.
3. `job budget <id> set` over the run-contract budget fields and the token budget profile, the
   word DECISION amend0905-vocab D4 gives those writes, with R-0906 and R-0909.
4. T004, which owes the visible group order of D4 and the README quickstart of R-0895.

## Risks

- 105 findings are open by distinct id before this round's record and 107 after it; three are
  High, R-0803, R-0804 and R-0807.
- The inventory proposes more rounds than F261's soft limit of 25 leaves; the session that
  reaches the limit owes the scope report and the split-and-close default.
- A rename keeps a payload only if every consumer is measured first, and a deletion's consumers
  include shell strings a guard cannot read, so every round of T003 runs the whole suite on its
  committed tree.
END PLAN19

── SLICE RECORD19 ── target `.agent/live_review.md` ── APPEND ──
BEGIN RECORD19 sha256=0411de7b5f63f1e79cbe1a276081fea5433fa664191faa6b0e1dfc071e4eda28

Gate: F261 R18 — the F261 round 18 entry. VERDICT PASS. Written by the planner and reviewer of session 39 after reading the committed range `43694261`..`ac87bcc4` and re-deriving the readings below; the worker's report was evidence for none of them. It is booked here by the first commit of round 19 that writes the record, per operator amendment amend0827-process-diet rule 1. THE TRANSPORT: `.agent/authored/f261-r18.md` at `46a0857c` and `.agent/last_block.md` at `f83cb299` are byte-identical to the reviewer's scratch original, sha256 `9258ed4be5ca4f83ecd64f6ff4f94bd4ba0460045c765dabda92ce85415554ad`, and the three tables committed at `0a3f4dcf`, `4ea59820` and `72a57e38` are byte-identical to the reviewer's, the first two the research helper's and the third the helper's with the two rows the reviewer added. THE STATE: at `9d28c213` and again at `ac87bcc4`, `.agent/plan.md` equals PLAN18, `.agent/live_review.md`, `.agent/decisions.md` and `.agent/prose_slips.md` equal their `43694261` blobs followed by RECORD18, DEC17 and SLIP18, and `docs/roadmap/features/T2_F273.md` equals its `43694261` blob with the pair P273 applied. THE TABLE COMMITS: at `0a3f4dcf`, `4ea59820` and `72a57e38` the `apps`, `tests`, `docs`, `scripts`, `packages`, `README.md` and `.claude` objects equal the reviewer's dry-run commits, which applied the record before the tables and, apart from the two smoke-script lines the reviewer's own rows rewrite, reproduced the helper's trees exactly; each commit's `--no-renames` path set is the dry run's plus its carrier, and `git show --numstat` reads 63, 47 and 46 insertions. In the dry run's production diff each group leaves with its handler module, its catalog entries and its tests, no package module and no package symbol is deleted, `context_inspector.py`, `token_economy.py` and `reviewer.py` keep every production caller that reads them, and every surviving hint that named a deleted command is re-pointed or dropped. The sweep pattern of the round 18 block matches in 25 files at `43694261`, and at `ac87bcc4` the same `git grep` over `apps`, `packages`, `scripts`, `tests`, `docs` without `docs/roadmap`, `README.md`, `AGENTS.md` and `.claude` exits 1 with no output. THE SMOKE SCRIPT: at `43694261` five words of the `for grp in` list of section 0, `policy`, `readiness`, `repo`, `dashboard` and `guide`, were no longer keys of `GROUPS`, so the section would have exited 1 on the first of them; at `ac87bcc4` the list reads fifteen words and every one is a group of the catalog, and `bash -n scripts/remedy_smoke.sh` exits 0. In the reviewer's dry run a full suite under `-n auto` without `tests/ui_server` read 1 failed, `test_vitest_passes`, 17269 passed and 29 skipped, and ten `tests/ui_server` files naming a deleted word read 388 passed. Over `tests/test_command_catalog.py`, `tests/cli/test_cli_ux.py`, `tests/test_grouped_cli.py`, `tests/orchestration/test_import_reachability.py`, `tests/cli/test_advertised_commands.py` and `tests/test_remedy_smoke_script.py`, which passed 537 unmutated, a `context`, a `token` and a `review` handler row each failed 1 test, the `token` group restored without commands failed 1, a `related=` naming `review.list` failed 1, a `review list` command in the view model failed 1, and `token` and `context-pack` named internal groups again failed 3; the probe that put `policy` back into the smoke script's group list passed 537, which is the reading R-0910 registers. THE REVIEWER'S RUN in the primary checkout at `ac87bcc4` of those six files, every other test file the round edited, `tests/ui_contracts/`, `tests/orchestration/test_test_runner.py`, `tests/cli/test_golden_path.py`, `tests/docs/`, `tests/orchestration/test_command_discovery.py` and four `tests/ui_server` files read 2325 passed and 4 skipped, `python3 -m ruff check` over sixteen edited files that survive printed `All checks passed!`, and `git branch --list 'remedy/job-*'` read 16 lines. The open set reads 105 by distinct id at `ac87bcc4`.

- R-0911 — Medium, DELETING `do evidence` LEAVES NO COMMAND THAT EXPORTS THE EVIDENCE OF A PING-PONG RUN, AND `job evidence`, THE NEAREST SURVIVING WORD, READS A DIFFERENT RECORD UNDER A DIFFERENT ID. Raised by the planner and reviewer of session 39 while preparing F261 round 19, after searching the open set for the evidence bundle and these commands under §3 item 30: R-0892 describes the root artifacts a provider-run package needs and names no run-scope export, and no other open finding describes this. THE DEFECT, read at `ac87bcc4` and on the reviewer's dry-run trees: `_cmd_do_evidence` in `apps/cli/commands/do_cmd.py` called `export_evidence` in `packages/orchestration/pingpong_evidence.py` and wrote ten files for a run id, while `job evidence` writes thirty-five files for a job id; the helper measured each command against the other's id and both exit 1 with `not found`, so the two read disjoint namespaces and the second is no heir of the first. DECISION amend0905-vocab D4 gives the `run` group `show` and `list` and no evidence word, so after this round no command exports a run's evidence, and `export_evidence` keeps callers under `tests/` alone, where eight classes drive the surviving `build_evidence_bundle`, `write_evidence_bundle` and `_redact_json_value` through it. WHY MEDIUM: a user-observable export leaves with no heir, and a public function with a redaction contract stays behind its own tests; nothing prints anything false. WHY F273's: adding `run evidence` would add a word D4 does not name, and deleting `export_evidence` means re-pointing the redaction coverage of code that survives — both are outside a prune. FIX: either re-point the eight test classes at `build_evidence_bundle` and `write_evidence_bundle` and delete `export_evidence` with `_cmd_do_evidence`'s last trace, or record a DECISION that a run's evidence is exported again under a named word and build it. Owner: F273.

- R-0912 — Low, `job evidence` ENDS IN AN UNCAUGHT TRACEBACK FOR A JOB WHOSE TASK CARRIES THE TASK-ID DEFAULT ITS OWN DATACLASS MINTS. Raised by the planner and reviewer of session 39 from a reading the round 19 research helper took while probing a neighbouring command, after searching the open set for the evidence bundle and the task id under §3 item 30: no open finding describes it. THE DEFECT, read at `ac87bcc4`: `_task_evidence_dir` in `packages/orchestration/job_evidence.py` requires a task id of the shape `T` followed by digits, while the `task_id` default of the `TaskEntry` dataclass is `mint_task_id()`, a sixteen-character hexadecimal string, so a job built through the dataclass default and exported with `remedy job evidence <id>` raises `ValueError` out of the handler and the user sees a traceback and exit 1 rather than a handled error. The planner path assigns `T001` in `packages/orchestration/pingpong_job.py`, so a job made by the product's own flow is unaffected, which is why no test covers it. WHY LOW: no supported flow reaches it and nothing is written; what is wrong is the failure mode and the disagreement between a default and a guard. WHY F273's: it is neither a catalog word nor a prune; F261 renames and deletes commands. FIX: make the two agree — either mint a `T<n>` id in the dataclass default or widen the guard — and where the guard still refuses, exit with a message naming the task id instead of raising, with a test that exports a job whose task carries the minted default. Owner: F273.
END RECORD19

── SLICE DEC18 ── target `.agent/decisions.md` ── APPEND ──
BEGIN DEC18 sha256=f10f32b8096e147bc0fb18933940b86d6e63ea14d5a96de568355703b9727b2a

## DECISION F261 D18 (2026-09-16, F261 round 19) — `do report` becomes the `run` group, and `do evidence` is deleted

CONTEXT. DECISION amend0905-vocab D4 gives the surviving tree a `run` group of `show <id>` and `list`, and `.agent/f261_t003_inventory.md` finding 1 reads `do report <run_id>` and `do report list` as those two words under an older name. Measured at `ac87bcc4` by the reviewer's research helper, which ran both commands in process against a scratch data root over one persisted ping-pong run, and re-read by the reviewer on the dry-run trees.

CHOSEN, FIRST: the rename. `do.report` becomes `run.show` and its `list` sentinel becomes `run.list`, a second entry of a new `run` group placed directly after `job`, the slot D4's visible order gives it; `_cmd_do_report` becomes `_cmd_run_show` and `_cmd_run_list` in `apps/cli/commands/do_cmd.py`, which keeps dozens of other handlers, so nothing moves module as `apps/cli/commands/plan_cmd.py` did under DECISION F261 D12. Every payload is unchanged: the helper compared the two commands' stdout, stderr and exit code over the same run in five invocations, 570759 stdout bytes in all, and each pair is byte-identical. Every hint that named the old word — the `report` and `report_json` keys and the shell flow of `_build_next_commands`, the `report_command` and `report_json_command` keys of the `do run --json` payload, the `Report:` line of `summarize_pingpong`, the quick start of `apps/cli/grouped.py` and the README quickstart — names the new one; the keys themselves are untouched. THE ONE DECLARED DIFFERENCE: `run.list`'s subcommand is `list`, so the catalog's own `_with_list_options` attaches `--sort`, `--desc`, `--since`, `--until` and `--limit`, which `do report list` did not take. They are implemented rather than decorative: `_cmd_run_list` passes them to `apply_list_options` with `default_sort_field=None`, the mode that leaves row order alone, so a call with no flag prints exactly what `do report list` printed, and a decorative flag that silently did nothing would be the worse of the two.

CHOSEN, SECOND: `do evidence` is deleted with its handler and its dispatch tests. `job evidence`, which D4 keeps, is not its heir: measured on the base tree, each command exits 1 on the other's id, `do evidence` writes ten files for a run and `job evidence` thirty-five for a job. `export_evidence` in `packages/orchestration/pingpong_evidence.py` stays, because eight test classes drive the surviving bundle builder and the redaction helper through it; R-0911 records both the lost export and that function's state for F273.

CONSEQUENCE. `remedy do report` and `remedy do evidence` are unknown words, their ids join the renamed and the deleted ledgers of `tests/test_command_catalog.py`, and `remedy run show <id>` and `remedy run list` carry the reports. The `run` group holds exactly what D4 names it; the visible ORDER of `GROUPS` is still not D4's, which T004 owes. `test_all_groups_still_in_catalog` gains `run`, and because that guard only asserts that a kept group has not left the catalog, the round also pins the new group with a test of its own. HOW TO REVERSE: revert the round's two table commits and delete this section.
END DEC18

── SLICE SLIP19 ── target `.agent/prose_slips.md` ── APPEND ──
BEGIN SLIP19 sha256=4c689ae4e005162d90274f1b7bafc1c63b711192b5fd290eada45d57c4748750

2026-09-16 · F261 R18 · CONSTRAINT 7 of the round 18 block stated the block's PROSE at 271 lines without saying whether a slice's `BEGIN` and `END` marker lines count as prose; the reviewer's own measurement counts them, the worker measured 227 without them, and the worker declared the difference rather than reading either number as violated. THE RULE THAT FOLLOWS: a size clause names what it counts — here, that PROSE is every line of the block that is not a line of slice content, markers included.
END SLIP19

── SLICE P273-FROM ── target `docs/roadmap/features/T2_F273.md` ── REWRITE FROM ──
BEGIN P273-FROM sha256=8867c58278a089c6e97a17ee77aa28a49bdd9a27a1bccb8f3169e3f89724652f
  `scripts/remedy_smoke.sh` and asserts every word is a group of the catalog.

## Do not touch
END P273-FROM

── SLICE P273-TO ── target `docs/roadmap/features/T2_F273.md` ── REWRITE TO ──
BEGIN P273-TO sha256=c0bd2c9e88edf21fbe59b0efef0991fafb28c2f1fa22e4e1308a1a6baeb73cf6
  `scripts/remedy_smoke.sh` and asserts every word is a group of the catalog.
- R-0911 carries a resolution line naming the commit that deleted `export_evidence` with the coverage its
  eight test classes moved to, or the DECISION and the commit that gave a run's evidence export a word again.
- R-0912 carries a resolution line naming the commit that made the minted task-id default and the evidence
  directory guard agree, with the test that exports a job whose task carries the minted default.

## Do not touch
END P273-TO

── SLICE MUT-1-FROM ── G5 (1) only ── never a file ──
BEGIN MUT-1-FROM sha256=38c1f5b87ab9a10518f0ad5ff8f742e1323edc3846708c6f3a47bdfbcf41d3df
    "run": GroupDef("run", "Run", "Show and list persisted ping-pong runs."),
END MUT-1-FROM

── SLICE MUT-1-TO ── G5 (1) only ── never a file ──
BEGIN MUT-1-TO sha256=05714f2939c96f29d7f16cde8c8295e0e1ad948e32e42844976e9fc86aeb7a2c
    # the run group was here
END MUT-1-TO

── SLICE MUT-2-FROM ── G5 (2) only ── never a file ──
BEGIN MUT-2-FROM sha256=6a7b6ebef34a64f516a83bbaa2f6ecc931e43d6e50a6f07eedfc036f92a7d5b5
    CommandEntry(
        command_id="run.show",
        group_id="run",
        subcommand="show",
        description="Show a persisted ping-pong run report.",
        action_class="read_only",
        supports_json=True,
        related=("do.run",),
        args=(
            ArgDef("run_id", "Run ID"),
            ArgDef("--repo", "Path to target repository", required=False, is_option=True, default="."),
            _JSON_OPT,
        ),
        may_mutate_repo=False,
        may_execute_commands=False,
    ),
END MUT-2-FROM

── SLICE MUT-2-TO ── G5 (2) only ── never a file ──
BEGIN MUT-2-TO sha256=c03474ab09bcf90ce01ad97c9763b16531c7883cbcb9e22dd717f023e2c1d793
    # the run.show entry was here
END MUT-2-TO

── SLICE MUT-3-FROM ── G5 (3) only ── never a file ──
BEGIN MUT-3-FROM sha256=ac5d9ca602dc0f3322f9302d520e2a3b891bd134f2e078513ec8f95aff74458d
    "run.show": lambda args: _cmd_run_show(
        args.run_id,
        json_output=getattr(args, "json", False),
    ),
END MUT-3-FROM

── SLICE MUT-3-TO ── G5 (3) only ── never a file ──
BEGIN MUT-3-TO sha256=6a8b6a00bc42e1c5d20c6f98e3fef161debf48631d471e2a936f63ebb3f1ef2e
    # the run.show dispatch row was here
END MUT-3-TO

── SLICE MUT-4-FROM ── G5 (4) only ── never a file ──
BEGIN MUT-4-FROM sha256=685bb1388c5d7f02f7e3918e8c741b4a25989b7a10185ad46917e725cb9b9bbb
        "report_command": f"remedy run show {result.run_id}",
END MUT-4-FROM

── SLICE MUT-4-TO ── G5 (4) only ── never a file ──
BEGIN MUT-4-TO sha256=3b768e6b7e4f77f368c14267b81ba2004afe42464ea1059b0e3362ab824efe52
        "report_command": f"remedy do report {result.run_id}",
END MUT-4-TO

── SLICE MUT-5-FROM ── G5 (5) only ── never a file ──
BEGIN MUT-5-FROM sha256=98ff25a3376cfd75478666bdb91fbd47aebcee00c8fa0ba15045b56f43ab844a
    CommandEntry(
        command_id="run.show",
END MUT-5-FROM

── SLICE MUT-5-TO ── G5 (5) only ── never a file ──
BEGIN MUT-5-TO sha256=9d13e1a89b2cd9b35acdf2b6c802dc83ea43c0ce623bae42e4c18a2391381a81
    CommandEntry(
        command_id="do.report",
        group_id="do",
        subcommand="report",
        description="Show a persisted ping-pong run report.",
        action_class="read_only",
        supports_json=True,
        related=("do.run",),
        args=(
            ArgDef("run_id", "Run ID"),
            _JSON_OPT,
        ),
        may_mutate_repo=False,
        may_execute_commands=False,
    ),

    CommandEntry(
        command_id="run.show",
END MUT-5-TO

── SLICE MUT-6-FROM ── G5 (6) only ── never a file ──
BEGIN MUT-6-FROM sha256=98ff25a3376cfd75478666bdb91fbd47aebcee00c8fa0ba15045b56f43ab844a
    CommandEntry(
        command_id="run.show",
END MUT-6-FROM

── SLICE MUT-6-TO ── G5 (6) only ── never a file ──
BEGIN MUT-6-TO sha256=d440a6e50844eb8162db7f87d7042f8e9c90e884aae4cd840180095493e897a5
    CommandEntry(
        command_id="do.evidence",
        group_id="do",
        subcommand="evidence",
        description="Show a persisted ping-pong run report.",
        action_class="read_only",
        supports_json=True,
        related=("do.run",),
        args=(
            ArgDef("run_id", "Run ID"),
            _JSON_OPT,
        ),
        may_mutate_repo=False,
        may_execute_commands=False,
    ),

    CommandEntry(
        command_id="run.show",
END MUT-6-TO

── SLICE MUT-7-FROM ── G5 (7) only ── never a file ──
BEGIN MUT-7-FROM sha256=c819e12f260553ff3e5a3b3b0633f4f92e7583ba7fb4a1ab81d6ca810721051e
        print(json.dumps(runs, indent=2))
END MUT-7-FROM

── SLICE MUT-7-TO ── G5 (7) only ── never a file ──
BEGIN MUT-7-TO sha256=7280024b26e797d13b0affb5b2c0568c1ad401eb2b6b5f4db4a10f0b3722cca2
        print(json.dumps(runs, indent=4))
END MUT-7-TO

── SLICE MUT-8-FROM ── G5 (8) only ── never a file ──
BEGIN MUT-8-FROM sha256=b22b82e623b3413bee7862b3b0848b2a391c840b4e4a627aa8b011740895e687
            sort=sort, desc=desc, since=since, until=until, limit=limit,
END MUT-8-FROM

── SLICE MUT-8-TO ── G5 (8) only ── never a file ──
BEGIN MUT-8-TO sha256=55bb03656eb32355f196bd7d8522a7add6783b10dac62f326ca19016d13e6ed8
            sort=sort, desc=desc, since=since, until=until, limit=None,
END MUT-8-TO
