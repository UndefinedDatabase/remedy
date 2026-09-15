# Handback — F261 round 13

## Session

`SESSION 3 of feature F261 · round 13 · rounds so far 13`

Context self-assessment: this worker's context is comfortable, and nothing in the round was cut short.

## Range

Review of `80e9cc0f`..`HEAD`: C0a, C0b, C1, C2 and C3, plus this handback commit C4. `.agent/STOP` was ABSENT at all
three readings constraint 2 orders: before C0a `ls -la .agent/STOP` exited 2 (`No such file or directory`); before C2
`test -e .agent/STOP` exited 1, re-read through Python's `subprocess.run(['test', '-e', '.agent/STOP'])` as `exit 1
absent`; before C4 `.remedy-wt/f261r13w/stopcheck.py` printed `test -e .agent/STOP exit 1 -> absent`.

## Commits

### 5b461ba9 F261 R13 C0a: save the round 13 step block

Commit total per constraint 5: **379** insertions, 0 deletions.

| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f261-r13.md` | +379 / -0 | the block, copied with `shutil.copyfile`; sha256 equal to the delegated digest |

### f567eda3 F261 R13 C0b: mirror the round 13 step block into last_block

Commit total per constraint 5: **247** insertions, 153 deletions.

| Path | +/- | Reason |
|---|---|---|
| `.agent/last_block.md` | +247 / -153 | the same bytes, the mirror |

### d2891eb9 F261 R13 C1: re-point the plan at round 13, book round 12's PASS, record DECISION F261 D12 and the T003 inventory

This is the FIRST SUBSTANTIVE COMMIT. Commit total per constraint 5: **126** insertions, 11 deletions.

| Path | +/- | Reason |
|---|---|---|
| `.agent/decisions.md` | +12 / -0 | slice DEC12 appended: DECISION F261 D12 |
| `.agent/f261_t003_inventory.md` | +97 / -0 | NEW: slice INV13, the T003 inventory |
| `.agent/live_review.md` | +2 / -0 | slice RECORD13 appended: `Gate: F261 R12 —` PASS |
| `.agent/plan.md` | +15 / -11 | slice PLAN13, a full replacement: 36 lines |

### f70e1611 F261 R13 C2: give GroupDef a hidden field that keeps a group out of both root helps, by the hidden table

Commit total per constraint 5: **76** insertions, 7 deletions.

| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f261-r13-hidden.jsonl` | +7 / -0 | the table, 7 `edit` rows, copied with `shutil.copyfile`; sha256 equal |
| `apps/cli/command_catalog.py` | +4 / -0 | `GroupDef.hidden: bool = False`, the last field, with its WHY comment |
| `apps/cli/grouped.py` | +7 / -3 | `_print_root_help` lists no hidden group in either form; the parser still adds every group |
| `tests/cli/test_cli_ux.py` | +54 / -1 | NEW class `TestHiddenGroup`: default, both root helps, the group's own help, dispatch |
| `tests/test_grouped_cli.py` | +4 / -3 | the two root-help tests skip hidden groups |

### ed02d512 F261 R13 C3: rename the plan group to the hidden roadmap group, by the roadmap table

Commit total per constraint 5: **136** insertions, 63 deletions.

| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f261-r13-roadmap.jsonl` | +41 / -0 | the table, 40 `edit` rows and 1 `move`, copied with `shutil.copyfile`; sha256 equal |
| `.claude/skills/remedy-self-drive/SKILL.md` | +2 / -2 | the Phase 0 probe lines call `remedy roadmap status` and `remedy roadmap next` |
| `apps/cli/command_catalog.py` | +9 / -8 | `plan` group removed; hidden `roadmap` group last in `GROUPS`; `roadmap.status`, `roadmap.next` and their `related=` |
| `apps/cli/commands/__init__.py` | +2 / -2 | imports and the handler loop name `roadmap_cmd` |
| `apps/cli/commands/{plan_cmd.py => roadmap_cmd.py}` | +6 / -6 | the move, with the docstring, `_cmd_roadmap_status`, `_cmd_roadmap_next` and the handler ids |
| `docs/README.md` | +1 / -1 | the index row names `remedy roadmap status`/`next` (a hidden group) |
| `docs/agents/self_drive_protocol.md` | +2 / -2 | the Phase 0 probe lines |
| `docs/system/roadmap-mirror-v1.md` | +13 / -8 | title, verbs, the hidden-group paragraph, the file table |
| `packages/orchestration/feature_mission_adapter.py` | +1 / -1 | the docstring names `remedy roadmap next` |
| `tests/cli/test_plan_cli.py` | +49 / -31 | calls read `roadmap`; new tests: the group is hidden, neither root help lists it, `plan` is an unknown command |
| `tests/orchestration/import_reachability_allowlist.txt` | +1 / -1 | `apps.cli.commands.roadmap_cmd` replaces `plan_cmd` |
| `tests/orchestration/test_roadmap_index.py` | +1 / -1 | the docstring names `roadmap next` |
| `tests/test_command_catalog.py` | +8 / -0 | the two pairs join `RENAMED`; new `test_no_old_id_is_left_in_the_dispatch_table` |

