# Handoff — F276 Data-root hygiene & disk budget · Round 1

## Session

SESSION 1 of feature F276 · round 1 · rounds so far 1

Context self-assessment: the worker read the step block and verified its digest before anything else, then AGENTS.md in full, `docs/agents/handback_template.md`, `docs/roadmap/features/T2_F276.md` and the `decisions.md` payload (DECISIONs F276 D1 and D2), and held all of it without loss; every numeral below is the output of a command run in this round, not a recollection.

## Range

Review of 43d14817..HEAD — branch `feature/f276-data-root-hygiene`.

## Summary

Round 1 claims F276 and builds T001.
- C1 claims the feature: eight reviewer payloads saved under `.agent/authored/`, plan and context rewritten, the review record re-headed on F273's carried findings, F273 round 25's PASS verdict and its hosted-CI colour booked, R-1001 registered, DECISIONs F276 D1 and D2 appended, STATUS `[~]`.
- C2 repairs R-1001, the node that reddened both hosted columns of F273's closure pull request while the same commit passed locally.
- C3 builds the data-root class registry in `data_paths` with its architecture test.
- C4 builds `footprint()`, `remedy data usage` and the advanced `data` group, and records the classes in `docs/system/architecture.md`.
- C5 is this handoff. No pull request was opened.

## Item status

| Item | Status | Reason |
|------|--------|--------|
| C1 claim | done | |
| C2 R-1001 | done | |
| C3 the registry | done | |
| C4 footprint, the `data` group and the doc | done | |
| C5 handoff | done | |
| G1 transport + state | done | every reading True, exit 0 |
| G2 code transport | done | four object ids and twelve paths as ordered |
| G3 targeted suite | done | 945 passed, exit 0 |
| G4 ruff | done | All checks passed! |
| G5 mutation red-proofs | done | control green, three mutations red |
| G6 push + clean tree | done | reported in the round report; it follows this commit |

Landed: R-1001 — `tests/cli/test_study_cmd.py::TestStudyCommandReachability::test_study_run_dispatch_e2e` now asserts that the loopback listener was contacted only when `importlib.util.find_spec("ollama") is not None`, with the comment naming the optional extra that decides it; the fake `REMEDY_OLLAMA_HOST` that bounds the subprocess away from a real model is untouched. Commit `57286568`. Only the reviewer's authored text resolves a finding, so R-1001 stays in the open set below.

## Commits

### b1395893 F276 R1 C1: claim F276 — the eight reviewer payloads saved under .agent/authored, plan and context rewritten, the review record re-headed on F273's carried findings, F273 round 25's PASS verdict and its hosted-CI colour booked, R-1001 registered, DECISIONs F276 D1 and D2 appended, and the STATUS line moved to in-progress
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/authored/f276-r1-block.md` | +114 / -0 | Byte copy of the block |
| `.agent/authored/f276-r1-context.md` | +42 / -0 | Byte copy of context.md |
| `.agent/authored/f276-r1-decisions.md` | +51 / -0 | Byte copy of decisions.md |
| `.agent/authored/f276-r1-ledger.md` | +6 / -0 | Byte copy of ledger.md |
| `.agent/authored/f276-r1-live_review_head.md` | +26 / -0 | Byte copy of live_review_head.md |
| `.agent/authored/f276-r1-plan.md` | +30 / -0 | Byte copy of plan.md |
| `.agent/authored/f276-r1-status_from.txt` | +1 / -0 | Byte copy of status_from.txt |
| `.agent/authored/f276-r1-status_to.txt` | +1 / -0 | Byte copy of status_to.txt |
| `.agent/context.md` | +23 / -21 | := context.md |
| `.agent/decisions.md` | +51 / -0 | `43d14817` bytes + decisions.md (DECISIONs F276 D1, D2) |
| `.agent/live_review.md` | +28 / -18 | live_review_head.md + the `43d14817` bytes from `## Findings` + ledger.md |
| `.agent/plan.md` | +20 / -15 | := plan.md |
| `docs/roadmap/STATUS.md` | +1 / -1 | The F276 line `[ ]` rewritten to `[~]` |

