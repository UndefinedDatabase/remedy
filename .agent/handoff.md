# Handback — F275 round 16

## Session

SESSION 9 of feature F275 · round 16 · rounds so far 16

F275's soft limit is 20 sessions and 60 rounds by operator amendment
amend0908-f275-finish rule 1, and it travels to no other feature. This round is
well inside it, so no scope report is owed.

## Range

Review of `38e03d2f`..`HEAD`

## Commits

### e5fe544f F275 R16 C0a: save the round 16 authored block.
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f275-r16.md | +395 / -0 | The delegation source copied byte for byte with `shutil.copyfile`, never retyped. |

### 3720c48b F275 R16 C0b: mirror the round 16 block into the last-block file.
| Path | +/- | Reason |
|---|---|---|
| .agent/last_block.md | +275 / -313 | The same bytes mirrored; a single `.agent/**` state-file rewrite. |

### 453b80d6 F275 R16 C1: advance the plan to round 16.
| Path | +/- | Reason |
|---|---|---|
| .agent/plan.md | +20 / -20 | Replaced WHOLE by the PLAN16 slice extracted from the committed C0a blob. |

### 876dc89e F275 R16 C2: book the round 15 PASS, resolve R-0855, register R-0859 and R-0860, record five prose slips.
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +8 / -0 | LEDGER16 appended: the round 15 PASS, `Done: R-0855`, and the R-0859 and R-0860 registrations. |
| .agent/prose_slips.md | +10 / -0 | SLIPS16 appended: the five round 15 slips. |

### 3384dd53 F275 R16 C3: delete the main builder adapter module group and repair the survivors.
| Path | +/- | Reason |
|---|---|---|
| packages/orchestration/main_builder_adapter.py | +0 / -964 | The module, removed whole by `git rm`. |
| apps/cli/commands/main_builder_adapter_cmd.py | +0 / -143 | Its handler file, removed whole. |
| tests/orchestration/test_main_builder_adapter.py | +0 / -474 | Its unit tests, removed whole. |
| tests/cli/test_main_builder_adapter_cli.py | +0 / -139 | Its CLI tests, removed whole. |
| docs/system/main-builder-adapter-v0-token-controlled-session-rail.md | +0 / -142 | Its spec page, removed whole. |
| docs/guides/main-builder-adapter-user-guide-v0.md | +0 / -80 | Its user guide, removed whole. |
| apps/cli/command_catalog.py | +1 / -142 | The `builder` GroupDef, the 110-line `builder` section holding ten `CommandEntry` records, the three `worker.doctor` / `worker.add` / `worker.disable` records (30 lines), and the one insertion repairing a `related=` tuple. |
| packages/orchestration/run_contract.py | +0 / -12 | Six `ContractAction` members and their six `_DEFAULT_ALLOWED_ACTIONS` rows. |
| apps/cli/commands/__init__.py | +1 / -2 | `main_builder_adapter_cmd` out of the import block and out of the `for mod in (…)` tuple. |
| apps/cli/commands/worker_facade_cmd.py | +0 / -218 | `_cmd_worker_doctor`, `_cmd_worker_add`, `_cmd_worker_disable`, their three `COMMAND_HANDLERS` rows, `_WORKER_ALIASES`, `_resolve_alias` and the four section-banner comment blocks. |
| tests/cli/test_worker_facade_cmd.py | +4 / -166 | Four test classes deleted with their banners, the two readerless `_ADAPTER_PATCH` / `_SAVE_ADAPTER` constants, the now-unused `unittest.mock.patch` import, and four rewritten assertions. |
| tests/cli/test_product_spine.py | +1 / -13 | Two tests deleted whole; the operator-command tuple narrowed. |
| tests/orchestration/test_development_artifact_boundary.py | +4 / -8 | `main_builder_adapter` out of `_PRODUCT_MODULES`, its test deleted, and the no-agent loop repointed at the four modules `_cmd_doctor_core` really imports. |
| tests/cli/test_cli_ux.py | +1 / -1 | `builder` out of the hardcoded `_INTERNAL_GROUPS` set. |
| tests/orchestration/test_cluster_deletion_map.py | +0 / -2 | The module and its handler file out of the cluster tuples. |
| tests/orchestration/import_reachability_allowlist.txt | +0 / -2 | The module and its handler out of the allowlist. |
| tests/orchestration/cluster_deletion_map.txt | +0 / -1 | The one recorded import edge into the module. |
| pyproject.toml | +0 / -1 | The handler out of the mypy module list. |
| scripts/remedy_test_fast.sh | +0 / -1 | The deleted test file out of the fast lane. |
| .agent/f275_deletion_order.md | +0 / -1 | REGENERATED from `measured_order()`, never typed; a pure shrink from five components to four. |
| docs/README.md | +0 / -2 | The two index rows linking the deleted pages, matched on the link target. |
| docs/system/core-product-spine-v0.md | +1 / -2 | The numbered operator path loses `6. Check worker` and is renumbered whole from seven steps to six. |
| docs/system/development-artifact-boundary-v0.md | +0 / -2 | The `Builder status` and `Package truth` table rows. |
| docs/system/test-lanes-v0.md | +0 / -1 | The deleted test file's lane row. |

