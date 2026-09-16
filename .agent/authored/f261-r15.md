── STEP T003/3 — F261 — ROUND 15 ──
Goal: Book round 14's PASS and its prose slip, register R-0904 for F273, record DECISION F261
D14, and delete the loop modules, the `queue` command group and the F048 job queue in three
commits by applying three tables; run the suite once.

Base commit: `8aa94f37`, on `feature/f261-cli-vocabulary-v2`. SESSION 4 of F261. Read AGENTS.md,
docs/agents/self_drive_protocol.md, `.agent/f261_t003_inventory.md`, and DECISION F261 D14 once
C1 has landed it.

THE FRAME RULE, per item 37 of §3, measured over the final bytes: NO LINE of this block is a run
of a single repeated character, and every box-drawing rule inside the STEP and SLICE header
lines is exactly two characters long.

ENVIRONMENT: `VAR=x cmd`, `env` and `export` are denied, so set environment in-process; `cp` is
denied, so copy with `shutil.copyfile`; bare `ruff` is denied, so use `python3 -m ruff check`.
Shell loops, `$(...)` and `$?` in a compound command are refused by form, so write such checks
as Python scripts under `.remedy-wt/f261r15w/`, and never name a script after a standard-library
module; a pipe into `tail` hides pytest's exit code. The editable install resolves `apps` and
`packages` to the PRIMARY checkout, so a pytest run inside a worktree goes through a runner
script that changes into the worktree, puts it first on `sys.path` and in `PYTHONPATH`, and
asserts `apps.cli.grouped` loaded from inside it. Never call `run_job` or a runner yourself: a
job run started from inside a checkout creates a `remedy/job-*` branch in it.
`git branch --list 'remedy/job-*'` reads 16 lines now; keep it so. While a deletion is staged
but not committed, `test_every_enumerated_path_exists_in_this_repo` fails; run no suite then.

## Bundle — the ordered commit sequence

C0a `.agent/authored/f261-r15.md`, the block file the delegating message names, by
    `shutil.copyfile`
C0b `.agent/last_block.md`, the same bytes
C1  THE RECORD, one commit: `.agent/plan.md` becomes slice PLAN15; slice RECORD15 is appended to
    `.agent/live_review.md`, slice DEC14 to `.agent/decisions.md` and slice SLIP15 to
    `.agent/prose_slips.md`; in `docs/roadmap/features/T2_F273.md` the bytes of slice P273-FROM
    are replaced by those of slice P273-TO
C2  THE LOOP MODULES: copy `.remedy-wt/f261-block/f261-r15-loop.jsonl` to
    `.agent/authored/f261-r15-loop.jsonl` and apply it per THE TABLES, in one commit
C3  THE QUEUE GROUP: the same with `f261-r15-queue.jsonl`, in one commit
C4  THE JOB QUEUE AND THE F048 BINDING: the same with `f261-r15-jobqueue.jsonl`, in one commit
C5  `.agent/handoff.md`, the handback; then `git push origin feature/f261-cli-vocabulary-v2`

C1 is the FIRST SUBSTANTIVE COMMIT, per item 23 of §3. No pull request is created.

## Change — exactly these paths and no others

C0a to C1: `.agent/authored/f261-r15.md`, `.agent/last_block.md`, `.agent/plan.md`,
`.agent/live_review.md`, `.agent/decisions.md`, `.agent/prose_slips.md` and
`docs/roadmap/features/T2_F273.md`. C2 to C4: each table's own carrier and the paths G3 names.
C5: `.agent/handoff.md`.

## The appends and the pair

RECORD15, DEC14 and SLIP15 each begin with an empty line, and their targets end in a
newline at `8aa94f37`: an append is the file's bytes followed by the slice's bytes, and nothing
else. The pair P273: TO contains FROM: false, so it is a REWRITE; P273-FROM occurs once
in `docs/roadmap/features/T2_F273.md` at `8aa94f37`, and at C1 P273-FROM occurs 0 times and
P273-TO once.

