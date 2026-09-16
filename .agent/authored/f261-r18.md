── STEP T003/6 — F261 — ROUND 18 ──
Goal: Book round 17's PASS and its prose slip, register R-0908 and R-0910 for F273 and R-0909
for this feature, record DECISION F261 D17, and delete the `context` group, the `token` group
with `context-pack` and the `review` group in three commits by applying three tables; run the
suite once.

Base commit: `43694261`, on `feature/f261-cli-vocabulary-v2`. SESSION 4 of F261. Read AGENTS.md,
docs/agents/self_drive_protocol.md, `.agent/f261_t003_inventory.md`, and DECISION F261 D17 once
C1 has landed it.

THE FRAME RULE, per item 37 of §3, measured over the final bytes: NO LINE of this block that is two or
more characters long is a run of a single repeated character, and every box-drawing rule inside the STEP and SLICE header
lines is exactly two characters long.

ENVIRONMENT: `VAR=x cmd`, `env` and `export` are denied, so set environment in-process; `cp` is
denied, so copy with `shutil.copyfile`; bare `ruff` is denied, so use `python3 -m ruff check`.
Shell loops, `$(...)` and `$?` in a compound command are refused by form, so write such checks
as Python scripts under `.remedy-wt/f261r18w/`, and never name a script after a standard-library
module; a pipe into `tail` hides pytest's exit code. The editable install resolves `apps` and
`packages` to the PRIMARY checkout, so a pytest run inside a worktree goes through a runner
script that changes into the worktree, puts it first on `sys.path` and in `PYTHONPATH`, and
asserts `apps.cli.grouped` loaded from inside it. Never call `run_job` or a runner yourself: a
job run started from inside a checkout creates a `remedy/job-*` branch in it.
`git branch --list 'remedy/job-*'` reads 16 lines now; keep it so. While a deletion is staged
but not committed, `test_every_enumerated_path_exists_in_this_repo` fails; run no suite then.

## Bundle — the ordered commit sequence

C0a `.agent/authored/f261-r18.md`, the block file the delegating message names, by
    `shutil.copyfile`
C0b `.agent/last_block.md`, the same bytes
C1  THE RECORD, one commit: `.agent/plan.md` becomes slice PLAN18; slice RECORD18 is appended to
    `.agent/live_review.md`, slice DEC17 to `.agent/decisions.md` and slice SLIP18 to
    `.agent/prose_slips.md`; in `docs/roadmap/features/T2_F273.md` the bytes of slice P273-FROM
    are replaced by those of slice P273-TO
C2  THE CONTEXT GROUP: copy `.remedy-wt/f261-block/f261-r18-context.jsonl` to
    `.agent/authored/f261-r18-context.jsonl` and apply it per THE TABLES, in one commit
C3  THE TOKEN GROUP WITH CONTEXT-PACK: the same with `f261-r18-token.jsonl`, in one commit
C4  THE REVIEW GROUP AND THE SMOKE SCRIPT'S GROUP LIST: the same with `f261-r18-review.jsonl`,
    in one commit
C5  `.agent/handoff.md`, the handback; then `git push origin feature/f261-cli-vocabulary-v2`

C1 is the FIRST SUBSTANTIVE COMMIT, per item 23 of §3. No pull request is created.

## Change — exactly these paths and no others

C0a to C1: `.agent/authored/f261-r18.md`, `.agent/last_block.md`, `.agent/plan.md`,
`.agent/live_review.md`, `.agent/decisions.md`, `.agent/prose_slips.md` and
`docs/roadmap/features/T2_F273.md`. C2 to C4: each table's own carrier and the paths G3 names.
C5: `.agent/handoff.md`.

## The appends and the pair

RECORD18, DEC17 and SLIP18 each begin with an empty line, and their targets end in a
newline at `43694261`: an append is the file's bytes followed by the slice's bytes, and nothing
else. The pair P273: TO contains FROM: false, so it is a REWRITE; P273-FROM occurs once
in `docs/roadmap/features/T2_F273.md` at `43694261`, and at C1 P273-FROM occurs 0 times and
P273-TO once.

## THE TABLES

Each carrier holds one JSON array per line. Their sha256 digests, to verify before copying:
`f261-r18-context.jsonl` `d8ed7b75a5b2288ffe882beedab6fbb7ab067990d6db406938cc5c4ec3b7c6e0`,
`f261-r18-token.jsonl` `330f85636d66cc569fe46dc51833b0bf0a73b3ab68fc365a1fbcb5eba78c23ee`,
`f261-r18-review.jsonl` `07403106a52d0239b43eca5da42163ba0e0e155df90cbc680b293d5dd13b377a`.
Apply the rows strictly
in file order, each against the tree as the previous rows left it, from the repository root:
`["edit", path, old, new, count]` opens the path with `encoding="utf-8", newline=""`, requires
the number of occurrences of `old` to equal `count` exactly, and replaces every occurrence with
`new`; `["delete", path]` removes the file; `["move", src, dst]` renames the file, whose target
must not exist; `["create", path, content]` writes `content` to a path that must not exist, with
the same encoding and newline setting. A count that differs or a target that exists is a STOP:
touch nothing further, commit nothing of that table, and hand back with the row and the reading.
Stage each commit with `git add -A` after its table and its carrier. The tables are the
reviewer's measured dry run of DECISION F261 D17, applied on top of C1's record: the context
table its CHOSEN FIRST, the token table its CHOSEN SECOND, and the review table its CHOSEN THIRD
with the two rows the reviewer added for the smoke script's group list.