C3 totals: 24 paths, +13 / -2519.

### C4 — this handback commit
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | rewritten whole | A handoff cannot table the commit that writes it (R-0149 pattern). |

## External actions

| Command | Outcome |
|---|---|
| `git worktree add .remedy-wt/base16 38e03d2f` | Created; used for the G5 base end, the G7b base ruff run and the G7f base collection. |
| `git worktree add .remedy-wt/rp16 3384dd53` | Created; used for all four G6 red-proofs. |
| `git worktree remove .remedy-wt/rp16 --force` | Removed. |
| `git worktree remove .remedy-wt/base16 --force` | Removed. |
| `git worktree prune` | Ran; `git worktree list` now names the primary checkout alone. |
| `git push -u origin feature/f275-one-world-completion-part-three` | ONE push, after C4. See below. |

No PR was created, edited or merged. No `gh` command was run.

## Verification

One line per gate, with its REAL exit code.

| Gate | Exit | Measurement |
|---|---|---|
| G1 TRANSPORT | 0 | All three artefacts 45340 bytes at sha256 `994447338d251f5fb4a068aef05ea266acd07e362d150b80713d7abf84e253bb` and byte-equal: the `.remedy-wt/f275-r16.md` source, the committed `.agent/authored/f275-r16.md` and the committed `.agent/last_block.md`. |
| G2 PLAN AND BLOCK | 0 | `.agent/plan.md` at C1 byte-identical to the PLAN16 slice extracted from the committed C0a blob: 2454 bytes, sha256 `da53b429ce39170d54e05fda0dd17fbedbe422df5ff6c62ed4d88d3925081b2d`, 45 lines against the cap of 50; `## Goal` and `## Next Steps` both present. C0a blob TOTAL 395 lines against the cap of 490. |
| G3 THE RECORD | 0 | (a) `.agent/live_review.md` 634559 → 650049, growth 15490 = 1 + 15489; `.agent/prose_slips.md` 185058 → 189111, growth 4053 = 1 + 4052; for each the pre-blob a byte-exact prefix, the slice a byte-exact suffix, the joining byte read back as `b'\n'`. (b) N COUNTED FROM EACH SLICE by the script: 4 and 5; the last N blank-line units of each post-file equal the slice's paragraphs in order, per-unit sha256 printed and equal on both sides for all nine units. (c) Both negative controls — one byte flipped IN MEMORY inside the FIRST appended paragraph — rejected by reader (a) and reader (b) alike, while both readers accept the truth; both files re-read from disk and byte-equal to their committed post-blobs. (d) `^Gate: ` 37 → 38, rise exactly 1; `^Gate: F275 R15 `, `^Done: R-0855 — `, `^- R-0859 — ` and `^- R-0860 — ` exactly 1 each. (e) OPEN SET BY DISTINCT ID: registered 87 → 89, done 4 → 5, OPEN 83 → 84. |
| G4 DELETION COMPLETE | **1** | All six whole-file removals ABSENT from `git ls-tree -r` at C3 over 4562 tracked files. The token sweep over the 1676 tracked files outside `.agent/` and `.data/` read 16 RAW lines and 6 STRIPPED lines. THREE STRIPPED LINES FALL OUTSIDE `docs/roadmap/features/`, so the gate's binding condition FAILS. See Deviations, item 1 — the path is not in the change set and constraint 2 forbids widening. |
| G5 SHIPPED READERS | 0 | Read BY IMPORT at both ends with `sys.path` pinned and the resolved `__file__` printed. `len(_BASE_CATALOG)` 250 → 237, `len(collect_all_handlers())` 250 → 237, `len(GROUPS)` 48 → 47, `len(ALL_KNOWN_ACTIONS)` 106 → 100, duplicate ids 0 at both ends. `builder` ABSENT from `GROUPS` at C3 and all ten `builder.` ids ABSENT from both readers; the `worker` GROUP still PRESENT with its nine survivors (`list`, `registry-integrity`, `registry-list`, `registry-show`, `resources`, `run`, `show`, `status`, `unload`) and `worker.doctor` / `worker.add` / `worker.disable` ABSENT from both readers; `patch.approve`, `do.continue`, `mission.run`, `mission.report` and `doctor.core` PRESENT in both readers at C3. REFERENTIAL CLOSURE: the dangling set is EXACTLY `dogfood.run-loop` and `readiness.show` at both ends, and does NOT contain `worker.doctor`. `# ── ` section comments in `apps/cli/command_catalog.py` 57 → 56, exactly one gone, `# ── brain ───` surviving. Order file 5 → 4 components with NO survivor moving, its 26-line header sha256 unchanged at `aff913e6eedb4d9c7e5ab6e76578be881ffffa3612018cf58b5a48ad508b0cc2`, and EQUAL to a fresh regeneration from the live import graph at both ends. |
| G6 RED-PROOFS | 0 | All four inside ONE disposable worktree at C3, `__pycache__` purged before every run, `python3 -B`, each control run over that probe's OWN selection in the SAME script immediately before its mutation. Controls exit 0 at 3, 3, 3 and 37 passed; mutants exit 1 at 1, 1, 2 and 2 failures. Every target restored and proved byte-identical by sha256 before and after; worktree porcelain empty at the end. |
| G7 RUFF, RATCHETS, SUITE | 0 | (a) `python3 -m ruff check` over all nine edited `.py` files still existing at C3 — `All checks passed!`, exit 0. (b) Repo-wide `ruff check .` at the base in a disposable worktree and at C3 in the primary checkout: 26 diagnostics at BOTH ends, ruff exit 1 at both, and the two SETS compared item by item and IDENTICAL. (c) The eight-path ratchet selection — 860 passed, exit 0. (d) The canary `tests/cli/test_golden_path.py` — 42 passed, exit 0. (e) THE FULL SUITE, `python3 -B -m pytest tests/ -q`, SERIALLY, in the PRIMARY checkout with C3 COMMITTED — 18603 passed, 23 skipped, ZERO failed, exit 0, in 22:18; 18603 + 23 = 18626, equal to the C3 collection exactly. (f) THE ARITHMETIC BY THE ID SET: 18712 at the base, 18626 at C3, 86 LOST and ZERO GAINED, attributed 51 to `tests/orchestration/test_main_builder_adapter.py`, 14 to `tests/cli/test_worker_facade_cmd.py`, 10 to `tests/cli/test_main_builder_adapter_cli.py`, 8 to `tests/test_grouped_cli.py` — which parametrises over the catalog and is in no change set — 2 to `tests/cli/test_product_spine.py` and 1 to `tests/orchestration/test_development_artifact_boundary.py`. |
| G8 THE TREE | 0 | `.agent/STOP` re-read from disk and ABSENT. `git status --porcelain` EMPTY. `git worktree list` names the primary checkout ALONE. Branch `feature/f275-one-world-completion-part-three`. `git diff --name-only 876dc89e..3384dd53` compared against the block's twenty-four C3 paths as a SET: MISSING set EMPTY, EXTRA set EMPTY. Every commit before C4 single-parent, insertions 395, 275, 20, 18 and 13, all under the DECISION F104 D1 cap of 500. |

