── STEP T003/5 — F261 — ROUND 17 ──
Goal: Book round 16's PASS, register R-0906 for this feature and R-0907 for F273, record
DECISION F261 D16, and delete the `readiness`, `contract` and `policy` groups in three commits
by applying three tables; run the suite once.

Base commit: `bf88d647`, on `feature/f261-cli-vocabulary-v2`. SESSION 4 of F261. Read AGENTS.md,
docs/agents/self_drive_protocol.md, `.agent/f261_t003_inventory.md`, and DECISION F261 D16 once
C1 has landed it.

THE FRAME RULE, per item 37 of §3, measured over the final bytes: NO LINE of this block that is two or
more characters long is a run of a single repeated character, and every box-drawing rule inside the STEP and SLICE header
lines is exactly two characters long.

ENVIRONMENT: `VAR=x cmd`, `env` and `export` are denied, so set environment in-process; `cp` is
denied, so copy with `shutil.copyfile`; bare `ruff` is denied, so use `python3 -m ruff check`.
Shell loops, `$(...)` and `$?` in a compound command are refused by form, so write such checks
as Python scripts under `.remedy-wt/f261r16w/`, and never name a script after a standard-library
module; a pipe into `tail` hides pytest's exit code. The editable install resolves `apps` and
`packages` to the PRIMARY checkout, so a pytest run inside a worktree goes through a runner
script that changes into the worktree, puts it first on `sys.path` and in `PYTHONPATH`, and
asserts `apps.cli.grouped` loaded from inside it. Never call `run_job` or a runner yourself: a
job run started from inside a checkout creates a `remedy/job-*` branch in it.
`git branch --list 'remedy/job-*'` reads 16 lines now; keep it so. While a deletion is staged
but not committed, `test_every_enumerated_path_exists_in_this_repo` fails; run no suite then.

## Bundle — the ordered commit sequence

C0a `.agent/authored/f261-r17.md`, the block file the delegating message names, by
    `shutil.copyfile`
C0b `.agent/last_block.md`, the same bytes
C1  THE RECORD, one commit: `.agent/plan.md` becomes slice PLAN17; slice RECORD17 is appended to
    `.agent/live_review.md` and slice DEC16 to `.agent/decisions.md`; in `docs/roadmap/features/T2_F273.md` the bytes of slice P273-FROM
    are replaced by those of slice P273-TO
C2  THE READINESS GROUP: copy `.remedy-wt/f261-block/f261-r17-readiness.jsonl` to
    `.agent/authored/f261-r17-readiness.jsonl` and apply it per THE TABLES, in one commit
C3  THE CONTRACT GROUP AND ITS HINTS: the same with `f261-r17-contract.jsonl`, in one commit
C4  THE POLICY GROUP: the same with `f261-r17-policy.jsonl`, in one commit
C5  `.agent/handoff.md`, the handback; then `git push origin feature/f261-cli-vocabulary-v2`

C1 is the FIRST SUBSTANTIVE COMMIT, per item 23 of §3. No pull request is created.

## Change — exactly these paths and no others

C0a to C1: `.agent/authored/f261-r17.md`, `.agent/last_block.md`, `.agent/plan.md`,
`.agent/live_review.md`, `.agent/decisions.md` and
`docs/roadmap/features/T2_F273.md`. C2 to C4: each table's own carrier and the paths G3 names.
C5: `.agent/handoff.md`.

## The appends and the pair

RECORD17 and DEC16 each begin with an empty line, and both targets end in a
newline at `bf88d647`: an append is the file's bytes followed by the slice's bytes, and nothing
else. The pair P273: TO contains FROM: false, so it is a REWRITE; P273-FROM occurs once
in `docs/roadmap/features/T2_F273.md` at `bf88d647`, and at C1 P273-FROM occurs 0 times and
P273-TO once.

## THE TABLES

Each carrier holds one JSON array per line. Their sha256 digests, to verify before copying:
`f261-r17-readiness.jsonl` `53281fb63f49d0f526ecd5568604d19042e798a5146e9564d342a0a2d3a5881a`,
`f261-r17-contract.jsonl` `b224acf8ef3fb53da03126d3348adb1f1ad57b28a34fdf0d12673868370d21a3`,
`f261-r17-policy.jsonl` `8c88b9daf6a5e87674569194a303997efec348827111bc168eed4ad8ab6ce339`.
Apply the rows strictly
in file order, each against the tree as the previous rows left it, from the repository root:
`["edit", path, old, new, count]` opens the path with `encoding="utf-8", newline=""`, requires
the number of occurrences of `old` to equal `count` exactly, and replaces every occurrence with
`new`; `["delete", path]` removes the file; `["move", src, dst]` renames the file, whose target
must not exist; `["create", path, content]` writes `content` to a path that must not exist, with
the same encoding and newline setting. A count that differs or a target that exists is a STOP:
touch nothing further, commit nothing of that table, and hand back with the row and the reading.
Stage each commit with `git add -A` after its table and its carrier. The tables are the
reviewer's measured dry run of DECISION F261 D16, applied on top of C1's record: the readiness
table its CHOSEN FIRST, the contract table its CHOSEN SECOND and the policy table its CHOSEN
THIRD.

