# Handback — F261 round 8

## Session

`SESSION 2 of feature F261 · round 8 · rounds so far 8`

Context self-assessment: this worker's context is comfortable, and nothing in the round was cut short.

## Range

Review of `22173331`..`HEAD`: C0a, C0b, C1, C2, C3, C4 and C5, plus this handback commit C6. `.agent/STOP` was ABSENT
at all three readings constraint 2 orders: before C0a (`ls -la .agent/STOP` exit 2, "No such file or directory"),
before C2 (exit 2) and before C6 (exit 2).

## Commits

### 505deb15 F261 R8 C0a: save the round 8 step block

| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f261-r8.md` | +295 / -0 | the block, copied with `shutil.copyfile`; sha256 equal to the delegated digest |

### 83dff65a F261 R8 C0b: mirror the round 8 step block into last_block

| Path | +/- | Reason |
|---|---|---|
| `.agent/last_block.md` | +188 / -130 | the same bytes, the mirror |

### 1c3bf3e3 F261 R8 C1: re-point the plan at round 8, book round 7's PASS, register R-0898 to R-0900, record DECISION F261 D7

This is the FIRST SUBSTANTIVE COMMIT.

| Path | +/- | Reason |
|---|---|---|
| `.agent/decisions.md` | +14 / -0 | slice DEC7 appended: DECISION F261 D7 |
| `.agent/live_review.md` | +8 / -0 | slice RECORD8 appended: `Gate: F261 R7 —` PASS and R-0898, R-0899, R-0900 |
| `.agent/plan.md` | +15 / -14 | slice PLAN8, a full replacement: 38 lines |
| `docs/roadmap/features/T2_F273.md` | +4 / -0 | pair P273: the Acceptance lines of R-0898 and R-0899 |

### 9d8d57f6 F261 R8 C2: give job show its --json and guard every advertised flag against its command, by show table 1

Commit total per constraint 5: **199** insertions, 10 deletions.

| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f261-r8-show-1.jsonl` | +10 / -0 | the table, copied with `shutil.copyfile`; sha256 `011479d6…cf23190e` equal |
| `apps/cli/command_catalog.py` | +3 / -3 | `job show` declares `--json`, `supports_json=True` |
| `packages/orchestration/orchestrator_brain.py` | +1 / -1 | the `patch approve` hint loses the undeclared `--json` |
| `packages/orchestration/repair_request_builder.py` | +1 / -1 | the same |
| `packages/orchestration/self_dogfood_execution.py` | +1 / -1 | the same |
| `tests/cli/test_advertised_commands.py` | +136 / -4 | the advertised-flag guard over production code and operator-facing paths, and its scanner tests (R-0896) |
| `tests/cli/test_job_show.py` | +47 / -0 | new: `--json` parses and changes nothing |

### 068ee126 F261 R8 C3: print the last-round findings of blocked tasks in job show, ten by default and all with --full, by show table 2

Commit total per constraint 5: **308** insertions, 6 deletions.

| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f261-r8-show-2.jsonl` | +9 / -0 | the table, copied with `shutil.copyfile`; sha256 `b8134144…23b13169` equal |
| `apps/cli/command_catalog.py` | +6 / -1 | `job show --full` |
| `apps/cli/commands/job.py` | +23 / -4 | `blocked_task_findings` appended to the JSON; the stderr findings block |
| `packages/orchestration/pingpong_job.py` | +51 / -0 | `BLOCKED_TASK_FINDINGS_CAP` and `collect_blocked_task_findings` (R-0806) |
| `tests/cli/test_job_show.py` | +219 / -1 | the findings tests, the blocked fake-provider run, and the default-output key order |

### 720874b8 F261 R8 C4: give job show --full its sections and fold job permissions in as the first, by show table 3

Commit total per constraint 5: **177** insertions, 77 deletions.

| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f261-r8-show-3.jsonl` | +15 / -0 | the table, copied with `shutil.copyfile`; sha256 `10d1c620…f475b98` equal |
| `apps/cli/command_catalog.py` | +3 / -11 | the `--full` help names the sections; entry `job.permissions` deleted; `job permit` relates to `job show` |
| `apps/cli/commands/job.py` | +53 / -16 | `_SHOW_SECTION_ORDER`, `_SHOW_SECTIONS`, `_build_show_sections`, the `permissions` section; `_cmd_show_permissions` and its handler row deleted |
| `docs/system/architecture.md` | +3 / -2 | the permissions paragraph names `remedy job show <job_id> --full` |
| `packages/orchestration/brain_detail.py` | +1 / -1 | the blocker hint names `remedy job show <id> --full` |
| `tests/cli/test_job_show.py` | +51 / -0 | `TestSections` |
| `tests/test_cli_main.py` | +50 / -46 | the permissions tests read the section of `job show --full` |
| `tests/test_command_catalog.py` | +1 / -1 | `job.permissions` leaves `REQUIRED` and joins `TestDeletedCommands` |

