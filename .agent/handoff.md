# Handback — F261 round 9

## Session

`SESSION 2 of feature F261 · round 9 · rounds so far 9`

Context self-assessment: this worker's context is comfortable, and nothing in the round was cut short.

## Range

Review of `aff2b676`..`HEAD`: C0a, C0b, C1, C2, C3 and C4, plus this handback commit C5. `.agent/STOP` was ABSENT at
all three readings constraint 2 orders: before C0a (`ls -la .agent/STOP` exit 2, "No such file or directory"), before
C2 (exit 2) and before C5 (exit 2).

## Commits

### da6f26fe F261 R9 C0a: save the round 9 step block

| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f261-r9.md` | +286 / -0 | the block, copied with `shutil.copyfile`; sha256 equal to the delegated digest |

### 743c09be F261 R9 C0b: mirror the round 9 step block into last_block

| Path | +/- | Reason |
|---|---|---|
| `.agent/last_block.md` | +174 / -183 | the same bytes, the mirror |

### 873d8e49 F261 R9 C1: re-point the plan at round 9, book round 8's PASS and the resolutions of R-0896 and R-0806, record DECISION F261 D8

This is the FIRST SUBSTANTIVE COMMIT. Commit total per constraint 5: **29** insertions, 13 deletions.

| Path | +/- | Reason |
|---|---|---|
| `.agent/decisions.md` | +14 / -0 | slice DEC8 appended: DECISION F261 D8 |
| `.agent/live_review.md` | +6 / -0 | slice RECORD9 appended: `Gate: F261 R8 —` PASS and the resolution paragraphs of R-0896 and R-0806 |
| `.agent/plan.md` | +9 / -13 | slice PLAN9, a full replacement: 34 lines |

### 9d6b8791 F261 R9 C2: fold job assumptions into the assumptions section of job show --full, by fold table 1

Commit total per constraint 5: **74** insertions, 58 deletions.

| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f261-r9-fold-1.jsonl` | +11 / -0 | the table, copied with `shutil.copyfile`; sha256 `a1a7ae9b…a0f9fa1` equal |
| `apps/cli/command_catalog.py` | +1 / -11 | the `--full` help names assumptions; entry `job.assumptions` deleted |
| `apps/cli/commands/job.py` | +22 / -27 | `_assumptions_section` registered; `_cmd_job_assumptions` and its handler row deleted |
| `tests/cli/test_decision_answers.py` | +38 / -19 | `TestAssumptionsCommand` reads the section of `job show --full` |
| `tests/cli/test_job_show.py` | +1 / -1 | the registry reads `permissions`, `assumptions` |
| `tests/test_command_catalog.py` | +1 / -0 | `job.assumptions` joins `TestDeletedCommands` |

### d683f3ed F261 R9 C3: fold job fences into the fences section of job show --full and let a section name its own error, by fold table 2

Commit total per constraint 5: **213** insertions, 166 deletions.

| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f261-r9-fold-2.jsonl` | +20 / -0 | the table, copied with `shutil.copyfile`; sha256 `b5dbef9a…24028fc03` equal |
| `apps/cli/command_catalog.py` | +2 / -13 | the `--full` help names fences; entry `job.fences` deleted; `job context` relates to `job show` alone |
| `apps/cli/commands/job.py` | +86 / -96 | `ShowSectionError`, its envelope in `_build_show_sections`, `_fences_section` registered; `_cmd_job_fences` and its handler row deleted |
| `apps/cli/commands/job_context_cmd.py` | +4 / -3 | the docstring names the `fences` section |
| `docs/guides/job-context-view-user-guide-v0.md` | +4 / -2 | the guide names the `fences` section |
| `tests/cli/test_job_show.py` | +21 / -1 | the registry order; a `ShowSectionError` becomes its own code and the command exits 0 |
| `tests/orchestration/test_fence_e2e.py` | +9 / -6 | `TestJobFencesCLI` reads `job show` and the registry |
| `tests/orchestration/test_fence_production_e2e.py` | +66 / -45 | `TestCLIJobFences` reads the section; the four error codes |
| `tests/test_command_catalog.py` | +1 / -0 | `job.fences` joins `TestDeletedCommands` |

### 64e54c35 F261 R9 C4: fold job dod into the dod section of job show --full, by fold table 3

Commit total per constraint 5: **91** insertions, 115 deletions.

| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f261-r9-fold-3.jsonl` | +10 / -0 | the table, copied with `shutil.copyfile`; sha256 `683e6c05…07165491` equal |
| `apps/cli/command_catalog.py` | +2 / -12 | the `--full` help names the Definition of Done; entry `job.dod` deleted |
| `apps/cli/commands/job.py` | +49 / -79 | `_dod_section` registered; `_cmd_job_dod` and its handler row deleted |
| `tests/cli/test_job_show.py` | +1 / -1 | the registry reads `permissions`, `fences`, `assumptions`, `dod` |
| `tests/orchestration/test_dod_gate.py` | +28 / -23 | `TestJobDodCommand` reads the section of `job show --full` |
| `tests/test_command_catalog.py` | +1 / -0 | `job.dod` joins `TestDeletedCommands` |

### C5 — this commit (self-reference, R-0149 pattern)

| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | NO NUMBERS | this handback; its own numstat is reported in the completion message only |

## External actions

| Command | Outcome |
|---|---|
| `git worktree add --detach .remedy-wt/f261r9w/wt 64e54c35` | created for G5; restored after each mutation with `git -C .remedy-wt/f261r9w/wt checkout -- apps/cli/commands/job.py` (rc 0, worktree status `''` after each), then removed with `git worktree remove --force .remedy-wt/f261r9w/wt`; `git worktree list` then read one row and `git branch --list 'remedy/job-*'` 16 lines |
| `git push origin feature/f261-cli-vocabulary-v2` | the one push, after this commit; its result is in the completion message (G7) |
| pull request create / merge / force-push / branch delete / `remedy` | NOT RUN |

## Verification

The scripts and raw outputs are under `.remedy-wt/f261r9w/`, not committed. Every exit code below is the real return
code of the command as the tool reported it.

