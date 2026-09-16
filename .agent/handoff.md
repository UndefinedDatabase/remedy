# Handback — F261 round 17

## Session

`SESSION 4 of feature F261 · round 17 · rounds so far 17`

Context self-assessment: this worker's context is comfortable, and nothing in the round was cut short.

## Range

Review of `bf88d647`..`HEAD`: C0a, C0b, C1, C2, C3 and C4, plus this handback commit C5. `.agent/STOP` was ABSENT at
all three readings constraint 2 orders. Before C0a, `ls -la .agent/STOP` exited 2 (`No such file or directory`); before
C2 and before C5, `.remedy-wt/f261r16w/stop_check.py`, a `pathlib.Path.exists` reading, printed `STOP exists: False`
and exited 0.

Every gate G1 to G6 read green. No table row stopped.

## Commits

### 09d7dd18 F261 R17 C0a: save the round 17 step block

Commit total per constraint 5: **352** insertions, 0 deletions.

| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f261-r17.md` | +352 / -0 | the block, copied with `shutil.copyfile`; sha256 equal to the delegated digest |

### a4d1bf03 F261 R17 C0b: mirror the round 17 step block into last_block

Commit total per constraint 5: **146** insertions, 121 deletions.

| Path | +/- | Reason |
|---|---|---|
| `.agent/last_block.md` | +146 / -121 | the same bytes, the mirror |

### a0860e35 F261 R17 C1: re-point the plan at round 17, book round 16's PASS, register R-0906 for this feature and R-0907 for F273 and record DECISION F261 D16

This is the FIRST SUBSTANTIVE COMMIT. Commit total per constraint 5: **32** insertions, 8 deletions.

| Path | +/- | Reason |
|---|---|---|
| `.agent/decisions.md` | +12 / -0 | slice DEC16 appended: DECISION F261 D16, the deletion paragraph of the three groups |
| `.agent/live_review.md` | +6 / -0 | slice RECORD17 appended: `Gate: F261 R16 —` PASS, R-0906 and R-0907 |
| `.agent/plan.md` | +11 / -8 | slice PLAN17, a full replacement: 36 lines |
| `docs/roadmap/features/T2_F273.md` | +3 / -0 | pair P273 (REWRITE): the R-0907 resolution line |

### 2f46e267 F261 R17 C2: delete the readiness group, its handler, its unbuildable guidance card and its smoke section, by the readiness table

Commit total per constraint 5: **54** insertions, 328 deletions.

| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f261-r17-readiness.jsonl` | +30 / -0 | the table, 29 `edit` rows and 1 `delete`, copied with `shutil.copyfile`; sha256 equal |
| `apps/cli/command_catalog.py` | +0 / -22 | the `readiness` `GroupDef` and the `readiness.job` and `readiness.project` entries |
| `apps/cli/commands/__init__.py` | +1 / -2 | `readiness` leaves the import list and the handler loop |
| `apps/cli/commands/readiness.py` | +0 / -105 | DELETED |
| `apps/ui/src/api/actionClass.test.ts` | +3 / -1 | the `_assessed` rule keeps a case of its own now that `readiness_assessed` left the catalog |
| `apps/ui/src/api/humanizeCatalog.ts` | +0 / -1 | the humanized sentence of `readiness_assessed` |
| `docs/system/architecture.md` | +3 / -1 | the CLI row points at the cockpit readiness payload and `remedy mission readiness` |
| `packages/orchestration/brain_detail.py` | +1 / -1 | the readiness node's hint becomes `remedy mission readiness` |
| `packages/orchestration/brain_viewer.py` | +1 / -1 | the viewer's Readiness suggestion becomes `remedy mission readiness` |
| `packages/orchestration/guidance.py` | +5 / -24 | the readiness card, whose import of `assess_readiness` named nothing, so it could never be built; the remaining cards renumber |
| `scripts/remedy_smoke.sh` | +4 / -55 | section 12i, the readiness JSON check, and the readiness half of section 12l |
| `tests/orchestration/import_reachability_allowlist.txt` | +0 / -1 | `apps.cli.commands.readiness` |
| `tests/test_autonomy_readiness.py` | +0 / -49 | `TestReadinessCLI` and its now-unused imports |
| `tests/test_command_catalog.py` | +2 / -0 | the two `readiness.*` ids join `TestDeletedCommands` |
| `tests/test_data_paths.py` | +0 / -18 | the `_cmd_readiness_project` routed-handler test |
| `tests/test_remedy_smoke_script.py` | +4 / -47 | the seven tests asserting the deleted smoke sections and the `readiness_assessed` event |