## THE TABLES

Each carrier holds one JSON array per line. Their sha256 digests, to verify before copying:
`f261-r15-loop.jsonl` `d0dd0c71a310df2d26a787707c65749b37a7d625a05a50702a6ae364511384d7`,
`f261-r15-queue.jsonl` `1139f4457bc13dadc46153e3275e1dcedeca402214c8bef71557bf510401eebd`,
`f261-r15-jobqueue.jsonl` `36e1ee460e7d063e63be8fc5670422ba8da724e391f3bef7a8683c48e06f262d`.
Apply the rows strictly
in file order, each against the tree as the previous rows left it, from the repository root:
`["edit", path, old, new, count]` opens the path with `encoding="utf-8", newline=""`, requires
the number of occurrences of `old` to equal `count` exactly, and replaces every occurrence with
`new`; `["delete", path]` removes the file; `["move", src, dst]` renames the file, whose target
must not exist; `["create", path, content]` writes `content` to a path that must not exist, with
the same encoding and newline setting. A count that differs or a target that exists is a STOP:
touch nothing further, commit nothing of that table, and hand back with the row and the reading.
Stage each commit with `git add -A` after its table and its carrier. The tables are the
reviewer's measured dry run of DECISION F261 D14, applied on top of C1's record: the loop table
its CHOSEN FIRST, the queue table its CHOSEN SECOND and the job queue table its CHOSEN THIRD.

## SPEC S — the suite, once, after G5 and before C5

From the primary checkout's root, serially:
`python3 -B -m pytest -q -p no:randomly -p no:cacheprovider --tb=short -rfEs`, with `PYTHONPATH`,
`REMEDY_PROJECT` and `REMEDY_DATA_DIR` removed and `PYTHONDONTWRITEBYTECODE=1`, output under
`.remedy-wt/f261r15w/`. Report pytest's return code, the run's last output line, and every
distinct bad node, the text after a line-initial `FAILED ` or `ERROR ` up to the first ` - `.
Re-run each bad node alone, once, the same way, and report that return code beside it.

## Constraints

1. NO SLICE AND NO TABLE IS EDITED. Extract each slice as the bytes strictly between its
   `BEGIN <NAME>` and `END <NAME>` lines and verify its sha256 before use.
2. READ `.agent/STOP` before C0a, before C2 and before C5, with real exit codes. If it exists:
   finish a half-written commit, write the handoff, push, stop.
3. A red gate is a STOP: commit what is honestly finished, hand back with the raw output.
4. Scratch, runner scripts and your worktree live under `.remedy-wt/f261r15w/`, uncommitted; no
   `.py` file under `.agent/`. Under `.remedy-wt/` open only `.remedy-wt/f261-block/` and your
   own directory. `git worktree list` reads one row now; leave it so. Create no symlink.
5. Every commit stays under 500 insertions, read as the first column of `git show --numstat
   --format= <commit>` with git's default rename detection.
6. NEVER merge, open a pull request, force-push, rewrite history or delete a branch. No `remedy`.
   Write no `Done:` paragraph and no `Landed:` line.
7. THE BLOCK'S OWN SIZE, measured on its final bytes: 307 lines TOTAL and 225 lines of PROSE,
   against the caps of 490 and 400.
8. GATE ORDER. G1 and G2 after C1; G3, G4 and G5 after C4; then SPEC S, whose result is G6; G7
   after C5 and the push, reported in the completion message only.
9. Every commit message ends with `Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>`, and
   no subject carries a leading-slash token or an absolute path.

## Done when — every gate run for real, its exit code recorded

G1 TRANSPORT. The sha256 of `.agent/authored/f261-r15.md` at C0a equals the digest the delegating
message gives, and `.agent/last_block.md` at C0b is byte-identical to it; the slices FOUND, each
matching its BEGIN-marker sha256; each committed carrier's sha256 equals its digest above.