394 insertions, 55 deletions (`git show --numstat`).

### 57286568 F276 R1 C2: repair R-1001 — the study dispatch test asserts the loopback probe only where the optional ollama extra makes that probe possible, so hosted CI stops failing a node the same commit passes locally; the fake model host that bounds the subprocess is untouched
| Path | +/- | Reason |
|------|-----|--------|
| `tests/cli/test_study_cmd.py` | +9 / -1 | The `asked` assertion guarded by `find_spec("ollama")`, with the reason in the comment |

9 insertions, 1 deletion (`git show --numstat`).

### 6e126dd2 F276 R1 C3: T001 the data-root class registry — EPHEMERAL_CLASSES and DURABLE_CLASSES declared as data in data_paths, each entry naming its owning module and its reclaim rule, classify_data_child and data_class_dir as the only readers, the eleven class-named dir helpers resolving through the registry so an unregistered name raises, and an architecture test that measures the children the code creates instead of listing them
| Path | +/- | Reason |
|------|-----|--------|
| `packages/orchestration/data_paths.py` | +98 / -12 | `DataRootClass`, five ephemeral and fifteen durable classes, `classify_data_child`, `data_class_dir`; eleven `*_dir()` helpers resolve through it |
| `tests/test_data_root_classes.py` | +253 / -0 | The architecture test: helper calls plus an `ast` scan of `packages/`, `apps/`, `scripts/`, with its own planted-tree red proof |

351 insertions, 12 deletions (`git show --numstat`).

### c8916d2d F276 R1 C4: T001 the footprint and the data group — data_footprint walks the root once with scandir, follows no symlink, shells out to nothing and writes nothing; remedy data usage reports bytes and files per class and per child, with --json; the advanced data group takes the catalog to thirty-one groups and the partition test says which one is new; architecture.md records the classes and what reclaim still owes
| Path | +/- | Reason |
|------|-----|--------|
| `apps/cli/command_catalog.py` | +12 / -0 | The `data` GroupDef (`user_facing=False`) and the `data.usage` entry |
| `apps/cli/commands/__init__.py` | +2 / -1 | `data_cmd` imported and added to the handler table |
| `apps/cli/commands/data_cmd.py` | +51 / -0 | The `data.usage` handler and `format_data_bytes` |
| `docs/system/architecture.md` | +12 / -0 | The data-root classes paragraph; reclaim is T002 and does not exist yet |
| `packages/orchestration/data_footprint.py` | +136 / -0 | `footprint()`, `ChildFootprint`, `DataFootprint`, `export_footprint_json` |
| `tests/cli/test_cli_ux.py` | +6 / -3 | `data` added to the internal groups; the partition count 30 to 31, the docstring naming the new group |
| `tests/cli/test_data_cmd.py` | +62 / -0 | `remedy data usage` through the grouped CLI, human and `--json` |
| `tests/orchestration/import_reachability_allowlist.txt` | +2 / -0 | `apps.cli.commands.data_cmd`, `packages.orchestration.data_footprint` |
| `tests/orchestration/test_data_footprint.py` | +79 / -0 | Per-child and per-class bytes, symlinks, a missing root, no subprocess, no write |

362 insertions, 4 deletions (`git show --numstat`).

