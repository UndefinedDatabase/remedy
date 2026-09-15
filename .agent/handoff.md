# Handback — F261 round 5

## Session

`SESSION 1 of feature F261 · round 5 · rounds so far 5`

Context self-assessment: this worker's context is comfortable, and nothing in the round was cut short.

## Range

Review of `350fa353`..`HEAD`: C0a, C0b, C1, C2 and C3, plus this handback commit C4. `.agent/STOP` was ABSENT at all
three readings constraint 2 orders: before C0a (`.remedy-wt/f261r5w/stop.py` printed `STOP exists: False`, exit 1),
before C2 (`stop.py` exit 1, `STOP exists: False`; `ls .agent/STOP` exit 2, "No such file or directory") and before C4
(`stop.py` exit 1, `STOP exists: False`; `ls .agent/STOP` exit 2).

## Commits

### c0b5045a F261 R5 C0a: save the round 5 step block

| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f261-r5.md` | +237 / -0 | the block, copied with `shutil.copyfile`; sha256 equal to the delegated digest |

### 871488f1 F261 R5 C0b: mirror the round 5 step block into last_block

| Path | +/- | Reason |
|---|---|---|
| `.agent/last_block.md` | +114 / -92 | the same bytes, the mirror |

### de5cd238 F261 R5 C1: re-point the plan at round 5, book round 4's PASS, register R-0896 and R-0897, record DECISION F261 D4

This is the FIRST SUBSTANTIVE COMMIT.

| Path | +/- | Reason |
|---|---|---|
| `.agent/decisions.md` | +14 / -0 | slice DEC4 appended: DECISION F261 D4 |
| `.agent/live_review.md` | +6 / -0 | slice RECORD5 appended: `Gate: F261 R4 —` PASS, R-0896, R-0897 |
| `.agent/plan.md` | +16 / -17 | slice PLAN5, a full replacement: 1665 bytes, 35 lines |
| `docs/roadmap/features/T2_F268.md` | +2 / -0 | pair P268B: the R-0897 Acceptance line after the R-0892 line |

### 592ab167 F261 R5 C2: delete do promote, its hints and their tests, by deletion table 1

| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f261-r5-delete-1.jsonl` | +22 / -0 | the table, copied with `shutil.copyfile`; sha256 `65f89231…a81cf2` equal |
| `apps/cli/command_catalog.py` | +0 / -20 | row 1: the `do.promote` entry |
| `apps/cli/commands/do_cmd.py` | +0 / -42 | rows 2–4: the report's next-step promote lines, `_cmd_do_promote`, the handler-table entry |
| `apps/cli/grouped.py` | +0 / -2 | row 5: the two `do promote` steps of `_QUICK_START` |
| `packages/orchestration/pingpong_loop.py` | +2 / -28 | rows 6–10: `original_repo_arg`, the promote keys and shell-flow steps of `_build_next_commands` |
| `packages/orchestration/pingpong_promote.py` | +0 / -4 | row 11: the `To apply:` hint |
| `tests/cli/test_cli_ux.py` | +0 / -55 | rows 13–18 |
| `tests/cli/test_product_spine.py` | +0 / -4 | row 19 |
| `tests/cli/test_task_input.py` | +0 / -1 | row 21 |
| `tests/orchestration/test_pingpong_promote.py` | +0 / -1 | row 12 |
| `tests/test_cli_execution_loop_closure.py` | +0 / -1 | row 20 |
| `tests/test_command_catalog.py` | +1 / -0 | row 22: `do.promote` joins `TestDeletedCommands.DELETED` |

### 3b860345 F261 R5 C3: delete the run-level promote library, its tests, the staged-snapshot writer and the promotion readers, by deletion table 2

| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f261-r5-delete-2.jsonl` | +36 / -0 | the table, copied with `shutil.copyfile`; sha256 `84ba79bf…ef37d` equal |
| `apps/cli/commands/do_cmd.py` | +0 / -27 | rows 5–6: the `promotion.json` readers of `do report` |
| `packages/orchestration/job_evidence.py` | +1 / -4 | row 24: the `load_promotion` reader of `job evidence` |
| `packages/orchestration/pingpong_evidence.py` | +5 / -53 | rows 7–23: the promotion parameter, `promotion.json`, its manifest section and readiness keys, the `export_evidence` reader |
| `packages/orchestration/pingpong_loop.py` | +0 / -19 | row 4: the staged-snapshot writer |
| `packages/orchestration/pingpong_promote.py` | +0 / -793 | row 1: the module, deleted whole |
| `tests/cli/test_cli_ux.py` | +0 / -31 | rows 25–26 |
| `tests/orchestration/import_reachability_allowlist.txt` | +0 / -1 | row 3: the module's allowlist line |
| `tests/orchestration/test_evidence_bundle.py` | +0 / -93 | rows 29–36 |
| `tests/orchestration/test_job_task_runner.py` | +0 / -4 | row 27 |
| `tests/orchestration/test_pingpong_promote.py` | +0 / -1468 | row 2: the test file, deleted whole |
| `tests/orchestration/test_repair_loop.py` | +0 / -21 | row 28 |

### C4 — this commit (self-reference, R-0149 pattern)

| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | NO NUMBERS | this handback; its own numstat is reported in the completion message only |

## External actions

| Command | Outcome |
|---|---|
| `git worktree add --detach .remedy-wt/f261r5w/wt 3b860345` | created for G5; restored after each mutation with `git -C .remedy-wt/f261r5w/wt checkout -- <file>` (worktree status `''` after each), then removed with `git worktree remove .remedy-wt/f261r5w/wt`; `git worktree list` then read one row |
| `git push origin feature/f261-cli-vocabulary-v2` | the one push, after this commit; its result is in the completion message (G7) |
| pull request create / merge / force-push / branch delete / `remedy` | NOT RUN |

## Verification

The scripts and raw outputs are under `.remedy-wt/f261r5w/`, not committed. Every exit code below is the real return
code of the command as the tool reported it.

| Gate | At | REAL exit | Decisive reading |
|---|---|---|---|
| G1 transport | after C1 `de5cd238` | `g1g2.py` 0 | sha256 of `.agent/authored/f261-r5.md` at C0a `6351d01cd98d59f4ce598f7e8278ccfd457be8e48e78f9cab50ee7138424e69c`, **equal** to the delegated digest; `.agent/last_block.md` at C0b **byte-identical**. Slices FOUND **5** (PLAN5, RECORD5, DEC4, P268B-FROM, ACC268B), each **matching** its BEGIN-marker sha256. Committed carriers: delete-1 at C2 `65f89231984657f1a6651e908f6e8ca810be790cdae4d1bb6ae2eaa7efa81cf2` **equal**; delete-2 at C3 `84ba79bfd2420066c08ec937e30c059c14d6c397ce50567475972dd8f34ef37d` **equal** (read by `g3g4.py`) |
| G2 the record | C1 | `g1g2.py` 0 | `plan.md` **equals** PLAN5; **35** lines; `^## Goal$` **1**; `^## Next Steps$` **1**. `live_review.md` **equals** its `350fa353` blob + RECORD5; `decisions.md` **equals** its `350fa353` blob + DEC4; `T2_F268.md` **equals** its `350fa353` blob with P268B's FROM (count **1**) replaced by its TO. `^Gate: F\d+ R\d+ — ` **113** → **114**; `Gate: F261 R4 — ` **1** at C1; distinct `^- R-\d+ — ` **98** → **100**; distinct `^Done: R-\d+ — ` **4** → **4**; open by distinct id **94** → **96**; C1 minus base `['R-0896', 'R-0897']`, base minus C1 `[]` |
| G3 deletion 1 | C2 `592ab167` | `g3g4.py 3` 0 | table 1: all **22** rows matched, each count 1. `--no-renames --name-only de5cd238 592ab167` printed exactly the carrier and the **11** paths. Trees: `apps` `aaad9640abc468379001a6ff61bcea4be94aef04`, `packages` `45f95bbc48dbc5e4884712c2fb9d7ff6154fb2a7`, `tests` `88dac13da3445963210dd1414998608d61100493`, each **match**; `scripts` `fb0b7d81…` and `README.md` `86ec95f3…` each **equal** `350fa353`; `docs` `eebc60ba…` **equal** C1. 25 insertions |
| G4 deletion 2 | C3 `3b860345` | `g3g4.py 4` 0 | table 2: all **36** rows matched (2 deletes, 34 edits each count 1). `--no-renames --name-only 592ab167 3b860345` printed exactly the carrier and the **11** paths. Trees: `apps` `8bb7bd9b09e80234fea6165dad1bca1c157bb564`, `packages` `60db4fa8b3472661541025b5f4dfd28fc5c10423`, `tests` `8e6ae952508ba8b68d7198fa1fb3f0925973aa40`, each **match**; `scripts`, `README.md` each **equal** `350fa353`; `docs` **equal** C1. Symbol `git grep -n -w` exit 1, output `''`. `git grep -n -F do.promote` exit 0, exactly **1** line: `3b860345:tests/test_command_catalog.py:306:        "do.promote",`. `python3 -m ruff check` over the **14** surviving `.py` paths of C2 and C3: exit 0, `All checks passed!`. 42 insertions |
| G5(a) control | worktree at C3 | 0 | `apps.cli.command_catalog` and `apps.cli.commands.do_cmd` loaded from the worktree; `30 passed in 0.36s` |
| G5(b) `"do.promote": lambda args: None,` inserted before `"do.repair-attest": lambda args: _cmd_do_repair_attest(` | same worktree | 1 | FROM count **1**; `1 failed, 29 passed in 0.36s`; failed: `tests/test_command_catalog.py::TestDeletedCommands::test_no_deleted_id_is_left_in_the_dispatch_table` |
| G5(c) `command_id="job.apply",` → `command_id="do.promote",` | same worktree, after `checkout --` | 1 | FROM count **1**; `3 failed, 27 passed in 0.36s`; failed: `tests/test_command_catalog.py::TestCatalogIntegrity::test_command_id_format`, `…::TestRenamedCommands::test_every_new_id_parses_from_its_words_and_has_a_handler`, `…::TestDeletedCommands::test_no_deleted_id_is_left_in_the_catalog` |
| G6 the suite, SPEC S | primary checkout at C3, serially | 0 | `suite.py`: argv `python3 -B -m pytest -q -p no:randomly -p no:cacheprovider --tb=short -rfEs`, `PYTHONPATH`, `REMEDY_PROJECT`, `REMEDY_DATA_DIR` removed, `PYTHONDONTWRITEBYTECODE=1`; last line `18173 passed, 23 skipped, 1 warning in 1340.10s (0:22:20)`; distinct bad nodes **0**; `git status --porcelain` `''` afterwards |
| G7 the tree | after C4 and the push | not yet run | reported in the completion message only |