G2 THE RECORD, at C1. `.agent/plan.md` is byte-identical to PLAN15, at most 50 lines, with
`^## Goal$` once and `^## Next Steps$` once. `.agent/live_review.md` equals its `8aa94f37` blob
followed by RECORD15, `.agent/decisions.md` its `8aa94f37` blob followed by DEC14, and
`.agent/prose_slips.md` its `8aa94f37` blob followed by SLIP15.
`docs/roadmap/features/T2_F273.md` equals its `8aa94f37` blob with the pair P273 applied, with
the counts The appends and the pair give. Over `.agent/live_review.md`: `^Gate: F\d+ R\d+ — `
reads 123 at `8aa94f37` and 124 at C1, with `Gate: F261 R14 — ` once at C1; distinct
`^- R-\d+ — ` ids 106 and 107, C1 minus base exactly `R-0904`; distinct `^Done: R-\d+ — ` ids 8
and 8; the open set by distinct id 98 and 99. `python3 -m pytest tests/docs/ -q` exits 0 at C1.

G3 THE TABLES, at C2, C3 and C4. `git diff --no-renames --name-only` from each commit's parent
prints exactly that commit's carrier and: at C2 `packages/orchestration/loop_run.py`, `packages/orchestration/loop_spec.py`, `packages/orchestration/run_report.py`, `tests/docs/test_retired_promote_word.py`, `tests/orchestration/import_reachability_allowlist.txt`, `tests/orchestration/test_loop_run.py`, `tests/orchestration/test_loop_spec.py` and `tests/orchestration/test_run_report.py`; at C3 `apps/cli/command_catalog.py`, `apps/cli/commands/__init__.py`, `apps/cli/commands/mission_cmd.py`, `apps/cli/commands/queue_cmd.py`, `packages/orchestration/config.py`, `tests/cli/test_queue_cmd.py`, `tests/orchestration/import_reachability_allowlist.txt` and `tests/test_command_catalog.py`; at C4
`packages/orchestration/config.py`, `packages/orchestration/data_paths.py`, `packages/orchestration/job_queue.py`, `packages/orchestration/long_run_executor.py`, `packages/orchestration/mission_state.py`, `tests/docs/test_retired_promote_word.py`, `tests/orchestration/import_reachability_allowlist.txt`, `tests/orchestration/test_job_queue.py`, `tests/orchestration/test_queue_concurrency.py` and `tests/orchestration/test_queue_executor_binding.py`. `git rev-parse <commit>:<object>` equals the reviewer's dry run, which applied C1's
record before the tables, for `apps`, `tests`, `docs`, `scripts`, `packages` and `README.md` in
that order: C2 `7952f315479e3656e0a3b8bb5d09cf5b055f8408`, `911181519996486e8e4d9430927fd42850ef7a39`, `5d82ca64fb0111f4254ab605bd90e45080bdc1f3`, `e3c01bde145e2c323bf157e1bb4a97cdaaa747cc`, `9855388649bfd28965b290a354113ade7986f4f5`, `15b9e0e8fec9721c7c17a872cc8f1a2bed3a2952`; C3 `ff5e76287693461ea5051df75fae3f138559ff3f`, `7411b171ce86384943ee1ef819f4914b761a39a5`, `5d82ca64fb0111f4254ab605bd90e45080bdc1f3`, `e3c01bde145e2c323bf157e1bb4a97cdaaa747cc`, `90310c8b2e55595ca4907371913a88ecdb98c95f`, `15b9e0e8fec9721c7c17a872cc8f1a2bed3a2952`; C4 `ff5e76287693461ea5051df75fae3f138559ff3f`, `d62dcbe038e566aaa9628f356859e46834159baf`, `5d82ca64fb0111f4254ab605bd90e45080bdc1f3`, `e3c01bde145e2c323bf157e1bb4a97cdaaa747cc`, `53712cf31a464163f987e63dc251387728c9c0c6`, `15b9e0e8fec9721c7c17a872cc8f1a2bed3a2952`.
Report each commit's insertions per constraint 5.