### C5 — this handoff commit
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/handoff.md` | rewrite | A handoff cannot table the commit that writes it (R-0149 pattern) |

## External actions

- `git checkout -b feature/f276-data-root-hygiene` from `main` at `43d14817` — created. The reviewer ran the Open PR Gate before this round: pull request 260 was merged and zero pull requests are open.
- `git worktree add --detach .remedy-wt/f276-r1-proof c8916d2d` — exit 0, for G5 only.
- `git worktree remove .remedy-wt/f276-r1-proof` — exit 0; `git worktree list` then shows the primary checkout and the operator's `.remedy-wt/job-468c8e62a2cc4fac` alone.
- `git push -u origin feature/f276-data-root-hygiene` — after this commit; its result is in the round report.
- No pull request was created. Nothing was merged, forced, amended or deleted.

## Verification

- G1 transport + state — `python3 -B .remedy-wt/f276-r1/g1.py`, EXIT 0. All eight payload digests matched; all eight `.agent/authored/f276-r1-*` copies equal their payloads; `plan.md == payload: True`; `context.md == payload: True`; `live_review.md == head + 43d14817[## Findings:] + ledger: True`; `decisions.md == 43d14817 bytes + decisions payload: True`; `STATUS.md == 43d14817 bytes with the pair applied: True`; `STATUS FROM 1x before / 0x after: True True`; `STATUS TO 0x before / 1x after: True True`; `TO contains FROM: False` — a rewrite, as the block's containment test says. Saved block: 114 lines, sha256 `6fded040586e53cbc2dbacb0dfeeea55ec691a21244ecd2222687fca6e3001ce`, identical to the block payload's own reading.
- G2 code transport — `git rev-parse c8916d2d:packages c8916d2d:apps c8916d2d:tests` printed `0545a9d3450fa2fdb41ac026c192d1e3ac4f7cfa`, `c57d66e877e5e4a370a9234cfd5fb8a2c6290e61`, `3ddec410900ee2f3cb14ddb6d7cb2c91b07089bc`; `git rev-parse c8916d2d:docs/system/architecture.md` printed `d39a7663e2ed5833715d74cad907e26d69bed610` — the four objects of the reviewer's dry run, exit 0. `git diff --name-only b1395893 c8916d2d` named 12 paths and no other: `apps/cli/command_catalog.py`, `apps/cli/commands/__init__.py`, `apps/cli/commands/data_cmd.py`, `docs/system/architecture.md`, `packages/orchestration/data_footprint.py`, `packages/orchestration/data_paths.py`, `tests/cli/test_cli_ux.py`, `tests/cli/test_data_cmd.py`, `tests/cli/test_study_cmd.py`, `tests/orchestration/import_reachability_allowlist.txt`, `tests/orchestration/test_data_footprint.py`, `tests/test_data_root_classes.py`.
- G3 targeted suite — `python3 -m pytest -q -p no:cacheprovider` over the seventeen ordered paths, serial, in the primary checkout: `945 passed in 171.51s (0:02:51)`, EXIT 0, 0 failed.
- G4 ruff — `python3 -m ruff check` over the eleven ordered paths: `All checks passed!`, EXIT 0.
- G5 mutation red-proofs — ONE disposable worktree at `c8916d2d`. `data_paths -> .../f276-r1-proof/packages/orchestration/data_paths.py` and `data_footprint -> .../f276-r1-proof/packages/orchestration/data_footprint.py`, both inside the worktree. `__pycache__` purged before each run (0 dirs each time, the worktree being fresh). CONTROL over the four files: `91 passed in 4.53s`, EXIT 0. (a) `def foo_dir(` count 0 before, 1 after the append: `tests/test_data_root_classes.py` EXIT 1, `FAILED tests/test_data_root_classes.py::test_every_child_the_code_creates_is_in_exactly_one_class`, the message naming `foo: data_paths.foo_dir(), packages/orchestration/data_paths.py:469`. (b) the 16-space `is_dir = entry.is_dir(follow_symlinks=False)` line counted 1, replaced by `is_dir = True`: `tests/orchestration/test_data_footprint.py` EXIT 1, `3 failed, 2 passed` — `test_bytes_and_files_per_child_and_per_class`, `test_a_symlink_is_counted_by_its_own_size_and_never_followed`, `test_the_walk_shells_out_to_nothing`. (c) the `"data": GroupDef(...)` line counted 1, deleted: `tests/cli/test_data_cmd.py` and `tests/cli/test_cli_ux.py` EXIT 1, `8 failed, 71 passed` — all four `test_data_cmd` nodes plus `TestAdvancedHelp::test_all_commands_shows_internal`, `TestHiddenCallable::test_hidden_group_callable`, `TestGroupDefIntegrity::test_internal_groups_marked` and `TestGroupDefIntegrity::test_catalog_partition_matches_d4`. No mutation stayed green. Each of the three files was reverted byte-identically before the next (True, True, True), the worktree's `git status --porcelain` was empty, and the worktree was removed as the step's last action.
- G6 push and clean tree — reported in the round report only, since this handoff commit precedes the push.

## Open findings

15 open BY DISTINCT ID and 15 by the canonical line formula (`scripts/rotate_live_review.py::count_open_findings`), both measured on the committed ledger at this branch's HEAD: 18 distinct ids match `^- R-\d+ — ` against 3 matching `^Done: R-\d+ — `. The open set: R-0499, R-0622, R-0662, R-0819, R-0820, R-0829, R-0866, R-0880, R-0892, R-0950, R-0984, R-0998, R-0999, R-1000, R-1001. The first fourteen are F273's carried set, owned by F282 under the OWNERSHIP AT CLOSE paragraph; the fifteenth is R-1001, registered and repaired this round and awaiting the reviewer's resolution.

## Authored-text proofs

All eight reviewer-authored payloads were copied byte-for-byte with `shutil.copyfile`, never retyped. Disk-to-disk comparison against the committed `.agent/authored/f276-r1-*` copies: `plan.md`, `context.md`, `live_review_head.md`, `ledger.md`, `decisions.md`, `status_from.txt`, `status_to.txt` and `block.md` each equal their payload — eight `True` readings under G1, and each payload's sha256 matched the digest the block states. The code carrier `.remedy-wt/f276-r1/f276-r1.diff` matched sha256 `35a318161ab8c2de5eb01557976128a32c40e9c20abf1fa3f4bbf82dd9f0ccca` and was applied with `git apply --include=` in three disjoint slices, never retyped and never edited.

## Deviations & assumptions

- None to the block's ordered commit sequence: C1, C2, C3, C4 and C5 were committed in that order, no extra commit, none dropped, none reordered.
- Reading, not a deviation: `git commit`'s own summary line for C1 printed `423 insertions(+), 84 deletions(-)` because it applied rename/rewrite detection to `.agent/context.md` and `.agent/plan.md`. The block's ordered measurement is `git show --numstat`, which reads 394 insertions for C1. Both numbers are below the 500-insertion cap, so no commit in this round is oversize under either reading.
- Assumption, stated because the block's wording admits a second reading: `.agent/authored/f276-r1-<name>` was built from the eight entries of the block's PAYLOADS list. The code carrier `f276-r1.diff` is listed under CODE, not under PAYLOADS, so it was applied rather than copied into `.agent/authored/`.
- Gates G3 and G4 were additionally run once on the staged C4 tree before the C4 commit, to satisfy the AGENTS.md Commit Gate; the readings reported above are that same tree, re-read after the commit for G1, G2 and G5. Nothing was committed while a gate was red.
- Operator questions open: 5 (`### Q` headings in `.agent/operator_questions.md`).

## Next

Phase 1 rule 1 of `docs/agents/self_drive_protocol.md` first — re-read `.agent/STOP` from disk, and if the sentinel exists write the handoff and end the session, doing nothing else. Then the review of round 1: the reviewer re-runs G1 to G6 and reads `43d14817..HEAD` bottom-up before any verdict. Then T002 — `remedy data reclaim`, dry run by default, `--apply` deleting only the paths its own preview named and refusing both a non-terminal workspace and any path that is not a direct child of a class directory.