### 130e68f0 F261 R17 C3: delete the contract group, its handler and the hints that named its commands, by the contract table

Commit total per constraint 5: **69** insertions, 333 deletions.

| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f261-r17-contract.jsonl` | +30 / -0 | the table, 28 `edit` rows and 2 `delete`, copied with `shutil.copyfile`; sha256 equal |
| `apps/cli/command_catalog.py` | +0 / -47 | the `contract` `GroupDef` and the `inspect`, `check` and `set` entries |
| `apps/cli/commands/__init__.py` | +1 / -2 | `contract_cmd` leaves the import list and the handler loop |
| `apps/cli/commands/contract_cmd.py` | +0 / -188 | DELETED |
| `docs/system/quality-baseline-v0.md` | +1 / -1 | the coverage row no longer names a live path |
| `docs/system/real-test-execution-v1.md` | +6 / -4 | the budget precondition and the two next-action rows: nothing writes a contract budget now |
| `docs/system/repair-loop-v1.md` | +1 / -1 | the denied-action next action becomes `remedy job show <job_id> --full --json` |
| `docs/system/run-contract-v1.md` | +10 / -6 | the mutation paragraph and the CLI block: the heir is `job show --full`, and the `set` write has none |
| `packages/orchestration/do_continue.py` | +1 / -3 | the `stop_before_apply_true` and `test_budget_unconfigured` next actions empty; the third re-points |
| `packages/orchestration/repair_loop.py` | +2 / -2 | the two "Review contract" next actions re-point |
| `packages/orchestration/run_contract.py` | +9 / -10 | nine `contract inspect` next actions re-point; the `max_test_runs` one empties (R-0906) |
| `packages/orchestration/self_dogfood.py` | +1 / -1 | the "Inspect contract" next action re-points |
| `packages/orchestration/self_dogfood_execution.py` | +1 / -1 | the eligibility next action re-points |
| `packages/orchestration/test_execution_service.py` | +1 / -6 | the next action re-points; the exhausted-budget `contract_guidance` and the runtime next action empty |
| `pyproject.toml` | +0 / -1 | the mypy override for the deleted module |
| `tests/cli/test_cli_ux.py` | +2 / -2 | `contract` leaves `_INTERNAL_GROUPS` and the default-help exclusion list |
| `tests/cli/test_contract_runtime.py` | +0 / -57 | DELETED |
| `tests/orchestration/import_reachability_allowlist.txt` | +0 / -1 | `apps.cli.commands.contract_cmd` |
| `tests/test_command_catalog.py` | +3 / -0 | the three `contract.*` ids join `TestDeletedCommands` |

### 23204d61 F261 R17 C4: delete the policy group, its handler and its smoke sections, declaring its two dead event couplings, by the policy table

Commit total per constraint 5: **65** insertions, 558 deletions.

| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f261-r17-policy.jsonl` | +31 / -0 | the table, 30 `edit` rows and 1 `delete`, copied with `shutil.copyfile`; sha256 equal |
| `apps/cli/command_catalog.py` | +0 / -33 | the `policy` `GroupDef` and the `contract`, `token` and `token-explain` entries |
| `apps/cli/commands/__init__.py` | +1 / -2 | `policy` leaves the import list and the handler loop |
| `apps/cli/commands/policy.py` | +0 / -116 | DELETED |
| `apps/ui/src/api/humanizeCatalog.ts` | +0 / -2 | the humanized sentences of `run_contract_inspected` and `token_policy_inspected` |
| `docs/system/architecture.md` | +6 / -4 | the two CLI blocks say the group is gone and name what still builds contract and policy |
| `packages/orchestration/brain_detail.py` | +3 / -4 | the run-contract node's hint re-points; the token-policy node's next actions empty |
| `packages/orchestration/guidance.py` | +2 / -19 | the token-policy card, whose command was `policy token`; the remaining cards renumber |
| `scripts/remedy_smoke.sh` | +3 / -158 | sections 12a, 12b and 12e, the two policy JSON checks and their run-log schema check |
| `tests/orchestration/import_reachability_allowlist.txt` | +0 / -1 | `apps.cli.commands.policy` |
| `tests/orchestration/test_event_name_coupling.py` | +7 / -2 | `run_contract_inspected` and `token_policy_inspected` join `KNOWN_DEAD_EVENT_COUPLINGS`; `_COUPLING_CEILING` 2 to 4 |
| `tests/test_command_catalog.py` | +4 / -3 | `policy` leaves `TestRequiredGroups`, the two read commands leave the JSON and required lists, the three ids join `TestDeletedCommands` |
| `tests/test_execution_foundation.py` | +1 / -80 | `TestCLIRunContract` and `TestCLITokenPolicy`, and the now-unused `pytest` import |
| `tests/test_grouped_cli.py` | +0 / -25 | the three grouped-dispatch and main-entrypoint `policy` tests |
| `tests/test_remedy_smoke_script.py` | +7 / -109 | the tests asserting the deleted smoke sections and the two events |