G4 THE SWEEP, at C4. `git grep -n -I -E 'remedy (queue|loop)\b|loop_spec|loop_run|job_queue|queue_cmd|loop_ref|LOOP_REF_METADATA_KEY|_pull_queue_when_idle|queued_entry_to_job|QueuePull|queue_binding_enabled|LEDGER_EVENT_QUEUE_PULL|queue\.executor_binding|queue\.reclaim_ttl_minutes|REMEDY_QUEUE_|def queue_dir\b'
<C4> -- apps packages scripts tests docs README.md AGENTS.md .claude ':!docs/roadmap'` exits 1
and prints nothing. `python3 -m ruff check` over every `.py` path of C2 to C4 that still exists
at C4 exits 0.

G5 THE RED-PROOF, in `git worktree add --detach .remedy-wt/f261r15w/wt <C4's sha>`, each run
through the runner over `tests/test_command_catalog.py`, `tests/cli/test_cli_ux.py`,
`tests/test_grouped_cli.py` and `tests/orchestration/test_import_reachability.py` with
`-rf --tb=no`. Mutation <n> is in the file its line below names, replaces the bytes of slice
MUT-<n>-FROM, whose count there must read 1, with those of slice MUT-<n>-TO, and is restored with
`git -C .remedy-wt/f261r15w/wt checkout -- <that file>`. (a) CONTROL: must exit 0. Each of (1)
to (4) must exit 1 with the named node among the failed nodes:
(1) `apps/cli/commands/status_cmd.py`, a `queue` handler row:
`TestDeletedCommands::test_no_deleted_id_is_left_in_the_dispatch_table`; (2)
`apps/cli/command_catalog.py`, the `queue` group restored without commands:
`TestCatalogIntegrity::test_every_group_has_at_least_one_command`; (3)
`tests/orchestration/import_reachability_allowlist.txt`, the `job_queue` module line restored,
and (4) the same file, the `loop_spec` module line restored: each
`test_every_allowlist_entry_still_resolves_to_a_file_on_disk`.
Report each exit code, summary line and number of failed nodes; then
`git worktree remove --force .remedy-wt/f261r15w/wt` and read `git branch --list 'remedy/job-*'`.

G6 THE SUITE, SPEC S at C4: must exit 0 with no bad node; report the last output line. A bad
node whose lone re-run exits 0 is reported as such with both readings, and is not a STOP; a bad
node whose lone re-run fails is.

G7 THE TREE, after C5 and the push. `git status --porcelain` prints `''`; C0a to C5 are
single-parent commits in that order on `8aa94f37`; `git rev-parse HEAD` equals
`git rev-parse origin/feature/f261-cli-vocabulary-v2`; `git worktree list` prints one row, and
`git branch --list 'remedy/job-*'` prints 16 lines.

## The handback, C5

`.agent/handoff.md` per `docs/agents/handback_template.md`, Session line
`SESSION 4 of feature F261 · round 15 · rounds so far 15`, with one sentence of context
self-assessment. `## Commits` lists C0a to C4, each row's `+/-` cell equal to constraint 5's
reading of that commit and its deletions column; C5's own numbers appear nowhere, per item 31 of
§3. `## Verification` gives G1 to G6 with real exit codes. It states the open findings at 99 by
distinct id, with the High ids R-0803, R-0804 and R-0807, and `Operator questions open: 0`. Its
`## Next` names, in order: Phase 1 rule 1; the reviewer's verdict on round 15; the `guide`,
`dashboard` and `repo` groups, as the inventory proposes.

── SLICE PLAN15 ── target `.agent/plan.md` ── FULL REPLACEMENT ──
BEGIN PLAN15 sha256=8b8b5b6d6b171b3d0a11660b1705a7380d5f694ffd83ad853fb3648700a0848c
# Plan — F261 CLI vocabulary v2 (rename & prune)