## SPEC S — the suite, once, after G5 and before C5

From the primary checkout's root, serially:
`python3 -B -m pytest -q -p no:randomly -p no:cacheprovider --tb=short -rfEs`, with `PYTHONPATH`,
`REMEDY_PROJECT` and `REMEDY_DATA_DIR` removed and `PYTHONDONTWRITEBYTECODE=1`, output under
`.remedy-wt/f261r16w/`. Report pytest's return code, the run's last output line, and every
distinct bad node, the text after a line-initial `FAILED ` or `ERROR ` up to the first ` - `.
Re-run each bad node alone, once, the same way, and report that return code beside it.

## Constraints

1. NO SLICE AND NO TABLE IS EDITED. Extract each slice as the bytes strictly between its
   `BEGIN <NAME>` and `END <NAME>` lines and verify its sha256 before use.
2. READ `.agent/STOP` before C0a, before C2 and before C5, with real exit codes. If it exists:
   finish a half-written commit, write the handoff, push, stop.
3. A red gate is a STOP: commit what is honestly finished, hand back with the raw output.
4. Scratch, runner scripts and your worktree live under `.remedy-wt/f261r16w/`, uncommitted; no
   `.py` file under `.agent/`. Under `.remedy-wt/` open only `.remedy-wt/f261-block/` and your
   own directory. `git worktree list` reads one row now; leave it so. Create no symlink.
5. Every commit stays under 500 insertions, read as the first column of `git show --numstat
   --format= <commit>` with git's default rename detection.
6. NEVER merge, open a pull request, force-push, rewrite history or delete a branch. No `remedy`.
   Write no `Done:` paragraph and no `Landed:` line.
7. THE BLOCK'S OWN SIZE, measured on its final bytes: 352 lines TOTAL and 260 lines of PROSE,
   against the caps of 490 and 400.
8. GATE ORDER. G1 and G2 after C1; G3, G4 and G5 after C4; then SPEC S, whose result is G6; G7
   after C5 and the push, reported in the completion message only.
9. Every commit message ends with `Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>`, and
   no subject carries a leading-slash token or an absolute path.

## Done when — every gate run for real, its exit code recorded

G1 TRANSPORT. The sha256 of `.agent/authored/f261-r17.md` at C0a equals the digest the delegating
message gives, and `.agent/last_block.md` at C0b is byte-identical to it; the slices FOUND, each
matching its BEGIN-marker sha256; each committed carrier's sha256 equals its digest above.

G2 THE RECORD, at C1. `.agent/plan.md` is byte-identical to PLAN17, at most 50 lines, with
`^## Goal$` once and `^## Next Steps$` once. `.agent/live_review.md` equals its `bf88d647` blob
followed by RECORD17 and `.agent/decisions.md` its `bf88d647` blob followed by DEC16.
`docs/roadmap/features/T2_F273.md` equals its `bf88d647` blob with the pair P273 applied, with
the counts The appends and the pair give. Over `.agent/live_review.md`: `^Gate: F\d+ R\d+ — `
reads 125 at `bf88d647` and 126 at C1, with `Gate: F261 R16 — ` once at C1; distinct
`^- R-\d+ — ` ids 108 and 110, C1 minus base exactly `R-0906` and `R-0907`; distinct `^Done: R-\d+ — ` ids 8
and 8; the open set by distinct id 100 and 102. `python3 -m pytest tests/docs/ -q` exits 0 at C1.

