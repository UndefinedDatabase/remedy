# Handback — F261 round 2

## Session

`SESSION 1 of feature F261 · round 2 · rounds so far 2`

Context self-assessment: this worker's context is comfortable, and nothing in the round was cut short.

## Range

Review of `0fbe97c1`..`HEAD`: C0a, C0b, C1, C2 and C3, plus this handback commit C4. `.agent/STOP` was ABSENT at all
three readings constraint 2 orders (before C0a, before C2, before C4): `.remedy-wt/f261r2w/stop.py` printed
`STOP exists: False` and exited 0 each time.

## Commits

### c200b024 F261 R2 C0a: save the round 2 step block

| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f261-r2.md` | +204 / -0 | the block, copied with `shutil.copyfile`; sha256 equal to the delegated digest |

### 29ccc3e2 F261 R2 C0b: mirror the round 2 step block into last_block

| Path | +/- | Reason |
|---|---|---|
| `.agent/last_block.md` | +152 / -395 | the same bytes, the mirror |

### 8ad30506 F261 R2 C1: re-point the plan at round 2, book F261 round 1's PASS, register R-0891

This is the FIRST SUBSTANTIVE COMMIT.

| Path | +/- | Reason |
|---|---|---|
| `.agent/live_review.md` | +4 / -0 | slice RECORD2 appended: `Gate: F261 R1 —` PASS and the registration of R-0891 |
| `.agent/plan.md` | +16 / -19 | slice PLAN2, a full replacement: 1824 bytes, 36 lines |
| `.agent/prose_slips.md` | +2 / -0 | slice SLIP2 appended |

### 9554eed8 F261 R2 C2: rename do job-promote to job apply, by edit table A

| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f261-r2-rename-a.jsonl` | +19 / -0 | the edit table, copied with `shutil.copyfile`; sha256 `71f42b5d…68503b3` equal |
| `apps/cli/command_catalog.py` | +5 / -5 | table A lines 1–3 |
| `apps/cli/commands/do_cmd.py` | +4 / -4 | lines 4–6 |
| `packages/orchestration/job_promote.py` | +1 / -1 | line 7 |
| `packages/orchestration/pingpong_job.py` | +1 / -1 | line 8 |
| `tests/orchestration/test_job_promote.py` | +19 / -19 | lines 9–14 |
| `tests/orchestration/test_job_task_runner.py` | +5 / -4 | lines 15–16 |
| `tests/orchestration/test_job_worktree_handoff.py` | +1 / -1 | line 17 |
| `tests/test_command_catalog.py` | +1 / -0 | line 19: the `("do.job-promote", "job.apply")` pair in `TestRenamedCommands` |
| `tests/test_observability_index.py` | +1 / -1 | line 18 |

### 2027d797 F261 R2 C3: rename do job-run to job run, by edit table B, and name job resume in the F114 paragraph

| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f261-r2-rename-b.jsonl` | +48 / -0 | the edit table, copied with `shutil.copyfile`; sha256 `bb8e4ff2…315625b` equal |
| `README.md` | +2 / -2 | lines 45–46: the F114 paragraph names `remedy job resume` and `job.resume` (R-0891) |
| `apps/cli/command_catalog.py` | +11 / -11 | lines 1–2 |
| `apps/cli/commands/do_cmd.py` | +7 / -7 | lines 3–6 |
| `apps/cli/commands/run_invocation.py` | +1 / -1 | line 7 |
| `docs/system/core-product-spine-v0.md` | +1 / -1 | line 12 |
| `packages/orchestration/job_evidence.py` | +1 / -1 | line 8 |
| `packages/orchestration/pingpong_job.py` | +3 / -3 | line 9 |
| `packages/orchestration/pingpong_provider.py` | +1 / -1 | line 10 |
| `packages/orchestration/self_use_job.py` | +2 / -2 | line 11 |
| `tests/cli/test_job_context_cmd.py` | +1 / -1 | line 18 |
| `tests/cli/test_job_run_invocation_truth.py` | +9 / -9 | lines 14, 15, 43, 44 |
| `tests/cli/test_stream_evidence_tristate.py` | +1 / -1 | line 16 |
| `tests/cli/test_teach_cmd.py` | +1 / -1 | line 17 |
| `tests/orchestration/test_f018_authority_integration.py` | +4 / -4 | lines 20–21 |
| `tests/orchestration/test_job_plan_state_reads.py` | +1 / -1 | line 19 |
| `tests/orchestration/test_job_state_field.py` | +2 / -2 | line 22 |
| `tests/orchestration/test_job_task_runner.py` | +46 / -46 | lines 29–34, 42 |
| `tests/orchestration/test_job_worktree_handoff.py` | +4 / -4 | lines 23–24 |
| `tests/orchestration/test_job_worktree_integration.py` | +1 / -1 | line 25 |
| `tests/orchestration/test_token_ledger.py` | +7 / -7 | lines 26–28 |
| `tests/test_command_catalog.py` | +3 / -2 | lines 13, 47, 48: the `("do.job-run", "job.run")` pair and the two tests renamed after `job resume` (R-0891) |
| `tests/test_do_job_flow.py` | +17 / -17 | lines 35–41 |

### C4 — this commit (self-reference, R-0149 pattern)

| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | NO NUMBERS | this handback; its own numstat is reported in the completion message only |

## External actions

| Command | Outcome |
|---|---|
| `git worktree add --detach .remedy-wt/f261r2w/wt 2027d797…` | created for G5; restored after each mutation with `git -C .remedy-wt/f261r2w/wt checkout -- <file>` (worktree status `''` after each), then removed with `git worktree remove .remedy-wt/f261r2w/wt`; `git worktree list` then read one row |
| `git push origin feature/f261-cli-vocabulary-v2` | the one push, after this commit; its result is in the completion message (G7) |
| pull request create / merge / force-push / branch delete / `remedy` | NOT RUN |

## Verification

The scripts and raw outputs are under `.remedy-wt/f261r2w/`, not committed. Every exit code below is the real return
code, printed by `.remedy-wt/f261r2w/rc.py` or by the gate script's own subprocess reading.

| Gate | At | REAL exit | Decisive reading |
|---|---|---|---|
| G1 transport | after C1 `8ad30506` | `g1g2.py` 0 | sha256 of `.agent/authored/f261-r2.md` at C0a `eda09a473f68d21415536f16a5ecfb8a7866e93eabfb946f26eaf5806c0669c9`, **equal** to the delegated digest; `.agent/last_block.md` at C0b **byte-identical**. Slices FOUND **3** (PLAN2, RECORD2, SLIP2), each **matching** its BEGIN-marker sha256. Committed carriers: rename A at C2 `71f42b5d936f21ed730bea12a3eccb90fcf913cc939a9b3044f7b39aa68503b3` **equal**; rename B at C3 `bb8e4ff2e0a16065cb4fbdfbfd08e7929c3cc69d47a3ec237144f0445315625b` **equal** (read by `g3g4.py`) |
| G2 bookkeeping | C1 | `g1g2.py` 0 | `plan.md` **equals** PLAN2; **36** lines; `^## Goal$` **1**; `^## Next Steps$` **1**. `live_review.md` **equals** its `0fbe97c1` blob + RECORD2; `prose_slips.md` **equals** its `0fbe97c1` blob + SLIP2. `^Gate: F\d+ R\d+ — ` **110** → **111**; `Gate: F261 R1 — ` **1**; open by distinct id **90** → **91**; C1 minus base `['R-0891']`, base minus C1 `[]` |
| G3 rename A | C2 `9554eed8` | `g3g4.py a` 0 | table A: all **19** lines matched their counts. numstat names exactly the **10** paths, 57 insertions. Trees: `apps` `0436a56ed63741607de0d9a3b2e81734f77efd13`, `packages` `a6ad0e0d18d870db078a176a7819d1034e32bcac`, `tests` `bc90517f0d15228739cd0db35f5b2b90562b4c33`, each **match** |
| G4 rename B | C3 `2027d797` | `g3g4.py b` 0; ruff 0 | table B: all **48** lines matched their counts. numstat names exactly the **23** paths, 174 insertions. Trees: `apps` `508aa87f…`, `packages` `ffa8be24…`, `tests` `3ba748d7…`, `docs/system` `4ac761f1…`, `README.md` `9d94d8b5…`, each **match**; `scripts` `79be9d31e1da20b56515616d2b87450257d7d4cf` at base and C3. `git grep` exit 0, exactly **2** lines: `tests/test_command_catalog.py:275:        ("do.job-promote", "job.apply"),` and `tests/test_command_catalog.py:276:        ("do.job-run", "job.run"),`. `python3 -m ruff check` over the **23** `.py` paths of C2 and C3: `All checks passed!` |
| G5(a) control | worktree at C3 | 0 | module loaded from the worktree; `28 passed in 0.38s` |
| G5(b) `command_id="job.apply",` → `command_id="do.job-promote",` | same worktree | 1 | FROM count **1**; `4 failed, 24 passed in 0.37s`; failed: `tests/test_command_catalog.py::TestCatalogIntegrity::test_command_id_format`, `…::TestCatalogIntegrity::test_every_related_reference_resolves_to_a_live_command`, `…::TestRenamedCommands::test_no_old_id_is_left_in_the_catalog`, `…::TestRenamedCommands::test_every_new_id_parses_from_its_words_and_has_a_handler` |
| G5(c) `"job.run": lambda` → `"job.rum": lambda` | same worktree, after `checkout --` | 1 | FROM count **1**; `1 failed, 27 passed in 0.37s`; failed: `tests/test_command_catalog.py::TestRenamedCommands::test_every_new_id_parses_from_its_words_and_has_a_handler` |
| G6 suites | primary checkout at C3, serially | each 0 | `tests/test_command_catalog.py` 28 passed · `tests/cli/` 1347 passed · `tests/test_grouped_cli.py` 397 passed · `tests/test_do_job_flow.py` 178 passed · `tests/test_observability_index.py` 14 passed · `tests/orchestration/test_job_promote.py` 85 passed · `tests/orchestration/test_job_task_runner.py` 214 passed · `tests/orchestration/test_job_worktree_handoff.py` 26 passed · `tests/orchestration/test_f018_authority_integration.py` 114 passed · `tests/orchestration/test_job_plan_state_reads.py` 4 passed · `tests/orchestration/test_job_state_field.py` 14 passed · `tests/orchestration/test_job_worktree_integration.py` 13 passed · `tests/orchestration/test_token_ledger.py` 120 passed · `tests/docs/` 306 passed · `tests/ui_server/test_dashboard_contract.py` 74 passed |
| G7 the tree | after C4 and the push | not yet run | reported in the completion message only |