## SPEC S — the suite, once, after G5 and before C5

From the primary checkout's root, serially:
`python3 -B -m pytest -q -p no:randomly -p no:cacheprovider --tb=short -rfEs`, with `PYTHONPATH`,
`REMEDY_PROJECT` and `REMEDY_DATA_DIR` removed and `PYTHONDONTWRITEBYTECODE=1`, output under
`.remedy-wt/f261r18w/`. Report pytest's return code, the run's last output line, and every
distinct bad node, the text after a line-initial `FAILED ` or `ERROR ` up to the first ` - `.
Re-run each bad node alone, once, the same way, and report that return code beside it.

## Constraints

1. NO SLICE AND NO TABLE IS EDITED. Extract each slice as the bytes strictly between its
   `BEGIN <NAME>` and `END <NAME>` lines and verify its sha256 before use.
2. READ `.agent/STOP` before C0a, before C2 and before C5, with real exit codes. If it exists:
   finish a half-written commit, write the handoff, push, stop.
3. A red gate is a STOP: commit what is honestly finished, hand back with the raw output.
4. Scratch, runner scripts and your worktree live under `.remedy-wt/f261r18w/`, uncommitted; no
   `.py` file under `.agent/`. Under `.remedy-wt/` open only `.remedy-wt/f261-block/` and your
   own directory. `git worktree list` reads one row now; leave it so. Create no symlink.
5. Every commit stays under 500 insertions, read as the first column of `git show --numstat
   --format= <commit>` with git's default rename detection.
6. NEVER merge, open a pull request, force-push, rewrite history or delete a branch. No `remedy`.
   Write no `Done:` paragraph and no `Landed:` line.
7. THE BLOCK'S OWN SIZE, measured on its final bytes: 370 lines TOTAL and 271 lines of PROSE,
   against the caps of 490 and 400.
8. GATE ORDER. G1 and G2 after C1; G3, G4 and G5 after C4; then SPEC S, whose result is G6; G7
   after C5 and the push, reported in the completion message only.
9. Every commit message ends with `Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>`, and
   no subject carries a leading-slash token or an absolute path.

## Done when — every gate run for real, its exit code recorded

G1 TRANSPORT. The sha256 of `.agent/authored/f261-r18.md` at C0a equals the digest the delegating
message gives, and `.agent/last_block.md` at C0b is byte-identical to it; the slices FOUND, each
matching its BEGIN-marker sha256; each committed carrier's sha256 equals its digest above.

G2 THE RECORD, at C1. `.agent/plan.md` is byte-identical to PLAN18, at most 50 lines, with
`^## Goal$` once and `^## Next Steps$` once. `.agent/live_review.md` equals its `43694261` blob
followed by RECORD18, `.agent/decisions.md` its `43694261` blob followed by DEC17, and
`.agent/prose_slips.md` its `43694261` blob followed by SLIP18.
`docs/roadmap/features/T2_F273.md` equals its `43694261` blob with the pair P273 applied, with
the counts The appends and the pair give. Over `.agent/live_review.md`: `^Gate: F\d+ R\d+ — `
reads 126 at `43694261` and 127 at C1, with `Gate: F261 R17 — ` once at C1; distinct
`^- R-\d+ — ` ids 110 and 113, C1 minus base exactly `R-0908`, `R-0909` and `R-0910`; distinct `^Done: R-\d+ — ` ids 8
and 8; the open set by distinct id 102 and 105. `python3 -m pytest tests/docs/ -q` exits 0 at C1.

