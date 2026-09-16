── STEP T003/8 — F261 — ROUND 21 ──
Goal: Book round 20's PASS, register R-0916 to R-0922 for F273, record DECISION F261 D20, then
delete `do continue` with `packages/orchestration/do_continue.py` and the repair-reconcile block
it was the only caller of, and resolve R-0900's group-only advertisements, one table per commit;
run the suite once.

Base commit: `ab748c47`, on `feature/f261-cli-vocabulary-v2`. SESSION 5 of F261. Read AGENTS.md,
docs/agents/self_drive_protocol.md, `.agent/f261_t003_inventory.md`, and DECISION F261 D20 once
C1 has landed it.

THE FRAME RULE, per item 37 of §3, measured over the final bytes: NO LINE of this block that is two or
more characters long is a run of a single repeated character, and every box-drawing rule inside the STEP and SLICE header
lines is exactly two characters long.

ENVIRONMENT: `VAR=x cmd`, `env` and `export` are denied, so set environment in-process; `cp` is
denied, so copy with `shutil.copyfile`; bare `ruff` is denied, so use `python3 -m ruff check`.
Shell loops, `$(...)` and `$?` in a compound command are refused by form, so write such checks
as Python scripts under `.remedy-wt/f261r21w/`, and never name a script after a standard-library
module; a pipe into `tail` hides pytest's exit code. The editable install resolves `apps` and
`packages` to the PRIMARY checkout, so a pytest run inside a worktree goes through a runner
script that changes into the worktree, puts it first on `sys.path` and in `PYTHONPATH`, and
asserts `apps.cli.grouped` loaded from inside it. Never call `run_job` or a runner yourself: a
job run started from inside a checkout creates a `remedy/job-*` branch in it.
`git branch --list 'remedy/job-*'` reads 16 lines now; keep it so. While a deletion is staged
but not committed, `test_every_enumerated_path_exists_in_this_repo` fails; run no suite then.

## Bundle — the ordered commit sequence

C0a `.agent/authored/f261-r21.md`, the block file the delegating message names, by
    `shutil.copyfile`
C0b `.agent/last_block.md`, the same bytes
C1  THE RECORD, one commit: `.agent/plan.md` becomes slice PLAN21; slice RECORD21 is appended to
    `.agent/live_review.md` and slice DEC20 to `.agent/decisions.md`; in `docs/roadmap/features/T2_F273.md` the bytes of slice P273-FROM
    are replaced by those of slice P273-TO
C2  `do continue`: copy `.remedy-wt/f261-block/f261-r21-continue.jsonl` to
    `.agent/authored/f261-r21-continue.jsonl` and apply it per THE TABLES, in one commit
C3  R-0900: the same with `f261-r21-r0900.jsonl`, in one commit
C4  `.agent/handoff.md`, the handback; then `git push origin feature/f261-cli-vocabulary-v2`

C1 is the FIRST SUBSTANTIVE COMMIT, per item 23 of §3. No pull request is created.

## Change — exactly these paths and no others

C0a to C1: `.agent/authored/f261-r21.md`, `.agent/last_block.md`, `.agent/plan.md`,
`.agent/live_review.md`, `.agent/decisions.md` and
`docs/roadmap/features/T2_F273.md`. C2 and C3: each table's own carrier and the paths G3 names.
C4: `.agent/handoff.md`.

## The appends and the pair

RECORD21 and DEC20 each begin with an empty line, and both targets end in a
newline at `ab748c47`: an append is the file's bytes followed by the slice's bytes, and nothing
else. The pair P273: TO contains FROM: false, so it is a REWRITE; P273-FROM occurs once
in `docs/roadmap/features/T2_F273.md` at `ab748c47`, and at C1 P273-FROM occurs 0 times and
P273-TO once.

## THE TABLES

Each carrier holds one JSON array per line. Their sha256 digests, to verify before copying:
`f261-r21-continue.jsonl` `92eb43232502a82646611512ea577442b55e291123feddc54a6bcdb416722f73`,
`f261-r21-r0900.jsonl` `09421a05caeca521dfe981a589ac6f7075dd1542c0c0863244b1fa1c0207073a`.
Apply the rows strictly
in file order, each against the tree as the previous rows left it, from the repository root:
`["edit", path, old, new, count]` opens the path with `encoding="utf-8", newline=""`, requires
the number of occurrences of `old` to equal `count` exactly, and replaces every occurrence with
`new`; `["delete", path]` removes the file; `["move", src, dst]` renames the file, whose target
must not exist; `["create", path, content]` writes `content` to a path that must not exist, with
the same encoding and newline setting. A count that differs or a target that exists is a STOP:
touch nothing further, commit nothing of that table, and hand back with the row and the reading.
Stage each commit with `git add -A` after its table and its carrier. The tables are the
reviewer's measured dry run of DECISION F261 D20, applied on `ab748c47` in the reviewer's own
worktree: the continue table its CHOSEN FIRST, the R-0900 table its CHOSEN SECOND. The R-0900
table's new guard is RED until the continue table has landed, which is why C2 precedes C3.

## SPEC S — the suite, once, after G5 and before C4

From the primary checkout's root, serially:
`python3 -B -m pytest -q -p no:randomly -p no:cacheprovider --tb=short -rfEs`, with `PYTHONPATH`,
`REMEDY_PROJECT` and `REMEDY_DATA_DIR` removed and `PYTHONDONTWRITEBYTECODE=1`, output under
`.remedy-wt/f261r21w/`. Report pytest's return code, the run's last output line, and every
distinct bad node, the text after a line-initial `FAILED ` or `ERROR ` up to the first ` - `.
Re-run each bad node alone, once, the same way, and report that return code beside it.

## Constraints

1. NO SLICE AND NO TABLE IS EDITED. Extract each slice as the bytes strictly between its
   `BEGIN <NAME>` and `END <NAME>` lines and verify its sha256 before use.