Open findings: **96** by distinct id, R-0896 (Medium, owner F261) and R-0897 (Medium, owner F268) among them. The open
High ids are **R-0803, R-0804, R-0806 and R-0807**.

Operator questions open: 1

## Authored-text proofs

| Text | Target | Result |
|---|---|---|
| the block | `.agent/authored/f261-r5.md`, `.agent/last_block.md` | sha256 **equal** to the delegated digest at C0a; mirror byte-identical at C0b (G1) |
| PLAN5 | `.agent/plan.md` | **equal** at C1 (G2) |
| RECORD5, DEC4 | `.agent/live_review.md`, `.agent/decisions.md` | each **equal** to its `350fa353` blob followed by the slice at C1 (G2) |
| P268B-FROM → ACC268B | `docs/roadmap/features/T2_F268.md` | **equal** to its `350fa353` blob with FROM replaced by TO at C1 (G2) |
| deletion table 1 | `.agent/authored/f261-r5-delete-1.jsonl` and its paths | carrier digest **equal**; the C2 trees equal the reviewer's dry run (G3) |
| deletion table 2 | `.agent/authored/f261-r5-delete-2.jsonl` and its paths | carrier digest **equal**; the C3 trees equal the reviewer's dry run (G4) |

NO SLICE AND NO TABLE WAS EDITED. Every slice was extracted programmatically from the COMMITTED
`.agent/authored/f261-r5.md` (read with `git show c0b5045a:`) and verified against its BEGIN-marker sha256 before use;
each table was verified against its digest before it was copied and applied.