G3 THE TABLES, at C2, C3 and C4. `git diff --no-renames --name-only` from each commit's parent
prints exactly that commit's carrier and: at C2 `apps/cli/command_catalog.py`, `apps/cli/commands/__init__.py`, `apps/cli/commands/context.py`, `docs/guides/do-run-v1.md`, `docs/system/architecture.md`, `docs/system/context-inspector.md`, `packages/orchestration/brain_detail.py`, `packages/orchestration/do_run.py`, `packages/orchestration/token_economy.py`, `scripts/remedy_smoke.sh`, `tests/cli/test_context_inspect_cli.py`, `tests/cli/test_context_inspect_runtime.py`, `tests/orchestration/import_reachability_allowlist.txt`, `tests/orchestration/test_do_run.py`, `tests/orchestration/test_token_economy.py`, `tests/test_command_catalog.py`, `tests/test_context_coverage.py` and `tests/test_project_context_coverage.py`; at C3 `apps/cli/command_catalog.py`, `apps/cli/commands/__init__.py`, `apps/cli/commands/token_cmd.py`, `docs/guides/token-economy-user-guide-v0.md`, `docs/system/token-economy-context-budget-optimizer-v0.md`, `packages/orchestration/token_economy.py`, `tests/cli/test_cli_ux.py`, `tests/cli/test_token_cli.py`, `tests/orchestration/import_reachability_allowlist.txt` and `tests/test_command_catalog.py`; at C4
`apps/cli/command_catalog.py`, `apps/cli/commands/__init__.py`, `apps/cli/commands/dev.py`, `apps/cli/commands/review_cmd.py`, `docs/guides/simple-operator-quickstart-v0.md`, `docs/system/core-product-spine-v0.md`, `docs/system/orchestrator-loop.md`, `packages/orchestration/ui_view_model.py`, `scripts/remedy_smoke.sh`, `tests/cli/test_job_commands.py`, `tests/cli/test_review_cmd.py`, `tests/orchestration/import_reachability_allowlist.txt`, `tests/test_cli_execution_loop_closure.py`, `tests/test_command_catalog.py` and `tests/test_data_paths.py`. `git rev-parse <commit>:<object>` equals the reviewer's dry run, which applied C1's
record before the tables, for `apps`, `tests`, `docs`, `scripts`, `packages` and `README.md` in
that order: C2 `de7e75f66ad6fbae57992d4f0d4226290cc5e5f7`, `7222a99c21e7078850fccf480621874c90175e00`, `31e2b724b03c6e5220fffd5ebdf9d87cde9d1923`, `6314b0d79f5e9a2460c3a22154f06656a67e8f61`, `2365aad43df49bb0895e901df33fa92d966cd8fb`, `15b9e0e8fec9721c7c17a872cc8f1a2bed3a2952`; C3 `fcfb42a7caebdddf412a9fa8460c1d0c79105bb7`, `2d162d7aa1d1e8b2c1b650491a86802b780fe055`, `d244ee0962f4a7b94b1496befeb74274c815222d`, `6314b0d79f5e9a2460c3a22154f06656a67e8f61`, `0a778e160c1b3f097404ed582d115a22198d7643`, `15b9e0e8fec9721c7c17a872cc8f1a2bed3a2952`; C4 `fcec307eb88f40cf88e241874719f1d67134986f`, `bbd5299ed5d8176353e98530b78e88bcba40e04c`, `e2bf8ac067db46dfe88c725c5e8e89233b358446`, `208d836b3d5d6532fe9354d9455ab71c67639ed2`, `bdd606d30705ed68d6e4ad96783661ff319a8dc4`, `15b9e0e8fec9721c7c17a872cc8f1a2bed3a2952`.
Report each commit's insertions per constraint 5.

G4 THE SWEEP, at C4. `git grep -n -I -E 'remedy (context|context-pack|token|review)\b|commands/(context|token_cmd|review_cmd)\.py|apps\.cli\.commands\.(context|token_cmd|review_cmd)\b|_cmd_context_inspect|_cmd_context_pack_recommend|_cmd_token_(budget_show|budget_set|estimate|economy_report)|_cmd_review_(run|list|accept|reject)'
<C4> -- apps packages scripts tests docs README.md AGENTS.md .claude ':!docs/roadmap'` exits 1
and prints nothing. `python3 -m ruff check` over every `.py` path of C2 to C4 that still exists
at C4 exits 0. Every word of the `for grp in` list of section 0 of `scripts/remedy_smoke.sh` at C4
is a key of `GROUPS` in `apps/cli/command_catalog.py` at C4; report the words and the count. At
`43694261` that same reading names 5 words that are not.

G5 THE RED-PROOF, in `git worktree add --detach .remedy-wt/f261r18w/wt <C4's sha>`, each run
through the runner over `tests/test_command_catalog.py`, `tests/cli/test_cli_ux.py`,
`tests/test_grouped_cli.py`, `tests/orchestration/test_import_reachability.py`,
`tests/cli/test_advertised_commands.py` and `tests/test_remedy_smoke_script.py` with
`-rf --tb=no`. Mutation <n> is in the file its line below names, replaces the bytes of slice
MUT-<n>-FROM, whose count there must read 1, with those of slice MUT-<n>-TO, and is restored with
`git -C .remedy-wt/f261r18w/wt checkout -- <that file>`. (a) CONTROL: must exit 0. Each of (1) to
(7) must exit 1 with the named node among the failed nodes:
(1) `apps/cli/commands/dev.py`, a `context` handler row, (2) the same file, a `token` handler
row, and (3) the same file, a `review` handler row: each
`TestDeletedCommands::test_no_deleted_id_is_left_in_the_dispatch_table`; (4)
`apps/cli/command_catalog.py`, the `token` group restored without commands:
`TestCatalogIntegrity::test_every_group_has_at_least_one_command`; (5) the same file, a
`related=` naming `review.list`:
`TestCatalogIntegrity::test_every_related_reference_resolves_to_a_live_command`; (6)
`packages/orchestration/ui_view_model.py`, a `review list` command in the view model:
`test_every_advertised_command_exists_in_the_catalog`; (7) `tests/cli/test_cli_ux.py`, `token`
and `context-pack` named internal groups again:
`TestGroupDefIntegrity::test_internal_groups_marked`.
(8) IS A PROBE, NOT A COLOUR: put `policy`, a group this branch deleted, back into the `for grp
in` list of section 0 of `scripts/remedy_smoke.sh` and run the same selection. Report its exit
code and summary line whatever they are; the reading is evidence for R-0910, which registers
that no guard reads that list, and neither colour is a STOP.
Report each exit code, summary line and number of failed nodes; then
`git worktree remove --force .remedy-wt/f261r18w/wt` and read `git branch --list 'remedy/job-*'`.