2. READ `.agent/STOP` before C0a, before C2 and before C4, with real exit codes. If it exists:
   finish a half-written commit, write the handoff, push, stop.
3. A red gate is a STOP: commit what is honestly finished, hand back with the raw output.
4. Scratch, runner scripts and your worktree live under `.remedy-wt/f261r21w/`, uncommitted; no
   `.py` file under `.agent/`. Under `.remedy-wt/` open only `.remedy-wt/f261-block/` and your
   own directory. `git worktree list` reads one row now; leave it so. Create no symlink.
5. Every commit stays under 500 insertions, read as the first column of `git show --numstat
   --format= <commit>` with git's default rename detection.
6. NEVER merge, open a pull request, force-push, rewrite history or delete a branch. No `remedy`.
   Write no `Done:` paragraph and no `Landed:` line.
7. THE BLOCK'S OWN SIZE, measured on its final bytes: 365 lines TOTAL and 248 lines of PROSE,
   against the caps of 490 and 400, where PROSE is every line that is not a line of slice CONTENT — the
   `BEGIN` and `END` marker lines count as prose.
8. GATE ORDER. G1 and G2 after C1; G3, G4 and G5 after C3; then SPEC S, whose result is G6; G7
   after C4 and the push, reported in the completion message only.
9. Every commit message ends with `Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>`, and
   no subject carries a leading-slash token or an absolute path.

## Done when — every gate run for real, its exit code recorded

G1 TRANSPORT. The sha256 of `.agent/authored/f261-r21.md` at C0a equals the digest the delegating
message gives, and `.agent/last_block.md` at C0b is byte-identical to it; the slices FOUND, each
matching its BEGIN-marker sha256; each committed carrier's sha256 equals its digest above.

G2 THE RECORD, at C1. `.agent/plan.md` is byte-identical to PLAN21, at most 50 lines, with
`^## Goal$` once and `^## Next Steps$` once. `.agent/live_review.md` equals its `ab748c47` blob
followed by RECORD21 and `.agent/decisions.md` its `ab748c47` blob followed by DEC20.
`docs/roadmap/features/T2_F273.md` equals its `ab748c47` blob with the pair P273 applied, with
the counts The appends and the pair give. Over `.agent/live_review.md`: `^Gate: F\d+ R\d+ — `
reads 129 at `ab748c47` and 130 at C1, with `Gate: F261 R20 — ` 0 times at `ab748c47` and once
at C1; distinct `^- R-\d+ — ` ids 118 and 125, C1 minus base exactly `R-0916` through `R-0922`;
distinct `^Done: R-\d+ — ` ids 8 and 8; the open set by distinct id 110 and 117.
`python3 -m pytest tests/docs/ -q` exits 0 at C1.

G3 THE TABLES, at C2 and C3. `git diff --no-renames --name-only` from each commit's parent
prints exactly that commit's carrier and, at C2, these paths: `README.md`, `apps/cli/command_catalog.py`, `apps/cli/commands/do_cmd.py`, `docs/README.md`, `docs/guides/do-continue-v1.md`, `docs/guides/do-run-v1.md`, `docs/system/operator-cockpit-v1.md`, `docs/system/provider-patch-materialization-v0.md`, `docs/system/real-test-execution-v1.md`, `docs/system/repair-loop-v0.md`, `docs/system/repair-loop-v1.md`, `docs/system/repair-request-builder-v0.md`, `docs/system/self-dogfood-execution-v0.md`, `docs/system/self-dogfood-v0.md`, `docs/system/snapshot-rollback-v1.md`, `packages/orchestration/do_continue.py`, `packages/orchestration/mission_readiness.py`, `packages/orchestration/provider_patch_material.py`, `packages/orchestration/repair_loop.py`, `packages/orchestration/repair_request_builder.py`, `packages/orchestration/repository_snapshot.py`, `packages/orchestration/run_contract.py`, `packages/orchestration/self_dogfood.py`, `packages/orchestration/self_dogfood_execution.py`, `tests/cli/test_do_continue_cli.py`, `tests/orchestration/import_reachability_allowlist.txt`, `tests/orchestration/test_do_continue.py`, `tests/orchestration/test_fence_e2e.py`, `tests/orchestration/test_fence_production_e2e.py`, `tests/orchestration/test_mission_readiness.py`, `tests/orchestration/test_repair_apply_cycle.py`, `tests/orchestration/test_repair_request_builder.py`, `tests/test_command_catalog.py`; and at C3 these: `docs/system/architecture.md`, `docs/system/vocabulary.md`, `packages/orchestration/brain_detail.py`, `packages/orchestration/flight_plan.py`, `packages/orchestration/orchestrator_loop.py`, `tests/cli/test_advertised_commands.py`.
`git rev-parse <commit>:<object>` equals the reviewer's dry run — which applied the two tables on
`ab748c47` itself, the record touching none of these objects — for `apps`, `packages`, `scripts`,
`tests`, `docs/guides`, `docs/system`, `docs/README.md`, `README.md` and `.claude` in that order:
C2 `10f52eca546afa604e2a61097af80339aeb2c872`, `47723c13f7cae9344910f66e7a7c65c67d38d8ef`, `208d836b3d5d6532fe9354d9455ab71c67639ed2`, `2628d401beab9b11b63f035607de3f543d9749b2`, `f45f164ae4ce579c42d8b4d707b010f281eeb261`, `7feec2429c3ece0ebc5d342435a1a565d33ee7ac`, `5fb479b19503fdfc63639c89f16a431d8c0e7e0f`, `60ca9975fc7ee622c78aaf9e61219ab89e210233`, `e3cd5e0ac262f3f993506e95825e270e39c03ec0`; C3 `10f52eca546afa604e2a61097af80339aeb2c872`, `973237d23fa4023b631cef7fe775da8a3cf20b1e`, `208d836b3d5d6532fe9354d9455ab71c67639ed2`, `185416da1efd33629973fe4fd14d70d08aa2b0bc`, `f45f164ae4ce579c42d8b4d707b010f281eeb261`, `ea4ece6386208842c2860c698ea8f99dc31fe586`, `5fb479b19503fdfc63639c89f16a431d8c0e7e0f`, `60ca9975fc7ee622c78aaf9e61219ab89e210233`, `e3cd5e0ac262f3f993506e95825e270e39c03ec0`.
Report each commit's insertions per constraint 5.