### G4 — the raw and stripped sweep, printed in full

RAW, 16 lines:

```
docs/guides/simple-operator-quickstart-v0.md:56: remedy worker doctor claude --json
docs/guides/simple-operator-quickstart-v0.md:65: remedy worker add claude --json
docs/guides/simple-operator-quickstart-v0.md:85: remedy worker disable claude --json
docs/guides/simple-operator-quickstart-v0.md:109: | `worker add claude`      | `builder adapter-enable`      |
docs/guides/simple-operator-quickstart-v0.md:110: | `worker doctor claude`   | `builder adapter-show`          |
docs/guides/simple-operator-quickstart-v0.md:111: | `worker disable claude`  | `builder adapter-enable --disabled` |
docs/roadmap/features/T2_F260.md:344: `self_repair_proposal.py`, `main_builder_adapter.py`,
docs/roadmap/features/T2_F262.md:75: catalog's 28. `builder.adapter-list`, `execution.template-list`,
docs/roadmap/features/T2_F262.md:79: dates (test.list, repair.item-list, builder.session-list,
docs/roadmap/features/T2_F267.md:14: - test.list · repair.item-list · builder.session-list ·
docs/roadmap/features/T2_F267.md:27: D4 excluded four of the 13 permanently — `builder.adapter-list`,
docs/roadmap/features/T8_F151.md:22: main_builder_adapter.py (the current builder's wrapping), plus the
docs/system/core-product-spine-v0.md:52: Adding a worker (`remedy worker add claude`) enables the adapter and template
docs/system/core-product-spine-v0.md:102: | `worker doctor <name>` | Check worker readiness | No | No |
docs/system/core-product-spine-v0.md:103: | `worker add <name>` | Enable adapter + template | Metadata | No |
docs/system/mission-run-loop-morning-report-v0.md:63: 1. Operator adds worker: `remedy worker add claude --json`
```