### C5 — this commit (self-reference, R-0149 pattern)

| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | NO NUMBERS | this handback; its own numstat is reported in the completion message only |

## External actions

| Command | Outcome |
|---|---|
| `git worktree add --detach .remedy-wt/f261r17w/wt 23204d61` | created for G5, at the path G5 names; restored after each mutation with `git -C .remedy-wt/f261r17w/wt checkout -- <that file>` (checkout exit 0, worktree status `''` after each), then removed with `git worktree remove --force .remedy-wt/f261r17w/wt` (exit 0); `git worktree list` then read one row and `git branch --list 'remedy/job-*'` 16 lines |
| `git push origin feature/f261-cli-vocabulary-v2` | the one push, after this commit; its result is in the completion message (G7) |
| pull request create / merge / force-push / branch delete / `remedy` | NOT RUN |

## Verification

The scripts and raw outputs are under `.remedy-wt/f261r16w/`, not committed. Every exit code below is the real return
code of the named script or command.

| Gate | At | REAL exit | Decisive reading |
|---|---|---|---|
| G1 transport | block after C0b; carriers after C4 | `slice_extract_r17.py` 0; `gate_g1g2_r17.py` 0; `gate_g3g4_r17.py` 0 | sha256 of `.agent/authored/f261-r17.md` at C0a `74be83b2d80f3da704da0464a9c4a324d605139376bcab0a68c1fbf0b7740d83`, **equal** to the delegated digest; `.agent/last_block.md` at C0b **byte-identical** (34499 bytes). Slices FOUND **21** (PLAN17, RECORD17, DEC16, P273-FROM, P273-TO, MUT-1-FROM to MUT-8-TO), each **matching** its BEGIN-marker sha256. Committed carriers: readiness at C2 `53281fb6…`, contract at C3 `b224acf8…`, policy at C4 `8c88b9da…`, each **equal** to its digest |
| G2 the record | C1 `a0860e35` | `gate_g1g2_r17.py` 0; `python3 -m pytest tests/docs/ -q` 0 | `plan.md` **equals** PLAN17; **36** lines; `^## Goal$` **1**; `^## Next Steps$` **1**. `live_review.md` **equals** its `bf88d647` blob + RECORD17 (1035812 + 8822 = 1044634 bytes); `decisions.md` + DEC16 (1393206 + 4030 = 1397236). P273: TO contains FROM **false**; FROM **1** at base, **0** at C1, TO **1** at C1; `T2_F273.md` **equals** its base blob with the pair applied. `^Gate: F\d+ R\d+ — ` **125** → **126**; `Gate: F261 R16 — ` **1** at C1; distinct `^- R-\d+ — ` **108** → **110**, C1 minus base exactly **R-0906 and R-0907**; distinct `^Done: R-\d+ — ` **8** → **8**; open by distinct id **100** → **102**. `tests/docs/`: `310 passed in 1.06s` |
| G3 the tables | C2 `2f46e267`, C3 `130e68f0`, C4 `23204d61` | `gate_g3g4_r17.py` 0 | tables: readiness **30** rows, contract **30**, policy **31**, every count as stated, every delete target present, no STOP. Each commit single-parent. `--no-renames --name-only` from each parent: exactly the carrier and the paths G3 names (15, 18 and 14 paths, so 16, 19 and 15 with the carrier). `apps`, `tests`, `docs`, `scripts`, `packages`, `README.md` **all 18 match** the dry-run ids G3 gives. Insertions: C2 **54** (328 deletions), C3 **69** (333), C4 **65** (558) |
| G4 the sweep | C4 `23204d61` | `gate_g3g4_r17.py` 0 | the `git grep` at C4: exit **1**, stdout `''`, stderr `''`. `python3 -m ruff check` over the 19 `.py` paths of C2 to C4 that exist at C4 (absent: `readiness.py`, `contract_cmd.py`, `policy.py`, `tests/cli/test_contract_runtime.py`): exit **0**, `All checks passed!` |
| G5(a) control | worktree at C4 | 0 | `apps.cli.grouped` loaded from the worktree; `416 passed in 31.23s`; **0** failed nodes |
| G5(1) a `readiness` handler row | same worktree | 1 | MUT-1-FROM count **1** in `apps/cli/commands/dev.py`; `1 failed, 415 passed in 31.25s`; **1** failed node, `TestDeletedCommands::test_no_deleted_id_is_left_in_the_dispatch_table` **among them** |
| G5(2) a `contract` handler row | same worktree, after `checkout --` | 1 | MUT-2-FROM count **1** in the same file; `1 failed, 415 passed in 31.37s`; **1** failed node, `TestDeletedCommands::test_no_deleted_id_is_left_in_the_dispatch_table` **among them** |
| G5(3) a `policy` handler row | same worktree, after `checkout --` | 1 | MUT-3-FROM count **1** in the same file; `1 failed, 415 passed in 31.05s`; **1** failed node, `TestDeletedCommands::test_no_deleted_id_is_left_in_the_dispatch_table` **among them** |
| G5(4) the `policy` group without commands | same worktree, after `checkout --` | 1 | MUT-4-FROM count **1** in `apps/cli/command_catalog.py`; `1 failed, 423 passed in 31.76s`; **1** failed node, `TestCatalogIntegrity::test_every_group_has_at_least_one_command` **among them** |
| G5(5) a `related=` naming `policy.contract` | same worktree, after `checkout --` | 1 | MUT-5-FROM count **1** in the same file; `1 failed, 415 passed in 31.30s`; **1** failed node, `TestCatalogIntegrity::test_every_related_reference_resolves_to_a_live_command` **among them** |
| G5(6) the readiness hint pointed back at `readiness job` | same worktree, after `checkout --` | 1 | MUT-6-FROM count **1** in `packages/orchestration/brain_detail.py`; `1 failed, 415 passed in 31.16s`; **1** failed node, `test_every_advertised_command_exists_in_the_catalog` **among them** |
| G5(7) `token_policy_inspected` undeclared | same worktree, after `checkout --` | 1 | MUT-7-FROM count **1** in `tests/orchestration/test_event_name_coupling.py`; `1 failed, 415 passed in 31.21s`; **1** failed node, `TestEventNameCouplingRatchet::test_every_dead_coupling_is_declared` **among them** |
| G5(8) `contract` named an internal group again | same worktree, after `checkout --` | 1 | MUT-8-FROM count **1** in `tests/cli/test_cli_ux.py`; `3 failed, 413 passed in 31.16s`; **3** failed nodes, `TestGroupDefIntegrity::test_internal_groups_marked` **among them** (the others: `TestAdvancedHelp::test_all_commands_shows_internal`, `TestHiddenCallable::test_hidden_group_callable`) |
| G6 the suite, SPEC S | primary checkout at C4, serially | 0 | `suite_spec_r17.py`: argv `python3 -B -m pytest -q -p no:randomly -p no:cacheprovider --tb=short -rfEs`, `PYTHONPATH`, `REMEDY_PROJECT`, `REMEDY_DATA_DIR` removed, `PYTHONDONTWRITEBYTECODE=1`; last line `17854 passed, 23 skipped, 1 warning in 1322.37s (0:22:02)`; distinct bad nodes **0**, so no re-run |
| G7 the tree | after C5 and the push | not yet run | reported in the completion message only |