G4 THE SWEEP, at C3. `git ls-tree <C3> -- packages/orchestration/do_continue.py` prints nothing.
`git grep -n -I -E '_cmd_do_continue|run_do_continue|ContinueRequest|ContinueStopReason|ContinuationLease|evaluate_continue_eligibility|summarize_continue_result|reconcile_repair_after_continue|RepairReconcileResult|find_attempt_by_repair_intent|resolve_failure_if_repaired|REPAIR_APPLY_EVENTS|remedy do continue|remedy do --continue'
<C3> -- apps packages scripts tests docs README.md AGENTS.md .claude ':!docs/roadmap'
':!docs/archive' ':!docs/guides/do-continue-v1.md'` exits 0 and prints exactly three lines, in
`docs/system/repair-loop-v1.md`, `tests/cli/test_advertised_commands.py` and
`tests/orchestration/test_self_dogfood_execution.py`, one each; the same command at `ab748c47`
exits 0 and prints 117 lines in 21 files. Report both line counts and the three surviving lines
verbatim. `python3 -m ruff check` over every `.py` path of C2 and C3 that still exists at C3
exits 0; report how many paths that was.

G5 THE RED-PROOF, in `git worktree add --detach .remedy-wt/f261r21w/wt <C3's sha>`, each run
through the runner over `tests/test_command_catalog.py`, `tests/cli/test_advertised_commands.py`,
`tests/docs/test_named_source_paths.py`, `tests/cli/test_cli_ux.py`, `tests/test_grouped_cli.py`
and `tests/orchestration/test_import_reachability.py` with `-rf --tb=no`. Mutation <n> is in the
file its line below names, replaces the bytes of slice MUT-<n>-FROM, whose count there must read
1, with those of slice MUT-<n>-TO, and is restored with `git -C .remedy-wt/f261r21w/wt checkout
-- <that file>`. (a) CONTROL: must exit 0. Each of (1) to (6) must exit 1 with the named node
among the failed nodes:
(1) `apps/cli/commands/do_cmd.py`, a `do.continue` dispatch row:
`TestDeletedCommands::test_no_deleted_id_is_left_in_the_dispatch_table`; (2)
`apps/cli/command_catalog.py`, a `do.continue` catalog entry:
`TestDeletedCommands::test_no_deleted_id_is_left_in_the_catalog`; (3)
`packages/orchestration/self_dogfood_execution.py`, the `remedy do continue` hint restored:
`test_every_advertised_command_exists_in_the_catalog`; (4)
`packages/orchestration/brain_detail.py` and (5) `docs/system/architecture.md`, the group-only
`remedy brain` form restored: `test_every_group_only_advertisement_reaches_a_command`; (6)
`docs/guides/do-continue-v1.md`, the deleted module's path restored into the status banner:
`test_every_source_path_an_operator_facing_page_names_exists`.
Report each exit code, summary line and number of failed nodes; then
`git worktree remove --force .remedy-wt/f261r21w/wt` and read `git branch --list 'remedy/job-*'`.

G6 THE SUITE, SPEC S at C3: must exit 0 with no bad node; report the last output line. A bad
node whose lone re-run exits 0 is reported as such with both readings, and is not a STOP; a bad
node whose lone re-run fails is.

G7 THE TREE, after C4 and the push. `git status --porcelain` prints `''`; C0a to C4 are
single-parent commits in that order on `ab748c47`; `git rev-parse HEAD` equals
`git rev-parse origin/feature/f261-cli-vocabulary-v2`; `git worktree list` prints one row, and
`git branch --list 'remedy/job-*'` prints 16 lines.

## The handback, C4

`.agent/handoff.md` per `docs/agents/handback_template.md`, Session line
`SESSION 5 of feature F261 · round 21 · rounds so far 21`, with one sentence of context
self-assessment. `## Commits` lists C0a to C3, each row's `+/-` cell equal to constraint 5's
reading of that commit and its deletions column; C4's own numbers appear nowhere, per item 31 of
§3. `## Verification` gives G1 to G6 with real exit codes. It states the open findings at 117 by
distinct id, with the High ids R-0803, R-0804 and R-0807, and `Operator questions open: 0`. Its
`## Next` names, in order: Phase 1 rule 1; the reviewer's verdict on round 21 with the `Done:`
paragraph R-0900 is owed once that verdict is taken; and round I of
`.agent/f261_t003_inventory.md`, the `propose` and `repair` groups.

── SLICE PLAN21 ── target `.agent/plan.md` ── FULL REPLACEMENT ──
BEGIN PLAN21 sha256=e0018978eaaf2eff776e8fae64c154e82e2b540e64c3b4dd1eb14d241f5ee01f
# Plan — F261 CLI vocabulary v2 (rename & prune)

Branch: feature/f261-cli-vocabulary-v2, cut from `main` at
`7cdde89b5d0dc8ef1fb96980105870e956699873`, the merge commit of pull request 250.

## Goal

The catalog `apps/cli/command_catalog.py` equals DECISION amend0905-vocab D4: one name per
command, and every retired word deleted rather than aliased, per
`docs/roadmap/features/T2_F261.md`.

## Current Step

