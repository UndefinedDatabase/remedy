── STEP T001/4 — F261 — ROUND 4 ──
Goal: Book round 3's PASS, register R-0894 and R-0895, record DECISION F261 D3, and delete
`do job-plan` and `do plan` in two commits by applying two tables; run the full suite once.

Base commit: `b8f019de`, on `feature/f261-cli-vocabulary-v2`. SESSION 1 of F261. Read AGENTS.md,
docs/agents/self_drive_protocol.md, and DECISIONs F261 D1 to D3 once C1 has landed D3.

THE FRAME RULE, per item 37 of §3, measured over the final bytes: NO LINE of this block is a run
of a single repeated character, and every box-drawing rule inside the STEP and SLICE header
lines is exactly two characters long.

ENVIRONMENT: `VAR=x cmd`, `env` and `export` are denied, so set environment in-process; `cp` is
denied, so copy with `shutil.copyfile`; bare `ruff` is denied, so use `python3 -m ruff check`.
Shell loops, `$(...)` and `$?` in a compound command are refused by form, so write such checks
as Python scripts under `.remedy-wt/f261r4w/`; a pipe into `tail` hides pytest's exit code. The
editable install resolves `apps` and `packages` to the PRIMARY checkout, so a pytest run inside a
worktree goes through a runner script that changes into the worktree, puts it first on
`sys.path` and in `PYTHONPATH`, and asserts `apps.cli.command_catalog` loaded from inside it.

## Bundle — the ordered commit sequence

C0a `.agent/authored/f261-r4.md`, the block file the delegating message names, by
    `shutil.copyfile`
C0b `.agent/last_block.md`, the same bytes
C1  THE RECORD, one commit: `.agent/plan.md` becomes slice PLAN4; slice RECORD4 is appended to
    `.agent/live_review.md` and slice DEC3 to `.agent/decisions.md`
C2  DELETION 1: copy `.remedy-wt/f261-block/f261-r4-delete-1.jsonl` to
    `.agent/authored/f261-r4-delete-1.jsonl` and apply it per THE TABLES, in one commit
C3  DELETION 2: the same with `f261-r4-delete-2.jsonl`, in one commit
C4  `.agent/handoff.md`, the handback; then `git push origin feature/f261-cli-vocabulary-v2`

C1 is the FIRST SUBSTANTIVE COMMIT, per item 23 of §3. No pull request is created.

## Change — exactly these paths and no others

C0a to C1: `.agent/authored/f261-r4.md`, `.agent/last_block.md`, `.agent/plan.md`,
`.agent/live_review.md` and `.agent/decisions.md`. C2 and C3: each table's own carrier and the paths G3 and G4
name. C4: `.agent/handoff.md`.

## The appends

RECORD4 and DEC3 each begin with an empty line, and both targets end in a newline at
`b8f019de`: an append is the file's bytes followed by the slice's bytes, and nothing else.

## THE TABLES

Each carrier holds one JSON array per line. The sha256 of `f261-r4-delete-1.jsonl` is
`432429e655ca22fd98173e095ecf7aec861570ecd2206413a5ef54b60693d13c` and that of `f261-r4-delete-2.jsonl` is
`1f7856e91a7087e8fdc77a1ce2e894a6ba3d3aa7092578792c71c95f95f730af`; verify each before copying. Apply the rows strictly
in file order, each against the tree as the previous rows left it, from the repository root:
`["edit", path, old, new, count]` opens the path with `encoding="utf-8", newline=""`, requires
the number of occurrences of `old` to equal `count` exactly, and replaces every occurrence with
`new`; `["delete", path]` removes the file; `["move", src, dst]` renames the file, whose target
must not exist; `["create", path, content]` writes `content` to a path that must not exist, with
the same encoding and newline setting. A count that differs or a target that exists is a STOP:
touch nothing further, commit nothing of that table, and hand back with the row and the reading.
Stage each commit with `git add -A` after its table and its carrier. The tables are the
reviewer's measured dry run of DECISION F261 D3: table 1 deletes `do job-plan` and table 2
`do plan`, each with the tests that tested only it and its id added to `TestDeletedCommands`.

## SPEC S — the suite, once, after G5 and before C4

From the primary checkout's root, serially:
`python3 -B -m pytest -q -p no:randomly -p no:cacheprovider --tb=short -rfEs`, with `PYTHONPATH`,
`REMEDY_PROJECT` and `REMEDY_DATA_DIR` removed and `PYTHONDONTWRITEBYTECODE=1`, output under
`.remedy-wt/f261r4w/`. Report pytest's return code, the run's last output line, and every
distinct bad node, the text after a line-initial `FAILED ` or `ERROR ` up to the first ` - `.

