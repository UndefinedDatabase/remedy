# Handback — F261 round 16

## Session

`SESSION 4 of feature F261 · round 16 · rounds so far 16`

Context self-assessment: this worker's context is comfortable, and nothing in the round was cut short.

## Range

Review of `782b4e02`..`HEAD`: C0a, C0b, C1, C2, C3 and C4, plus this handback commit C5. `.agent/STOP` was ABSENT at
all three readings constraint 2 orders. Before C0a, `ls .agent/STOP` exited 2 (`No such file or directory`) and
`.remedy-wt/f261r16w/stop_check.py`, a `pathlib.Path.exists` reading, printed `STOP exists: False` and exited 0. Before
C2 and before C5 the same script printed `STOP exists: False` and exited 0.

Every gate G1 to G6 read green. No table row stopped.

## Commits

### d11fd434 F261 R16 C0a: save the round 16 step block

Commit total per constraint 5: **327** insertions, 0 deletions.

| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f261-r16.md` | +327 / -0 | the block, copied with `shutil.copyfile`; sha256 equal to the delegated digest |

### 4613018a F261 R16 C0b: mirror the round 16 step block into last_block

Commit total per constraint 5: **141** insertions, 121 deletions.

| Path | +/- | Reason |
|---|---|---|
| `.agent/last_block.md` | +141 / -121 | the same bytes, the mirror |

### decdbbcc F261 R16 C1: re-point the plan at round 16, book round 15's PASS and its prose slip, register R-0905 for F273 and record DECISION F261 D15

This is the FIRST SUBSTANTIVE COMMIT. Commit total per constraint 5: **29** insertions, 10 deletions.

| Path | +/- | Reason |
|---|---|---|
| `.agent/decisions.md` | +12 / -0 | slice DEC15 appended: DECISION F261 D15 |
| `.agent/live_review.md` | +4 / -0 | slice RECORD16 appended: `Gate: F261 R15 —` PASS and R-0905 |
| `.agent/plan.md` | +8 / -10 | slice PLAN16, a full replacement: 33 lines |
| `.agent/prose_slips.md` | +2 / -0 | slice SLIP16 appended: the round 15 frame-rule slip |
| `docs/roadmap/features/T2_F273.md` | +3 / -0 | pair P273 (REWRITE): the R-0905 resolution line |

### 995dd07e F261 R16 C2: delete the guide group, its route and its guidance exports, with the group-count guard, by the guide table

Commit total per constraint 5: **44** insertions, 219 deletions.

| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f261-r16-guide.jsonl` | +22 / -0 | the table, 21 `edit` rows and 1 `delete`, copied with `shutil.copyfile`; sha256 equal |
| `apps/cli/command_catalog.py` | +0 / -13 | the `guide` group and `guide.job` |
| `apps/cli/commands/__init__.py` | +1 / -2 | `guide` leaves the import list and the handler loop |
| `apps/cli/commands/guide.py` | +0 / -48 | DELETED |
| `packages/orchestration/brain_viewer.py` | +0 / -1 | the viewer's `guide job` suggestion |
| `packages/orchestration/guidance.py` | +0 / -43 | `export_guidance_json` and `summarize_guidance` |
| `packages/orchestration/ui_server.py` | +0 / -20 | `_build_guide_json` and the `guide` route |
| `scripts/remedy_smoke.sh` | +0 / -32 | section 12al, the guidance rail |
| `tests/cli/test_cli_ux.py` | +13 / -1 | `test_all_groups_still_in_catalog` asserts D4's kept groups instead of a floor of 40 |
| `tests/orchestration/import_reachability_allowlist.txt` | +0 / -1 | `apps.cli.commands.guide` |
| `tests/orchestration/test_test_runner.py` | +0 / -13 | the `_build_guide_json` degraded-signal test |
| `tests/test_command_catalog.py` | +1 / -0 | `guide.job` joins `TestDeletedCommands` |
| `tests/test_data_paths.py` | +2 / -2 | the routed-handler test calls `_cmd_brain` |
| `tests/ui_contracts/test_responsive.py` | +5 / -35 | the export and summary tests; the leak test reads the cards directly; the `guide.job` assertions leave the viewer tests, one renamed `test_viewer_handlers_registered` |
| `tests/ui_server/test_live_state.py` | +0 / -8 | the `guide` endpoint test |

