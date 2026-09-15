# Handback — F261 round 15

## Session

`SESSION 4 of feature F261 · round 15 · rounds so far 15`

Context self-assessment: this worker's context is comfortable, and nothing in the round was cut short.

## Range

Review of `8aa94f37`..`HEAD`: C0a, C0b, C1, C2, C3 and C4, plus this handback commit C5. `.agent/STOP` was ABSENT at
all three readings constraint 2 orders. Before C0a, `ls .agent/STOP` exited 2 (`No such file or directory`) and
`.remedy-wt/f261r15w/stop_check.py`, a `pathlib.Path.exists` reading, printed `STOP exists: False` and exited 0. Before
C2 and before C5 the same script printed `STOP exists: False` and exited 0.

Every gate G1 to G6 read green. No table row stopped.

## Commits

### b08cb881 F261 R15 C0a: save the round 15 step block

Commit total per constraint 5: **307** insertions, 0 deletions.

| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f261-r15.md` | +307 / -0 | the block, copied with `shutil.copyfile`; sha256 equal to the delegated digest |

### 9b58103c F261 R15 C0b: mirror the round 15 step block into last_block

Commit total per constraint 5: **130** insertions, 113 deletions.

| Path | +/- | Reason |
|---|---|---|
| `.agent/last_block.md` | +130 / -113 | the same bytes, the mirror |

### 42fe8f07 F261 R15 C1: re-point the plan at round 15, book round 14's PASS and its prose slip, register R-0904 for F273 and record DECISION F261 D14

This is the FIRST SUBSTANTIVE COMMIT. Commit total per constraint 5: **31** insertions, 9 deletions.

| Path | +/- | Reason |
|---|---|---|
| `.agent/decisions.md` | +12 / -0 | slice DEC14 appended: DECISION F261 D14 |
| `.agent/live_review.md` | +4 / -0 | slice RECORD15 appended: `Gate: F261 R14 —` PASS and R-0904 |
| `.agent/plan.md` | +10 / -9 | slice PLAN15, a full replacement: 35 lines |
| `.agent/prose_slips.md` | +2 / -0 | slice SLIP15 appended: the round 14 G3 slip |
| `docs/roadmap/features/T2_F273.md` | +3 / -0 | pair P273 (REWRITE): the R-0904 resolution line |

### 96a0f098 F261 R15 C2: delete the loop modules and the run report's loop reference, by the loop table

Commit total per constraint 5: **13** insertions, 1508 deletions.

| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f261-r15-loop.jsonl` | +12 / -0 | the table, 8 `edit` rows and 4 `delete`, copied with `shutil.copyfile`; sha256 equal |
| `packages/orchestration/loop_run.py` | +0 / -310 | DELETED |
| `packages/orchestration/loop_spec.py` | +0 / -339 | DELETED |
| `packages/orchestration/run_report.py` | +0 / -11 | the `loop_ref` field, its read of `LOOP_REF_METADATA_KEY` and the `- Loop:` line |
| `tests/docs/test_retired_promote_word.py` | +0 / -3 | the `loop_spec.py` kept-by-sense entry |
| `tests/orchestration/import_reachability_allowlist.txt` | +0 / -2 | `packages.orchestration.loop_run`, `packages.orchestration.loop_spec` |
| `tests/orchestration/test_loop_run.py` | +0 / -516 | DELETED |
| `tests/orchestration/test_loop_spec.py` | +0 / -292 | DELETED |
| `tests/orchestration/test_run_report.py` | +1 / -35 | the `loop_run` import and `TestLoopProvenanceLine` |

### 16d3940d F261 R15 C3: delete the queue command group, by the queue table

Commit total per constraint 5: **18** insertions, 708 deletions.

| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f261-r15-queue.jsonl` | +10 / -0 | the table, 8 `edit` rows and 2 `delete`, copied with `shutil.copyfile`; sha256 equal |
| `apps/cli/command_catalog.py` | +0 / -51 | the `queue` group and `queue.add`, `queue.list`, `queue.rm`, `queue.reclaim` |
| `apps/cli/commands/__init__.py` | +1 / -2 | `queue_cmd` leaves the import list and the handler loop |
| `apps/cli/commands/mission_cmd.py` | +2 / -2 | the docstring no longer names `remedy queue` |
| `apps/cli/commands/queue_cmd.py` | +0 / -280 | DELETED |
| `packages/orchestration/config.py` | +1 / -1 | the `queue.reclaim_ttl_minutes` description no longer names the deleted command |
| `tests/cli/test_queue_cmd.py` | +0 / -371 | DELETED |
| `tests/orchestration/import_reachability_allowlist.txt` | +0 / -1 | `apps.cli.commands.queue_cmd` |
| `tests/test_command_catalog.py` | +4 / -0 | the four `queue.*` ids join `TestDeletedCommands` |

### 3055e98f F261 R15 C4: delete the F048 job queue, its executor binding, configuration keys and data path, by the job queue table

Commit total per constraint 5: **16** insertions, 1761 deletions.

| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f261-r15-jobqueue.jsonl` | +15 / -0 | the table, 11 `edit` rows and 4 `delete`, copied with `shutil.copyfile`; sha256 equal |
| `packages/orchestration/config.py` | +0 / -25 | the `queue.executor_binding` and `queue.reclaim_ttl_minutes` keys |
| `packages/orchestration/data_paths.py` | +0 / -9 | `queue_dir` |
| `packages/orchestration/job_queue.py` | +0 / -682 | DELETED |
| `packages/orchestration/long_run_executor.py` | +0 / -141 | the F048 binding: `QueuePull`, `queue_binding_enabled`, `queued_entry_to_job`, `_pull_queue_when_idle`, `LEDGER_EVENT_QUEUE_PULL`, `CycleLoopResult.queue_pull`, the unused `contextlib` import |
| `packages/orchestration/mission_state.py` | +1 / -1 | the `_ID_RE` comment no longer names `job_queue` |
| `tests/docs/test_retired_promote_word.py` | +0 / -3 | the `job_queue.py` kept-by-sense entry |
| `tests/orchestration/import_reachability_allowlist.txt` | +0 / -1 | `packages.orchestration.job_queue` |
| `tests/orchestration/test_job_queue.py` | +0 / -526 | DELETED |
| `tests/orchestration/test_queue_concurrency.py` | +0 / -185 | DELETED |
| `tests/orchestration/test_queue_executor_binding.py` | +0 / -188 | DELETED |

### C5 — this commit (self-reference, R-0149 pattern)

| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | NO NUMBERS | this handback; its own numstat is reported in the completion message only |

## External actions

| Command | Outcome |
|---|---|
| `git worktree add --detach .remedy-wt/f261r15w/wt 3055e98f` | created for G5; restored after each mutation with `git -C .remedy-wt/f261r15w/wt checkout -- <that file>` (worktree status `''` after each), then removed with `git worktree remove --force .remedy-wt/f261r15w/wt` (exit 0); `git worktree list` then read one row and `git branch --list 'remedy/job-*'` 16 lines |
| `git push origin feature/f261-cli-vocabulary-v2` | the one push, after this commit; its result is in the completion message (G7) |
| pull request create / merge / force-push / branch delete / `remedy` | NOT RUN |

## Verification

The scripts and raw outputs are under `.remedy-wt/f261r15w/`, not committed. Every exit code below is the real return
code of the named script or command.