G3 THE TABLES, at C2, C3 and C4. `git diff --no-renames --name-only` from each commit's parent
prints exactly that commit's carrier and: at C2 `apps/cli/command_catalog.py`, `apps/cli/commands/__init__.py`, `apps/cli/commands/readiness.py`, `apps/ui/src/api/actionClass.test.ts`, `apps/ui/src/api/humanizeCatalog.ts`, `docs/system/architecture.md`, `packages/orchestration/brain_detail.py`, `packages/orchestration/brain_viewer.py`, `packages/orchestration/guidance.py`, `scripts/remedy_smoke.sh`, `tests/orchestration/import_reachability_allowlist.txt`, `tests/test_autonomy_readiness.py`, `tests/test_command_catalog.py`, `tests/test_data_paths.py` and `tests/test_remedy_smoke_script.py`; at C3 `apps/cli/command_catalog.py`, `apps/cli/commands/__init__.py`, `apps/cli/commands/contract_cmd.py`, `docs/system/quality-baseline-v0.md`, `docs/system/real-test-execution-v1.md`, `docs/system/repair-loop-v1.md`, `docs/system/run-contract-v1.md`, `packages/orchestration/do_continue.py`, `packages/orchestration/repair_loop.py`, `packages/orchestration/run_contract.py`, `packages/orchestration/self_dogfood.py`, `packages/orchestration/self_dogfood_execution.py`, `packages/orchestration/test_execution_service.py`, `pyproject.toml`, `tests/cli/test_cli_ux.py`, `tests/cli/test_contract_runtime.py`, `tests/orchestration/import_reachability_allowlist.txt` and `tests/test_command_catalog.py`; at C4
`apps/cli/command_catalog.py`, `apps/cli/commands/__init__.py`, `apps/cli/commands/policy.py`, `apps/ui/src/api/humanizeCatalog.ts`, `docs/system/architecture.md`, `packages/orchestration/brain_detail.py`, `packages/orchestration/guidance.py`, `scripts/remedy_smoke.sh`, `tests/orchestration/import_reachability_allowlist.txt`, `tests/orchestration/test_event_name_coupling.py`, `tests/test_command_catalog.py`, `tests/test_execution_foundation.py`, `tests/test_grouped_cli.py` and `tests/test_remedy_smoke_script.py`. `git rev-parse <commit>:<object>` equals the reviewer's dry run, which applied C1's
record before the tables, for `apps`, `tests`, `docs`, `scripts`, `packages` and `README.md` in
that order: C2 `64b96c3cfe93b2d5a6fc8b00518d1dfbf5fc8795`, `4227848131d304116cfa0d994ac747915a366e48`, `b8bda65ced35f1228dcddb728f1cd1fff50f86af`, `8cee7c743b6d65101fb284637d9db112c5248f35`, `35148a28175e50db86fae55328e2c612e34f1d6c`, `15b9e0e8fec9721c7c17a872cc8f1a2bed3a2952`; C3 `8e208dce75af1b68d22f30356175ae1a7b804f35`, `71a19b9cd924ce7f6eb9d9fee692a0b4ab5e4eaf`, `c2410d195b4c22d1b3ba0f1f85793e0b11aebd66`, `8cee7c743b6d65101fb284637d9db112c5248f35`, `7eaa0ad5890313a7dff4000c92384a77edcbd535`, `15b9e0e8fec9721c7c17a872cc8f1a2bed3a2952`; C4 `8a2b5ba003ff088791183387a48ba091920925fa`, `31412c90e3171055e857dca191ba4a7fe148f017`, `7eb0caab58166e1598fa2e90a8e83c7e45624823`, `3439f8f1e6698ee3ea69f6b2245854ade46c1f37`, `ed064a2b9369cd2917994191fee6e03739021cba`, `15b9e0e8fec9721c7c17a872cc8f1a2bed3a2952`.
Report each commit's insertions per constraint 5.

G4 THE SWEEP, at C4. `git grep -n -I -E 'remedy (readiness|contract|policy)\b|commands/(readiness|policy|contract_cmd)\.py|apps\.cli\.commands\.(readiness|policy|contract_cmd)|_cmd_readiness_(job|project)|_cmd_run_contract|_cmd_token_policy|_cmd_token_explain|_cmd_contract_(inspect|check|set)'
<C4> -- apps packages scripts tests docs README.md AGENTS.md .claude ':!docs/roadmap'` exits 1
and prints nothing. `python3 -m ruff check` over every `.py` path of C2 to C4 that still exists
at C4 exits 0.