Branch: feature/f261-cli-vocabulary-v2, cut from `main` at
`7cdde89b5d0dc8ef1fb96980105870e956699873`, the merge commit of pull request 250.

## Goal

The catalog `apps/cli/command_catalog.py` equals DECISION amend0905-vocab D4: one name per
command, and every retired word deleted rather than aliased, per
`docs/roadmap/features/T2_F261.md`.

## Current Step

ROUND 15 continues T003. It books round 14's PASS and its prose slip, registers R-0904 for
F273 and records DECISION F261 D14, then deletes the loop modules with the run report's loop
reference, the `queue` command group, and `job_queue.py` with the F048 binding, its
configuration keys and its data path, one table per commit.

## Next Steps

1. The `guide` group with the group-count guard, the `dashboard` group, and the `repo` group
   with its `dev status` block, as `.agent/f261_t003_inventory.md` proposes.
2. The rest of T003 in the inventory's order, each round re-measured before it is authored,
   with R-0767, R-0894 and R-0900.
3. T004.

## Risks

- 98 findings are open by distinct id before this round's record and 99 after it; three are
  High, R-0803, R-0804 and R-0807.
- The inventory proposes more rounds than F261's soft limit of 25 leaves; the session that
  reaches the limit owes the scope report and the split-and-close default.
- A deletion's consumers include shell strings, subprocess help calls, configuration key
  descriptions and the UI event catalog, so every deletion round runs the whole suite on its
  committed tree.
END PLAN15

── SLICE RECORD15 ── target `.agent/live_review.md` ── APPEND ──
BEGIN RECORD15 sha256=c4c07c91d4d50ec0a0d261355ac7cf8fd3372a73743122f1696386c3508430f9

Gate: F261 R14 — the F261 round 14 entry. VERDICT PASS. Written by the planner and reviewer of session 38 after reading the committed range `c3047df0`..`71fb95dc` and re-deriving the readings below; the worker's report was evidence for none of them. It is carried by `.agent/handoff.md` in the session-close commit that follows `71fb95dc` and booked by the first commit of round 15 that writes the record, per operator amendment amend0827-process-diet rule 1. THE TRANSPORT: `.agent/authored/f261-r14.md` at `8d6a7bee` and `.agent/last_block.md` at `b5d87e1d` are byte-identical to the reviewer's scratch original, sha256 `ec743657d65cf88693654218b20e6f98baf9f0a83e5f78fe5f712723f46d004e`, and the three tables committed at `98866b80`, `4bf17d32` and `be6ae79d` are byte-identical to the reviewer's. THE STATE: at `ebd3c812` and again at `71fb95dc`, `.agent/plan.md` equals PLAN14, `.agent/live_review.md` and `.agent/decisions.md` equal their `c3047df0` blobs followed by RECORD14 and DEC13, and `docs/roadmap/features/T2_F273.md` equals its `c3047df0` blob with the pair P273 applied. THE TABLE COMMITS: at `98866b80`, `4bf17d32` and `be6ae79d` the `apps`, `tests`, `scripts`, `packages` and `README.md` objects equal the reviewer's dry-run commits of the tables, which had reproduced the research helper's trees exactly, and the `docs` object differs from the dry run's by `docs/roadmap/features/T2_F273.md` alone, which at each of those commits equals the P273 result; each commit's `--no-renames` path set is the dry run's plus its carrier, and `git show --numstat` reads 38, 48 and 26 insertions. G3 of the block ordered the `docs` object equal to the dry run's, which the reviewer had measured before applying the record slices, so no commit carrying C1's pair could meet it; the worker read that gate red, measured that the one differing file was the one C1 changes, and declared the deviation, and the slip is the reviewer's. In the dry run's production diff each deleted group leaves with its handlers, its catalog entries, its tests and the package code only it called; `list_decisions`, `list_rollback_proofs` and `audit_rollback_safety` stay for the cockpit and `test integrity`, `snapshot create` relates to `snapshot show`, and the two pages keep their text under dated status lines. At `71fb95dc` the grep of `remedy orchestrator`, `remedy rollback`, `remedy loop`, the two deleted handler modules and the three deleted rollback functions over `apps`, `packages`, `scripts`, `tests`, `docs` without `docs/roadmap`, and `README.md` exits 1 with no output. In the reviewer's dry run a full suite under `-n auto` without `tests/ui_server` read 1 failed, `test_vitest_passes`, and 17618 passed, and the cockpit, docs, canary and smoke-script tests read 633 passed. Over `tests/test_command_catalog.py`, `tests/cli/test_cli_ux.py`, `tests/test_grouped_cli.py` and `tests/orchestration/test_import_reachability.py`, which passed 461 unmutated, an `orchestrator`, a `rollback` and a `loop` handler row each failed 1 test and the `loop` group restored without commands failed 1. The record slices and the pair applied on top of the dry run passed `tests/docs/` and the other files the reviewer ran among those that read the edited state files, apart from `test_vitest_passes`, at 840 passed. THE REVIEWER'S RUN in the primary checkout at `71fb95dc` of those four files, the orchestrator, real test execution, cost preview, decision evidence, model routing, loop spec and loop run tests, `tests/ui_server/test_dashboard_cockpit_truth.py`, `tests/ui_server/test_dashboard_contract.py`, `tests/cli/test_golden_path.py`, `tests/cli/test_advertised_commands.py`, `tests/docs/` and `tests/test_remedy_smoke_script.py` read 1727 passed and 3 skipped, and `git branch --list 'remedy/job-*'` read 16 lines. The open set reads 98 by distinct id at `71fb95dc`.