STRIPPED (every backtick-quoted span deleted before matching), 6 lines:

```
docs/guides/simple-operator-quickstart-v0.md:56: remedy worker doctor claude --json
docs/guides/simple-operator-quickstart-v0.md:65: remedy worker add claude --json
docs/guides/simple-operator-quickstart-v0.md:85: remedy worker disable claude --json
docs/roadmap/features/T2_F262.md:79: dates (test.list, repair.item-list, builder.session-list,
docs/roadmap/features/T2_F267.md:14: - test.list · repair.item-list · builder.session-list ·
docs/roadmap/features/T8_F151.md:22: main_builder_adapter.py (the current builder's wrapping), plus the
```

Three of the six lie in `docs/roadmap/features/`, which is the round's declared scope
ruling. The other three lie in `docs/guides/simple-operator-quickstart-v0.md`, which the
block's exhaustive change set does not name.

## Authored-text proofs

| Slice | Target | Result |
|---|---|---|
| PLAN16 | `.agent/plan.md` at C1 | Extracted from the COMMITTED C0a blob between its marker lines, markers excluded; 2454 bytes, sha256 `da53b429…`; disk-to-disk BYTE-IDENTICAL to the committed `.agent/plan.md`. |
| LEDGER16 | `.agent/live_review.md` at C2 | 15489 bytes, sha256 `9ce796a88005e18c3345238f401dadfd51e2537c8be5dd0ccdabedf826da8fe9`; byte-exact SUFFIX of the committed post-blob, growth 15490 = 1 + 15489, per-paragraph sha256 equal for all 4 units. |
| SLIPS16 | `.agent/prose_slips.md` at C2 | 4052 bytes, sha256 `a9d04b8acb90644e8b7b10f7bebea88269e6bbcd565a558e6758ceb25ee34458`; byte-exact SUFFIX of the committed post-blob, growth 4053 = 1 + 4052, per-paragraph sha256 equal for all 5 units. |