G5 THE RED-PROOF, in `git worktree add --detach .remedy-wt/f261r17w/wt <C4's sha>`, each run
through the runner over `tests/test_command_catalog.py`, `tests/cli/test_cli_ux.py`,
`tests/test_grouped_cli.py`, `tests/orchestration/test_import_reachability.py`,
`tests/cli/test_advertised_commands.py` and `tests/orchestration/test_event_name_coupling.py`
with `-rf --tb=no`. Mutation <n> is in the file its line below names, replaces the bytes of slice
MUT-<n>-FROM, whose count there must read 1, with those of slice MUT-<n>-TO, and is restored with
`git -C .remedy-wt/f261r17w/wt checkout -- <that file>`. (a) CONTROL: must exit 0. Each numbered
mutation must exit 1 with the named node among the failed nodes:
(1) `apps/cli/commands/dev.py`, a `readiness` handler row, (2) the same file, a `contract`
handler row, and (3) the same file, a `policy` handler row: each
`TestDeletedCommands::test_no_deleted_id_is_left_in_the_dispatch_table`; (4)
`apps/cli/command_catalog.py`, the `policy` group restored without commands:
`TestCatalogIntegrity::test_every_group_has_at_least_one_command`; (5) the same file, a
`related=` naming `policy.contract`:
`TestCatalogIntegrity::test_every_related_reference_resolves_to_a_live_command`; (6)
`packages/orchestration/brain_detail.py`, the readiness node's hint pointed back at
`readiness job`: `test_every_advertised_command_exists_in_the_catalog`; (7)
`tests/orchestration/test_event_name_coupling.py`, `token_policy_inspected` undeclared:
`TestEventNameCouplingRatchet::test_every_dead_coupling_is_declared`; (8)
`tests/cli/test_cli_ux.py`, `contract` named an internal group again:
`TestGroupDefIntegrity::test_internal_groups_marked`.
Report each exit code, summary line and number of failed nodes; then
`git worktree remove --force .remedy-wt/f261r17w/wt` and read `git branch --list 'remedy/job-*'`.

G6 THE SUITE, SPEC S at C4: must exit 0 with no bad node; report the last output line. A bad
node whose lone re-run exits 0 is reported as such with both readings, and is not a STOP; a bad
node whose lone re-run fails is.

G7 THE TREE, after C5 and the push. `git status --porcelain` prints `''`; C0a to C5 are
single-parent commits in that order on `bf88d647`; `git rev-parse HEAD` equals
`git rev-parse origin/feature/f261-cli-vocabulary-v2`; `git worktree list` prints one row, and
`git branch --list 'remedy/job-*'` prints 16 lines.

## The handback, C5

`.agent/handoff.md` per `docs/agents/handback_template.md`, Session line
`SESSION 4 of feature F261 · round 17 · rounds so far 17`, with one sentence of context
self-assessment. `## Commits` lists C0a to C4, each row's `+/-` cell equal to constraint 5's
reading of that commit and its deletions column; C5's own numbers appear nowhere, per item 31 of
§3. `## Verification` gives G1 to G6 with real exit codes. It states the open findings at 102 by
distinct id, with the High ids R-0803, R-0804 and R-0807, and `Operator questions open: 0`. Its
`## Next` names, in order: Phase 1 rule 1; the reviewer's verdict on round 17; the `context`
group, the `token` group with `context-pack`, and the `review` group, as the inventory
proposes.

── SLICE PLAN17 ── target `.agent/plan.md` ── FULL REPLACEMENT ──
BEGIN PLAN17 sha256=6566d9abdc5888f04dfc42ec08daa5f599e7d8ebcc0480d25b6d2793c1160904
# Plan — F261 CLI vocabulary v2 (rename & prune)

Branch: feature/f261-cli-vocabulary-v2, cut from `main` at
`7cdde89b5d0dc8ef1fb96980105870e956699873`, the merge commit of pull request 250.

## Goal

The catalog `apps/cli/command_catalog.py` equals DECISION amend0905-vocab D4: one name per
command, and every retired word deleted rather than aliased, per
`docs/roadmap/features/T2_F261.md`.

## Current Step

ROUND 17 continues T003. It books round 16's PASS, registers R-0906 for this feature and R-0907
for F273 and records DECISION F261 D16, then deletes the `readiness` group, the `contract` group
with its hints, and the `policy` group, one table per commit.

## Next Steps

1. The `context` group, the `token` group with `context-pack`, and the `review` group, as
   `.agent/f261_t003_inventory.md` proposes.
2. The rest of T003 in the inventory's order, each round re-measured before it is authored,
   with R-0767, R-0894 and R-0900.
3. `job budget <id> set` over the run-contract budget fields, the word DECISION amend0905-vocab
   D4 gives the write that `contract set` performed, with R-0906.
4. T004.

## Risks

- 100 findings are open by distinct id before this round's record and 102 after it; three are
  High, R-0803, R-0804 and R-0807.
- The inventory proposes more rounds than F261's soft limit of 25 leaves; the session that
  reaches the limit owes the scope report and the split-and-close default.
- A deletion's consumers include shell strings, subprocess help calls, event readers, the UI
  event catalog and the readiness signals, so every deletion round runs the whole suite on its
  committed tree.
END PLAN17

── SLICE RECORD17 ── target `.agent/live_review.md` ── APPEND ──
BEGIN RECORD17 sha256=defe5e1474dea6d7a8ab13f753b27c705751b985b7556fed088717f985577183