ROUND 21 continues T003. It books round 20's PASS, registers R-0916 to R-0922 for F273 and
records DECISION F261 D20, then deletes `do continue` with its module and the repair-reconcile
block it was the only caller of, and repairs the group-only advertisements of R-0900 with a
guard that measures them.

## Next Steps

1. The `propose` and `repair` groups, as `.agent/f261_t003_inventory.md` proposes in its round I,
   each re-measured before it is authored.
2. The rest of T003 in the inventory's order, with R-0767 and R-0894.
3. `job budget <id> set` over the run-contract budget fields and the token budget profile, the
   word DECISION amend0905-vocab D4 gives those writes, with R-0906 and R-0909.
4. T004, which owes the visible group order of D4 and the README quickstart of R-0895.

## Risks

- 110 findings are open by distinct id before this round's record and 117 after it; three are
  High, R-0803, R-0804 and R-0807.
- The feature's soft limit of 25 rounds leaves four after this one, and the inventory proposes
  more than four; the session that reaches the limit owes the scope report and executes the
  split-and-close default of operator amendment amend0905-throughput, placing the follow-up
  feature directly after F261 per amend0906.
- Every deletion of a `do` word is measured against its heir on a fixture before it is authored,
  because six of this round's capabilities turned out to have no heir or a partial one.
END PLAN21

── SLICE RECORD21 ── target `.agent/live_review.md` ── APPEND ──
BEGIN RECORD21 sha256=326b2388b8ec0c5f3d700716eba9996903a8e9e9e43e5c810741502c5746fc91

Gate: F261 R20 — the F261 round 20 entry. VERDICT PASS. Written by the planner and reviewer of session 39 after reading the committed range `71cba20e`..`7c0de436` and re-deriving the readings below; the worker's report was evidence for none of them. It is carried by `.agent/handoff.md` in the session-close commit that follows `7c0de436` and booked by the first commit of round 21 that writes the record, per operator amendment amend0827-process-diet rule 1. THE TRANSPORT: `.agent/authored/f261-r20.md` at `6e3405ba` and `.agent/last_block.md` at `00bef4fc` are byte-identical to the reviewer's scratch original, sha256 `713761a2d0a064666e021dd54249fec39e325d8b352760977530016ee5bb9085`, and the three tables committed at `c26c3a1a`, `f6c723b8` and `bab42400` are byte-identical to the reviewer's, which are the research helper's. THE STATE: at `893a9a95` and again at `7c0de436`, `.agent/plan.md` equals PLAN20, `.agent/live_review.md` and `.agent/decisions.md` equal their `71cba20e` blobs followed by RECORD20 and DEC19, and `docs/roadmap/features/T2_F273.md` equals its `71cba20e` blob with the pair P273 applied. THE TABLE COMMITS: at `c26c3a1a`, `f6c723b8` and `bab42400` the `apps`, `tests`, `docs`, `scripts`, `packages`, `README.md` and `.claude` objects equal the reviewer's dry-run commits, which applied the record before the tables and reproduced the helper's trees exactly; each commit's `--no-renames` path set is the dry run's plus its carrier, and `git show --numstat` reads 7, 21 and 20 insertions. In the dry run's production diff each command leaves with its catalog entry and its handler, `collect_diff_stat` leaves with the handler that was its only caller, `attest_operator_repair`, `resume_job_plan`, `replan` and `ReplanRejectedError` stay behind the test files that drive them, and the six rejections that named `do replan` name no command rather than a deleted one. The sweep pattern of the round 20 block matches 30 lines in 11 files at `71cba20e`, and at `7c0de436` the same `git grep` over `apps`, `packages`, `scripts`, `tests`, `docs` without `docs/roadmap`, `README.md`, `AGENTS.md` and `.claude` exits 1 with no output. In the reviewer's dry run a full suite under `-n auto` without `tests/ui_server` read 1 failed, `test_vitest_passes`, 17268 passed and 29 skipped. Over `tests/test_command_catalog.py`, `tests/cli/test_cli_ux.py`, `tests/test_grouped_cli.py`, `tests/orchestration/test_import_reachability.py` and `tests/cli/test_advertised_commands.py`, which passed 395 unmutated, a `do.repair-attest`, a `do.job-resume` and a `do.replan` handler row each failed 1 test, a `related=` naming `do.job-resume` failed 1, and the `do replan` line restored after the rejection failed 1. THE LINT EXCEPTION the block named reads as the block states it: `python3 -m ruff check` over `tests/orchestration/test_prompt_trace.py` exits 1 with two `I001` findings at `7c0de436`, and the same command over that file's `71cba20e` blob through `--stdin-filename` exits 1 with the same two findings ten lines lower, so the round neither caused nor repaired them. THE REVIEWER'S RUN in the primary checkout at `7c0de436` of those five files, every other test file the round edited, the worktree-integrity, flight-plan, decision-command, manual-completion-bundle and job-evidence tests, `tests/cli/test_golden_path.py`, `tests/docs/`, `tests/test_remedy_smoke_script.py` and `tests/orchestration/test_command_discovery.py` read 1319 passed, `python3 -m ruff check` over thirteen edited files that survive printed `All checks passed!`, and `git branch --list 'remedy/job-*'` read 16 lines. The open set reads 110 by distinct id at `7c0de436`.