### C4 — this commit (self-reference, R-0149 pattern)

| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | NO NUMBERS | this handback; its own numstat is reported in the completion message only |

## External actions

| Command | Outcome |
|---|---|
| `git worktree add --detach .remedy-wt/f261r13w/wt ed02d51254580b3e053fb33344c6e15010669dcf` | created for G5; restored after each mutation with `git -C .remedy-wt/f261r13w/wt checkout -- <that file>` (exit 0, worktree status `''` after each), then removed with `git worktree remove --force .remedy-wt/f261r13w/wt` (exit 0); `git worktree list` then read one row and `git branch --list 'remedy/job-*'` 16 lines |
| `git push origin feature/f261-cli-vocabulary-v2` | the one push, after this commit; its result is in the completion message (G7) |
| pull request create / merge / force-push / branch delete / `remedy` | NOT RUN |

## Verification

The scripts and raw outputs are under `.remedy-wt/f261r13w/`, not committed. Every exit code below is the real return
code of the command as the tool reported it.

| Gate | At | REAL exit | Decisive reading |
|---|---|---|---|
| G1 transport | after C1 `d2891eb9`; carriers after C3 | `slices_r13.py` 0; `gate_g1g2.py` 0; `gate_g3g4.py` 0 | sha256 of `.agent/authored/f261-r13.md` at C0a `0aebf9128ef0c7de15a917dd345716030399c1101de00cec2ef308b8b1f7b815`, **equal** to the delegated digest; `.agent/last_block.md` at C0b **byte-identical** (29933 bytes). Slices FOUND **14** (PLAN13, RECORD13, DEC12, INV13, MUT-1-FROM to MUT-5-TO), each **matching** its BEGIN-marker sha256. Committed carriers: hidden at C2 `a3099103…918ad3`, roadmap at C3 `fd0bd680…00ac59`, each **equal** to its digest |
| G2 the record | C1 | `gate_g1g2.py` 0 | `plan.md` **equals** PLAN13; **36** lines; `^## Goal$` **1**; `^## Next Steps$` **1**. `f261_t003_inventory.md` **equals** INV13. `live_review.md` **equals** its `80e9cc0f` blob + RECORD13 (1015481 + 3791 = 1019272 bytes); `decisions.md` **equals** its `80e9cc0f` blob + DEC12 (1380049 + 2779 = 1382828). `^Gate: F\d+ R\d+ — ` **121** → **122**; `Gate: F261 R12 — ` **1** at C1; distinct `^- R-\d+ — ` **105** → **105**, sets equal; distinct `^Done: R-\d+ — ` **8** → **8**, sets equal; open by distinct id **97** → **97** |
| G3 the tables | C2 `f70e1611`, C3 `ed02d512` | `gate_g3g4.py` 0 | tables: hidden **7** rows, roadmap **41**, every count as stated, no STOP. `--no-renames --name-only` from each parent: exactly the carrier and the paths G3 names (5 and 14 paths). `apps`, `tests`, `docs`, `scripts`, `packages`, `README.md`, `.claude` each **match** the dry run at C2 (`87c3490a…`, `430b31b6…`, `43175c76…`, `e3c01bde…`, `0e39ea4b…`, `15b9e0e8…`, `3f74bb69…`) and C3 (`c52ed435…`, `166acfa6…`, `11be22ad…`, `e3c01bde…`, `2fc99e37…`, `15b9e0e8…`, `e3cd5e0a…`). Insertions: C2 **76** (7 deletions), C3 **136** (63); each single-parent |
| G4 the sweep | C3 `ed02d512` | `gate_g3g4.py` 0 | the `git grep` at C3: exit 0, exactly **5** lines: `docs/system/vocabulary.md:228`, `tests/orchestration/test_failure_postmortem.py:1055` and `:1066`, `tests/test_command_catalog.py:276` and `:277`. `python3 -m ruff check` over the 10 `.py` paths of C2 and C3 that exist at C3 (the moved-away `apps/cli/commands/plan_cmd.py` is checked as `roadmap_cmd.py`): exit **0**, `All checks passed!` |
| G5(a) control | worktree at C3 | 0 | `apps.cli.grouped` loaded from the worktree; `506 passed in 38.33s`; **0** failed nodes |
| G5(1) `--all-commands` lists hidden groups | same worktree | 1 | MUT-1-FROM count **1** in `apps/cli/grouped.py`; `2 failed, 504 passed in 38.25s`; **2** failed nodes, `TestHiddenGroup::test_a_hidden_group_is_absent_from_all_commands` **among them** (with `TestCatalogRegistration::test_neither_root_help_lists_the_group`) |
| G5(2) the default help lists hidden groups | same worktree, after `checkout --` | 1 | MUT-2-FROM count **1** in `apps/cli/grouped.py`; `1 failed, 505 passed in 38.31s`; **1** failed node, `TestHiddenGroup::test_a_hidden_group_is_absent_from_the_default_help` **among them** |
| G5(3) `roadmap` not hidden | same worktree, after `checkout --` | 1 | MUT-3-FROM count **1** in `apps/cli/command_catalog.py`; `2 failed, 504 passed in 38.31s`; **2** failed nodes, `TestCatalogRegistration::test_the_group_is_hidden` **among them** (with `test_neither_root_help_lists_the_group`) |
| G5(4) a `plan.next` handler row | same worktree, after `checkout --` | 1 | MUT-4-FROM count **1** in `apps/cli/commands/roadmap_cmd.py`; `1 failed, 505 passed in 38.39s`; **1** failed node, `TestRenamedCommands::test_no_old_id_is_left_in_the_dispatch_table` **among them** |
| G5(5) the parser skips hidden groups | same worktree, after `checkout --` | 1 | MUT-5-FROM count **1** in `apps/cli/grouped.py`; `19 failed, 487 passed in 34.79s`; **19** failed nodes, `TestHiddenGroup::test_a_hidden_groups_command_still_dispatches` **among them** (with 17 of `tests/cli/test_plan_cli.py` and `test_every_new_id_parses_from_its_words_and_has_a_handler`) |
| G6 the suite, SPEC S | primary checkout at C3, serially | 0 | `suite_spec.py`: argv `python3 -B -m pytest -q -p no:randomly -p no:cacheprovider --tb=short -rfEs`, `PYTHONPATH`, `REMEDY_PROJECT`, `REMEDY_DATA_DIR` removed, `PYTHONDONTWRITEBYTECODE=1`; last line `18192 passed, 23 skipped, 1 warning in 1333.32s (0:22:13)`; distinct bad nodes **0**, so no re-run; `git status --porcelain` `''` and `git branch --list 'remedy/job-*'` 16 lines afterwards |
| G7 the tree | after C4 and the push | not yet run | reported in the completion message only |