Gate: F261 R16 — the F261 round 16 entry. VERDICT PASS. Written by the planner and reviewer of session 39 after reading the committed range `782b4e02`..`bf88d647` and re-deriving the readings below; the worker's report was evidence for none of them. It is booked here by the first commit of round 17 that writes the record, per operator amendment amend0827-process-diet rule 1. THE TRANSPORT: `.agent/authored/f261-r16.md` at `d11fd434` and `.agent/last_block.md` at `4613018a` are byte-identical to the reviewer's scratch original, sha256 `30c5067a9e6531a00ade3ee4a2ab9a5dc15e6b01c85a50f055cb6ec5677b7d94`, and the three tables committed at `995dd07e`, `5db11427` and `ae95e09d` are byte-identical to the reviewer's. THE STATE: at `decdbbcc` and again at `bf88d647`, `.agent/plan.md` equals PLAN16, `.agent/live_review.md`, `.agent/decisions.md` and `.agent/prose_slips.md` equal their `782b4e02` blobs followed by RECORD16, DEC15 and SLIP16, and `docs/roadmap/features/T2_F273.md` equals its `782b4e02` blob with the pair P273 applied. THE TABLE COMMITS: at `995dd07e`, `5db11427` and `ae95e09d` the `apps`, `tests`, `docs`, `scripts`, `packages`, `README.md` and `.claude` objects equal the reviewer's dry-run commits, which applied the record before the tables; the first two tables are the research helper's and reproduced its trees, and the third is the helper's repo table with one row the reviewer added, which declares `git_status_read` in `KNOWN_DEAD_EVENT_COUPLINGS` with the ceiling raised to 2 so that no commit of the round leaves `test_every_dead_coupling_is_declared` red, and whose tree differs from the helper's only in that file's comment. Each commit's `--no-renames` path set is the dry run's plus its carrier, and `git show --numstat` reads 44, 21 and 63 insertions. In the dry run's production diff each deleted group leaves with its handlers, catalog entries and tests, the `guide` route of the cockpit server whose payload was the `guide job` output, the two guidance exports, `packages/orchestration/dashboard.py`, the two git-status exports and the commit-readiness block of `dev status`; `build_guidance_cards` and `read_git_status` stay for the cockpit and the brain graph, and every deleted symbol's production callers at `782b4e02` were in the deleted code. The sweep pattern of the round 16 block matches in 24 files at `782b4e02`, and at `bf88d647` the same `git grep` over `apps`, `packages`, `scripts`, `tests`, `docs` without `docs/roadmap`, `README.md`, `AGENTS.md` and `.claude` exits 1 with no output. In the reviewer's dry run a full suite under `-n auto` without `tests/ui_server` read 1 failed, `test_vitest_passes`, 17415 passed and 29 skipped, and the ten `tests/ui_server` files naming a deleted group read 328 passed. Over `tests/test_command_catalog.py`, `tests/cli/test_cli_ux.py`, `tests/test_grouped_cli.py`, `tests/orchestration/test_import_reachability.py`, `tests/cli/test_advertised_commands.py` and `tests/orchestration/test_event_name_coupling.py`, which passed 443 unmutated, a `guide` handler row failed 1 test, the `repo` group restored without commands failed 1, the `ci` group removed failed 6 with `test_all_groups_still_in_catalog` among them, a `related=` naming `dashboard.job` failed 1, the `repo commit-readiness` hint restored failed 1, and `git_status_read` undeclared failed 1. THE REVIEWER'S RUN in the primary checkout at `bf88d647` of those six files, every other test file the round edited, `tests/ui_contracts/`, `tests/orchestration/test_test_runner.py`, `tests/cli/test_golden_path.py`, `tests/docs/`, `tests/orchestration/test_command_discovery.py` and those ten `tests/ui_server` files read 2641 passed and 11 skipped, `test_vitest_passes` alone read 1 passed, `python3 -m ruff check` over sixteen edited files printed `All checks passed!`, and `git branch --list 'remedy/job-*'` read 16 lines. The open set reads 100 by distinct id at `bf88d647`.