## Item-status table

| Item | Status | Reason |
|---|---|---|
| C0a / C0b | done | two commits, as the Bundle orders |
| C1 PLAN5, RECORD5, DEC4, P268B | done | one commit, the first substantive commit |
| C2 deletion table 1 | done | one commit |
| C3 deletion table 2 | done | one commit |
| C4 handoff | done | this commit |
| G1 · G2 · G3 · G4 · G5 · G6 | done | exit codes and readings above |
| G7 | skipped | runs after this commit and its push; results in the completion message |

## Deviations & assumptions

1. **G1's carrier clause was read at C2 and C3, not after C1.** Constraint 8 places G1 after C1, but the carriers are
   first committed at C2 and C3; their committed digests were read by `g3g4.py` right after each commit, and each source
   carrier's digest was also verified before `shutil.copyfile`.
2. **Each table was validated in memory first.** `.remedy-wt/f261r5w/apply_table.py` reads each path with
   `encoding="utf-8", newline=""`, runs every row strictly in file order against a virtual tree the previous rows left,
   and only after every row passed copies the carrier and performs the rows on disk in the same order. No count
   differed and no target was missing.
3. **G4's ruff clause.** Two `.py` paths of C2 and C3, `packages/orchestration/pingpong_promote.py` and
   `tests/orchestration/test_pingpong_promote.py`, are deleted at C3, so ruff ran over the 14 surviving `.py` paths;
   ruff also ran over each commit's surviving `.py` paths before that commit, exit 0 each time.
4. **G5 ran through a runner**, `.remedy-wt/f261r5w/runner.py`, invoked as `python3 -B`: it changes into the worktree,
   puts it first on `sys.path` and in `PYTHONPATH`, asserts that `apps.cli.command_catalog` and
   `apps.cli.commands.do_cmd` loaded from inside the worktree, and calls `pytest.main` with
   `-p no:randomly -p no:cacheprovider -rf --tb=no tests/test_command_catalog.py`.
5. **G4 ran twice.** The first run passed `HEAD` as the C3 revision (exit 0, every check OK, grep lines prefixed
   `HEAD:`); it was repeated with `3b860345` so the recorded grep line names the commit, with the same readings.
6. **Constraint 4, a directory listing.** While probing the block directory before C0a, one `ls -la` also listed the
   top level of `.remedy-wt/` itself; no file there outside `.remedy-wt/f261-block/` and `.remedy-wt/f261r5w/` was opened.
7. **File reading before edits.** The tables were applied programmatically, so instead of reading each target file in
   full I read the staged diff of C2 and of C3 and ran ruff over the touched `.py` files before committing; the tree-id
   gates prove each result.

## Next

1. Phase 1 rule 1: the next session reads `.agent/STOP` first.
2. The reviewer's verdict on round 5.
3. The rename of `job_promote.py` to `job_apply.py`.

Operator questions open: 1

## Session close — session 36, written after the reviewer's verdict on round 5

The planner and reviewer of session 36 reviewed round 5 and ended the session after six
delegated rounds, all PASS: F275 round 110, which repaired pull request 250's hosted CI before
the Open PR Gate merged it as `7cdde89b`, and F261 rounds 1 to 5. Context self-assessment: the
reviewer's context had grown long across six rounds of research helpers and dry runs, and the
next step of T002 opens with fresh research and several rulings, so the session ends at a round
boundary rather than inside that research. Nothing is half-written; the branch is pushed.

### The verdict to book

Round 6's first commit that writes the record appends the paragraph below to
`.agent/live_review.md` byte for byte, preceded by one empty line, per operator amendment
amend0827-process-diet rule 1.