| Gate | At | REAL exit | Decisive reading |
|---|---|---|---|
| G1 transport | after C1 `873d8e49` | `gate_g1g2.py` 0 | sha256 of `.agent/authored/f261-r9.md` at C0a `41710658bb8d027160387a4b0f83c8a2d96d3eaa63d1881a214641ca8c4c4fdb`, **equal** to the delegated digest; `.agent/last_block.md` at C0b **byte-identical**. Slices FOUND **13** (PLAN9, RECORD9, DEC8, MUT-1-FROM to MUT-5-TO), each **matching** its BEGIN-marker sha256. Committed carriers read by `gate_g3g4.py` (exit 0): fold-1 at C2 `a1a7ae9b68ba24d067b58ca05998e396571be911cec0592f86256d131a0f9fa1`, fold-2 at C3 `b5dbef9a488431e85ef88dcd3ff95087ca8feb66ee57925041332cd24028fc03`, fold-3 at C4 `683e6c0595e342975b74272131c7892ee12be9c8ca72dae88a8e04e607165491`, each **equal** |
| G2 the record | C1 | `gate_g1g2.py` 0 | `plan.md` **equals** PLAN9; **34** lines; `^## Goal$` **1**; `^## Next Steps$` **1**. `live_review.md` **equals** its `aff2b676` blob + RECORD9; `decisions.md` **equals** its `aff2b676` blob + DEC8. `^Gate: F\d+ R\d+ — ` **117** → **118**; `Gate: F261 R8 — ` **1** at C1; distinct `^- R-\d+ — ` **103** → **103**; distinct `^Done: R-\d+ — ` **4** → **6**, C1 minus base `R-0806`, `R-0896`, base minus C1 empty; open by distinct id **99** → **97** |
| G3 the folds | C2 `9d6b8791`, C3 `d683f3ed`, C4 `64e54c35` | `gate_g3g4.py` 0 | tables: fold-1 **11** rows, fold-2 **20**, fold-3 **10**, every count **1** as stated. `--no-renames --name-only` from each parent: exactly the carrier and the paths G3 names, at each commit. Trees, each **match**: C2 `apps` `fd8eab43…`, `tests` `2b5ab527…`; C3 `apps` `d14bb7f2…`, `tests` `fdbb77e5…`, `docs` `d74ed73f…`; C4 `apps` `d8be0bc2…`, `tests` `7979b693…`, `docs` `d74ed73f…`. At all three, `packages`, `scripts` and `README.md` **equal** `aff2b676`; at C2 `docs` **equals** `aff2b676`. Insertions: C2 **74** (58 deletions), C3 **213** (166), C4 **91** (115) |
| G4 the sweep | C4 `64e54c35` | `gate_g3g4.py` 0 | the fixed-string `git grep` exit **0**, exactly three lines: `64e54c35:tests/test_command_catalog.py:306:        "job.assumptions",`, `…:307:        "job.dod",`, `…:308:        "job.fences",`. The extended `git grep` of `remedy job (assumptions\|fences\|dod)\b` exit **1**, stdout `''`. `python3 -m ruff check` over the 9 `.py` paths of C2, C3 and C4: exit **0**, `All checks passed!` |
| G5(a) control | worktree at C4 | 0 | `apps.cli.commands.job` loaded from the worktree; `256 passed in 6.48s`; **0** failed nodes |
| G5(1) a `job.fences` handler row | same worktree | 1 | MUT-1-FROM count **1**; `1 failed, 255 passed in 6.45s`; **1** failed node, `TestDeletedCommands::test_no_deleted_id_is_left_in_the_dispatch_table` **among them** |
| G5(2) a plain `RuntimeError` for a missing target repo | same worktree, after `checkout --` | 1 | MUT-2-FROM count **1**; `1 failed, 255 passed in 6.42s`; **1** failed node, `TestCLIJobFences::test_missing_target_repo_is_a_no_target_repo_error` **among them** |
| G5(3) two registry entries swapped | same worktree, after `checkout --` | 1 | MUT-3-FROM count **1**; `1 failed, 255 passed in 6.41s`; **1** failed node, `TestSections::test_full_prints_the_registered_sections_in_the_d4_order` **among them** |
| G5(4) the dod `check_count` key dropped | same worktree, after `checkout --` | 1 | MUT-4-FROM count **1**; `2 failed, 254 passed in 6.33s`; **2** failed nodes, `TestJobDodCommand::test_json_output_carries_the_gate_record` **among them** (the other `TestJobDodCommand::test_a_job_with_no_dod_says_so`) |
| G5(5) empty assumptions markdown | same worktree, after `checkout --` | 1 | MUT-5-FROM count **1**; `2 failed, 254 passed in 6.32s`; **2** failed nodes, `TestAssumptionsCommand::test_the_section_holds_the_log` **among them** (the other `TestAssumptionsCommand::test_the_section_on_a_job_without_a_plan`) |
| G6 the suite, SPEC S | primary checkout at C4, serially | 0 | `suite_spec.py`: argv `python3 -B -m pytest -q -p no:randomly -p no:cacheprovider --tb=short -rfEs`, `PYTHONPATH`, `REMEDY_PROJECT`, `REMEDY_DATA_DIR` removed, `PYTHONDONTWRITEBYTECODE=1`; last line `18196 passed, 23 skipped, 1 warning in 1327.75s (0:22:07)`; distinct bad nodes **0**, so no re-run; `git status --porcelain` `''` afterwards |
| G7 the tree | after C5 and the push | not yet run | reported in the completion message only |