### 5db11427 F261 R16 C3: delete the dashboard group, its handler and the dashboard module, by the dashboard table

Commit total per constraint 5: **21** insertions, 439 deletions.

| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f261-r16-dashboard.jsonl` | +16 / -0 | the table, 14 `edit` rows and 2 `delete`, copied with `shutil.copyfile`; sha256 equal |
| `apps/cli/command_catalog.py` | +1 / -22 | the `dashboard` group, `dashboard.job`, `dashboard.project`, and `ui.start`'s `related=` entry |
| `apps/cli/commands/__init__.py` | +1 / -2 | `dashboard_cmd` leaves the import list and the handler loop |
| `apps/cli/commands/dashboard_cmd.py` | +0 / -91 | DELETED |
| `packages/orchestration/brain_viewer.py` | +0 / -1 | the viewer's `dashboard job` suggestion |
| `packages/orchestration/dashboard.py` | +0 / -207 | DELETED |
| `packages/orchestration/guidance.py` | +1 / -12 | the guidance card pointing at `dashboard job` |
| `scripts/remedy_smoke.sh` | +0 / -40 | section 12ag, the dashboard |
| `tests/orchestration/import_reachability_allowlist.txt` | +0 / -2 | `apps.cli.commands.dashboard_cmd`, `packages.orchestration.dashboard` |
| `tests/test_command_catalog.py` | +2 / -0 | the two `dashboard.*` ids join `TestDeletedCommands` |
| `tests/ui_server/test_dashboard_contract.py` | +0 / -62 | `TestDashboard` and its `_make_events` helper |

### ae95e09d F261 R16 C4: delete the repo group, its git status exports and the commit-readiness block of dev status, by the repo table

Commit total per constraint 5: **63** insertions, 1009 deletions.

| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f261-r16-repo.jsonl` | +43 / -0 | the table, 42 `edit` rows and 1 `delete`, copied with `shutil.copyfile`; sha256 equal |
| `apps/cli/command_catalog.py` | +0 / -30 | the `repo` group, `repo.status` and `repo.commit-readiness` |
| `apps/cli/commands/__init__.py` | +1 / -2 | `repo` leaves the import list and the handler loop |
| `apps/cli/commands/dev.py` | +1 / -25 | the commit-readiness block of `dev status`: `commit_readiness_ok`, its blocker and advisory lines, its hint |
| `apps/cli/commands/repo.py` | +0 / -279 | DELETED |
| `apps/ui/src/api/humanizeCatalog.ts` | +0 / -1 | the humanized sentence of `git_status_read` |
| `packages/orchestration/brain_detail.py` | +1 / -3 | the git node's next action |
| `packages/orchestration/decision_queue.py` | +2 / -2 | a comment no longer names `apps/cli/commands/repo.py` |
| `packages/orchestration/git_status.py` | +0 / -43 | `export_git_status_json`, `summarize_git_status` and the unused `Any` import |
| `packages/orchestration/guidance.py` | +1 / -18 | the git-status card whose import had no target |
| `scripts/remedy_smoke.sh` | +0 / -59 | section 12x, `repo status`, and section 12c, the commit-readiness preview |
| `tests/cli/test_command_catalog.py` | +0 / -14 | the two `repo commit-readiness` catalog tests |
| `tests/cli/test_job_commands.py` | +0 / -101 | `TestSafeTaskLabelSanitization`, which drove commit-readiness, and `TestGitStatusCLI` |
| `tests/orchestration/import_reachability_allowlist.txt` | +0 / -1 | `apps.cli.commands.repo` |
| `tests/orchestration/test_autonomy.py` | +1 / -219 | the commit-readiness preview, `dev status` commit-readiness and commit-readiness next-action test classes |
| `tests/orchestration/test_decision_evidence.py` | +2 / -2 | comment and docstring name the deleted command in words |
| `tests/orchestration/test_event_name_coupling.py` | +6 / -3 | `git_status_read` joins `KNOWN_DEAD_EVENT_COUPLINGS`; `_COUPLING_CEILING` 1 to 2 |
| `tests/orchestration/test_project_brain.py` | +0 / -26 | the job-aware `repo status` test |
| `tests/regression/test_named_bugs.py` | +0 / -23 | `TestSmokeCommitReadinessSection` |
| `tests/test_command_catalog.py` | +2 / -0 | the two `repo.*` ids join `TestDeletedCommands` |
| `tests/test_data_paths.py` | +0 / -1 | the `commit-readiness` routed-handler case |
| `tests/test_remedy_smoke_script.py` | +1 / -7 | `test_smoke_has_repo_status` |
| `tests/test_repair_context_reviewer_memory.py` | +1 / -47 | the `dev status` commit-readiness tests |
| `tests/ui_contracts/test_ux_quality.py` | +1 / -103 | `TestCommitReadinessSchemaCompleteness` |