### 178ae847 F261 R8 C5: mark R-0896 and R-0806 landed

| Path | +/- | Reason |
|---|---|---|
| `.agent/live_review.md` | +4 / -0 | slice LANDED8 appended: `Landed: R-0896 —` and `Landed: R-0806 —` |

### C6 — this commit (self-reference, R-0149 pattern)

| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | NO NUMBERS | this handback; its own numstat is reported in the completion message only |

## External actions

| Command | Outcome |
|---|---|
| `git worktree add --detach .remedy-wt/f261r8w/wt 720874b8` | created for G5; restored after each mutation with `git -C .remedy-wt/f261r8w/wt checkout -- <file>` (rc 0, worktree status `''` after each), then removed with `git worktree remove --force .remedy-wt/f261r8w/wt`; `git worktree list` then read one row and `git branch --list 'remedy/job-*'` 16 lines |
| `git push origin feature/f261-cli-vocabulary-v2` | the one push, after this commit; its result is in the completion message (G8) |
| pull request create / merge / force-push / branch delete / `remedy` | NOT RUN |

## Verification

The scripts and raw outputs are under `.remedy-wt/f261r8w/`, not committed. Every exit code below is the real return
code of the command as the tool reported it.

| Gate | At | REAL exit | Decisive reading |
|---|---|---|---|
| G1 transport | after C1 `1c3bf3e3` | `g12.py` 0 | sha256 of `.agent/authored/f261-r8.md` at C0a `2da5521352b55cac563eadaa828144af0435198ab6609057f822824147439e7a`, **equal** to the delegated digest; `.agent/last_block.md` at C0b **byte-identical**. Slices FOUND **8** (PLAN8, RECORD8, DEC7, P273-FROM, ACC273, LANDED8, MUT-B-FROM, MUT-B-TO), each **matching** its BEGIN-marker sha256. Committed carriers read at C4 by `g34.py` (exit 0): show-1 `011479d6fa07a1fbb37e760db790334562cf5297243d4c7da3b1a183cf23190e`, show-2 `b8134144d0ec1c953be1171392245c29678133b3552ef10dd7da5c107cb13169`, show-3 `10d1c62056bcb60e99e9536742188d6e4b74f69eb05df984c55b40cb9f475b98`, each **equal** |
| G2 the record | C1 | `g12.py` 0 | `plan.md` **equals** PLAN8; **38** lines; `^## Goal$` **1**; `^## Next Steps$` **1**. `live_review.md` **equals** its `22173331` blob + RECORD8; `decisions.md` **equals** its `22173331` blob + DEC7; `T2_F273.md` **equals** its `22173331` blob with P273's FROM (count **1**) replaced by its TO. `^Gate: F\d+ R\d+ — ` **116** → **117**; `Gate: F261 R7 — ` **1** at C1; distinct `^- R-\d+ — ` **100** → **103**, C1 minus base `R-0898`, `R-0899`, `R-0900`, base minus C1 empty; distinct `^Done: R-\d+ — ` **4** → **4**; open by distinct id **96** → **99** |
| G3 the show commits | C2 `9d8d57f6`, C3 `068ee126`, C4 `720874b8` | `g34.py` 0 | tables: show-1 **10** rows, show-2 **9**, show-3 **15**, every count as stated, no target existed. `--no-renames --name-only` from each parent: exactly the carrier and the paths G3 names, at each commit. Trees, each **match**: C2 `apps` `6a32ca21…`, `packages` `66fcac08…`, `tests` `6da54dc5…`; C3 `apps` `cd096440…`, `packages` `8ae6a584…`, `tests` `97fe2f2f…`; C4 `apps` `92dc18cc…`, `packages` `f614c5a2…`, `tests` `6207c33b…`, `docs/system` `a2a587aa…`. At all three, `scripts` and `README.md` **equal** `22173331` and `docs/roadmap` **equals** C1; at C2 and C3 `docs` **equals** C1. Insertions: C2 **199** (10 deletions), C3 **308** (6), C4 **177** (77) |
| G4 the sweep | C4 `720874b8` | `g34.py` 0 | the `git grep` exit **0**, exactly one line: `720874b8:tests/test_command_catalog.py:306:        "job.permissions",`. `python3 -m ruff check` over the 11 `.py` paths of C2, C3 and C4: exit **0**, `All checks passed!` |
| G5(a) control | worktree at C4 | 0 | `apps.cli.commands.job` (and `apps.cli.command_catalog`, `packages.orchestration.pingpong_job`) loaded from the worktree; `52 passed in 1.73s`; **0** failed nodes |
| G5(b) MUT-B-FROM → MUT-B-TO in `apps/cli/command_catalog.py` | same worktree | 1 | count **1**; `5 failed, 47 passed in 1.74s`; **5** failed nodes, `test_every_advertised_flag_is_declared_by_its_command` **among them** |
| G5(c) `BLOCKED_TASK_FINDINGS_CAP = 10` → `11` | same worktree, after `checkout --` | 1 | count **1**; `1 failed, 51 passed in 1.65s`; **1** failed node, `TestBlockedTaskFindings::test_the_default_shows_ten_findings_and_names_the_overflow` |
| G5(d) `last = rounds[-1]` → `rounds[0]` | same worktree, after `checkout --` | 1 | count **1**; `3 failed, 49 passed in 1.73s`; **3** failed nodes, `TestBlockedTaskFindings::test_only_the_last_round_of_the_blocked_task_appears` **among them** |
| G5(e) `except Exception as exc:  # noqa: BLE001` → `except KeyError …` | same worktree, after `checkout --` | 1 | count **1**; `1 failed, 51 passed in 1.77s`; **1** failed node, `TestSections::test_a_raising_section_becomes_section_failed_and_the_command_exits_zero` |
| G5(f) a `"job.permissions"` row before `"job.budget"` | same worktree, after `checkout --` | 1 | count **1**; `1 failed, 51 passed in 1.79s`; **1** failed node, `TestDeletedCommands::test_no_deleted_id_is_left_in_the_dispatch_table` |
| G5(g) `shown["blocked_task_findings"] = []` | same worktree, after `checkout --` | 1 | count **1**; `6 failed, 46 passed in 1.81s`; **6** failed nodes, `TestABlockedFakeRunShowsItsFindingText::test_the_persisted_finding_summary_appears_in_job_show` **among them** |
| G6 the landed lines | C5 `178ae847` | `g6.py` 0 | `live_review.md` **equals** its C4 blob + LANDED8; among the added lines `^Landed: R-0896 — ` **1** and `^Landed: R-0806 — ` **1**; open by distinct id **99** at C4 and **99** at C5, **equal** as sets |
| G7 the suite, SPEC S | primary checkout at C5, serially | 0 | `suite.py`: argv `python3 -B -m pytest -q -p no:randomly -p no:cacheprovider --tb=short -rfEs`, `PYTHONPATH`, `REMEDY_PROJECT`, `REMEDY_DATA_DIR` removed, `PYTHONDONTWRITEBYTECODE=1`; last line `18193 passed, 23 skipped, 1 warning in 1465.96s (0:24:25)`; distinct bad nodes **0**, so no re-run; `git status --porcelain` `''` afterwards |
| G8 the tree | after C6 and the push | not yet run | reported in the completion message only |