## Constraints

1. NO SLICE AND NO TABLE IS EDITED. Extract each slice as the bytes strictly between its
   `BEGIN <NAME>` and `END <NAME>` lines and verify its sha256 before use.
2. READ `.agent/STOP` before C0a, before C2 and before C4, with real exit codes. If it exists:
   finish a half-written commit, write the handoff, push, stop.
3. A red gate is a STOP: commit what is honestly finished, hand back with the raw output.
4. Scratch, runner scripts and your worktree live under `.remedy-wt/f261r4w/`, uncommitted; no
   `.py` file under `.agent/`. Under `.remedy-wt/` open only `.remedy-wt/f261-block/` and your
   own directory. `git worktree list` reads one row now; leave it so.
5. Every commit stays under 500 insertions by `git show --numstat`.
6. NEVER merge, open a pull request, force-push, rewrite history or delete a branch. No `remedy`.
   Write no `Done:` paragraph.
7. THE BLOCK'S OWN SIZE, measured on its final bytes: 215 lines TOTAL and 159 lines of PROSE,
   against the caps of 490 and 400.
8. GATE ORDER. G1 and G2 after C1; G3 after C2; G4 and G5 after C3; then SPEC S, whose result is
   G6; G7 after C4 and the push, reported in the completion message only.
9. Every commit message ends with `Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>`, and
   no subject carries a leading-slash token or an absolute path.

## Done when — every gate run for real, its exit code recorded

G1 TRANSPORT. The sha256 of `.agent/authored/f261-r4.md` at C0a equals the digest the delegating
message gives, and `.agent/last_block.md` at C0b is byte-identical to it; the slices FOUND, each
matching its BEGIN-marker sha256; each committed carrier's sha256 equals its digest above.

G2 THE RECORD, at C1. `.agent/plan.md` is byte-identical to PLAN4, at most 50 lines, with
`^## Goal$` once and `^## Next Steps$` once. `.agent/live_review.md` equals its `b8f019de` blob
followed by RECORD4, and `.agent/decisions.md` its `b8f019de` blob followed by DEC3. Over
`.agent/live_review.md`: `^Gate: F\d+ R\d+ — ` reads 112 at `b8f019de` and 113 at C1, with
`Gate: F261 R3 — ` once; distinct `^- R-\d+ — ` ids 96 and 98; distinct `^Done: R-\d+ — ` ids 4
and 4; the open set by distinct id 92 and 94, with C1 minus base exactly `R-0894` and `R-0895`
and base minus C1 empty.

G3 DELETION 1, at C2. `git diff --no-renames --name-only <C1> <C2>` prints exactly
`.agent/authored/f261-r4-delete-1.jsonl` and these: `apps/cli/command_catalog.py`, `apps/cli/commands/do_cmd.py`, `tests/orchestration/test_f018_authority_integration.py`, `tests/orchestration/test_job_task_runner.py` and `tests/test_command_catalog.py`. `git rev-parse <C2>:<dir>`
equals the dry run: `apps` `0ff86c0343fb1732a86bb6fdde7a4d8582bf63f6`,
`tests` `937a8aed02e7e141c5cb0eedfad624897ebc2f14`; `packages`, `scripts`, `docs` and `README.md` equal their objects
at `b8f019de`.

G4 DELETION 2, at C3. `git diff --no-renames --name-only <C2> <C3>` prints exactly
`.agent/authored/f261-r4-delete-2.jsonl` and these: `README.md`, `apps/cli/command_catalog.py`, `apps/cli/commands/do_cmd.py`, `tests/cli/test_scope_plan.py`, `tests/orchestration/test_stream_evidence_integration.py` and `tests/test_command_catalog.py`. `git rev-parse <C3>:<dir>`
equals the dry run: `apps` `f800c1d6d77fe4b9c0adfc74c8d98c5be6d40bd0`, `tests` `ab1cb821a2bae58bac8e089f3dfba4c62277e348`, `README.md`
`86ec95f3c4d8b1c47514cc7c7de5fe25510fec47`; `packages`, `scripts` and `docs` equal their objects at `b8f019de`.
`git grep -n -w -e _cmd_do_job_plan -e _cmd_do_plan <C3> -- apps packages scripts tests docs
':!docs/roadmap'` prints nothing, and `git grep -n -F -e do.job-plan -e do.plan <C3> -- apps
packages scripts tests docs ':!docs/roadmap'` prints exactly the two `DELETED` entries in
`tests/test_command_catalog.py`; accepted history under `docs/roadmap/` is not edited.
`python3 -m ruff check` over every `.py` path of C2 and C3 exits 0.