Open findings: **102** by distinct id. The open High ids are **R-0803, R-0804 and R-0807**.

## Authored-text proofs

| Text | Target | Result |
|---|---|---|
| the block | `.agent/authored/f261-r17.md`, `.agent/last_block.md` | sha256 **equal** to the delegated digest at C0a; mirror byte-identical at C0b (G1) |
| PLAN17 | `.agent/plan.md` | **equal** at C1 (G2) |
| RECORD17, DEC16 | `.agent/live_review.md`, `.agent/decisions.md` | each **equal** to its `bf88d647` blob followed by the slice at C1 (G2) |
| P273-FROM, P273-TO | `docs/roadmap/features/T2_F273.md` | **equal** to its `bf88d647` blob with the pair applied at C1 (G2) |
| the three tables | `.agent/authored/f261-r17-{readiness,contract,policy}.jsonl` and their paths | carrier digests **equal**; all six gated objects equal the dry run at C2, C3 and C4 (G3) |
| MUT-1-FROM to MUT-8-TO | the G5 worktree only | used as the mutation bytes; never written to the checkout |

NO SLICE AND NO TABLE WAS EDITED. Every slice was extracted programmatically as the bytes strictly between its `BEGIN`
and `END` lines and verified against its BEGIN-marker sha256 before use; each table was verified against its digest
before it was applied and copied.