- R-0906 — Medium, DELETING `contract set` LEAVES NO COMMAND THAT CAN RAISE `max_test_runs`, SO `remedy test run` IS REFUSED FOR EVERY JOB WHOSE CONTRACT NOTHING OVERRIDES, AND THE WORD DECISION amend0905-vocab D4 GIVES THAT WRITE, `job budget <id> set`, DOES NOT EXIST. Raised by the planner and reviewer of session 39 while preparing F261 round 17, after searching the open set for the `contract` and `policy` commands and for the run contract under §3 item 30: no open finding describes it. THE DEFECT, read at `bf88d647`: `build_default_run_contract` in `packages/orchestration/run_contract.py` sets `max_test_runs=0`, and `evaluate_run_action` refuses the run-test action while that field is 0, with the reason "max_test_runs is 0 — set it above 0 to enable test execution"; `_cmd_contract_set` in `apps/cli/commands/contract_cmd.py` was the only caller of `save_contract` that wrote a user-chosen field, the two that remain being `do_run.py`, which overrides `stop_before_apply`, `autonomy_level` and `max_loops` only, and `job_fulfillment.py`, which writes the fixture contract. The `job.budget` entry of `apps/cli/command_catalog.py` is `action_class="read_only"` and takes a job id and `--json`, so the `set` form D4 names is not built. This round deletes the `contract` group and empties that refusal's `next_safe_action`, which until now named `contract set`, and with it the next actions of the `stop_before_apply_true` and `test_budget_unconfigured` blockers of `evaluate_continue_eligibility` in `packages/orchestration/do_continue.py` and the `contract_guidance` line `execute_test_run` printed for an exhausted test budget, each of which named the same deleted write. WHY MEDIUM: a surviving user-facing command is refused for every job the operator did not fix by hand, and the refusal now names no way out; nothing is written and nothing prints anything false. WHY F261's: `job budget <id> [set …]` is a word of D4, and this feature's Goal is the catalog equal to D4, so the write belongs to a later round of T003 or T004 rather than to findings paydown. FIX: build `job budget <id> set <field> <value>` over the run-contract budget fields, with a test that raises `max_test_runs` and runs `test run` against the raised budget, and point the refusal's `next_safe_action`, the two `do continue` blockers and the exhausted-budget guidance at it. Owner: F261.

- R-0907 — Low, WITH THE `policy` GROUP GONE NOTHING EMITS `run_contract_inspected` OR `token_policy_inspected`, SO NO JOB CAN REACH AUTONOMY READINESS LEVEL 4 AGAIN, AND SIX EXPORTS OF THE THREE MODULES THIS ROUND KEEPS ARE NOW CALLED BY TESTS ALONE. Raised by the planner and reviewer of session 39 while preparing F261 round 17, after searching the open set for the readiness signals and these event names under §3 item 30: no open finding describes them, and R-0905, which records the same class for `git_status_read`, names neither event. THE DEFECT, read at `bf88d647` and on the reviewer's dry-run trees: `_cmd_token_policy` and `_cmd_run_contract` in `apps/cli/commands/policy.py` are the only emitters of the two events, and `_assess_level` in `packages/orchestration/autonomy_readiness.py` checks the signals `run_contract` and `token_policy`, which `_has_run_contract` and `_has_token_policy` derive from them, before it grants level 4, `bounded_loop`; both signals therefore read false for every job whose run log this round's commits precede, and levels 4 and above become unreachable. DECISION F261 D16 declares both names in `KNOWN_DEAD_EVENT_COUPLINGS` of `tests/orchestration/test_event_name_coupling.py` so the coupling stays visible. In the same three modules `assess_project_readiness` and `summarize_readiness` of `autonomy_readiness.py`, `summarize_run_contract` and `export_run_action_decision_json` of `run_contract.py`, and `export_token_policy_json` and `summarize_token_policy` of `token_policy.py` lose their last production caller with the three groups and keep callers under `tests/` only; with `assess_project_readiness` goes the project-scope readiness the deleted `readiness project` printed, which no surviving command offers. WHY LOW: each reader returns an honest result for a job nobody inspected by hand, and no command prints anything false. WHY F273's: raising a readiness level again means giving the two events an emitter or changing what a level requires, and deleting a public export with its tests is findings paydown; F261 prunes the catalog and does not change what a surviving surface decides. FIX: give each event an emitter in a surviving command, or drop the two signals from level 4 and say so where the levels are documented; delete each test-only export with its tests, or name the surviving caller that keeps it; and in either case take the two names out of `KNOWN_DEAD_EVENT_COUPLINGS` and lower `_COUPLING_CEILING` in the same commit. Owner: F273.
END RECORD17

── SLICE DEC16 ── target `.agent/decisions.md` ── APPEND ──
BEGIN DEC16 sha256=f529f4781cc3eb54a3818f9441a64674ab06ea472f3714040318d25a1353b7b3

## DECISION F261 D16 (2026-09-16, F261 round 17) — the deletion paragraph of the `readiness`, `contract` and `policy` groups

CONTEXT. DECISION amend0905-vocab D4 deletes `readiness`, `policy` and the `contract` group that wears the run-permission word, and `.agent/f261_t003_inventory.md` puts them in its round D, in the `related=` order readiness, contract, policy. Measured at `bf88d647` by the reviewer's research helper, which ran each of the eight commands in process against a scratch data root, and re-read by the reviewer on the dry-run trees. As in DECISION F261 D13, package code goes with a command when that command was its only production caller.