G6 THE SUITE, SPEC S at C4: must exit 0 with no bad node; report the last output line. A bad
node whose lone re-run exits 0 is reported as such with both readings, and is not a STOP; a bad
node whose lone re-run fails is.

G7 THE TREE, after C5 and the push. `git status --porcelain` prints `''`; C0a to C5 are
single-parent commits in that order on `43694261`; `git rev-parse HEAD` equals
`git rev-parse origin/feature/f261-cli-vocabulary-v2`; `git worktree list` prints one row, and
`git branch --list 'remedy/job-*'` prints 16 lines.

## The handback, C5

`.agent/handoff.md` per `docs/agents/handback_template.md`, Session line
`SESSION 4 of feature F261 · round 18 · rounds so far 18`, with one sentence of context
self-assessment. `## Commits` lists C0a to C4, each row's `+/-` cell equal to constraint 5's
reading of that commit and its deletions column; C5's own numbers appear nowhere, per item 31 of
§3. `## Verification` gives G1 to G6 with real exit codes. It states the open findings at 105 by
distinct id, with the High ids R-0803, R-0804 and R-0807, and `Operator questions open: 0`. Its
`## Next` names, in order: Phase 1 rule 1; the reviewer's verdict on round 18; `do report`
becoming `run show` and `run list` with `do evidence`, as the inventory proposes.

── SLICE PLAN18 ── target `.agent/plan.md` ── FULL REPLACEMENT ──
BEGIN PLAN18 sha256=a5d4dfc6aefdc42e09104687aa757ea5ce7d1d3190cc3c741965c1a86e0911c3
# Plan — F261 CLI vocabulary v2 (rename & prune)

Branch: feature/f261-cli-vocabulary-v2, cut from `main` at
`7cdde89b5d0dc8ef1fb96980105870e956699873`, the merge commit of pull request 250.

## Goal

The catalog `apps/cli/command_catalog.py` equals DECISION amend0905-vocab D4: one name per
command, and every retired word deleted rather than aliased, per
`docs/roadmap/features/T2_F261.md`.

## Current Step

ROUND 18 continues T003. It books round 17's PASS and a prose slip, registers R-0908 and R-0910
for F273 and R-0909 for this feature and records DECISION F261 D17, then deletes the `context`
group, the `token` group with `context-pack`, and the `review` group, one table per commit, and
takes the groups rounds 16 and 17 deleted out of the smoke script's group-help loop.

## Next Steps

1. `do report` becomes `run show` and `run list`, and `do evidence` goes, as
   `.agent/f261_t003_inventory.md` proposes.
2. The rest of T003 in the inventory's order, each round re-measured before it is authored,
   with R-0767, R-0894 and R-0900.
3. `job budget <id> set` over the run-contract budget fields and the token budget profile, the
   word DECISION amend0905-vocab D4 gives those writes, with R-0906 and R-0909.
4. T004.

## Risks

- 102 findings are open by distinct id before this round's record and 105 after it; three are
  High, R-0803, R-0804 and R-0807.
- The inventory proposes more rounds than F261's soft limit of 25 leaves; the session that
  reaches the limit owes the scope report and the split-and-close default.
- A deletion's consumers include shell strings a guard cannot read, subprocess help calls,
  event readers and the UI event catalog, so every deletion round runs the whole suite on its
  committed tree and re-reads the smoke script.
END PLAN18

── SLICE RECORD18 ── target `.agent/live_review.md` ── APPEND ──
BEGIN RECORD18 sha256=9d8c657980d487916de8c9f1983dede3866fc1127d8330f585265cad1310c5ed