G5 THE RED-PROOF, in `git worktree add --detach .remedy-wt/f261r4w/wt <C3's sha>`, each run
through the runner over `tests/test_command_catalog.py` with `-rf --tb=no`. (a) CONTROL: must
exit 0. (b) In `apps/cli/commands/do_cmd.py` the bytes
`    "do.promote": lambda args: _cmd_do_promote(`, whose count there must read 1, become
`    "do.plan": lambda args: None,` followed by a newline and those same bytes: must exit 1
with `TestDeletedCommands::test_no_deleted_id_is_left_in_the_dispatch_table` among the failed
nodes. Restore with `git -C .remedy-wt/f261r4w/wt checkout -- apps/cli/commands/do_cmd.py`.
(c) In `apps/cli/command_catalog.py` the bytes `command_id="job.apply",`, count 1, become
`command_id="do.job-plan",`: must exit 1 with
`TestDeletedCommands::test_no_deleted_id_is_left_in_the_catalog` among the failed nodes. Restore
the same way. Report each exit code, summary line and every failed node id; then
`git worktree remove .remedy-wt/f261r4w/wt`.

G6 THE SUITE, SPEC S at C3: must exit 0 with no bad node; report the last output line.

G7 THE TREE, after C4 and the push. `git status --porcelain` prints `''`; C0a to C4 are
single-parent commits in that order on `b8f019de`; `git rev-parse HEAD` equals
`git rev-parse origin/feature/f261-cli-vocabulary-v2`; `git worktree list` prints one row.

## The handback, C4

`.agent/handoff.md` per `docs/agents/handback_template.md`, Session line
`SESSION 1 of feature F261 · round 4 · rounds so far 4`, with one sentence of context
self-assessment. `## Commits` lists C0a to C3, each row's `+/-` cell equal to
`git show --numstat` of that commit; C4's own numbers appear nowhere, per item 31 of §3.
`## Verification` gives G1 to G6 with real exit codes. It states the open findings at 94 by
distinct id, R-0894 and R-0895 owned by F261 among them, with the High ids R-0803, R-0804,
R-0806 and R-0807, and `Operator questions open: 1`. Its `## Next` names, in order: Phase 1
rule 1; the reviewer's verdict on round 4; T002, `apply` for `promote` and `job show --full`.

── SLICE PLAN4 ── target `.agent/plan.md` ── FULL REPLACEMENT ──
BEGIN PLAN4 sha256=aff19347f507809003587a5da3e85d99dc5bf8ff89b57cbcccccdd8be7b674da
# Plan — F261 CLI vocabulary v2 (rename & prune)

Branch: feature/f261-cli-vocabulary-v2, cut from `main` at
`7cdde89b5d0dc8ef1fb96980105870e956699873`, the merge commit of pull request 250.

## Goal

The catalog `apps/cli/command_catalog.py` equals DECISION amend0905-vocab D4: one name per
command, and every retired word deleted rather than aliased, per
`docs/roadmap/features/T2_F261.md`.

## Current Step

ROUND 4 books round 3's PASS, registers R-0894 and R-0895, records DECISION F261 D3, the
deletion paragraph of `do job-plan` and `do plan`, and deletes the two commands in two commits,
each applying a table the round saves under `.agent/authored/` and adding its id to the
deleted-command guard. That finishes T001 as DECISION F261 D1 re-scoped it.

## Next Steps

1. T002: `apply` replaces `promote` in code, catalog and docs, `do promote` joins `job apply`,
   and `job show --full` absorbs the read commands and `do job-report`.
2. T003, the prune to D4, which also removes `do run`'s `--scope-file` and `--approve-scope`
   with the scope-plan writer, as R-0894 records.
3. T004: descriptions, role labels, help wrapping, the catalog tests, and the README Quickstart
   re-derived from the catalog, as R-0895 records.
4. The integration gate, then the closure sequence.

## Risks

- 94 findings are open by distinct id once this round's record lands; four are High, R-0803,
  R-0804, R-0806 and R-0807, all owned by F273.
- A deleted `do` word falls through to the `do` goal entry, and for `do plan` that entry starts
  a job; DECISION F261 D3 records the measured effect beside D1's fifth ruling.
- No command writes the root artifacts a provider-run review package needs, which R-0892
  records for F268.
END PLAN4

── SLICE RECORD4 ── target `.agent/live_review.md` ── APPEND ──
BEGIN RECORD4 sha256=4157768d501bb15382c120efe0509bb2cbdc6cf3e8b68afadf1c397976462706