CHOSEN, FIRST: `readiness`. Deleted: the group, `readiness.job` and `readiness.project`, `apps/cli/commands/readiness.py` and its tests; the guidance card whose import of `assess_readiness` named nothing in `packages/orchestration/autonomy_readiness.py`, so the card could never be built; the humanized sentence of `readiness_assessed`, whose only emitter was the deleted handler and which no code reads; and the smoke section that ran the command. `packages/orchestration/autonomy_readiness.py` stays whole: `assess_job_readiness` and `export_readiness_json` are read by `mission readiness`, the cockpit's readiness route, the autonomy loop, the brain graph and the teacher. THE HEIR: `remedy mission readiness <job_id>`, the cockpit's readiness payload under `remedy ui start`, and the `autonomy_readiness` node of `remedy brain graph`; the project-scope report of `readiness project` has no heir.

CHOSEN, SECOND: `contract`. Deleted: the group, `contract.inspect`, `contract.check` and `contract.set`, `apps/cli/commands/contract_cmd.py` with its tests and its mypy override, the hints that named those commands, and `contract` as an internal group of `tests/cli/test_cli_ux.py`. `packages/orchestration/run_contract.py` stays: `ensure_contract` alone has eleven production callers, and `do run`, `job fulfillment`, `test run`, the repair loop and the brain graph read the contract. THE HEIR, as the vocabulary's Contract row names it: the `permissions` and `fences` sections of `remedy job show <id> --full`, which print the boundary a run holds; the write `contract set` performed has no heir, because `job budget <id> set`, the word D4 gives it, is not built — the refusal of a run-test action therefore names no next action any more, and R-0906 records that for this feature.

CHOSEN, THIRD: `policy`. Deleted: the group, `policy.contract`, `policy.token` and `policy.token-explain`, `apps/cli/commands/policy.py` with its tests, the requirement of `tests/test_command_catalog.py` that the group and its two read commands exist, the humanized sentences of `run_contract_inspected` and `token_policy_inspected`, the brain node's `policy token` next action, and the smoke sections that ran the commands. `packages/orchestration/token_policy.py` stays for the autonomy loop, the guidance cards and the brain graph. Both event names lose their only emitter while `packages/orchestration/autonomy_readiness.py` still reads them, so they join `KNOWN_DEAD_EVENT_COUPLINGS` in `tests/orchestration/test_event_name_coupling.py` with the ceiling raised by two, in the shape DECISION F261 D15 used for `git_status_read`, and R-0907 records the readers and the readiness level they gate. THE HEIR: the `run_contract` and `token_policy` nodes of `remedy brain graph <job> --json`, which build the DEFAULT contract and policy rather than the persisted one; the explainer text of `token-explain` has no heir.

CONSEQUENCE. `remedy readiness`, `remedy contract` and `remedy policy` are unknown commands and their ids join `TestDeletedCommands`; a job's autonomy readiness stops below level 4, which R-0907 records; and `remedy test run` is refused for every job whose contract nothing overrides, which R-0906 routes to a later round of this feature as the `job budget <id> set` word of D4. HOW TO REVERSE: revert the round's three table commits and delete this section.
END DEC16

── SLICE P273-FROM ── target `docs/roadmap/features/T2_F273.md` ── REWRITE FROM ──
BEGIN P273-FROM sha256=ff543c2a676d8fae01823a938025e0cc465c46839dfe7571328662fb196e82d2
  name out of `KNOWN_DEAD_EVENT_COUPLINGS`.

## Do not touch
END P273-FROM

── SLICE P273-TO ── target `docs/roadmap/features/T2_F273.md` ── REWRITE TO ──
BEGIN P273-TO sha256=0dff26110f99adae60c972a54a4193527906584aeb051cd6cfd1e8c18c57cc04
  name out of `KNOWN_DEAD_EVENT_COUPLINGS`.
- R-0907 carries a resolution line naming, for `run_contract_inspected` and `token_policy_inspected`, the
  commit that gave each an emitter or dropped its signal from readiness level 4, and for each of the six
  test-only exports the commit that deleted it with its tests or the surviving caller that keeps it.

## Do not touch
END P273-TO

── SLICE MUT-1-FROM ── G5 (1) only ── never a file ──
BEGIN MUT-1-FROM sha256=b80c9cb6a8186d1e0e037407c5cb67f8a716ea462f41563da837cf74561af360
    "dev.status": lambda args: _dev_status(json_output=getattr(args, "json", False)),
}
END MUT-1-FROM

── SLICE MUT-1-TO ── G5 (1) only ── never a file ──
BEGIN MUT-1-TO sha256=a759de23af0719997d0582db31a15fd1c9a51f5f1d22da5860b26ef8641cd700
    "dev.status": lambda args: _dev_status(json_output=getattr(args, "json", False)),
    "readiness.job": lambda args: None,
}
END MUT-1-TO

