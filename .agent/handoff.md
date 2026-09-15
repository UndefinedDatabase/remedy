# Handback — F261 round 14

## Session

`SESSION 3 of feature F261 · round 14 · rounds so far 14`

Context self-assessment: this worker's context is comfortable, and nothing in the round was cut short.

## Range

Review of `c3047df0`..`HEAD`: C0a, C0b, C1, C2, C3 and C4, plus this handback commit C5. `.agent/STOP` was ABSENT at
all three readings constraint 2 orders: before C0a, before C2 and before C5 `.remedy-wt/f261r14w/stop_check.py` (a
`pathlib.Path.exists` reading) printed `STOP exists: False` and exited 0 each time.

**G3 IS RED on one of its six objects**: the `docs` subtree id differs from the dry run at C2, C3 and C4, and in each
case `git diff-tree -r` between the dry-run tree and the committed tree names exactly one path,
`roadmap/features/T2_F273.md`, the file C1's pair P273 rewrites. See Verification and Deviation 1.

## Commits

### 8d6a7bee F261 R14 C0a: save the round 14 step block

Commit total per constraint 5: **290** insertions, 0 deletions.

| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f261-r14.md` | +290 / -0 | the block, copied with `shutil.copyfile`; sha256 equal to the delegated digest |

### b5d87e1d F261 R14 C0b: mirror the round 14 step block into last_block

Commit total per constraint 5: **166** insertions, 255 deletions.

| Path | +/- | Reason |
|---|---|---|
| `.agent/last_block.md` | +166 / -255 | the same bytes, the mirror |

### ebd3c812 F261 R14 C1: re-point the plan at round 14, book round 13's PASS, register R-0903 for F273 and record DECISION F261 D13

This is the FIRST SUBSTANTIVE COMMIT. Commit total per constraint 5: **33** insertions, 16 deletions.

| Path | +/- | Reason |
|---|---|---|
| `.agent/decisions.md` | +12 / -0 | slice DEC13 appended: DECISION F261 D13 |
| `.agent/live_review.md` | +4 / -0 | slice RECORD14 appended: `Gate: F261 R13 —` PASS and R-0903 |
| `.agent/plan.md` | +14 / -16 | slice PLAN14, a full replacement: 34 lines |
| `docs/roadmap/features/T2_F273.md` | +3 / -0 | pair P273 (REWRITE): the R-0903 resolution line |

### 98866b80 F261 R14 C2: delete the orchestrator group and the engine only it called, by the orchestrator table

Commit total per constraint 5: **38** insertions, 1385 deletions.

| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f261-r14-orchestrator.jsonl` | +17 / -0 | the table, 15 `edit` rows and 2 `delete`, copied with `shutil.copyfile`; sha256 equal |
| `apps/cli/command_catalog.py` | +0 / -50 | the `orchestrator` group and its four commands |
| `apps/cli/commands/__init__.py` | +1 / -2 | `orchestrator_cmd` leaves the import list and the handler loop |
| `apps/cli/commands/orchestrator_cmd.py` | +0 / -83 | DELETED |
| `docs/system/orchestrator-brain-v0.md` | +6 / -5 | the dated status line of DECISION F261 D13 |
| `packages/orchestration/decision_evidence.py` | +3 / -10 | comments no longer name the deleted engine |
| `packages/orchestration/model_routing.py` | +0 / -13 | the docstring paragraph on the deleted routing plan |
| `packages/orchestration/orchestrator_brain.py` | +4 / -866 | only `list_decisions` and its root helper remain |
| `tests/cli/test_orchestrator_brain_cli.py` | +0 / -86 | DELETED |
| `tests/orchestration/import_reachability_allowlist.txt` | +0 / -1 | `apps.cli.commands.orchestrator_cmd` |
| `tests/orchestration/test_orchestrator_brain.py` | +3 / -269 | only the `list_decisions` tests remain |
| `tests/test_command_catalog.py` | +4 / -0 | the four `orchestrator.*` ids join `TestDeletedCommands` |

### 4bf17d32 F261 R14 C3: delete the rollback group and the proof writer only it called, by the rollback table

Commit total per constraint 5: **48** insertions, 174 deletions.

| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f261-r14-rollback.jsonl` | +29 / -0 | the table, 29 `edit` rows, copied with `shutil.copyfile`; sha256 equal |
| `apps/cli/command_catalog.py` | +2 / -27 | the `rollback` group and `rollback.proof`, `rollback.show`; `snapshot.create` relates to `snapshot.show` |
| `apps/cli/commands/real_test_execution_cmd.py` | +2 / -33 | the two rollback handlers and their rows |
| `docs/guides/real-test-execution-snapshot-rollback-user-guide-v1.md` | +0 / -7 | the rollback command section |
| `docs/system/real-test-execution-snapshot-rollback-proof-v1.md` | +6 / -3 | the dated status line of DECISION F261 D13 |
| `packages/orchestration/real_test_execution.py` | +3 / -77 | `RollbackProof`, `create_rollback_proof`, `get_rollback_proof`, `export_rollback_proof_json`, `_rollback_path` |
| `tests/cli/test_real_test_execution_cli.py` | +1 / -15 | the rollback CLI tests |
| `tests/orchestration/test_real_test_execution.py` | +3 / -12 | the rollback writer tests |
| `tests/test_command_catalog.py` | +2 / -0 | the two `rollback.*` ids join `TestDeletedCommands` |

### be6ae79d F261 R14 C4: delete the loop command group, by the loop table

Commit total per constraint 5: **26** insertions, 708 deletions.

| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f261-r14-loop.jsonl` | +14 / -0 | the table, 12 `edit` rows and 2 `delete`, copied with `shutil.copyfile`; sha256 equal |
| `apps/cli/command_catalog.py` | +0 / -38 | the `loop` group and `loop.list`, `loop.validate`, `loop.run` |
| `apps/cli/commands/__init__.py` | +1 / -2 | `loop_cmd` leaves the import list and the handler loop |
| `apps/cli/commands/loop_cmd.py` | +0 / -277 | DELETED |
| `apps/cli/cost_preview_confirm.py` | +2 / -3 | the docstring no longer names `loop_cmd.py` |
| `docs/system/vocabulary.md` | +3 / -3 | the three `remedy loop` mentions read as the `loop` group, or drop it |
| `packages/orchestration/loop_spec.py` | +1 / -1 | the docstring no longer names `remedy loop validate` |
| `tests/cli/test_cost_preview_confirm.py` | +2 / -3 | the docstring no longer names `tests/cli/test_loop_cmd.py` |
| `tests/cli/test_loop_cmd.py` | +0 / -380 | DELETED |
| `tests/orchestration/import_reachability_allowlist.txt` | +0 / -1 | `apps.cli.commands.loop_cmd` |
| `tests/test_command_catalog.py` | +3 / -0 | the three `loop.*` ids join `TestDeletedCommands` |

### C5 — this commit (self-reference, R-0149 pattern)

| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | NO NUMBERS | this handback; its own numstat is reported in the completion message only |

## External actions

| Command | Outcome |
|---|---|
| `git worktree add --detach .remedy-wt/f261r14w/wt be6ae79d` | created for G5; restored after each mutation with `git -C .remedy-wt/f261r14w/wt checkout -- <that file>` (exit 0, worktree status `''` after each), then removed with `git worktree remove --force .remedy-wt/f261r14w/wt` (exit 0); `git worktree list` then read one row and `git branch --list 'remedy/job-*'` 16 lines |
| `git push origin feature/f261-cli-vocabulary-v2` | the one push, after this commit; its result is in the completion message (G7) |
| pull request create / merge / force-push / branch delete / `remedy` | NOT RUN |

## Verification

The scripts and raw outputs are under `.remedy-wt/f261r14w/`, not committed. Every exit code below is the real return
code, printed by `.remedy-wt/f261r14w/rc_wrap.py` as `RC=<n>`.