- R-0904 — Low, THE HEIR THE F261 DESIGN NAMES FOR A QUEUED GOAL, `mission list --status planned`, DOES NOT EXIST, AND ONCE THE `queue` GROUP AND THE F048 BINDING ARE DELETED NOTHING PICKS A WAITING GOAL UP WHEN A RUN GOES IDLE. Raised by the planner and reviewer of session 39 while preparing F261 round 15, after searching the open set for `queue`, `mission list` and `status planned` under §3 item 30: no open finding describes it. THE DEFECT, read at `8aa94f37`: the Design section of `docs/roadmap/features/T2_F261.md` names `mission list --status planned` as the heir of a queued goal, while the `mission.list` entry of `apps/cli/command_catalog.py` takes `--project`, `--all-projects` and `--json` only, `_cmd_mission_list` in `apps/cli/commands/mission_cmd.py` filters nothing, and `MISSION_STATUSES` in `packages/orchestration/mission_state.py` holds active, paused, achieved and abandoned and no planned status. `mission start "<goal>"` records a goal without running it and `mission list` lists it, so the operator keeps a list of goals, but no status tells a goal no job has started from one being worked. The F048 binding `_pull_queue_when_idle` in `packages/orchestration/long_run_executor.py` claimed the next queued goal of a project when a run ended idle; its configuration key `queue.executor_binding` defaulted to false, and at `8aa94f37` the only files under `apps`, `packages`, `scripts` and `docs` that name that key or its environment variable are `packages/orchestration/config.py`, `long_run_executor.py` and `docs/roadmap/features/T1_F048.md`, so nothing the product ships switches it on. WHY LOW: no surviving command prints anything false, and the pickup was an opt-in the product never enabled. WHY F273's: a filter or a status on a surviving command is findings paydown, and F261 prunes without changing what a surviving command does. FIX: give `mission list` a `--status` filter over a status that marks a mission no job has started, with a test, or record by DECISION that the goal list needs no such filter and amend the heir sentence of the F261 Design to name `mission start` and `mission list`. Owner: F273.
END RECORD15

── SLICE DEC14 ── target `.agent/decisions.md` ── APPEND ──
BEGIN DEC14 sha256=bcbeb7ec2ade5769f24c91c0a86a5c595cca05a4e02ee842bc22bf6dad5847ff