── SLICE MUT-2-FROM ── G5 (2) only ── never a file ──
BEGIN MUT-2-FROM sha256=b80c9cb6a8186d1e0e037407c5cb67f8a716ea462f41563da837cf74561af360
    "dev.status": lambda args: _dev_status(json_output=getattr(args, "json", False)),
}
END MUT-2-FROM

── SLICE MUT-2-TO ── G5 (2) only ── never a file ──
BEGIN MUT-2-TO sha256=21a8c0865cc726773ed8ef951ae0e4c72ea88cd13facec55cf46f24077b141c3
    "dev.status": lambda args: _dev_status(json_output=getattr(args, "json", False)),
    "contract.set": lambda args: None,
}
END MUT-2-TO

── SLICE MUT-3-FROM ── G5 (3) only ── never a file ──
BEGIN MUT-3-FROM sha256=b80c9cb6a8186d1e0e037407c5cb67f8a716ea462f41563da837cf74561af360
    "dev.status": lambda args: _dev_status(json_output=getattr(args, "json", False)),
}
END MUT-3-FROM

── SLICE MUT-3-TO ── G5 (3) only ── never a file ──
BEGIN MUT-3-TO sha256=569f133ecfb0dd57d187bf4b955bc2124ac44474f9fedd44bb0d57293461d59d
    "dev.status": lambda args: _dev_status(json_output=getattr(args, "json", False)),
    "policy.token": lambda args: None,
}
END MUT-3-TO

── SLICE MUT-4-FROM ── G5 (4) only ── never a file ──
BEGIN MUT-4-FROM sha256=7048056fc379469f4167ab957a64cd68fb2c735884bc490198ed15a47d36a731
    "file": GroupDef("file", "File", "File-level provenance and tracing.", user_facing=False),
END MUT-4-FROM

── SLICE MUT-4-TO ── G5 (4) only ── never a file ──
BEGIN MUT-4-TO sha256=b68acc17a822d8f38dbebcbb7b6cd4422aa97d43844624d9e9b0baeaf26399eb
    "file": GroupDef("file", "File", "File-level provenance and tracing.", user_facing=False),
    "policy": GroupDef("policy", "Policy", "Run contract and token policy.", user_facing=False),
END MUT-4-TO

── SLICE MUT-5-FROM ── G5 (5) only ── never a file ──
BEGIN MUT-5-FROM sha256=2cd882e3544109f710e0a8b3c592d8630ddfb5d26298b828241e8202c83cbe93
        related=("brain.view",),
END MUT-5-FROM

── SLICE MUT-5-TO ── G5 (5) only ── never a file ──
BEGIN MUT-5-TO sha256=6373c375adbcd698f2576601afe036dc2b0d9f8c8a66124714954f4f678fd389
        related=("brain.view", "policy.contract"),
END MUT-5-TO

── SLICE MUT-6-FROM ── G5 (6) only ── never a file ──
BEGIN MUT-6-FROM sha256=08b70cd5f9850d2ddaa98c9b823cdd43155a3b6b26f4054aec669c0973fe317e
            f"Inspect with `remedy mission readiness {job_id_str[:8]}`.",
END MUT-6-FROM

── SLICE MUT-6-TO ── G5 (6) only ── never a file ──
BEGIN MUT-6-TO sha256=0dca695c0a11df218f1a08fcf255ef56aeebb4e990898e66ffba0bc315270afa
            f"Inspect with `remedy readiness job {job_id_str[:8]}`.",
END MUT-6-TO

── SLICE MUT-7-FROM ── G5 (7) only ── never a file ──
BEGIN MUT-7-FROM sha256=bf60e76e0f88deb419dd4979f222fd19669fd4bf5058ca67d8e8b57f60f6af72
    "run_contract_inspected",
    "token_policy_inspected",
)
END MUT-7-FROM

── SLICE MUT-7-TO ── G5 (7) only ── never a file ──
BEGIN MUT-7-TO sha256=9d53b8bda8ab3519321b0683d83deb9c29ef60f8e86149ae556e1c893dd114a6
    "run_contract_inspected",
)
END MUT-7-TO

── SLICE MUT-8-FROM ── G5 (8) only ── never a file ──
BEGIN MUT-8-FROM sha256=f4b00c8750409a5ba0c85fa53973a145925596c4122b93268e445838f188b5e2
    "snapshot", "integrity",
END MUT-8-FROM

── SLICE MUT-8-TO ── G5 (8) only ── never a file ──
BEGIN MUT-8-TO sha256=ef9a7c1d08d77fe11f7d8a59e41d317b7650c9279db513fa16016bae888dc5f8
    "snapshot", "contract", "integrity",
END MUT-8-TO