Open findings: **91** by distinct id, R-0891 among them (Low, owner F261). The open High ids are **R-0803, R-0804,
R-0806 and R-0807**.

## Authored-text proofs

| Text | Target | Result |
|---|---|---|
| the block | `.agent/authored/f261-r2.md`, `.agent/last_block.md` | sha256 **equal** to the delegated digest at C0a; mirror byte-identical at C0b (G1) |
| PLAN2 | `.agent/plan.md` | **equal** at C1 (G2) |
| RECORD2, SLIP2 | `.agent/live_review.md`, `.agent/prose_slips.md` | each **equal** to its `0fbe97c1` blob followed by the slice at C1 (G2) |
| edit table A | `.agent/authored/f261-r2-rename-a.jsonl` and its 9 paths | carrier digest **equal**; the C2 `apps`, `packages` and `tests` trees equal the reviewer's dry run (G3) |
| edit table B | `.agent/authored/f261-r2-rename-b.jsonl` and its 22 paths | carrier digest **equal**; the C3 trees equal the reviewer's dry run (G4) |

NO SLICE AND NO TABLE WAS EDITED. Every slice was extracted programmatically from the COMMITTED
`.agent/authored/f261-r2.md` and verified against its BEGIN-marker sha256 before use; each table was verified against
its digest before it was copied and applied.

## Item-status table

| Item | Status | Reason |
|---|---|---|
| C0a / C0b | done | two commits, as the Bundle orders |
| C1 PLAN2, RECORD2, SLIP2 | done | one commit, the first substantive commit |
| C2 rename A | done | one commit |
| C3 rename B | done | one commit |
| C4 handoff | done | this commit |
| G1 · G2 · G3 · G4 · G5 · G6 | done | exit codes and readings above |
| G7 | skipped | runs after this commit and its push; results in the completion message |

## Deviations & assumptions

1. **G1's carrier clause was read at C2 and C3, not after C1.** Constraint 8 places G1 after C1, but the carriers are
   first committed at C2 and C3; their committed digests were read by `g3g4.py` right after each commit, and each source
   carrier's digest was also verified before `shutil.copyfile`.
2. **Each table was applied in memory first.** `.remedy-wt/f261r2w/apply_table.py` reads each path with
   `encoding="utf-8", newline=""`, applies the lines strictly in file order against the text the previous lines left,
   checks each count, and writes the files only after every count matched; the result is identical to writing after
   each line, and a mismatch would have left every target untouched. No count differed.
3. **G5 ran through a runner**, `.remedy-wt/f261r2w/runner.py`, invoked as `python3 -B`: it changes into the worktree,
   puts it first on `sys.path` and in `PYTHONPATH`, sets `PYTHONDONTWRITEBYTECODE`, asserts that
   `apps.cli.command_catalog` loaded from inside the worktree, and calls `pytest.main` with `-rf --tb=no` and the path.
4. **G6** ran through `.remedy-wt/f261r2w/g6.py`, which runs each exact `python3 -B -m pytest -q -p no:randomly <path>`
   argv serially as its own subprocess in the primary checkout and reads that subprocess's return code.
5. **File reading before edits.** The tables were applied programmatically, so instead of reading each of the 31 target
   files in full I read the whole `git diff` of C2 and of C3 before committing; the tree-id gates prove each result.

## Next

1. Phase 1 rule 1: the next session reads `.agent/STOP` first.
2. The reviewer's verdict on round 2.
3. The deletion of `do job-flow`, with its deletion paragraph.

Operator questions open: 1