### C5 — this commit (self-reference, R-0149 pattern)

| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | NO NUMBERS | this handback; its own numstat is reported in the completion message only |

## External actions

| Command | Outcome |
|---|---|
| `git worktree add --detach .remedy-wt/f261r16w/wt ae95e09d` | created for G5; restored after each mutation with `git -C .remedy-wt/f261r16w/wt checkout -- <that file>` (checkout exit 0, worktree status `''` after each), then removed with `git worktree remove --force .remedy-wt/f261r16w/wt` (exit 0); `git worktree list` then read one row and `git branch --list 'remedy/job-*'` 16 lines |
| `git push origin feature/f261-cli-vocabulary-v2` | the one push, after this commit; its result is in the completion message (G7) |
| pull request create / merge / force-push / branch delete / `remedy` | NOT RUN |

## Verification

The scripts and raw outputs are under `.remedy-wt/f261r16w/`, not committed. Every exit code below is the real return
code of the named script or command.

| Gate | At | REAL exit | Decisive reading |
|---|---|---|---|
| G1 transport | block after C0b; carriers after C4 | `gate_g1g2.py` 0; `gate_g3g4.py` 0 | sha256 of `.agent/authored/f261-r16.md` at C0a `30c5067a9e6531a00ade3ee4a2ab9a5dc15e6b01c85a50f055cb6ec5677b7d94`, **equal** to the delegated digest; `.agent/last_block.md` at C0b **byte-identical** (30748 bytes). Slices FOUND **18** (PLAN16, RECORD16, DEC15, SLIP16, P273-FROM, P273-TO, MUT-1-FROM to MUT-6-TO), each **matching** its BEGIN-marker sha256 (`slice_extract.py`, exit 0). Committed carriers: guide at C2 `b629cbf3…`, dashboard at C3 `d7cbe8ba…`, repo at C4 `d2c2ff35…`, each **equal** to its digest |
| G2 the record | C1 `decdbbcc` | `gate_g1g2.py` 0; `python3 -m pytest tests/docs/ -q` 0 | `plan.md` **equals** PLAN16; **33** lines; `^## Goal$` **1**; `^## Next Steps$` **1**. `live_review.md` **equals** its `782b4e02` blob + RECORD16 (1030265 + 5547 = 1035812 bytes); `decisions.md` + DEC15 (1389423 + 3783 = 1393206); `prose_slips.md` + SLIP16 (308732 + 493 = 309225). P273: TO contains FROM **false**; FROM **1** at base, **0** at C1, TO **1** at C1; `T2_F273.md` **equals** its base blob with the pair applied. `^Gate: F\d+ R\d+ — ` **124** → **125**; `Gate: F261 R15 — ` **1** at C1; distinct `^- R-\d+ — ` **107** → **108**, C1 minus base exactly **R-0905**; distinct `^Done: R-\d+ — ` **8** → **8**; open by distinct id **99** → **100**. `tests/docs/`: `310 passed in 1.06s` |
| G3 the tables | C2 `995dd07e`, C3 `5db11427`, C4 `ae95e09d` | `gate_g3g4.py` 0 | tables: guide **22** rows, dashboard **16**, repo **43**, every count as stated, every delete target present, no STOP. Each commit single-parent. `--no-renames --name-only` from each parent: exactly the carrier and the paths G3 names (15, 11 and 24 paths). `apps`, `tests`, `docs`, `scripts`, `packages`, `README.md` **all 18 match** the dry-run ids G3 gives. Insertions: C2 **44** (219 deletions), C3 **21** (439), C4 **63** (1009) |
| G4 the sweep | C4 `ae95e09d` | `gate_g3g4.py` 0 | the `git grep` at C4: exit **1**, stdout `''`, stderr `''`. `python3 -m ruff check` over the 26 `.py` paths of C2 to C4 that exist at C4 (absent: `guide.py`, `dashboard_cmd.py`, `repo.py`, `packages/orchestration/dashboard.py`): exit **0**, `All checks passed!` |
| G5(a) control | worktree at C4 | 0 | `apps.cli.grouped` loaded from the worktree; `443 passed in 34.18s`; **0** failed nodes |
| G5(1) a `guide` handler row | same worktree | 1 | MUT-1-FROM count **1** in `apps/cli/commands/dev.py`; `1 failed, 442 passed in 34.28s`; **1** failed node, `TestDeletedCommands::test_no_deleted_id_is_left_in_the_dispatch_table` **among them** |
| G5(2) the `repo` group without commands | same worktree, after `checkout --` | 1 | MUT-2-FROM count **1** in `apps/cli/command_catalog.py`; `1 failed, 450 passed in 34.85s`; **1** failed node, `TestCatalogIntegrity::test_every_group_has_at_least_one_command` **among them** |
| G5(3) the `ci` group removed | same worktree, after `checkout --` | 1 | MUT-3-FROM count **1** in the same file; `6 failed, 429 passed in 33.50s`; **6** failed nodes, `TestGroupDefIntegrity::test_all_groups_still_in_catalog` **among them** (the others: both advertised-command tests, two `TestHiddenGroup` tests, `test_every_command_belongs_to_known_group`) |
| G5(4) a `related=` naming `dashboard.job` | same worktree, after `checkout --` | 1 | MUT-4-FROM count **1** in the same file; `1 failed, 442 passed in 34.25s`; **1** failed node, `TestCatalogIntegrity::test_every_related_reference_resolves_to_a_live_command` **among them** |
| G5(5) the `repo commit-readiness` hint | same worktree, after `checkout --` | 1 | MUT-5-FROM count **1** in `apps/cli/commands/dev.py`; `1 failed, 442 passed in 34.31s`; **1** failed node, `test_every_advertised_command_exists_in_the_catalog` **among them** |
| G5(6) `git_status_read` undeclared | same worktree, after `checkout --` | 1 | MUT-6-FROM count **1** in `tests/orchestration/test_event_name_coupling.py`; `1 failed, 442 passed in 33.96s`; **1** failed node, `TestEventNameCouplingRatchet::test_every_dead_coupling_is_declared` **among them** |
| G6 the suite, SPEC S | primary checkout at C4, serially | 0 | `suite_spec.py`: argv `python3 -B -m pytest -q -p no:randomly -p no:cacheprovider --tb=short -rfEs`, `PYTHONPATH`, `REMEDY_PROJECT`, `REMEDY_DATA_DIR` removed, `PYTHONDONTWRITEBYTECODE=1`; last line `17919 passed, 23 skipped, 1 warning in 1316.95s (0:21:56)`; distinct bad nodes **0**, so no re-run; `git status --porcelain` `''` and `git branch --list 'remedy/job-*'` 16 lines afterwards |
| G7 the tree | after C5 and the push | not yet run | reported in the completion message only |