Gate: F261 R17 — the F261 round 17 entry. VERDICT PASS. Written by the planner and reviewer of session 39 after reading the committed range `bf88d647`..`43694261` and re-deriving the readings below; the worker's report was evidence for none of them. It is booked here by the first commit of round 18 that writes the record, per operator amendment amend0827-process-diet rule 1. THE TRANSPORT: `.agent/authored/f261-r17.md` at `09d7dd18` and `.agent/last_block.md` at `a4d1bf03` are byte-identical to the reviewer's scratch original, sha256 `74be83b2d80f3da704da0464a9c4a324d605139376bcab0a68c1fbf0b7740d83`, and the three tables committed at `2f46e267`, `130e68f0` and `23204d61` are byte-identical to the reviewer's, which are the research helper's. THE STATE: at `a0860e35` and again at `43694261`, `.agent/plan.md` equals PLAN17, `.agent/live_review.md` and `.agent/decisions.md` equal their `bf88d647` blobs followed by RECORD17 and DEC16, and `docs/roadmap/features/T2_F273.md` equals its `bf88d647` blob with the pair P273 applied. THE TABLE COMMITS: at `2f46e267`, `130e68f0` and `23204d61` the `apps`, `tests`, `docs`, `scripts`, `packages`, `README.md` and `.claude` objects equal the reviewer's dry-run commits, which applied the record before the tables and reproduced the helper's trees exactly; each commit's `--no-renames` path set is the dry run's plus its carrier, and `git show --numstat` reads 54, 69 and 65 insertions. In the dry run's production diff each group leaves with its handler module, its catalog entries and its tests, `packages/orchestration/autonomy_readiness.py`, `run_contract.py` and `token_policy.py` stay with every production caller that reads them, the guidance card whose import named nothing goes, and every surviving hint that named a deleted command is re-pointed at `job show --full` or `mission readiness` or dropped. The sweep pattern of the round 17 block matches in 21 files at `bf88d647`, and at `43694261` the same `git grep` over `apps`, `packages`, `scripts`, `tests`, `docs` without `docs/roadmap`, `README.md`, `AGENTS.md` and `.claude` exits 1 with no output. In the reviewer's dry run a full suite under `-n auto` without `tests/ui_server` read 1 failed, `test_vitest_passes`, 17350 passed and 29 skipped, and the eight `tests/ui_server` files naming a deleted group read 312 passed. Over `tests/test_command_catalog.py`, `tests/cli/test_cli_ux.py`, `tests/test_grouped_cli.py`, `tests/orchestration/test_import_reachability.py`, `tests/cli/test_advertised_commands.py` and `tests/orchestration/test_event_name_coupling.py`, which passed 416 unmutated, a `readiness`, a `contract` and a `policy` handler row each failed 1 test, the `policy` group restored without commands failed 1, a `related=` naming `policy.contract` failed 1, the readiness node's hint pointed back at the deleted command failed 1, `token_policy_inspected` undeclared failed 1, and `contract` named an internal group again failed 3 with `test_internal_groups_marked` among them. The worker declared that constraint 4 and SPEC S of the block name the previous round's scratch directory while G5 names this round's, and resolved it in favour of G5's literal command; the directories are uncommitted scratch, nothing of the round depended on the name, and the slip is the reviewer's. THE REVIEWER'S RUN in the primary checkout at `43694261` of those six files, every other test file the round edited, the run contract, repair loop, do-continue and test-execution tests, `tests/ui_contracts/`, `tests/orchestration/test_test_runner.py`, `tests/cli/test_golden_path.py`, `tests/docs/`, `tests/orchestration/test_command_discovery.py` and five `tests/ui_server` files read 2428 passed and 4 skipped, `python3 -m ruff check` over nineteen edited files that survive printed `All checks passed!`, and `git branch --list 'remedy/job-*'` read 16 lines. The open set reads 102 by distinct id at `43694261`.

- R-0908 — Medium, DELETING THE `review` GROUP LEAVES THE REVIEWER RECOMMENDATIONS WITH NO WRITER WHILE TWO COCKPIT SURFACES STILL READ THEM, AND NOTHING TURNS A RECOMMENDATION INTO A PROPOSED TASK ANY MORE. Raised by the planner and reviewer of session 39 while preparing F261 round 18, after searching the open set for the reviewer recommendations and the `review` commands under §3 item 30: R-0844 describes `review bundle`, a different command F275 deleted, and no open finding describes these readers. THE DEFECT, read at `43694261` and on the reviewer's dry-run trees: `store_recommendations`, `accept_recommendation` and `reject_recommendation` in `packages/orchestration/reviewer.py` were reachable only from `apps/cli/commands/review_cmd.py`, which this round deletes, while `packages/orchestration/ui_server.py` and `packages/orchestration/ui_view_model.py` still read `job.metadata["reviewer_recommendations"]`, so both render a list nothing fills; `propose_from_recommendation` in `packages/orchestration/proposed_tasks.py` keeps one caller, `reviewer.py`, which no production code calls, so the step that turned a reviewer recommendation into a proposed task has no surface. In the same module `run_reviewer` keeps one production caller, `apps/cli/commands/dev.py`, which only asserts that it is callable for the `reviewer_loop_ok` key of `dev status`, and `_fixture_reviewer` and `list_recommendations` keep callers under `tests/` alone; four exports of `packages/orchestration/token_economy.py` are in the same state after the `token` group goes. WHY MEDIUM: a user-observable step of the operator's loop leaves with no heir, and two cockpit surfaces show an empty list where they used to show its result; nothing prints anything false. WHY F273's: deleting a reader with its cockpit surface, or giving the recommendations a writer, changes surviving surfaces, and deleting a public export with its tests is findings paydown; F261 prunes the catalog. FIX: delete the two cockpit readers with the tests that pin them and the reviewer symbols no surviving surface calls, or give the recommendations a writer on a surviving command and name it in the cockpit; and either way say in `docs/system/` which step of the operator's loop replaced `review accept`. Owner: F273.