- R-0916 — Medium, THE ONE-WORD CONTINUATION CYCLE LEAVES WITH NO HEIR, AND ITS LEASE AND ITS DURABLE PHASE CHECKPOINTS HAVE NO SURVIVING WRITER AT ALL. Raised by the planner and reviewer of session 40 while preparing F261 round 21, from readings its research helper took at the base tree, the reviewer having re-applied and re-measured the deletion itself, after searching the open set for the continuation, the lease and the checkpoints under §3 item 30: no open finding describes them, and R-0900, which this round resolves, names the printed hints rather than the capability. THE DEFECT, read at `ab748c47`: `run_do_continue` in `packages/orchestration/do_continue.py` ran eligibility, a verified snapshot, an apply, a real test and a proof as ONE operator word, holding a `flock`-keyed lease over job, repository and intent with the stop reason `lease_unavailable`, and writing a durable phase ledger under `workspaces/<job>/do_continue/checkpoints.json`; `_cmd_do_continue` was its only production caller, and this round deletes both under DECISION amend0905-vocab D4. The helper measured the surviving words against one scratch data root and one scratch repository: `patch apply` applies idempotently and writes the same snapshot manifest, `test run` runs the budget-gated test, and `change proof --json` returns the same `verified` or `failed` verdict the cycle returned — so the OUTCOME survives in three commands. Nothing surviving takes a lease, and a second continuation of the same job in the same repository is no longer refused; nothing writes a phase checkpoint, so a crash between the three commands is invisible to the next one; in the helper's measurement a second run of the cycle read `snapshot resumed`, `apply resumed` and `test resumed` and consumed no second test budget. WHY MEDIUM: a user-observable composition and its concurrency guard leave with no replacement; every individual phase still works and nothing prints anything false. WHY F273's: giving the composition a word again, or ruling that three commands are the answer and deleting the lease and checkpoint code paths that now have no caller, changes surviving surfaces; F261 prunes the catalog. FIX: either build the cycle behind a surviving word with a test that proves the lease refuses a concurrent second run, or record a DECISION that the three commands are the cycle, and in that case give `patch apply` a printed next action naming `test run` with the ids of R-0917. Owner: F273.

- R-0917 — Low, AFTER `do continue` NOTHING CARRIES AN APPLY'S IDS INTO THE TEST RUN THAT VERIFIES IT, THOUGH `test run` STILL DECLARES ALL THREE FLAGS. Raised by the planner and reviewer of session 40 while preparing F261 round 21, after searching the open set for the linkage, `linked_apply_id` and `linked_intent_id` under §3 item 30: no open finding describes it, and R-0916 records the loss of the cycle rather than of the identity it passed. THE DEFECT, read at `ab748c47`: `run_do_continue` built its `TestExecutionRequest(job_id=…, source='do_continue_v1', task_id=…, intent_id=…, apply_id=…)`, so the test run that verified an apply carried that apply's identity, and the helper measured that a standalone `remedy test run <job> --json` on the same fixture returns `linked_apply_id`, `linked_intent_id` and `linked_task_id` all empty. The surviving command CAN carry them: the `test.run` entry of `apps/cli/command_catalog.py` declares `--task-id`, `--intent-id` and `--apply-id`, and `apps/cli/commands/test_cmds.py` passes all three into the request. What is gone is the automatic step — `patch apply` prints no next action naming them, so an operator must copy three ids by hand, and `change proof` still reports `verified` without the linkage, so nothing makes the omission visible. WHY LOW: the capability survives behind flags a live command declares, and only the hint that would make it usable is missing. WHY F273's: printing a next action is a change to what a surviving command does, which F261 does not make. FIX: have the apply path print `remedy test run <job> --intent-id <id> --apply-id <id>` as its next safe action, with a test that asserts the three ids the apply record carries appear in it. Owner: F273.

- R-0918 — Medium, THE REPAIR-RECONCILE BLOCK LEAVES WITH ITS ONLY CALLER, SO NO REPAIR ATTEMPT REACHES `tested_passed` AND NO FAILURE IS EVER MARKED RESOLVED AGAIN. Raised by the planner and reviewer of session 40 while preparing F261 round 21, after searching the open set for the repair reconciliation and the repair statuses under §3 item 30: no open finding describes it, and R-0908, which records the reviewer recommendations losing their writer, names a different module. THE DEFECT, read at `ab748c47`: `reconcile_repair_after_continue` in `packages/orchestration/repair_loop.py` heads a block that also holds `REPAIR_APPLY_EVENTS`, `RepairReconcileResult`, `find_attempt_by_repair_intent`, `resolve_failure_if_repaired` and `_link_new_failure`; it moved a repair attempt to `tested_passed` or `tested_failed`, resolved the original failure only on `expected_effect == source_fix` with a verified snapshot, a linked passing test, complete evidence and a verified proof, and linked a post-repair failure to its attempt. The reviewer measured its reach with `git grep` over `apps`, `packages`, `scripts` and `tests` at `ab748c47`: `do_continue.py` was the only caller of any symbol in the block, production or test, so inventory ruling 1 takes the whole block with the command, and `tests/orchestration/test_repair_apply_cycle.py` reached it only through `run_do_continue`. The three event names the block emitted have no surviving reader, measured by the same grep, so no dead coupling is created here. The statuses stay defined: `RepairStatus.APPLIED`, `TESTED_PASSED`, `TESTED_FAILED` and `EVIDENCE_INCOMPLETE` remain in the enum and in the terminal-status set, and nothing sets them any more. WHY MEDIUM: a repair attempt applied through `patch apply` stays `approval_required` for ever and the failure it repaired is never recorded as resolved, so the repair loop's own truth stops being written. WHY F273's: recording repair truth from the surviving apply path is a change to what a surviving command does. FIX: either call a reconciliation from the apply path with a test that drives a repair intent to `tested_passed` and its failure to resolved, or delete the four unreachable statuses and say in `docs/system/repair-loop-v1.md` that a repair attempt has no post-apply state. Owner: F273.