Open findings: **100** by distinct id. The open High ids are **R-0803, R-0804 and R-0807**.

## Authored-text proofs

| Text | Target | Result |
|---|---|---|
| the block | `.agent/authored/f261-r16.md`, `.agent/last_block.md` | sha256 **equal** to the delegated digest at C0a; mirror byte-identical at C0b (G1) |
| PLAN16 | `.agent/plan.md` | **equal** at C1 (G2) |
| RECORD16, DEC15, SLIP16 | `.agent/live_review.md`, `.agent/decisions.md`, `.agent/prose_slips.md` | each **equal** to its `782b4e02` blob followed by the slice at C1 (G2) |
| P273-FROM, P273-TO | `docs/roadmap/features/T2_F273.md` | **equal** to its `782b4e02` blob with the pair applied at C1 (G2) |
| the three tables | `.agent/authored/f261-r16-{guide,dashboard,repo}.jsonl` and their paths | carrier digests **equal**; all six gated objects equal the dry run at C2, C3 and C4 (G3) |
| MUT-1-FROM to MUT-6-TO | the G5 worktree only | used as the mutation bytes; never written to the checkout |

NO SLICE AND NO TABLE WAS EDITED. Every slice was extracted programmatically as the bytes strictly between its `BEGIN`
and `END` lines and verified against its BEGIN-marker sha256 before use; each table was verified against its digest
before it was applied and copied.