- R-0909 — Medium, DELETING `token budget-set` LEAVES THE PER-JOB TOKEN BUDGET PROFILE WITH NO WRITER, SO EVERY JOB SILENTLY RUNS ON THE BUILT-IN DEFAULT WHEREVER THAT PROFILE IS READ. Raised by the planner and reviewer of session 39 while preparing F261 round 18, after searching the open set for the token budget profile under §3 item 30: no open finding describes it, and R-0906, which this finding names, describes the run contract's budget fields rather than this store. THE DEFECT, read at `43694261` and on the reviewer's dry-run trees: `save_token_budget_profile` in `packages/orchestration/token_economy.py` was reachable only from `apps/cli/commands/token_cmd.py`, which this round deletes, while `load_token_budget_profile` keeps reading `budget_profile.json` under a job's workspace for `token_economy_report`, which the cockpit's token-economy section and the run contract's report read; with no writer it returns the built-in default for every job, and `token_economy_integrity` scans a directory nothing fills. WHY MEDIUM: a budget the operator could set per job is now fixed for every job, and a surviving surface reports that default as the job's profile; nothing prints anything false. WHY F261's: the write word DECISION amend0905-vocab D4 gives is `job budget <id> set`, the same word R-0906 needs and the same feature's Goal, so the repair belongs to a later round of this feature. FIX: give `job budget <id> set` the token profile fields beside the run-contract budget fields R-0906 names, with a test that sets one and reads it back through the token economy report, or delete the profile store with its readers and say where a per-job token budget lives instead. Owner: F261.

- R-0910 — Medium, SECTION 0 OF THE SMOKE SCRIPT RUNS EVERY GROUP WORD THROUGH A SHELL VARIABLE, SO NO ADVERTISED-COMMAND GUARD CAN SEE IT, AND ROUNDS 16 AND 17 LEFT FIVE DELETED GROUPS IN IT FOR A ROUND EACH. Raised by the planner and reviewer of session 39 while preparing F261 round 18, after its research helper measured the line and after searching the open set for the smoke script's group help under §3 item 30: no open finding describes it. THE DEFECT, read at `43694261`: `scripts/remedy_smoke.sh` section 0 loops `for grp in job project patch test brain policy worker memory dev readiness file change repo event blocker decision dashboard guide ui do` and runs `remedy "${grp}"`, returning 1 on the first failure, while `policy`, `readiness`, `repo`, `dashboard` and `guide` are the groups F261 rounds 16 and 17 deleted, so the section fails on `policy`; the two regular expressions of `tests/cli/test_advertised_commands.py` need a literal lowercase word after `remedy`, so neither can read a word out of `"${grp}"`, and no other test reads that list against the catalog. The helper measured the blindness directly: restoring `context` to that loop on this round's final tree left the six-file catalog selection and `tests/test_remedy_smoke_script.py` at 574 passed, exit 0. This round's third table takes the five words and the two other stale words out of the loop and out of the line the section prints, so the script's own defect is repaired here. WHY MEDIUM: the operator's smoke script, which `docs/` names as the end-to-end check, exits 1 in its first section on a tree whose suite is green. WHY F273's: the repair that outlives this round is a guard that reads the loop's list against the catalog, which is a test this feature does not own; the stale words themselves are already gone. FIX: pin section 0's group list against `apps/cli/command_catalog.py` — a test that reads the loop's words out of the script and asserts each is a catalog group — so that deleting a group reds a test rather than a smoke run. Owner: F273.
END RECORD18

── SLICE DEC17 ── target `.agent/decisions.md` ── APPEND ──
BEGIN DEC17 sha256=20f95a5b66ecacb1aa4597ec6a56fd01123690ab74ffe41a8761fd4c24e486e3

## DECISION F261 D17 (2026-09-16, F261 round 18) — the deletion paragraph of the `context`, `token`, `context-pack` and `review` groups

CONTEXT. DECISION amend0905-vocab D4 deletes `context`, `context-pack`, `token` and `review`, and `.agent/f261_t003_inventory.md` puts them in its round E. Measured at `43694261` by the reviewer's research helper, which ran all ten commands in process against a scratch data root and found every one of them working, and re-read by the reviewer on the dry-run trees. As in DECISION F261 D13, package code goes with a command only when that command was its only production caller; no package module and no package symbol is deleted this round.