Open findings: **97** by distinct id. The open High ids are **R-0803, R-0804 and R-0807**.

Operator questions open: 0

## Authored-text proofs

| Text | Target | Result |
|---|---|---|
| the block | `.agent/authored/f261-r13.md`, `.agent/last_block.md` | sha256 **equal** to the delegated digest at C0a; mirror byte-identical at C0b (G1) |
| PLAN13 | `.agent/plan.md` | **equal** at C1 (G2) |
| RECORD13, DEC12 | `.agent/live_review.md`, `.agent/decisions.md` | each **equal** to its `80e9cc0f` blob followed by the slice at C1 (G2) |
| INV13 | `.agent/f261_t003_inventory.md` | **equal** at C1 (G2) |
| the two tables | `.agent/authored/f261-r13-hidden.jsonl`, `.agent/authored/f261-r13-roadmap.jsonl` and their paths | carrier digests **equal**; the C2 and C3 trees equal the reviewer's dry run (G3) |
| MUT-1-FROM to MUT-5-TO | the G5 worktree only | used as the mutation bytes; never written to the checkout |

NO SLICE AND NO TABLE WAS EDITED. Every slice was extracted programmatically as the bytes strictly between its `BEGIN`
and `END` lines and verified against its BEGIN-marker sha256 before use; each table was verified against its digest
before it was applied and copied.