Gate: F261 R3 — the F261 round 3 entry. VERDICT PASS. Written by the planner and reviewer of session 36 after reading the committed range `d58efc3a`..`b8f019de` and re-deriving the readings below; the worker's report was evidence for none of them. It is booked here by the first commit of round 4 that writes the record, per operator amendment amend0827-process-diet rule 1. THE TRANSPORT: `.agent/authored/f261-r3.md` at `5c683687` and `.agent/last_block.md` at `ecf90780` are byte-identical to the reviewer's scratch original, sha256 `b5d7fc650d67ea18ee0886200ea3b8894dbd563c6297e606159395a46383babc`, and `.agent/authored/f261-r3-delete-1.jsonl` at `70c78773` and `.agent/authored/f261-r3-delete-2.jsonl` at `e617bf7a` are byte-identical to the reviewer's tables. THE STATE: at `a2c033e0` and again at `b8f019de`, `.agent/plan.md` equals PLAN3, `.agent/live_review.md` and `.agent/decisions.md` equal their `d58efc3a` blobs followed by RECORD3 and DEC2, and `docs/roadmap/features/T2_F268.md` and `docs/roadmap/features/T2_F271.md` equal their `d58efc3a` blobs with pairs P268 and P271 applied. THE DELETIONS: at `70c78773` the `apps`, `packages`, `tests` and `scripts` trees equal the reviewer's dry run of table 1 and `docs` equals its object at `a2c033e0`; at `e617bf7a` the same four equal the dry run of table 2, `docs` still equals its object at `a2c033e0` and `README.md` its object at `d58efc3a`; each commit's `--no-renames` path set is the dry run's plus its own carrier. The reviewer's dry run had first reproduced the research helper's table-1 tree, `272a4643`, before adding `TestDeletedCommands`. In that dry run a full suite under `-n auto` read 12 failed and 18249 passed against a base control of 12 failed, every failure on both sides in `tests/ui_server` or `test_vitest_passes` except `TestPorcelainParsing::test_every_enumerated_path_exists_in_this_repo`, which read the dry run's uncommitted index and passed once the tree was committed; and the reviewer's mutations failed `TestDeletedCommands::test_no_deleted_id_is_left_in_the_dispatch_table` for a `do.job-flow` handler entry and `TestDeletedCommands::test_no_deleted_id_is_left_in_the_catalog` for a catalog id changed to `do.job-flow`. THE REVIEWER'S RUN in the primary checkout at `b8f019de` of `tests/test_command_catalog.py`, `tests/test_role_override_flags.py`, `tests/orchestration/test_review_package_status.py`, `tests/cli/test_job_evidence_review_base.py`, `tests/test_observability_index.py`, `tests/cli/test_advertised_commands.py`, `tests/orchestration/test_relevant_regression_coverage.py`, `tests/orchestration/test_import_reachability.py`, `tests/docs/`, `tests/ui_server/test_dashboard_contract.py` and `tests/cli/test_golden_path.py` read 536 passed. The open set reads 92 by distinct id at `b8f019de`.

- R-0894 — Medium, ONCE `do plan` IS DELETED, `do run --scope-file` AND `--approve-scope` ACCEPT A SCOPE PLAN THAT NO COMMAND CAN WRITE ANY MORE, AND D4 LEAVES THOSE FLAGS NO PLACE UNDER `do`. Raised by the planner and reviewer of session 36 while preparing F261 round 4, after searching the open set for the defect under §3 item 30: no open finding describes it. THE DEFECT, read at `b8f019de`: `_cmd_do_plan` in `apps/cli/commands/do_cmd.py` is the only caller under `apps/`, `packages/` and `scripts/` of `extract_scope_plan` and `persist_scope_plan` in `packages/orchestration/scope_plan.py`, and the only reader of the file they write is `_cmd_do`'s `scope_file` branch, which calls `load_scope_plan` when `--approve-scope` is given. DECISION amend0905-vocab D4 lists the flags of `do <order>` and ends "Nothing else under `do`", and neither flag is in that list. WHY MEDIUM: after the round a user can pass `--scope-file` but has no CLI word that produces one, so the approve-each-feature step before a run is unreachable while its flags stay advertised. WHY F261's: the catalog equal to D4 is F261's goal, so removing the flags is its own T003 prune. FIX: T003 deletes `--scope-file` and `--approve-scope` from `do`, the scope-plan writer and loader, and the scope contracts they feed, in one commit with a deletion paragraph naming the heir of the idea or stating that it has none. Owner: F261.