Open findings: **99** by distinct id. The open High ids are **R-0803, R-0804, R-0806 and R-0807**. R-0896 and R-0806
are marked **landed** at C5; a landed finding stays open until its `Done:` line.

Operator questions open: 0

## Authored-text proofs

| Text | Target | Result |
|---|---|---|
| the block | `.agent/authored/f261-r8.md`, `.agent/last_block.md` | sha256 **equal** to the delegated digest at C0a; mirror byte-identical at C0b (G1) |
| PLAN8 | `.agent/plan.md` | **equal** at C1 (G2) |
| RECORD8, DEC7 | `.agent/live_review.md`, `.agent/decisions.md` | each **equal** to its `22173331` blob followed by the slice at C1 (G2) |
| P273-FROM → ACC273 | `docs/roadmap/features/T2_F273.md` | **equal** to its `22173331` blob with FROM replaced by TO at C1 (G2) |
| show tables 1, 2, 3 | `.agent/authored/f261-r8-show-{1,2,3}.jsonl` and their paths | carrier digests **equal**; the C2, C3 and C4 trees equal the reviewer's dry run (G3) |
| LANDED8 | `.agent/live_review.md` | **equal** to its C4 blob followed by the slice at C5 (G6) |
| MUT-B-FROM, MUT-B-TO | the G5(b) worktree only | used as the mutation bytes; never written to the checkout |