| Gate | At | REAL exit | Decisive reading |
|---|---|---|---|
| G1 transport | block after C0b; carriers after C4 | `gate_g1g2.py` 0; `gate_g3g4.py` 0 | sha256 of `.agent/authored/f261-r15.md` at C0a `5f62f9147cbf6ba6abc43e63e02cd95b132f62e5d3f326ae4ebdb93197889818`, **equal** to the delegated digest; `.agent/last_block.md` at C0b **byte-identical** (28494 bytes). Slices FOUND **14** (PLAN15, RECORD15, DEC14, SLIP15, P273-FROM, P273-TO, MUT-1-FROM to MUT-4-TO), each **matching** its BEGIN-marker sha256 (`slice_extract.py`). Committed carriers: loop at C2 `d0dd0c71…`, queue at C3 `1139f445…`, jobqueue at C4 `36e1ee46…`, each **equal** to its digest |
| G2 the record | C1 `42fe8f07` | `gate_g1g2.py` 0; `python3 -m pytest tests/docs/ -q` 0 | `plan.md` **equals** PLAN15; **35** lines; `^## Goal$` **1**; `^## Next Steps$` **1**. `live_review.md` **equals** its `8aa94f37` blob + RECORD15 (1024256 + 6009 = 1030265 bytes); `decisions.md` + DEC14 (1386040 + 3383 = 1389423); `prose_slips.md` + SLIP15 (308256 + 476 = 308732). P273: TO contains FROM **false**; FROM **1** at base, **0** at C1, TO **1** at C1; `T2_F273.md` **equals** its base blob with the pair applied. `^Gate: F\d+ R\d+ — ` **123** → **124**; `Gate: F261 R14 — ` **1** at C1; distinct `^- R-\d+ — ` **106** → **107**, C1 minus base exactly **R-0904**; distinct `^Done: R-\d+ — ` **8** → **8**; open by distinct id **98** → **99**. `tests/docs/`: `310 passed in 1.06s` |
| G3 the tables | C2 `96a0f098`, C3 `16d3940d`, C4 `3055e98f` | `gate_g3g4.py` 0 | tables: loop **12** rows, queue **10**, jobqueue **15**, every count as stated, every delete target present, no STOP. Each commit single-parent. `--no-renames --name-only` from each parent: exactly the carrier and the paths G3 names (9, 9 and 11 paths). `apps`, `tests`, `docs`, `scripts`, `packages`, `README.md` **all 18 match** the dry-run ids G3 gives. Insertions: C2 **13** (1508 deletions), C3 **18** (708), C4 **16** (1761) |
| G4 the sweep | C4 `3055e98f` | `gate_g3g4.py` 0 | the `git grep` at C4: exit **1**, stdout `''`, stderr `''`. `python3 -m ruff check` over the 11 `.py` paths of C2 to C4 that exist at C4 (absent: the 10 deleted `.py` files): exit **0**, `All checks passed!` |
| G5(a) control | worktree at C4 | 0 | `apps.cli.grouped` loaded from the worktree; `453 passed in 30.67s`; **0** failed nodes |
| G5(1) a `queue` handler row | same worktree | 1 | MUT-1-FROM count **1** in `apps/cli/commands/status_cmd.py`; `1 failed, 452 passed in 30.81s`; **1** failed node, `TestDeletedCommands::test_no_deleted_id_is_left_in_the_dispatch_table` **among them** |
| G5(2) the `queue` group without commands | same worktree, after `checkout --` | 1 | MUT-2-FROM count **1** in `apps/cli/command_catalog.py`; `1 failed, 460 passed in 31.19s`; **1** failed node, `TestCatalogIntegrity::test_every_group_has_at_least_one_command` **among them** |
| G5(3) the `job_queue` allowlist line | same worktree, after `checkout --` | 1 | MUT-3-FROM count **1** in `tests/orchestration/import_reachability_allowlist.txt`; `1 failed, 452 passed in 30.84s`; **1** failed node, `test_every_allowlist_entry_still_resolves_to_a_file_on_disk` **among them** |
| G5(4) the `loop_spec` allowlist line | same worktree, after `checkout --` | 1 | MUT-4-FROM count **1** in the same file; `1 failed, 452 passed in 31.31s`; **1** failed node, `test_every_allowlist_entry_still_resolves_to_a_file_on_disk` **among them** |
| G6 the suite, SPEC S | primary checkout at C4, serially | 0 | `suite_spec.py`: argv `python3 -B -m pytest -q -p no:randomly -p no:cacheprovider --tb=short -rfEs`, `PYTHONPATH`, `REMEDY_PROJECT`, `REMEDY_DATA_DIR` removed, `PYTHONDONTWRITEBYTECODE=1`; last line `18002 passed, 23 skipped, 1 warning in 1330.98s (0:22:10)`; distinct bad nodes **0**, so no re-run; `git status --porcelain` `''` and `git branch --list 'remedy/job-*'` 16 lines afterwards |
| G7 the tree | after C5 and the push | not yet run | reported in the completion message only |

Open findings: **99** by distinct id. The open High ids are **R-0803, R-0804 and R-0807**.

## Authored-text proofs

| Text | Target | Result |
|---|---|---|
| the block | `.agent/authored/f261-r15.md`, `.agent/last_block.md` | sha256 **equal** to the delegated digest at C0a; mirror byte-identical at C0b (G1) |
| PLAN15 | `.agent/plan.md` | **equal** at C1 (G2) |
| RECORD15, DEC14, SLIP15 | `.agent/live_review.md`, `.agent/decisions.md`, `.agent/prose_slips.md` | each **equal** to its `8aa94f37` blob followed by the slice at C1 (G2) |
| P273-FROM, P273-TO | `docs/roadmap/features/T2_F273.md` | **equal** to its `8aa94f37` blob with the pair applied at C1 (G2) |
| the three tables | `.agent/authored/f261-r15-{loop,queue,jobqueue}.jsonl` and their paths | carrier digests **equal**; all six gated objects equal the dry run at C2, C3 and C4 (G3) |
| MUT-1-FROM to MUT-4-TO | the G5 worktree only | used as the mutation bytes; never written to the checkout |