No slice was edited. The marker lines reached no target file.

## Deviations & assumptions

1. **G4 IS RED AND THE ROUND DID NOT REPAIR IT — SCOPE, NOT OVERSIGHT.** Three
   STRIPPED sweep lines fall outside `docs/roadmap/features/`, all in
   `docs/guides/simple-operator-quickstart-v0.md`: lines 56, 65 and 85 are fenced
   `bash` blocks reading `remedy worker doctor claude --json`, `remedy worker add
   claude --json` and `remedy worker disable claude --json`, each the body of its own
   `###` section ("Check worker readiness", "Add a worker", "Disable a worker"). Lines
   109 to 111 of the same file are an "Advanced commands" table mapping all three
   deleted `worker` commands onto the deleted `builder adapter-*` commands; they are
   backtick-quoted, so they survive the stripped reading but are equally dead. That
   path is NOT in the block's twenty-four-path change set, and constraint 2 orders me
   to stop and declare rather than widen. I declared and did not touch it. Note that
   `tests/cli/test_advertised_commands.py` PASSED over this state, which is the
   R-0847 blindness again: the guard does not see these forms.
2. **`apps/cli/commands/worker_facade_cmd.py` measured 0 / 218, the block predicted
   0 / 210.** The spec was applied exactly: the three command functions, their three
   `COMMAND_HANDLERS` rows, `_WORKER_ALIASES`, `_resolve_alias` and the four
   section-banner comment blocks. The file went from 533 physical lines to 315, and
   315 = 533 − 218; the surviving text keeps two blank lines on each side of `_err`
   and of the `mission run facade` banner, and ruff is clean over it.
3. **`tests/cli/test_worker_facade_cmd.py` measured 4 / 166, the block predicted
   4 / 157.** The four insertions are exactly the four rewritten assertions the block
   names. The nine extra deletions are the blank lines carried by the four deleted
   class/banner regions plus the two-line `_ADAPTER_PATCH` / `_SAVE_ADAPTER` constant
   pair — see deviation 4.
4. **`_ADAPTER_PATCH` and `_SAVE_ADAPTER` were deleted although the block does not
   name them.** They are inside a listed path. After the three test classes go they
   have no reader, and both are string literals containing the token
   `main_builder_adapter` OUTSIDE backticks, so leaving them would have put two more
   lines into G4's stripped result. Deleting them is R-0855's fix clause applied
   within the change set, not a widening of it.
5. **C3 totals measured +13 / -2519; the block predicted 13 insertions against 2502
   deletions.** The 13 insertions match exactly. The 17-deletion difference is exactly
   deviations 2 and 3 summed (8 + 9). Every other path's `+/-` matched the block cell
   for cell.
6. **The `related=("worker.doctor", "mission.report")` tuple belongs to the
   `doctor.core` record, not to `mission.run`.** The block's catalog spec attributes it
   to `mission.run`. I applied the ORDER as written — that tuple became
   `related=("mission.report",)`, the one insertion — on the record that actually
   carries it, at what was line 1601. `mission.run`'s own tuple is
   `("mission.report", "mission.ledger", "dogfood.run-loop")` and was left untouched;
   its dangling `dogfood.run-loop` is one of the two R-0859 registers.