- R-0919 — Low, THE COCKPIT `continuation` SECTION STILL FILTERS `do_continue_stopped`, AN EVENT NOTHING EMITS AFTER THIS ROUND, SO ITS LAST RESULT AND STOP REASON READ EMPTY ON EVERY JOB. Raised by the planner and reviewer of session 40 while preparing F261 round 21, after searching the open set for the cockpit continuation section and the event under §3 item 30: no open finding describes it; R-0905 and R-0907 record the same CLASS for `git_status_read` and for `run_contract_inspected` with `token_policy_inspected`, and name neither this event nor this reader. THE DEFECT, read at `ab748c47`: `_build_continuation_section` in `packages/orchestration/ui_server.py` filters the job's events for `do_continue_stopped` and is called as the `continuation` key of the job dashboard payload; `packages/orchestration/do_continue.py` was the only emitter of that name, measured by `git grep` over `apps`, `packages` and `scripts` at `ab748c47`, which returns `ui_server.py` alone once the emitting module is excluded. The section's other half stays live: `available` is a light check over approved intents that `patch approve` still writes, so the section is not empty, and `apps/ui/src/api/remedyApi.ts` and `types.ts` still map it while no React component reads it. The section is KEPT this round rather than deleted, because inventory ruling 2 binds a cockpit ROUTE whose payload is a deleted command's output and this is a payload KEY with a live half — the reading DECISION F261 D13 took for the orchestrator section, R-0903. WHY LOW: two fields of one cockpit section go permanently empty; nothing prints anything false and no other surface is affected. WHY F273's: deleting the dead half, or giving it a writer, changes a surviving surface. FIX: either delete the event half of the section with its client mapping and its two fixtures in `tests/ui_server/test_dashboard_cockpit_truth.py`, or give the surviving apply path an event the section reads. Owner: F273.

- R-0920 — Medium, THE EVENT-NAME COUPLING RATCHET RECOVERS NO EVENT NAME FROM A MODULE THAT EMITS THROUGH A HELPER, SO THIS ROUND'S DEAD COUPLING CANNOT BE DECLARED AND DECLARING IT REDS THE RATCHET. Raised by the planner and reviewer of session 40 while preparing F261 round 21, after searching the open set for the ratchet and the dead couplings under §3 item 30: R-0832 asked for the second measurement beside the import map and the ratchet is that measurement, R-0905 and R-0907 declared couplings THROUGH it, and no open finding says the instrument is blind. THE DEFECT, measured by the reviewer at `ab748c47` by calling the ratchet's own `_emitted_names` over the blobs it would read: `EMIT_FUNCS` in `tests/orchestration/test_event_name_coupling.py` is `{log, _emit, emit, log_event, write_event, record_event}` and the name must be a string constant in FIRST positional position, while `packages/orchestration/do_continue.py` emits all eight of its names through `_emit_continue(data_dir, job_id, event, metadata)` — wrong function name and third position — so the ratchet recovers the empty set from a module carrying 24 literal event-name lines, and `packages/orchestration/repair_loop.py` likewise recovers the empty set. The consequence is not only silence: the reviewer declared `do_continue_stopped` in `KNOWN_DEAD_EVENT_COUPLINGS` with the ceiling raised to 5 inside a disposable worktree at its dry-run tip and ran the file, which exited 1 with `TestEventNameCouplingRatchet::test_no_declared_entry_is_stale` reporting `these are no longer dead couplings and must leave the list: ['do_continue_stopped']`, because `dead_event_couplings` derives its own set from the same blind recovery. So the declaration DECISION F261 D16 and D17 established as this feature's practice is unavailable here, and the coupling is recorded as R-0919 instead. WHY MEDIUM: a gate over production code is shown blind on the exact class it was built to catch, and it reports green over it. WHY F273's: widening the recovery is a repair to a guard and will surface couplings from every module this branch and its predecessors deleted, which is more than one round. FIX: recover an event name from any positional slot of a call whose name ends in `emit` or which the module uses as its emit helper, re-measure the dead set over the whole deleted corpus, declare what appears and raise the ceiling once, with a test that the recovery finds a name a helper emits. Owner: F273.

- R-0921 — Medium, `test run --intent-id` IS REFUSED FOR EVERY JOB, BECAUSE ITS LINKAGE GATE READS AN ARTIFACT METADATA KEY NOTHING IN THE REPOSITORY WRITES. Raised by the planner and reviewer of session 40 while preparing F261 round 21, from a defect its research helper hit while probing the continuation cycle, after searching the open set for the linkage gate and `patch_intents` under §3 item 30: no open finding describes it. THE DEFECT, read and then run by the reviewer at `ab748c47`: `_validate_linkage` in `packages/orchestration/test_execution_service.py` collects `known_intents` from `art.metadata.get('patch_intents')` over the job's artifacts and refuses any supplied `intent_id` outside it with `gate='linkage'`; `git grep` over `apps`, `packages`, `scripts` and `tests` shows that key is READ there and WRITTEN nowhere — the applier writes `patch_intent_apply_records` and the approval path writes `patch_intent_explanations` and `patch_intent_approvals` — and the two other occurrences, in `context_coverage.py` and `project_context_coverage.py`, are a coverage SIGNAL key and not artifact metadata. The reviewer built a job carrying one minted intent and called the function directly: it returned `allowed=False`, `gate='linkage'`, `reason="intent_id '77e3a924-0' not found in job"`, with the collected set empty. So `remedy test run <job> --intent-id <id>` is refused for every job and every id, which is exactly the flag R-0917 asks an operator to start using. The suite never saw it: the deleted `tests/orchestration/test_do_continue.py` monkeypatched `execute_test_run`, and no surviving test supplies an intent id to the real function. WHY MEDIUM: a declared flag of a live command is unusable in every case, and the gate that refuses it reports a linkage failure rather than its own missing writer. WHY F273's: the repair is inside `test_execution_service.py`, a module F261 does not touch. FIX: resolve a supplied intent id against the key the approval path really writes, or write `patch_intents` where an intent is minted, and pin it with a test that runs the real `execute_test_run` with an intent id of a job that has one. Owner: F273.