NO SLICE AND NO TABLE WAS EDITED. Every slice was extracted programmatically as the bytes strictly between its `BEGIN`
and `END` lines and verified against its BEGIN-marker sha256 before use; each table was verified against its digest
before it was applied and copied.

## Item-status table

| Item | Status | Reason |
|---|---|---|
| C0a / C0b | done | two commits, as the Bundle orders |
| C1 PLAN8, RECORD8, DEC7, P273 | done | one commit, the first substantive commit |
| C2 show table 1 | done | one commit |
| C3 show table 2 | done | one commit |
| C4 show table 3 | done | one commit |
| C5 LANDED8 | done | one commit |
| C6 handoff | done | this commit |
| G1 · G2 · G3 · G4 · G5 · G6 · G7 | done | exit codes and readings above |
| G8 | skipped | runs after this commit and its push; results in the completion message |

## Deviations & assumptions

1. **The first G5(a) control run never reached pytest.** My scratch helper `.remedy-wt/f261r8w/copy.py` sat in the
   runner's own directory, which Python puts first on `sys.path`, so it shadowed the standard library `copy` module
   and the runner's import of `apps.cli.commands.job` raised `IndexError` (exit 1, no test collected). That is a
   harness defect, not a gate reading: I renamed the helper to `copyfile_check.py`, confirmed the worktree status read
   `''`, and re-ran the control, which read exit 0 as recorded above. No mutation had been applied before it.
2. **G1's carrier clause was read at C4, not after C1.** Constraint 8 places G1 after C1, but the carriers are first
   committed at C2 to C4; their committed digests were read by `g34.py` at C4, and each source carrier's digest was
   also verified before its table was applied and copied.
3. **Tables were applied directly on disk.** `.remedy-wt/f261r8w/apply_table.py` checks the carrier digest, then
   applies every row strictly in file order against the tree the previous rows left, with `encoding="utf-8",
   newline=""`, the exact-count check and the must-not-exist check, stopping on the first mismatch; it copies the
   carrier after the last row. No count differed and no target existed, so no STOP arose.
4. **G5 ran through a runner**, `.remedy-wt/f261r8w/runner.py`, invoked as `python3 -B`: it changes into the worktree,
   puts it first on `sys.path` and in `PYTHONPATH`, removes `REMEDY_PROJECT` and `REMEDY_DATA_DIR`, sets
   `PYTHONDONTWRITEBYTECODE=1`, asserts that `apps.cli.commands.job`, and also `apps.cli.command_catalog` and
   `packages.orchestration.pingpong_job`, loaded from inside the worktree, and calls `pytest.main` with
   `-q -p no:randomly -p no:cacheprovider -rf --tb=no` over the three test files G5 names.
5. **The open set** was computed as the distinct `^- R-\d+ — ` ids minus the distinct `^Done: R-\d+ — ` ids; a
   `Landed:` line does not close a finding.
6. **The suite ran in the foreground**, inside one tool call with a 60-minute limit, from the primary checkout; it
   finished in 24 minutes and nothing else ran meanwhile.
7. **File reading before edits.** The tables and slices were applied programmatically, so instead of reading each
   target file in full I read the unstaged diff of each of C1 to C5 before committing; the byte-equality, tree-id
   gates and ruff prove each result.

## Next

1. Phase 1 rule 1: the next session reads `.agent/STOP` first.
2. The reviewer's verdict on round 8.
3. The folds of `job assumptions`, `job fences` and `job dod` into sections of `job show --full`.