| Gate | At | REAL exit | Decisive reading |
|---|---|---|---|
| G1 transport | after C1 `ebd3c812`; carriers after C4 | `gate_g1g2.py` 0; `gate_g3g4.py` 1 (its G1 lines all PASS; the 1 is G3's `docs`) | sha256 of `.agent/authored/f261-r14.md` at C0a `ec743657d65cf88693654218b20e6f98baf9f0a83e5f78fe5f712723f46d004e`, **equal** to the delegated digest; `.agent/last_block.md` at C0b **byte-identical** (26192 bytes). Slices FOUND **13** (PLAN14, RECORD14, DEC13, P273-FROM, P273-TO, MUT-1-FROM to MUT-4-TO), each **matching** its BEGIN-marker sha256. Committed carriers: orchestrator at C2, rollback at C3, loop at C4, each **equal** to its digest |
| G2 the record | C1 | `gate_g1g2.py` 0; `pytest tests/docs/ -q` 0 | `plan.md` **equals** PLAN14; **34** lines; `^## Goal$` **1**; `^## Next Steps$` **1**. `live_review.md` **equals** its `c3047df0` blob + RECORD14 (1019272 + 4984 = 1024256 bytes); `decisions.md` **equals** its `c3047df0` blob + DEC13 (1382828 + 3212 = 1386040). P273: TO contains FROM **false**; FROM count **1** at base, **0** at C1, TO **1** at C1; `T2_F273.md` **equals** its base blob with the pair applied. `^Gate: F\d+ R\d+ — ` **122** → **123**; `Gate: F261 R13 — ` **1** at C1; distinct `^- R-\d+ — ` **105** → **106**, C1 minus base exactly **R-0903**; distinct `^Done: R-\d+ — ` **8** → **8**; open by distinct id **97** → **98**. `tests/docs/`: `310 passed in 1.09s` |
| G3 the tables | C2 `98866b80`, C3 `4bf17d32`, C4 `be6ae79d` | `gate_g3g4.py` **1** — **RED** | tables: orchestrator **17** rows, rollback **29**, loop **14**, every count as stated, no delete target missing, no STOP. `--no-renames --name-only` from each parent: exactly the carrier and the paths G3 names (12, 9 and 11 paths); each single-parent. `apps`, `tests`, `scripts`, `packages`, `README.md` each **match** the dry run at C2, C3 and C4. **`docs` does NOT match**: C2 `786c8d72a5f0ecf1024b723ed517a8f544e10555` against `d86c24c6…`, C3 `211481c58748f8985cf2c1a83169eb902411ba9a` against `cd7dbc5c…`, C4 `46cc5d56ce7a352a61bf62e969bfb74e9248cb24` against `cf0d7c41…`; in all three `git diff-tree -r --name-status <dry-run> <committed>` prints exactly `M roadmap/features/T2_F273.md`. Before each commit a probe in a temporary index put `docs/roadmap/features/T2_F273.md` back to its `c3047df0` blob and the `docs` tree then **equalled** the dry run's id at C2, C3 and C4 (`docs_tree_probe.py` exit 0 each). Insertions: C2 **38** (1385 deletions), C3 **48** (174), C4 **26** (708) |
| G4 the sweep | C4 `be6ae79d` | `gate_g3g4.py` G4 lines PASS | the `git grep` at C4: exit **1**, stdout `''`, stderr `''`. `python3 -m ruff check` over the 14 `.py` paths of C2 to C4 that exist at C4 (absent: `apps/cli/commands/loop_cmd.py`, `apps/cli/commands/orchestrator_cmd.py`, `tests/cli/test_loop_cmd.py`, `tests/cli/test_orchestrator_brain_cli.py`): exit **0**, `All checks passed!` |
| G5(a) control | worktree at C4 | 0 | `apps.cli.grouped` loaded from the worktree; `461 passed in 31.60s`; **0** failed nodes |
| G5(1) an `orchestrator` handler row | same worktree | 1 | MUT-1-FROM count **1** in `apps/cli/commands/self_cmd.py`; `1 failed, 460 passed in 31.63s`; **1** failed node, `TestDeletedCommands::test_no_deleted_id_is_left_in_the_dispatch_table` **among them** |
| G5(2) a `rollback` handler row | same worktree, after `checkout --` | 1 | MUT-2-FROM count **1** in `apps/cli/commands/real_test_execution_cmd.py`; `1 failed, 460 passed in 31.64s`; **1** failed node, `TestDeletedCommands::test_no_deleted_id_is_left_in_the_dispatch_table` **among them** |
| G5(3) a `loop` handler row | same worktree, after `checkout --` | 1 | MUT-3-FROM count **1** in `apps/cli/commands/real_test_execution_cmd.py`; `1 failed, 460 passed in 31.50s`; **1** failed node, `TestDeletedCommands::test_no_deleted_id_is_left_in_the_dispatch_table` **among them** |
| G5(4) the `loop` group without commands | same worktree, after `checkout --` | 1 | MUT-4-FROM count **1** in `apps/cli/command_catalog.py`; `1 failed, 468 passed in 32.16s`; **1** failed node, `TestCatalogIntegrity::test_every_group_has_at_least_one_command` **among them** |
| G6 the suite, SPEC S | primary checkout at C4, serially | 0 | `suite_spec.py`: argv `python3 -B -m pytest -q -p no:randomly -p no:cacheprovider --tb=short -rfEs`, `PYTHONPATH`, `REMEDY_PROJECT`, `REMEDY_DATA_DIR` removed, `PYTHONDONTWRITEBYTECODE=1`; last line `18128 passed, 23 skipped, 1 warning in 1281.79s (0:21:21)`; distinct bad nodes **0**, so no re-run; `git status --porcelain` `''` and `git branch --list 'remedy/job-*'` 16 lines afterwards |
| G7 the tree | after C5 and the push | not yet run | reported in the completion message only |

Open findings: **98** by distinct id. The open High ids are **R-0803, R-0804 and R-0807**.

Operator questions open: 0

## Authored-text proofs

| Text | Target | Result |
|---|---|---|
| the block | `.agent/authored/f261-r14.md`, `.agent/last_block.md` | sha256 **equal** to the delegated digest at C0a; mirror byte-identical at C0b (G1) |
| PLAN14 | `.agent/plan.md` | **equal** at C1 (G2) |
| RECORD14, DEC13 | `.agent/live_review.md`, `.agent/decisions.md` | each **equal** to its `c3047df0` blob followed by the slice at C1 (G2) |
| P273-FROM, P273-TO | `docs/roadmap/features/T2_F273.md` | **equal** to its `c3047df0` blob with the pair applied at C1 (G2) |
| the three tables | `.agent/authored/f261-r14-{orchestrator,rollback,loop}.jsonl` and their paths | carrier digests **equal**; `apps`, `tests`, `scripts`, `packages`, `README.md` equal the dry run; `docs` differs only by C1's `T2_F273.md` (G3) |
| MUT-1-FROM to MUT-4-TO | the G5 worktree only | used as the mutation bytes; never written to the checkout |

NO SLICE AND NO TABLE WAS EDITED. Every slice was extracted programmatically as the bytes strictly between its `BEGIN`
and `END` lines and verified against its BEGIN-marker sha256 before use; each table was verified against its digest
before it was applied and copied.

## Item-status table

| Item | Status | Reason |
|---|---|---|
| C0a / C0b | done | two commits, as the Bundle orders |
| C1 PLAN14, RECORD14, DEC13, P273 | done | one commit, the first substantive commit |
| C2 the orchestrator table | done | one commit |
| C3 the rollback table | done | one commit |
| C4 the loop table | done | one commit |
| C5 handoff | done | this commit |
| G1 · G2 · G4 · G5 · G6 | done | exit codes and readings above |
| G3 | deviated | RED on the `docs` object at C2, C3 and C4; the only differing path is C1's `T2_F273.md` (Deviation 1) |
| G7 | skipped | runs after this commit and its push; results in the completion message |

## Deviations & assumptions

1. **G3 is red, and the round went on to G4, G5 and G6 anyway.** G3's `docs` tree ids cannot be met by the Bundle
   as ordered: C1 rewrites `docs/roadmap/features/T2_F273.md` with pair P273, every later commit inherits that file,
   and the dry-run `docs` ids equal the committed trees with that one file at its `c3047df0` blob. All other objects,
   every path set, every row count and every carrier digest match. Constraint 3 makes a red gate a STOP: commit what
   is honestly finished and hand back. C2 to C4 were already applied under the table rules, none of which stopped, so
   they count as finished. G4, G5 and G6 only read the tree: the G5 worktree was removed and the suite changed nothing.
   They ran to give the reviewer evidence before the handback. No commit beyond this handback was made after the red
   reading. The mismatch was first seen in a pre-commit index probe before C2. Stopping there would have committed
   nothing of the tables for a mismatch the Bundle itself causes.
2. **Tables were applied directly on disk.** `.remedy-wt/f261r14w/apply_table.py` checks the carrier digest, then
   applies every row strictly in file order against the tree the previous rows left, with `encoding="utf-8",
   newline=""`, the exact-count check and the must-not-exist checks, stopping on the first mismatch; it copies the
   carrier after the last row. No count differed and no target existed, so no table STOP arose.
3. **G1's carrier clause was read after C4, not after C1.** The carriers are first committed at C2 to C4; their
   committed digests were read by `gate_g3g4.py` after C4, and each source carrier's digest was also verified before
   its table was applied and copied.
4. **G5 ran through a runner**, `.remedy-wt/f261r14w/wt_runner.py`, invoked as `python3 -B`: it drops its own directory
   from `sys.path`, changes into the worktree, puts it first on `sys.path` and in `PYTHONPATH`, removes
   `REMEDY_PROJECT` and `REMEDY_DATA_DIR`, sets `PYTHONDONTWRITEBYTECODE=1`, asserts that `apps.cli.grouped` loaded
   from inside the worktree, and calls `pytest.main` with `-q -p no:randomly -p no:cacheprovider -rf --tb=no` over the
   four test files G5 names.
5. **Commit subjects** were worded by this worker, since the block names each commit's content but not its subject.
6. **The open set** was computed as the distinct `^- R-\d+ — ` ids minus the distinct `^Done: R-\d+ — ` ids.
7. **File reading before edits.** The tables and slices were applied programmatically, so instead of reading each
   target file in full I read the staged diff of each of C1 to C4 before committing and ran `ruff` on the touched
   `.py` files; the byte-equality, tree-id gates, ruff, the red-proofs and the suite prove each result.

## Next

1. Phase 1 rule 1: the next session reads `.agent/STOP` first.
2. The reviewer's verdict on round 14, including G3's red `docs` reading (Deviation 1).
3. The next deletion round `.agent/f261_t003_inventory.md` proposes: the loop modules with the run report's loop
   reference, the `queue` group and `job_queue.py`.

## Session close — session 38, written after the reviewer's verdict on round 14

The planner and reviewer of session 38 reviewed rounds 10 to 14 of F261 and ends the session after
those five delegated rounds, all PASS. Context self-assessment: the reviewer's context carries the
protocol, five rounds of research, dry runs and verdicts and the whole T003 measurement, and its
authoring slips are accumulating, the signal operator amendment amend0905-throughput names: one
reached the worker in round 14 as a gate no commit could meet, and two more, a mutation's bytes and
a command id in a decision, were caught by the reviewer's own checks before emission. The next
step opens a deletion slice whose rulings need fresh measurement, so the session ends at this round
boundary. Nothing is half-written; the branch is pushed.

### The verdict to book

Round 15's first commit that writes the record appends the paragraph below to
`.agent/live_review.md` byte for byte, preceded by one empty line, per operator amendment
amend0827-process-diet rule 1.

Gate: F261 R14 — the F261 round 14 entry. VERDICT PASS. Written by the planner and reviewer of session 38 after reading the committed range `c3047df0`..`71fb95dc` and re-deriving the readings below; the worker's report was evidence for none of them. It is carried by `.agent/handoff.md` in the session-close commit that follows `71fb95dc` and booked by the first commit of round 15 that writes the record, per operator amendment amend0827-process-diet rule 1. THE TRANSPORT: `.agent/authored/f261-r14.md` at `8d6a7bee` and `.agent/last_block.md` at `b5d87e1d` are byte-identical to the reviewer's scratch original, sha256 `ec743657d65cf88693654218b20e6f98baf9f0a83e5f78fe5f712723f46d004e`, and the three tables committed at `98866b80`, `4bf17d32` and `be6ae79d` are byte-identical to the reviewer's. THE STATE: at `ebd3c812` and again at `71fb95dc`, `.agent/plan.md` equals PLAN14, `.agent/live_review.md` and `.agent/decisions.md` equal their `c3047df0` blobs followed by RECORD14 and DEC13, and `docs/roadmap/features/T2_F273.md` equals its `c3047df0` blob with the pair P273 applied. THE TABLE COMMITS: at `98866b80`, `4bf17d32` and `be6ae79d` the `apps`, `tests`, `scripts`, `packages` and `README.md` objects equal the reviewer's dry-run commits of the tables, which had reproduced the research helper's trees exactly, and the `docs` object differs from the dry run's by `docs/roadmap/features/T2_F273.md` alone, which at each of those commits equals the P273 result; each commit's `--no-renames` path set is the dry run's plus its carrier, and `git show --numstat` reads 38, 48 and 26 insertions. G3 of the block ordered the `docs` object equal to the dry run's, which the reviewer had measured before applying the record slices, so no commit carrying C1's pair could meet it; the worker read that gate red, measured that the one differing file was the one C1 changes, and declared the deviation, and the slip is the reviewer's. In the dry run's production diff each deleted group leaves with its handlers, its catalog entries, its tests and the package code only it called; `list_decisions`, `list_rollback_proofs` and `audit_rollback_safety` stay for the cockpit and `test integrity`, `snapshot create` relates to `snapshot show`, and the two pages keep their text under dated status lines. At `71fb95dc` the grep of `remedy orchestrator`, `remedy rollback`, `remedy loop`, the two deleted handler modules and the three deleted rollback functions over `apps`, `packages`, `scripts`, `tests`, `docs` without `docs/roadmap`, and `README.md` exits 1 with no output. In the reviewer's dry run a full suite under `-n auto` without `tests/ui_server` read 1 failed, `test_vitest_passes`, and 17618 passed, and the cockpit, docs, canary and smoke-script tests read 633 passed. Over `tests/test_command_catalog.py`, `tests/cli/test_cli_ux.py`, `tests/test_grouped_cli.py` and `tests/orchestration/test_import_reachability.py`, which passed 461 unmutated, an `orchestrator`, a `rollback` and a `loop` handler row each failed 1 test and the `loop` group restored without commands failed 1. The record slices and the pair applied on top of the dry run passed `tests/docs/` and the other files the reviewer ran among those that read the edited state files, apart from `test_vitest_passes`, at 840 passed. THE REVIEWER'S RUN in the primary checkout at `71fb95dc` of those four files, the orchestrator, real test execution, cost preview, decision evidence, model routing, loop spec and loop run tests, `tests/ui_server/test_dashboard_cockpit_truth.py`, `tests/ui_server/test_dashboard_contract.py`, `tests/cli/test_golden_path.py`, `tests/cli/test_advertised_commands.py`, `tests/docs/` and `tests/test_remedy_smoke_script.py` read 1727 passed and 3 skipped, and `git branch --list 'remedy/job-*'` read 16 lines. The open set reads 98 by distinct id at `71fb95dc`.

### The prose slip to book

The same first commit appends this line to `.agent/prose_slips.md`, preceded by one empty line:

2026-09-15 · F261 R14 · G3 of the round 14 block ordered each table commit's `docs` object equal to the reviewer's dry run, which applied the tables before the record slices, while C1 of the same block rewrote `docs/roadmap/features/T2_F273.md`; the gate was unmeetable by construction, the worker declared it after measuring that file as the only difference, and the rule that follows is that a dry run whose record commit touches a gated object applies the record first.

### What the next session needs to know

- T003 follows `.agent/f261_t003_inventory.md`, measured at `80e9cc0f` and not re-verified; its
  round B is next: the loop modules `packages/orchestration/loop_spec.py` and `loop_run.py` with
  the run report's `loop_ref`, the `queue` command group, and `packages/orchestration/job_queue.py`
  with the F048 binding in `long_run_executor.py`, its configuration keys and `queue_dir`, with a
  deletion paragraph; the queue heir the feature file names, `mission list --status planned`, is
  not built, so that paragraph registers it.
- The method of rounds 10 to 14 held: a research helper builds JSON-lines tables in its own
  detached worktree; the reviewer re-applies them on the real tip, compares tree ids, reads the
  production diff, runs its own mutations and a full suite under `-n auto` without
  `tests/ui_server`, applies the record slices on top for the state-file tests, removes its
  worktree, and gates the worker on tree ids. When a record commit touches `docs/` or any other
  gated object, the dry run applies the record before measuring tree ids.
- Deletion consumers an importer sweep misses: `tests/test_remedy_smoke_script.py` reads
  `scripts/remedy_smoke.sh` as text, `tests/ui_contracts/test_humanize_catalog.py` pins UI event
  keys to emitters, `tests/orchestration/test_command_discovery.py` runs help in a subprocess,
  and `tests/cli/test_advertised_commands.py` reads hints in `apps`, `packages`, `scripts`,
  `docs/system` and `docs/guides`. `tests/cli/test_cli_ux.py` asserts at least 40 groups; 41
  remain after round 14.
- Findings registered this session: R-0901 and R-0902, owner F261, fixed by round 11 and resolved
  in round 12's record; R-0903, owner F273, with its Acceptance line in `T2_F273.md`.
- Every helper brief and block forbade calling a runner; `git branch --list 'remedy/job-*'`
  read 16 lines at every gate of the session.

### Next

1. Phase 1 rule 1: the next session reads `.agent/STOP` first; then the Open PR Gate, which finds
   no open pull request for this branch.
2. Round 15's first record commit books `Gate: F261 R14` and the prose slip from this section.
3. Round B of `.agent/f261_t003_inventory.md`.

Operator questions open: 0