- R-0922 — Medium, `do run` READS A `--yes` ITS CATALOG ENTRY DOES NOT DECLARE, SO THE F034 AUTO-APPROVE BRANCH CANNOT BE ENTERED FROM THE COMMAND LINE AND THE FLAG EXITS 2. Raised by the planner and reviewer of session 40 while preparing F261 round 21, from a reading its research helper took while harvesting advertised flags for R-0900, after searching the open set for `--yes` and the auto-approve path under §3 item 30: R-0891 names `--yes` only as one of the flags F275 round 34 moved onto `job resume`, and R-0851 names an approval policy, so no open finding describes this. THE DEFECT, read by the reviewer at `ab748c47`: the `do.run` entry of `apps/cli/command_catalog.py` declares no `--yes` among its arguments, while the `do.run` dispatch row of `apps/cli/commands/do_cmd.py` passes `yes=getattr(args, 'yes', False)` into the handler, so the value is False on every invocation; the branch it guards calls `auto_approve_flight_plan` and labels the plan `approved via --yes`, and it is therefore unreachable from the CLI. Because the parser is built from the catalog, the flag the branch is named after is an unrecognized argument. WHY MEDIUM: a documented unattended behaviour of the repository's main command cannot be reached at all, and the code that implements it sits on disk looking live. WHY F273's: deciding whether `do run` regains an unattended approval or loses the branch changes what a surviving command does, and DECISION amend0905-vocab D4 gives F261 the catalog rather than the behaviour. FIX: either declare `--yes` on `do.run` with a test that a bare run with the flag reaches `auto_approve_flight_plan`, or delete the branch and the parameter with the assumption-log text that names them. Owner: F273.
END RECORD21

── SLICE DEC20 ── target `.agent/decisions.md` ── APPEND ──
BEGIN DEC20 sha256=894801ccc9db8c9bceee29913e1912f14ebb36c21515d111e8c21d53ece386eb

## DECISION F261 D20 (2026-09-16, F261 round 21) — the deletion paragraph of `do continue`, and the group-only advertisement guard R-0900 asks for

CONTEXT. DECISION amend0905-vocab D4 leaves `do` with an order and its flags and deletes every other word under it, and `.agent/f261_t003_inventory.md` puts `do continue` in its round H together with finding R-0900, whose fix clause asks that each advertised line name a command the catalog carries and that a test cover the group-only form. Measured at `ab748c47` by two of the reviewer's research helpers in their own detached worktrees, each running the command and its proposed heirs in process against one scratch data root and a scratch repository, and re-applied and re-measured by the reviewer on its own dry-run tree. As in DECISION F261 D13 and D19, package code goes with a command when that command was its only production caller; a symbol whose surviving callers are tests stays and the loss is registered instead.

CHOSEN, FIRST: `do continue` goes, with `_cmd_do_continue`, its catalog entry, `packages/orchestration/do_continue.py`, and the repair-reconcile block of `packages/orchestration/repair_loop.py` that module was the only caller of, with the four test files that reached them. THE HEIR: `remedy patch apply <job> <intent>`, then `remedy test run <job>`, then `remedy change proof <job> --json`, which the helper measured to reach the same `verified` or `failed` verdict on the same fixture; a failed test still reaches `remedy repair start`. The printed hints and doc lines that named the deleted word are re-pointed at `patch apply`, which is what `change proof` already recommends, and the two that no single command answers name none. What the three commands do NOT reproduce — the lease, the phase checkpoints, the apply-to-test linkage, the repair reconciliation, the cockpit event — is registered as R-0916, R-0917, R-0918 and R-0919 rather than stubbed.

CHOSEN, SECOND: `docs/guides/do-continue-v1.md` is KEPT under a dated status banner naming the three surviving commands and what has no heir, its command forms rewritten to the past tense, with its rows in `docs/README.md` and `README.md` relabelled. No round of this feature has deleted a `docs/` page, other pages link to it, and round 14's banner on `orchestrator-brain-v0.md` and round 18's dated prose in `token-economy-user-guide-v0.md` are the precedent. The banner names no source path, because `tests/docs/test_named_source_paths.py` forbids an operator-facing page naming a file that does not exist — a guard the reviewer's own run found after the helper's targeted set had passed.

CHOSEN, THIRD: the cockpit `continuation` section STAYS. Inventory ruling 2 binds a cockpit ROUTE whose payload is a deleted command's output; measured, `continuation` is a key of the job dashboard payload and its `available` half is a live read of approved intents that `patch approve` still writes. This is the reading DECISION F261 D13 took for the orchestrator section under R-0903. The event half goes dead and is R-0919.

CHOSEN, FOURTH: the dead event coupling is NOT declared, against the practice DECISION F261 D16 and D17 set, because it cannot be: the ratchet's recovery of emitted names is blind to this module's emit helper, and the reviewer measured that declaring `do_continue_stopped` reds `test_no_declared_entry_is_stale`. The blindness is R-0920.

CHOSEN, FIFTH: R-0900 is repaired by naming `brain graph` at every site that advertised the `brain` group alone, by deleting the `remedy project <project_id>` alias line that never existed and correcting the sentence beside it, by naming `do run` where `remedy do --yes` and `remedy do --task-file` were written, and by a new guard in `tests/cli/test_advertised_commands.py` that resolves a one-token advertisement against the default-subcommand map it IMPORTS from `apps/cli/grouped.py` rather than against the group list. Sixty group-only advertisements are in its reach at the round's tip and none is unrunnable. Two defects found while harvesting are registered rather than repaired here: R-0921 and R-0922.

CONSEQUENCE. `remedy do continue` is an unknown word and its id joins `TestDeletedCommands`; `do` keeps `run` and the words rounds I and J still owe. A one-token advertisement can no longer pass by naming a group that exists. HOW TO REVERSE: revert the round's two table commits and delete this section.
END DEC20