7. **R-0859's prose misattributes both dangling references.** Measured through the
   shipped reader at the base: `dogfood.run-loop` is named by `mission.run` (R-0859
   says `mission.ledger`), and `readiness.show` is named by `repo.status` (R-0859 says
   "a `readiness`-group record"). The finding's SUBSTANCE holds — exactly two dangling
   `related=` references, exactly those two ids, no guard sees them — and I applied the
   slice byte for byte without editing it.
8. **The block's `I001` prediction did not materialise.** The change set says that
   after `from unittest.mock import patch` goes, "the blank line ruff's `I001` wants
   after `import pytest` goes with it". Removing only the import left the import block
   correctly sorted; ruff reported `All checks passed!` at exit 0 over the file with
   that blank line still in place, so no blank line was removed.
9. **Two readerless comment regions survive inside listed paths, because the block's
   per-path numstats forbid touching them and constraint 8 says no further sweep is
   owed.** `packages/orchestration/run_contract.py` lines 144-147 still carry the
   four-line "Main Builder Adapter v0 (Step 1985)" comment that explained the six
   deleted members — the spec's `0 / 12` is exactly the members and their rows.
   `docs/system/test-lanes-v0.md` still describes `test_worker_facade_cmd.py` as
   covering "Worker add/doctor/disable, alias registry, catalog wiring" — the spec's
   `0 / 1` is exactly the deleted lane row.
10. **`docs/system/core-product-spine-v0.md` still advertises two deleted commands in
    its command-taxonomy table** (lines 102-103, `worker doctor <name>` and
    `worker add <name>`) and in prose at line 52. Backtick-quoted, so they survive
    G4's stripped reading. The block orders `1 / 2` for this file — the numbered
    operator path only — so they were left.
11. **No `Landed:` line was written, and no verdict, finding or `Done:` paragraph of
    my own.** The only `Done:` text applied this round is the reviewer-authored
    `Done: R-0855` paragraph inside the LEDGER16 slice, applied as part of that slice.
12. **The bundle's ordered commit sequence was followed exactly**: C0a, C0b, C1, C2,
    C3, C4. No commit was added, dropped or reordered.

## Item-status table

| Item | Status | Reason |
|---|---|---|
| C0a save the authored block | done | |
| C0b mirror to `.agent/last_block.md` | done | |
| C1 advance the plan | done | |
| C2 the record (LEDGER16 + SLIPS16) | done | |
| C3 delete the module group, 24 paths | done | |
| C4 the handback | done | |
| G1 transport | done | exit 0 |
| G2 plan and block | done | exit 0 |
| G3 the record | done | exit 0 |
| G4 deletion complete | deviated | exit 1 — binding condition fails on three lines in a path outside the change set; declared, not repaired (deviation 1) |
| G5 shipped readers | done | exit 0 |
| G6 red-proofs | done | exit 0 |
| G7 ruff, ratchets, suite | done | exit 0 |
| G8 the tree | done | exit 0 |
| R-0855 fix clause | done | discharged by C3 as constraint 8 describes |
| R-0857 fix clause | done | the three `worker` commands deleted whole |

## Open findings

**84 by distinct id** at C2, up from 83 at the base `38e03d2f`: R-0859 and R-0860
registered, R-0855 resolved. Registered 89, done 5. Four are High — R-0803, R-0804,
R-0806 and R-0807 — all F273's rather than this feature's, per DECISION F272 D12.

## Next

The planner and reviewer of session 9 re-runs all eight gates itself against the
committed blobs over `38e03d2f`..`HEAD` and issues the round 16 verdict, weighing the
red G4 against the scope constraint that produced it. Before authoring the next round
it re-reads `.agent/STOP` from disk (Phase 1 rule 1) and only then the Open PR Gate
(rule 2). Round 17's target is the `overnight_executor` component, which this round's
regeneration made the order file's first line and which is a SINGLE module.