CHOSEN, FIRST: `context`. Deleted: the group, `context.inspect`, `apps/cli/commands/context.py` with its tests, the hints that named the command, and the smoke section that ran it. `packages/orchestration/context_inspector.py` stays for `do run` and the token economy report. THE HEIR: `remedy job context <id> --task <t> --json`, which D4 keeps and which shares no module with the deleted group, and `remedy brain context <id>` for the coverage reading; the inspector's policy gates, readiness status and inclusion reasons have no heir.

CHOSEN, SECOND: `token` with `context-pack`. Deleted: both groups, `token.budget-show`, `token.budget-set`, `token.estimate`, `token.economy-report` and `context-pack.recommend`, the single handler `apps/cli/commands/token_cmd.py` that served both, with its tests, both words as internal groups of `tests/cli/test_cli_ux.py`, and the command fences of the two pages that document the package code, each replaced by a dated paragraph naming the heir. `packages/orchestration/token_economy.py` stays: its estimator and its bands are read by the budget guard, the cost preview, the prompt trace, the context compiler and the cockpit. THE HEIR: the `token_economy` section of a job's cockpit payload under `remedy ui start`; the per-job budget WRITE has no heir, because `job budget <id> set`, the word D4 gives it, is not built, and R-0909 records that for this feature.

CHOSEN, THIRD: `review`. Deleted: the group, `review.run`, `review.list`, `review.accept` and `review.reject`, `apps/cli/commands/review_cmd.py` with its tests, the `remedy review run` line of `dev status`, and the smoke sections that ran the commands, one of which checked a key the command never printed. `packages/orchestration/reviewer.py` stays whole: cutting the symbols only its handlers called would take the `reviewer_loop_ok` key out of `dev status`, which is a surviving command, so R-0908 records them with the two cockpit surfaces that read the recommendations. THE HEIR: `remedy propose list <id>`, which lists the proposed tasks the job runner and the self-use track still write; turning a reviewer recommendation into a proposed task has no heir.

ALSO IN THIS ROUND, NOT A DELETION OF THIS ROUND'S GROUPS: section 0 of `scripts/remedy_smoke.sh` ran `remedy "${grp}"` over a list that still held `policy`, `readiness`, `repo`, `dashboard` and `guide`, the groups rounds 16 and 17 deleted, so the section failed on the first of them; the third table takes those five words out of the loop and out of the line the section prints, and R-0910 records the guard that could not see them.

CONSEQUENCE. `remedy context`, `remedy context-pack`, `remedy token` and `remedy review` are unknown commands and their ids join `TestDeletedCommands`; the reviewer recommendations and the token budget profile are read where nothing writes them, which R-0908 and R-0909 record; and the smoke script's group help runs only groups the catalog holds. HOW TO REVERSE: revert the round's three table commits and delete this section.
END DEC17

── SLICE SLIP18 ── target `.agent/prose_slips.md` ── APPEND ──
BEGIN SLIP18 sha256=16126aa1b3ff0583c361e4437041774e3cbd9036c5fbcf42ab71b230a982ad0d

2026-09-16 · F261 R17 · THE ENVIRONMENT PARAGRAPH, SPEC S and constraint 4 of the round 17 block named `.remedy-wt/f261r16w/` as the round's scratch directory while G5 ordered its worktree under `.remedy-wt/f261r17w/`, because the reviewer adapted the previous round's block with a replacement of the hyphenated form `f261-r16` alone; the worker declared the contradiction and followed G5, and the rule that follows is that adapting a block sweeps every spelling of the round's own number, not the one form the replacement matched.
END SLIP18

── SLICE P273-FROM ── target `docs/roadmap/features/T2_F273.md` ── REWRITE FROM ──
BEGIN P273-FROM sha256=e5e8ab2918efb82416cc6f08bf2ec3c60c2d31d9834e6e14677eb1b37c89a7b2
  test-only exports the commit that deleted it with its tests or the surviving caller that keeps it.

## Do not touch
END P273-FROM

── SLICE P273-TO ── target `docs/roadmap/features/T2_F273.md` ── REWRITE TO ──
BEGIN P273-TO sha256=c62226619845139943db04fc3a3a905ad2b7410cebede60380c38f0caafcd583
  test-only exports the commit that deleted it with its tests or the surviving caller that keeps it.
- R-0908 carries a resolution line naming the commit that deleted the two cockpit readers of the reviewer
  recommendations with their tests, or the commit that gave the recommendations a writer, and the page that
  says what replaced `review accept`.
- R-0910 carries a resolution line naming the test that reads the group list of section 0 of
  `scripts/remedy_smoke.sh` and asserts every word is a group of the catalog.

## Do not touch
END P273-TO

── SLICE MUT-1-FROM ── G5 (1) only ── never a file ──
BEGIN MUT-1-FROM sha256=b80c9cb6a8186d1e0e037407c5cb67f8a716ea462f41563da837cf74561af360
    "dev.status": lambda args: _dev_status(json_output=getattr(args, "json", False)),
}
END MUT-1-FROM