NO SLICE AND NO TABLE WAS EDITED. Every slice was extracted programmatically as the bytes strictly between its `BEGIN`
and `END` lines and verified against its BEGIN-marker sha256 before use; each table was verified against its digest
before it was applied and copied.

## Item-status table

| Item | Status | Reason |
|---|---|---|
| C0a / C0b | done | two commits, as the Bundle orders |
| C1 PLAN15, RECORD15, DEC14, SLIP15, P273 | done | one commit, the first substantive commit |
| C2 the loop table | done | one commit |
| C3 the queue table | done | one commit |
| C4 the job queue table | done | one commit |
| C5 handoff | done | this commit |
| G1 · G2 · G3 · G4 · G5 · G6 | done | exit codes and readings above |
| G7 | skipped | runs after this commit and its push; results in the completion message |

## Deviations & assumptions

1. **The frame rule, read literally, flags two lines.** Lines 261 and 269 of the block are a lone `}` inside slices
   MUT-1-FROM and MUT-1-TO, a one-character line. I read "a run of a single repeated character" as a rule line of two
   or more characters. No such line exists, and every box-drawing rule in the STEP and SLICE headers is two characters.
   This is an authoring property of the block, not a worker gate, so nothing was edited and the round went on.
   Measured on the final bytes, the block reads 307 lines TOTAL and 225 PROSE (total minus the 82 slice-body lines),
   as constraint 7 states.
2. **Tables were applied directly on disk.** `.remedy-wt/f261r15w/apply_table.py` checks the carrier digest, then
   applies every row strictly in file order against the tree the previous rows left, with `encoding="utf-8",
   newline=""`, the exact-count check and the must-exist and must-not-exist checks, stopping on the first mismatch. It
   copies the carrier after the last row. Before each of C2 to C4, a read-only probe (`tree_probe.py` over
   `git write-tree`) compared the staged objects with G3's ids and found all six matching.
3. **G1's carrier clause was read after C4, not after C1.** The carriers are first committed at C2 to C4. Their
   committed digests were read by `gate_g3g4.py` after C4, and each source carrier's digest was also verified before
   its table was applied and copied.
4. **A gate script crashed once before reading anything.** The first run of `gate_g3g4.py` failed at import with a
   `KeyError` in my own helper `tree_probe.py`, which ran its command-line body when imported. I added a `__main__`
   guard and re-ran; the reading above is from that second run. The first `pytest tests/docs/ -q` run was piped
   through `grep`, which hides the exit code, so I re-ran it without a pipe for the real exit code of 0.
5. **G5 ran through a runner**, `.remedy-wt/f261r15w/wt_runner.py`, invoked as `python3 -B`. It drops its own directory
   from `sys.path`, changes into the worktree, puts the worktree first on `sys.path` and in `PYTHONPATH`, and removes
   `REMEDY_PROJECT` and `REMEDY_DATA_DIR`. It sets `PYTHONDONTWRITEBYTECODE=1`, asserts that `apps.cli.grouped` loaded
   from inside the worktree, and calls `pytest.main` with `-q -p no:randomly -p no:cacheprovider -rf --tb=no` over the
   four test files G5 names. Mutations were applied by `mutate_wt.py`, which requires the FROM count to be 1. G5(2)
   collects 461 tests rather than 453 because the restored group adds parametrized cases.
6. **Commit subjects** were worded by this worker, since the block names each commit's content but not its subject.
7. **The open set** was computed as the distinct `^- R-\d+ — ` ids minus the distinct `^Done: R-\d+ — ` ids.
8. **File reading before edits.** The tables and slices were applied programmatically, so instead of reading each
   target file in full I read the staged diff of each of C1 to C4 before committing. I also ran `ruff` on C4's edited
   `.py` files before committing. The byte-equality checks, tree-id gates, ruff, the red-proofs and the suite prove
   each result.

## Next

1. Phase 1 rule 1: the next session reads `.agent/STOP` first.
2. The reviewer's verdict on round 15.
3. The `guide`, `dashboard` and `repo` groups, as `.agent/f261_t003_inventory.md` proposes: `guide` with the
   group-count guard, `dashboard`, and `repo` with its `dev status` block.

Operator questions open: 0