## Item-status table

| Item | Status | Reason |
|---|---|---|
| C0a / C0b | done | two commits, as the Bundle orders |
| C1 PLAN17, RECORD17, DEC16, P273 | done | one commit, the first substantive commit |
| C2 the readiness table | done | one commit |
| C3 the contract table | done | one commit |
| C4 the policy table | done | one commit |
| C5 handoff | done | this commit |
| G1 · G2 · G3 · G4 · G5 · G6 | done | exit codes and readings above |
| G7 | skipped | runs after this commit and its push; results in the completion message |

## Deviations & assumptions

1. **The block's own measures.** On its final bytes the block reads 352 lines TOTAL and 260 PROSE (352 minus the 92
   slice-body lines), as constraint 7 states, against the caps of 490 and 400. No line of two or more characters is a
   run of one repeated character, and all 86 box-drawing runs in the STEP and SLICE headers are two characters long.
   Nothing to declare against the frame rule.
2. **The G5 worktree path contradicts constraint 4.** Constraint 4 says scratch, runner scripts and my worktree live
   under `.remedy-wt/f261r16w/`; G5 names the exact command `git worktree add --detach .remedy-wt/f261r17w/wt <C4's
   sha>`. I followed G5's literal path for the worktree and kept every script, slice and raw output under
   `.remedy-wt/f261r16w/`. The worktree was removed with `--force`; the now-empty `.remedy-wt/f261r17w/` directory
   remains, uncommitted and ignored. `git worktree list` reads one row.