- R-0895 — Low, THE README QUICKSTART NAMES COMMANDS AND FLAGS THE CATALOG DOES NOT HOLD. Raised by the planner and reviewer of session 36 while preparing F261 round 4, after searching the open set under §3 item 30: no open finding describes it. THE DEFECT, read at `b8f019de`: the `## Quickstart` block of `README.md` lists `remedy job create --plan plan.yaml`, while the catalog's `job.create` declares no `--plan`; `remedy do run <job-id>`, while `do.run` takes a goal and no job id; `remedy do report <job-id>`, while `do.report` takes a run id; and `remedy do plan <job-id>`, which this round deletes together with its README line. `tests/cli/test_advertised_commands.py` reads no `README.md`, so no test sees it. WHY LOW: a first command copied from the README fails or does something else, and nothing else is wrong. WHY F261's: that block's own comment says "F261 renames the command", and F261 is where the command words settle. FIX: T004 re-derives every Quickstart line from the catalog as it stands then, runs each against a fixture, and extends the advertised-commands test to `README.md`. Owner: F261.
END RECORD4

── SLICE DEC3 ── target `.agent/decisions.md` ── APPEND ──
BEGIN DEC3 sha256=855c40977032893c7174ea1671878bd3817abf95ccc353a87a9cdaafe4317ce1

## DECISION F261 D3 (2026-09-15, F261 round 4) — the deletion paragraph of `do job-plan` and `do plan`: both commands go, the libraries they called stay for their other users, and the scope flags they fed go in T003

CONTEXT. DECISION F261 D1 ordered `do job-plan` and `do plan` deleted in T001, each in its own commit with the deletion paragraph DECISION amend0905-vocab D3 requires. This is that paragraph for both.

WHAT IS DELETED, measured at `b8f019de` by an `ast` call graph over `apps/cli/commands/do_cmd.py` rooted at every other handler-table entry, which the reviewer's research helper built, and re-read by the reviewer in the dry-run trees of the round: in the first commit the catalog entry `do.job-plan`, its handler-table entry and `_cmd_do_job_plan`, which no other function was reachable only from, with the tests that tested only it, and the `related=` tuples and argument help that named it; in the second commit the catalog entry `do.plan`, its handler-table entry and `_cmd_do_plan`, with `TestCliPlan` in `tests/cli/test_scope_plan.py` and the `remedy do plan <job-id>` line of `README.md`. Each commit adds its id to `TestDeletedCommands` in `tests/test_command_catalog.py`.

THE HEIRS. Making a job from a Markdown order without a provider call belongs to F268's `remedy do <order> --plan-only`, as D1 names; the budget flags given at planning time belong to `job create` and `job run`, which both take them; the `Next:` hint of `do job-plan` has no heir. The scope plan `do plan` wrote, and the step in which a user approves, denies or defers each extracted feature before a run, have no heir in F268's flag list, and DECISION amend0905-vocab D4 leaves the `--scope-file` and `--approve-scope` flags that read it no place under `do`; R-0894 routes their removal to this feature's T003.

CHOSEN, FIRST: THE LIBRARIES STAY. `plan_job_from_file` in `packages/orchestration/pingpong_job.py` stays because `packages/orchestration/self_use_job.py` calls it, and `_print_scope_summary` stays because other handlers call it. `packages/orchestration/scope_plan.py` and `do run`'s two scope flags stay in this round, because removing them changes a surviving command; T003 removes them in one commit with their own paragraph. ALTERNATIVE: delete the flags and the scope-plan writer here, rejected because a command deletion that also changes `do run` is two changes under one paragraph.

CHOSEN, SECOND: THE FALL-THROUGH IS ACCEPTED AS D1 RULED, AND ITS EFFECT IS NOW MEASURED. With both words gone, `remedy do plan` is read as a goal: the research helper's parse probe, with the handlers mocked, sent a bare `remedy do plan` to the `do` goal entry for missions and `remedy do plan --task-file <path>` to the `do run` goal entry, each of which saves a job, where at `b8f019de` the first exited with a usage error and the second wrote only a scope plan; and `remedy do job-plan --job-file <path>` exits with an argument error. DECISION D-B still forbids a list of refused retired words, and the meaning of `remedy do <order>` is F268's.

CONSEQUENCE. T001 as D1 re-scoped it is finished. `README.md`'s Quickstart keeps lines that the catalog contradicts, which R-0895 routes to T004. HOW TO REVERSE: restore both commands from the parent of the round's first deletion commit, and delete this section and the registrations it names.
END DEC3