Open findings: **97** by distinct id. The open High ids are **R-0803, R-0804 and R-0807**.

Operator questions open: 0

## Authored-text proofs

| Text | Target | Result |
|---|---|---|
| the block | `.agent/authored/f261-r9.md`, `.agent/last_block.md` | sha256 **equal** to the delegated digest at C0a; mirror byte-identical at C0b (G1) |
| PLAN9 | `.agent/plan.md` | **equal** at C1 (G2) |
| RECORD9, DEC8 | `.agent/live_review.md`, `.agent/decisions.md` | each **equal** to its `aff2b676` blob followed by the slice at C1 (G2) |
| fold tables 1, 2, 3 | `.agent/authored/f261-r9-fold-{1,2,3}.jsonl` and their paths | carrier digests **equal**; the C2, C3 and C4 trees equal the reviewer's dry run (G3) |
| MUT-1-FROM to MUT-5-TO | the G5 worktree only | used as the mutation bytes; never written to the checkout |

NO SLICE AND NO TABLE WAS EDITED. Every slice was extracted programmatically as the bytes strictly between its `BEGIN`
and `END` lines and verified against its BEGIN-marker sha256 before use; each table was verified against its digest
before it was applied and copied.

## Item-status table

| Item | Status | Reason |
|---|---|---|
| C0a / C0b | done | two commits, as the Bundle orders |
| C1 PLAN9, RECORD9, DEC8 | done | one commit, the first substantive commit |
| C2 fold table 1, `job assumptions` | done | one commit |
| C3 fold table 2, `job fences` | done | one commit |
| C4 fold table 3, `job dod` | done | one commit |
| C5 handoff | done | this commit |
| G1 · G2 · G3 · G4 · G5 · G6 | done | exit codes and readings above |
| G7 | skipped | runs after this commit and its push; results in the completion message |

## Deviations & assumptions

1. **G1's carrier clause was read after C4, not after C1.** Constraint 8 places G1 after C1, but the carriers are first
   committed at C2 to C4; their committed digests were read by `gate_g3g4.py` after C4, and each source carrier's
   digest was also verified before its table was applied and copied.
2. **Tables were applied directly on disk.** `.remedy-wt/f261r9w/apply_table.py` checks the carrier digest, then
   applies every row strictly in file order against the tree the previous rows left, with `encoding="utf-8",
   newline=""`, the exact-count check and the must-not-exist check, stopping on the first mismatch; it copies the
   carrier after the last row. No count differed and no target existed, so no STOP arose.
3. **G5 ran through a runner**, `.remedy-wt/f261r9w/wt_runner.py`, invoked as `python3 -B`: it drops its own directory
   from `sys.path`, changes into the worktree, puts it first on `sys.path` and in `PYTHONPATH`, removes
   `REMEDY_PROJECT` and `REMEDY_DATA_DIR`, sets `PYTHONDONTWRITEBYTECODE=1`, asserts that `apps.cli.commands.job`
   loaded from inside the worktree, and calls `pytest.main` with `-q -p no:randomly -p no:cacheprovider -rf --tb=no`
   over the six test files G5 names.
4. **Commit subjects** were worded by this worker, since the block names each commit's content but not its subject.
5. **The open set** was computed as the distinct `^- R-\d+ — ` ids minus the distinct `^Done: R-\d+ — ` ids.
6. **The suite ran in the foreground**, inside one tool call with a 60-minute limit, from the primary checkout; it
   finished in 22 minutes and nothing else ran meanwhile.
7. **File reading before edits.** The tables and slices were applied programmatically, so instead of reading each
   target file in full I read the unstaged diff of each of C1 to C4 before committing; the byte-equality, tree-id
   gates and ruff prove each result.

## Next

1. Phase 1 rule 1: the next session reads `.agent/STOP` first.
2. The reviewer's verdict on round 9.
3. The folds of `job summary`, `job digest`, `job status` and `job report`.