## DECISION F261 D14 (2026-09-15, F261 round 15) — the deletion paragraph of the loop modules, the `queue` group and the F048 job queue

CONTEXT. `docs/roadmap/features/T2_F261.md` deletes `queue` and `loop` with their modules, each with a deletion paragraph naming the heir, and `.agent/f261_t003_inventory.md` puts them in its round B. Measured at `8aa94f37` by the reviewer's research helper and re-read by the reviewer on the dry-run trees. As in DECISION F261 D13, a command's package code goes with it when the command was its only production caller.

CHOSEN, FIRST: the loop modules. Deleted: `packages/orchestration/loop_spec.py`, which parsed the top-level `[[loop]]` tables of `remedy.toml`, and `packages/orchestration/loop_run.py`, which turned one into a planned job carrying a `loop_ref` in its metadata, with their tests; from `packages/orchestration/run_report.py` the `loop_ref` field, its read and the `- Loop:` line, with `TestLoopProvenanceLine`. At `8aa94f37` the run report's read of `LOOP_REF_METADATA_KEY` was the only production import of either module, because round 14 deleted `apps/cli/commands/loop_cmd.py`. THE HEIR, as DECISION F261 D13 names it: a recurring order is an order file started with `remedy do <file>`; a scheduler has no heir. `load_config` in `packages/orchestration/config.py` reads only the `remedy` table, so a `[[loop]]` table left in a `remedy.toml` is ignored.

CHOSEN, SECOND: `queue`. Deleted: the group, its commands `queue.add`, `queue.list`, `queue.rm` and `queue.reclaim`, `apps/cli/commands/queue_cmd.py` and `tests/cli/test_queue_cmd.py`; the description of the `queue.reclaim_ttl_minutes` key no longer names the deleted command, and the docstring of `apps/cli/commands/mission_cmd.py` no longer names the group. THE HEIR: a goal kept for later is a mission, recorded by `remedy mission start "<goal>"` and listed by `remedy mission list`. The Design names `mission list --status planned`, and that filter and that status do not exist; R-0904 records it for F273.

CHOSEN, THIRD: `packages/orchestration/job_queue.py` and the F048 binding. Deleted: the module and `tests/orchestration/test_job_queue.py`, `test_queue_concurrency.py` and `test_queue_executor_binding.py`; from `packages/orchestration/long_run_executor.py` the binding that let an idle run claim its project's next queued goal and plan it as a job, with `QueuePull`, `queue_binding_enabled`, `queued_entry_to_job`, `_pull_queue_when_idle`, the `queue_pull` ledger event and the `queue_pull` field of `CycleLoopResult`; the configuration keys `queue.executor_binding` and `queue.reclaim_ttl_minutes`; and `queue_dir` in `packages/orchestration/data_paths.py`. `packages/orchestration/worker_queue.py` stays for `job enqueue` and `worker run`, which a later round of the inventory takes; it writes its own files directly in the same `queue` directory and never read the per-project folders. THE HEIR: none for the unattended pickup, which was off by default.

CONSEQUENCE. `remedy queue` is an unknown command and its ids join `TestDeletedCommands`; `remedy config` knows neither `queue.*` key; a run report prints no `- Loop:` line; per-project queue folders and `loop_ref` metadata already on disk stay there unread, under DECISION D-A of `docs/roadmap/features/T2_F261.md`. HOW TO REVERSE: revert the round's three table commits and delete this section.
END DEC14

── SLICE SLIP15 ── target `.agent/prose_slips.md` ── APPEND ──
BEGIN SLIP15 sha256=473615f7ba7e991fff5ca3a084807bf24178df00e01b1d3dd6ad7c442843c2ae