── SLICE P273-FROM ── target `docs/roadmap/features/T2_F273.md` ── REWRITE FROM ──
BEGIN P273-FROM sha256=745534c2d03ba24c2319ce20d18aa2d4827a08e8197b3725c8dbe3d5d2529e57
  rejections at what a user does next.

## Do not touch
END P273-FROM

── SLICE P273-TO ── target `docs/roadmap/features/T2_F273.md` ── REWRITE TO ──
BEGIN P273-TO sha256=ca857d2614074257e8f4b46c37bf13a3d901ebc5c4279c62782c3a427797c0de
  rejections at what a user does next.
- R-0916 carries a resolution line naming the surviving word that runs the continuation cycle with the
  test that proves its lease refuses a concurrent second run, or the DECISION that rules three commands
  are the cycle with the commit that gave the apply path its printed next action.
- R-0917 carries a resolution line naming the commit that made the apply path print the test-run
  invocation with the intent and apply ids, with the test that holds the printed ids against the apply
  record.
- R-0918 carries a resolution line naming the commit that records repair truth after an apply, with the
  test that drives a repair intent to a tested status and its failure to resolved, or the commit that
  deleted the four statuses nothing sets with the doc sentence that says so.
- R-0919 carries a resolution line naming the commit that deleted the cockpit continuation section's
  event half with its client mapping and its two fixtures, or the commit that gave it a surviving
  emitter.
- R-0920 carries a resolution line naming the commit that widened the event-name recovery to a helper
  emit call, with the test that finds a name a helper emits, and the re-measured declared set.
- R-0921 carries a resolution line naming the commit that made the test-run linkage gate resolve an
  intent id against the key the approval path writes, with the test that runs the real executor with an
  intent id.
- R-0922 carries a resolution line naming the commit that declared `--yes` on the run command with the
  test that reaches the auto-approve path, or the commit that deleted that branch and its parameter.

## Do not touch
END P273-TO

── SLICE MUT-1-FROM ── G5 (1) only ── never a file ──
BEGIN MUT-1-FROM sha256=c766dbac068e02072c1c2674cd7f67a7d381c07b2bdc0a932c4195a1f2de40c8
    "job.run": lambda args: _cmd_job_run(
END MUT-1-FROM

── SLICE MUT-1-TO ── G5 (1) only ── never a file ──
BEGIN MUT-1-TO sha256=8c76f1a32bb1b63a83bd129e5b4447409dd48f5d788019e53b8cb7cd2d03f64e
    "do.continue": lambda args: None,
    "job.run": lambda args: _cmd_job_run(
END MUT-1-TO

── SLICE MUT-2-FROM ── G5 (2) only ── never a file ──
BEGIN MUT-2-FROM sha256=98ff25a3376cfd75478666bdb91fbd47aebcee00c8fa0ba15045b56f43ab844a
    CommandEntry(
        command_id="run.show",
END MUT-2-FROM

── SLICE MUT-2-TO ── G5 (2) only ── never a file ──
BEGIN MUT-2-TO sha256=db8cbf9d602cbbc52fe2a46e11a67891bbe0c4bef347c24eafc67cc2d252f526
    CommandEntry(
        command_id="do.continue",
        group_id="do",
        subcommand="continue",
        description="Run one controlled continuation cycle.",
        action_class="apply_write",
        args=(_JOB_ID,),
    ),
    CommandEntry(
        command_id="run.show",
END MUT-2-TO

── SLICE MUT-3-FROM ── G5 (3) only ── never a file ──
BEGIN MUT-3-FROM sha256=8ec6a7f7795e01b2362ba3d2ace751934cd725bd7fc2fe190a32fad1f64d869f
return f"remedy patch apply {a.job_id} {a.patch_intent_id} --json"
END MUT-3-FROM

── SLICE MUT-3-TO ── G5 (3) only ── never a file ──
BEGIN MUT-3-TO sha256=344773d283d2b23257da33b28773823abc6cd518c26b712ac4acef1c6f64ffc0
return f"remedy do continue {a.job_id} --intent-id {a.patch_intent_id} --json"
END MUT-3-TO

── SLICE MUT-4-FROM ── G5 (4) only ── never a file ──
BEGIN MUT-4-FROM sha256=249d2019700b9833f082065e0b26f55ec51ae65c467912ab5537b8dd1a058919
next_actions.append(f"remedy brain graph {job_id_str}")
END MUT-4-FROM

── SLICE MUT-4-TO ── G5 (4) only ── never a file ──
BEGIN MUT-4-TO sha256=694d2e0ee857dab6dc8048f6cd35a0d5c4fbd25e41711a894d7978e03c443dfe
next_actions.append(f"remedy brain {job_id_str}")
END MUT-4-TO

── SLICE MUT-5-FROM ── G5 (5) only ── never a file ──
BEGIN MUT-5-FROM sha256=8ba7f5bba916f575fd4a339547fb437b635b6bfca5dd79199c1e3c5b09dae11f
remedy brain graph <job_id> --json    # JSON export
END MUT-5-FROM

── SLICE MUT-5-TO ── G5 (5) only ── never a file ──
BEGIN MUT-5-TO sha256=3ae8d2cd951b7949216d78297b5db1ab586508db17af4082909018b71780f33d
remedy brain <job_id> --json    # JSON export
END MUT-5-TO

── SLICE MUT-6-FROM ── G5 (6) only ── never a file ──
BEGIN MUT-6-FROM sha256=b50226df6706046cf6ac0c8097375aa05a8ae8ee451668a675979a9ad0782847
> the orchestration module behind it were deleted by F261 round 21
END MUT-6-FROM

── SLICE MUT-6-TO ── G5 (6) only ── never a file ──
BEGIN MUT-6-TO sha256=73a9f3ee3ac5ed683b2ee12a98322aec084690202b6ff5ae873429c8892eab18
> `packages/orchestration/do_continue.py` were deleted by F261 round 21
END MUT-6-TO