3. **G2's docs run was taken twice.** The first run was piped through `tail`, which hid its exit code. I re-ran the
   exact `python3 -m pytest tests/docs/ -q` without a pipe, through `subprocess.run`. That run exited 0 with
   `310 passed in 1.06s`, and it is the reading above.
4. **SPEC S ran in the foreground.** I first tried to launch it with `nohup … &` so I could poll the output file; the
   harness refuses the `&` background operator, so the suite ran in the foreground to completion instead. The command,
   the environment and the readings are unchanged.
5. **Tables were applied directly on disk.** `.remedy-wt/f261r16w/apply_table_r17.py` checks the carrier digest, then
   simulates every row in memory, strictly in file order, against the state the previous rows left. It uses
   `encoding="utf-8", newline=""`, the exact-count check and the must-exist and must-not-exist checks. Only when no row
   stops does it write the result and copy the carrier. Before each of C2 to C4, a read-only probe
   (`tree_probe_r17.py` over `git write-tree`) compared the staged objects with G3's ids and found all six matching,
   so no commit was made on an unverified tree.
6. **G1's carrier clause was read after C4, not after C1.** The carriers are first committed at C2 to C4. Their
   committed digests were read by `gate_g3g4_r17.py` after C4, and each source carrier's digest was also verified
   before its table was applied and copied.
7. **G5 ran through a runner**, `.remedy-wt/f261r16w/wt_runner_r17.py`, invoked as `python3 -B` by `g5_drive_r17.py`.
   It drops its own directory from `sys.path`, changes into the worktree, puts the worktree first on `sys.path` and in
   `PYTHONPATH`, and removes `REMEDY_PROJECT` and `REMEDY_DATA_DIR`. It sets `PYTHONDONTWRITEBYTECODE=1`, asserts that
   `apps.cli.grouped` loaded from inside the worktree — the printed path is under `.remedy-wt/f261r17w/wt/` in every
   one of the nine runs — and calls `pytest.main` with `-q -p no:randomly -p no:cacheprovider -rf --tb=no` over the six
   test files G5 names. Mutations were applied by `mutate_wt_r17.py`, which requires the FROM count to be 1. The
   collection count differs at G5(4) (424 rather than 416) because restoring the `policy` group parametrizes some
   tests over the group set.
8. **Scratch scripts were adapted from round 16.** The round 16 helpers under `.remedy-wt/f261r16w/` were copied to
   `_r17` names with this round's digests, paths, slice directory (`slices17/`), counts and mutation table, rather than
   written from nothing. Each was read before reuse. No round 16 script or output file was overwritten.
9. **Commit subjects** were worded by this worker, since the block names each commit's content but not its subject.
10. **The open set** was computed as the distinct `^- R-\d+ — ` ids minus the distinct `^Done: R-\d+ — ` ids. The three
    High ids were read as `High` registrations with no `Done:` line.
11. **File reading before edits.** The tables and slices were applied programmatically, so instead of reading each
    target file in full I read the staged or committed diff of each of C1 to C4 before writing this handback, and the
    staged diff of C1 before committing it. The byte-equality checks, the tree-id gates, ruff, the eight red-proofs and
    the full suite prove each result.

## Next

1. Phase 1 rule 1: the next session reads `.agent/STOP` first.
2. The reviewer's verdict on round 17.
3. The `context` group, the `token` group with `context-pack`, and the `review` group, as
   `.agent/f261_t003_inventory.md` proposes.

Operator questions open: 0