## Item-status table

| Item | Status | Reason |
|---|---|---|
| C0a / C0b | done | two commits, as the Bundle orders |
| C1 PLAN16, RECORD16, DEC15, SLIP16, P273 | done | one commit, the first substantive commit |
| C2 the guide table | done | one commit |
| C3 the dashboard table | done | one commit |
| C4 the repo table | done | one commit |
| C5 handoff | done | this commit |
| G1 · G2 · G3 · G4 · G5 · G6 | done | exit codes and readings above |
| G7 | skipped | runs after this commit and its push; results in the completion message |

## Deviations & assumptions

1. **The block's own measures.** On its final bytes the block reads 327 lines TOTAL and 246 PROSE (327 minus the 81
   slice-body lines), as constraint 7 states. No line of two or more characters is a run of one repeated character,
   and all 74 box-drawing runs in the STEP and SLICE headers are two characters long. Nothing to declare against the
   frame rule.
2. **One directory listing outside the two permitted directories.** While reading the sizes of the documents, one
   `ls -la .remedy-wt/ .remedy-wt/f261-block/` also listed the top level of `.remedy-wt/`. No file there was opened,
   read or written. Every later command under `.remedy-wt/` touched only `.remedy-wt/f261-block/` and
   `.remedy-wt/f261r16w/`.
3. **G2's docs run was taken twice.** The first run added `-p no:cacheprovider` and was piped through `tail`, so it was
   not the exact command and hid its exit code. I re-ran the exact `python3 -m pytest tests/docs/ -q` without a pipe.
   That run exited 0 with `310 passed in 1.06s`, and it is the reading above.
4. **Tables were applied directly on disk.** `.remedy-wt/f261r16w/apply_table.py` checks the carrier digest, then
   simulates every row in memory, strictly in file order, against the state the previous rows left. It uses
   `encoding="utf-8", newline=""`, the exact-count check and the must-exist and must-not-exist checks. Only when no row
   stops does it write the result and copy the carrier. Before its first use I fixed a bug in my own helper: it would
   have opened a `create` target before checking that the target exists. No table has a `create` row. Before each of
   C2 to C4, a read-only probe (`tree_probe.py` over `git write-tree`) compared the staged objects with G3's ids and
   found all six matching.
5. **G1's carrier clause was read after C4, not after C1.** The carriers are first committed at C2 to C4. Their
   committed digests were read by `gate_g3g4.py` after C4, and each source carrier's digest was also verified before
   its table was applied and copied.
6. **G5 ran through a runner**, `.remedy-wt/f261r16w/wt_runner.py`, invoked as `python3 -B` by `g5_drive.py`. It drops
   its own directory from `sys.path`, changes into the worktree, puts the worktree first on `sys.path` and in
   `PYTHONPATH`, and removes `REMEDY_PROJECT` and `REMEDY_DATA_DIR`. It sets `PYTHONDONTWRITEBYTECODE=1`, asserts that
   `apps.cli.grouped` loaded from inside the worktree, and calls `pytest.main` with `-q -p no:randomly -p
   no:cacheprovider -rf --tb=no` over the six test files G5 names. Mutations were applied by `mutate_wt.py`, which
   requires the FROM count to be 1. Collection counts differ under mutation (451 at G5(2), 435 at G5(3)) because the
   group set parametrizes some tests.
7. **Commit subjects** were worded by this worker, since the block names each commit's content but not its subject.
8. **The open set** was computed as the distinct `^- R-\d+ — ` ids minus the distinct `^Done: R-\d+ — ` ids. The three
   High ids were read as `High` registrations with no `Done:` line.
9. **File reading before edits.** The tables and slices were applied programmatically, so instead of reading each
   target file in full I read the staged diff of each of C1 to C4 before committing. I also ran `python3 -m ruff check`
   on each of C2 to C4's edited `.py` files before committing, all `All checks passed!`. The byte-equality checks,
   tree-id gates, ruff, the red-proofs and the suite prove each result.

## Next

1. Phase 1 rule 1: the next session reads `.agent/STOP` first.
2. The reviewer's verdict on round 16.
3. The `readiness` group, the `contract` group and the `policy` group, as `.agent/f261_t003_inventory.md` proposes.

Operator questions open: 0