── SLICE MUT-1-TO ── G5 (1) only ── never a file ──
BEGIN MUT-1-TO sha256=4335184d7a4d5497c8c97b38307ef1b1e246f8296bca35a11c85c3d920224891
    "dev.status": lambda args: _dev_status(json_output=getattr(args, "json", False)),
    "context.inspect": lambda args: None,
}
END MUT-1-TO

── SLICE MUT-2-FROM ── G5 (2) only ── never a file ──
BEGIN MUT-2-FROM sha256=b80c9cb6a8186d1e0e037407c5cb67f8a716ea462f41563da837cf74561af360
    "dev.status": lambda args: _dev_status(json_output=getattr(args, "json", False)),
}
END MUT-2-FROM

── SLICE MUT-2-TO ── G5 (2) only ── never a file ──
BEGIN MUT-2-TO sha256=0b07c120b247cb4d4e6b76028b0b6c771c40fbe2edcd6c356d216037c9badd64
    "dev.status": lambda args: _dev_status(json_output=getattr(args, "json", False)),
    "token.estimate": lambda args: None,
}
END MUT-2-TO

── SLICE MUT-3-FROM ── G5 (3) only ── never a file ──
BEGIN MUT-3-FROM sha256=b80c9cb6a8186d1e0e037407c5cb67f8a716ea462f41563da837cf74561af360
    "dev.status": lambda args: _dev_status(json_output=getattr(args, "json", False)),
}
END MUT-3-FROM

── SLICE MUT-3-TO ── G5 (3) only ── never a file ──
BEGIN MUT-3-TO sha256=5e34e8b9a2bdc5e1cc73c6de04f8be0aa57c3955e75831cc72595e6194bfde4e
    "dev.status": lambda args: _dev_status(json_output=getattr(args, "json", False)),
    "review.run": lambda args: None,
}
END MUT-3-TO

── SLICE MUT-4-FROM ── G5 (4) only ── never a file ──
BEGIN MUT-4-FROM sha256=7048056fc379469f4167ab957a64cd68fb2c735884bc490198ed15a47d36a731
    "file": GroupDef("file", "File", "File-level provenance and tracing.", user_facing=False),
END MUT-4-FROM

── SLICE MUT-4-TO ── G5 (4) only ── never a file ──
BEGIN MUT-4-TO sha256=271b9040ae823dd81eb67d321ae7751c2b51a46fc40bf1f99619c52a8b3a60e2
    "file": GroupDef("file", "File", "File-level provenance and tracing.", user_facing=False),
    "token": GroupDef("token", "Token", "Token budgets and estimates.", user_facing=False),
END MUT-4-TO

── SLICE MUT-5-FROM ── G5 (5) only ── never a file ──
BEGIN MUT-5-FROM sha256=2cd882e3544109f710e0a8b3c592d8630ddfb5d26298b828241e8202c83cbe93
        related=("brain.view",),
END MUT-5-FROM

── SLICE MUT-5-TO ── G5 (5) only ── never a file ──
BEGIN MUT-5-TO sha256=cf3f2c793a726ba7bbf7ab5e136d48819b5e9747eee598033023865973550879
        related=("brain.view", "review.list"),
END MUT-5-TO

── SLICE MUT-6-FROM ── G5 (6) only ── never a file ──
BEGIN MUT-6-FROM sha256=bbd5cc27e0ac14ae875d85101e097ac1e7bc378afc27111ab559f1f6b36cb647
            "command": f"remedy job show {job_id} --full --json",
END MUT-6-FROM

── SLICE MUT-6-TO ── G5 (6) only ── never a file ──
BEGIN MUT-6-TO sha256=4b03523f4cfdb3d65571df6379615770078fd51ee162bceb81630eb50d713e61
            "command": f"remedy review list {job_id}",
END MUT-6-TO

── SLICE MUT-7-FROM ── G5 (7) only ── never a file ──
BEGIN MUT-7-FROM sha256=f4b00c8750409a5ba0c85fa53973a145925596c4122b93268e445838f188b5e2
    "snapshot", "integrity",
END MUT-7-FROM

── SLICE MUT-7-TO ── G5 (7) only ── never a file ──
BEGIN MUT-7-TO sha256=90fcb9be42c523cd871e311e882098655e7d2c46d1cbc52d39482cba57a73789
    "token", "context-pack",
    "snapshot", "integrity",
END MUT-7-TO

── SLICE MUT-8-FROM ── G5 (8) only ── never a file ──
BEGIN MUT-8-FROM sha256=558d44041a0673d7e093d529e52678b3f573cf6fcd2f3b88fd3c9762de0e81bc
    for grp in job project patch test brain worker memory dev file change event blocker decision ui do; do
END MUT-8-FROM

── SLICE MUT-8-TO ── G5 (8) only ── never a file ──
BEGIN MUT-8-TO sha256=3a845b9649e2deaaf1c6307b9bff04489cbe9e623cb4b1d3889e6425052b9d7c
    for grp in job project patch test brain policy worker memory dev file change event blocker decision ui do; do
END MUT-8-TO