## Item-status table

| Item | Status | Reason |
|---|---|---|
| C0a / C0b | done | two commits, as the Bundle orders |
| C1 PLAN13, RECORD13, DEC12, INV13 | done | one commit, the first substantive commit |
| C2 the hidden table | done | one commit |
| C3 the roadmap table | done | one commit |
| C4 handoff | done | this commit |
| G1 · G2 · G3 · G4 · G5 · G6 | done | exit codes and readings above |
| G7 | skipped | runs after this commit and its push; results in the completion message |

## Deviations & assumptions

1. **G1's carrier clause was read after C3, not after C1.** Constraint 8 places G1 after C1, but the carriers are first
   committed at C2 and C3; their committed digests were read by `gate_g3g4.py` after C3, and each source carrier's
   digest was also verified before its table was applied and copied.
2. **Tables were applied directly on disk.** `.remedy-wt/f261r13w/apply_table.py` checks the carrier digest, then
   applies every row strictly in file order against the tree the previous rows left, with `encoding="utf-8",
   newline=""`, the exact-count check and the must-not-exist checks, stopping on the first mismatch; it copies the
   carrier after the last row. No count differed and no target existed, so no STOP arose.
3. **G4's ruff ran over the working tree at C3** (HEAD `ed02d512`, status `''`), over the 10 `.py` paths that exist
   there; `apps/cli/commands/plan_cmd.py`, one of C3's `--no-renames` paths, no longer exists and its content is
   checked as `apps/cli/commands/roadmap_cmd.py`.
4. **G5 ran through a runner**, `.remedy-wt/f261r13w/wt_runner.py`, invoked as `python3 -B`: it drops its own directory
   from `sys.path`, changes into the worktree, puts it first on `sys.path` and in `PYTHONPATH`, removes
   `REMEDY_PROJECT` and `REMEDY_DATA_DIR`, sets `PYTHONDONTWRITEBYTECODE=1`, asserts that `apps.cli.grouped` loaded
   from inside the worktree, and calls `pytest.main` with `-q -p no:randomly -p no:cacheprovider -rf --tb=no` over the
   four test files G5 names.
5. **Commit subjects** were worded by this worker, since the block names each commit's content but not its subject.
6. **The open set** was computed as the distinct `^- R-\d+ — ` ids minus the distinct `^Done: R-\d+ — ` ids.
7. **The STOP readings used three forms** (`ls`, `test -e`, and `stopcheck.py` running `test -e`), each with its real
   exit code as stated under Range; the `test -e` before C2 was re-read through Python because the tool printed no
   exit line for it.
8. **The suite ran in the foreground**, inside one tool call, from the primary checkout; it finished in 22 minutes and
   nothing else ran meanwhile.
9. **File reading before edits.** The tables and slices were applied programmatically, so instead of reading each
   target file in full I read the full diff of each of C1 to C3 before committing; the byte-equality, tree-id gates,
   ruff, the red-proofs and the suite prove each result.

## Next

1. Phase 1 rule 1: the next session reads `.agent/STOP` first.
2. The reviewer's verdict on round 13.
3. The first deletion round `.agent/f261_t003_inventory.md` proposes: round A, `orchestrator`, `rollback` and the `loop`
   command.