Gate: F261 R5 — the F261 round 5 entry. VERDICT PASS. Written by the planner and reviewer of session 36 after reading the committed range `350fa353`..`2cef254d` and re-deriving the readings below; the worker's report was evidence for none of them. It is carried by `.agent/handoff.md` in the session-close commit that follows `2cef254d` and booked by the first commit of round 6 that writes the record, per operator amendment amend0827-process-diet rule 1. THE TRANSPORT: `.agent/authored/f261-r5.md` at `c0b5045a` and `.agent/last_block.md` at `871488f1` are byte-identical to the reviewer's scratch original, sha256 `6351d01cd98d59f4ce598f7e8278ccfd457be8e48e78f9cab50ee7138424e69c`, and `.agent/authored/f261-r5-delete-1.jsonl` at `592ab167` and `.agent/authored/f261-r5-delete-2.jsonl` at `3b860345` are byte-identical to the reviewer's tables. THE STATE: at `de5cd238` and again at `2cef254d`, `.agent/plan.md` equals PLAN5, `.agent/live_review.md` and `.agent/decisions.md` equal their `350fa353` blobs followed by RECORD5 and DEC4, and `docs/roadmap/features/T2_F268.md` equals its `350fa353` blob with pair P268B applied. THE DELETIONS: at `592ab167` the `apps`, `packages`, `tests`, `scripts` and `README.md` objects equal the reviewer's dry run of table 1, and at `3b860345` its dry run of tables 1 and 2, which had reproduced the research helper's trees `77eef6c5` and `ef2bc0e5` exactly; `docs` at both equals its object at `de5cd238`, and each commit's `--no-renames` path set is the dry run's plus its own carrier. In the reviewer's dry run a full suite under `-n auto` read 15 failed and 18152 passed, every failure in `tests/ui_server` or `test_vitest_passes`, classes the helper's base control also failed, and a `do.promote` handler-table entry failed `TestDeletedCommands::test_no_deleted_id_is_left_in_the_dispatch_table` alone. THE REVIEWER'S RUN in the primary checkout at `2cef254d` of `tests/test_command_catalog.py`, `tests/cli/test_cli_ux.py`, `tests/cli/test_product_spine.py`, `tests/orchestration/test_evidence_bundle.py`, `tests/orchestration/test_repair_loop.py`, `tests/orchestration/test_import_reachability.py`, `tests/cli/test_advertised_commands.py`, `tests/docs/`, `tests/ui_server/test_dashboard_contract.py` and `tests/cli/test_golden_path.py` read 766 passed. The open set reads 96 by distinct id at `2cef254d`.

### What the next session needs to know

- T002's next step is the rename of `packages/orchestration/job_promote.py` to
  `job_apply.py` with its two test files, then its identifiers, then its output-visible words,
  each commit under the insertion cap; DECISION F261 D4 fixes that order and keeps
  `promote_ready` and the recommended-action strings of `final_verifier.py` as evidence words.
- Rulings still open for T002, to be made in the rounds that need them: whether the
  Acceptance grep for `promote` yields to the keep-by-sense clause of DECISION amend0905-vocab
  D5 for the model-routing and other senses; whether the staging-to-target writes of
  `packages/orchestration/staging_workspace.py` and `packages/orchestration/job_fulfillment.py`
  are the job-result sense; whether `job show` keeps JSON on stdout and gains `--json` for
  R-0896; which report variants and which failing sections `job show --full` carries; and
  whether renaming `promoted` statuses to `applied` collides with the existing task and manifest
  status `applied`.
- D5 says its kept occurrences were recorded in `.agent/live_review.md`; no such list is
  there, so T002 writes it.
- The reviewer's research found that `job show` stdout is parsed as JSON by
  `tests/cli/test_golden_path.py`, `tests/cli/test_plan_approval.py` and
  `scripts/remedy_smoke.sh`, so `--full` may only add keys to that JSON.

### Next

1. Phase 1 rule 1: the next session reads `.agent/STOP` first; then the Open PR Gate, which finds
   no open pull request for this branch.
2. Round 6's first record commit books `Gate: F261 R5` from this section.
3. The rename of `job_promote.py` to `job_apply.py`.

Operator questions open: 1