2026-09-15 · F261 R14 · G3 of the round 14 block ordered each table commit's `docs` object equal to the reviewer's dry run, which applied the tables before the record slices, while C1 of the same block rewrote `docs/roadmap/features/T2_F273.md`; the gate was unmeetable by construction, the worker declared it after measuring that file as the only difference, and the rule that follows is that a dry run whose record commit touches a gated object applies the record first.
END SLIP15

── SLICE P273-FROM ── target `docs/roadmap/features/T2_F273.md` ── REWRITE FROM ──
BEGIN P273-FROM sha256=f72eb475d6f2ef05e4c6810e791515b586f96d089d99e26ddf6b3237390401bf
  tests that pinned it or the producer that now writes what it reads.

## Do not touch
END P273-FROM

── SLICE P273-TO ── target `docs/roadmap/features/T2_F273.md` ── REWRITE TO ──
BEGIN P273-TO sha256=dcdedcfbdadd46ce4ed1bb06a000a949b7260bff3877907d175eb885017d0e75
  tests that pinned it or the producer that now writes what it reads.
- R-0904 carries a resolution line naming the commit that gave `mission list` its status filter with
  the test that pins it, or the DECISION that rules the filter unneeded with the commit that amended
  the heir sentence of the F261 Design.

## Do not touch
END P273-TO

── SLICE MUT-1-FROM ── G5 (1) only ── never a file ──
BEGIN MUT-1-FROM sha256=a8d1b10753770463455ca2373f361ac5b3b8ab8f1d189178c8fa77ac4d6cd485
        json_output=getattr(args, "json", False),
    ),
}
END MUT-1-FROM

── SLICE MUT-1-TO ── G5 (1) only ── never a file ──
BEGIN MUT-1-TO sha256=f8f984968bf4f3561187970283b70b3871907f304f3768e3a175e799dad0029f
        json_output=getattr(args, "json", False),
    ),
    "queue.list": lambda args: None,
}
END MUT-1-TO

── SLICE MUT-2-FROM ── G5 (2) only ── never a file ──
BEGIN MUT-2-FROM sha256=49d2f3881a3c6514131918758024efddf4ff886c007adf78de5a7c5855bbebe3
    "job": GroupDef("job", "Job", "Create, inspect, and manage jobs."),
END MUT-2-FROM

── SLICE MUT-2-TO ── G5 (2) only ── never a file ──
BEGIN MUT-2-TO sha256=34f80a9546af1ba875974de0d78116efaf6da12d259f09ed1ead188ffc6bee32
    "job": GroupDef("job", "Job", "Create, inspect, and manage jobs."),
    "queue": GroupDef("queue", "Queue", "Queue goals for unattended execution."),
END MUT-2-TO

── SLICE MUT-3-FROM ── G5 (3) only ── never a file ──
BEGIN MUT-3-FROM sha256=89730ea9664fb336a01b86193112e46a74c4db7e2b8c2694b626675a4585133d
packages.orchestration.job_fulfillment
packages.orchestration.job_runner
END MUT-3-FROM

── SLICE MUT-3-TO ── G5 (3) only ── never a file ──
BEGIN MUT-3-TO sha256=e58e5f4b23a27c05ca69646a382215a70bd874610c51bdea6ee56527d50c8ba4
packages.orchestration.job_fulfillment
packages.orchestration.job_queue
packages.orchestration.job_runner
END MUT-3-TO

── SLICE MUT-4-FROM ── G5 (4) only ── never a file ──
BEGIN MUT-4-FROM sha256=986456d49d41f437af5e8cd6151f5772f0b1b0d158acc8618d561907d9ea76e4
packages.orchestration.long_run_executor
packages.orchestration.manifest_schema
END MUT-4-FROM

── SLICE MUT-4-TO ── G5 (4) only ── never a file ──
BEGIN MUT-4-TO sha256=7170ef53ee027b6e2a7203299417c28a1f2ffe939d7ac1f47107d1e1b90f4ff1
packages.orchestration.long_run_executor
packages.orchestration.loop_spec
packages.orchestration.manifest_schema
END MUT-4-TO
