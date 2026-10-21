# Handback — F307 round 5: book round 4 and five resolutions, DECISION F307 D6, R-1290, R-1292

## Session

SESSION 1 of feature F307 · round 5 · rounds so far 5

Context self-assessment: this worker verified every prepared digest, byte-copied the prepared files, self-reviewed each diff before committing, ran each gate once and wrote this handback from what it read; context is ample and nothing was lost.

Fortschritt: ~30 % (T001 to T004, T014, R-1280, R-1290 and R-1292 landed · the rest open) — Schätzung

## Range

Review of `0c0e290db`..`HEAD` on `feature/f307-findings-paydown-v9`.

## Commits

### ecd158b3b F307 R5 C1: book round 4, R-1302, R-1306, R-1307, R-1319 and R-1280, DECISION F307 D6, the plan
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f307-r5.md` | 115/0 | NEW FILE, this round's block, byte copy (115 lines, sha256 `6f86db451ac6e0ed4ad301cf01f8a0f6c119ba986500a326224faca8cac303e4`, equal to `block.md`) |
| `.agent/decisions.md` | 12/0 | prepared file, byte copy (DECISION F307 D6) |
| `.agent/live_review.md` | 12/0 | prepared file, byte copy (round 4's verdict and its five resolutions booked: R-1302, R-1306, R-1307, R-1319, R-1280) |
| `.agent/plan.md` | 7/7 | prepared file, byte copy |

### e607a8d72 F307 R5 C2: the home-path helper in a module of its own and four private names made public (R-1290)
| Path | +/- | Reason |
|---|---|---|
| `apps/cli/commands/job.py` | 2/2 | prepared file, byte copy (`list_projects_readonly` reader updated) |
| `apps/cli/commands/project.py` | 2/2 | prepared file, byte copy (`list_projects_readonly` reader updated) |
| `apps/cli/grouped.py` | 1/1 | prepared file, byte copy (`home_relative_text` import moved to `paths_text`) |
| `packages/orchestration/client_changes.py` | 2/2 | prepared file, byte copy (`list_projects_readonly` reader updated) |
| `packages/orchestration/client_digest.py` | 2/2 | prepared file, byte copy (`list_projects_readonly` reader updated) |
| `packages/orchestration/client_scope.py` | 2/2 | prepared file, byte copy (`list_projects_readonly` reader updated) |
| `packages/orchestration/crash_report.py` | 3/3 | prepared file, byte copy (`home_relative_text` import moved; `config_snapshot` reader updated) |
| `packages/orchestration/paths_text.py` | 17/0 | NEW FILE, prepared file, byte copy (`home_relative_text` moved here unchanged) |
| `packages/orchestration/project_registry.py` | 3/3 | prepared file, byte copy (`_list_projects_readonly` renamed to `list_projects_readonly` at definition and readers) |
| `packages/orchestration/project_scope.py` | 2/2 | prepared file, byte copy (`list_projects_readonly` reader updated) |
| `packages/orchestration/repository_snapshot.py` | 4/4 | prepared file, byte copy (`_SNAPSHOT_DIR_NAME` and `_check_snapshot_integrity` renamed public at definition and readers) |
| `packages/orchestration/run_manifest.py` | 2/2 | prepared file, byte copy (`_config_snapshot` renamed to `config_snapshot` at definition and readers) |
| `packages/orchestration/self_health.py` | 7/14 | prepared file, byte copy (`home_relative_text` moved out; renamed imports read `SNAPSHOT_DIR_NAME`, `check_snapshot_integrity`, `list_projects_readonly`) |
| `tests/cli/test_json_envelope.py` | 1/1 | prepared file, byte copy (`home_relative_text` import moved to `paths_text`) |
| `tests/orchestration/import_reachability_allowlist.txt` | 1/0 | prepared file, byte copy (`packages.orchestration.paths_text` added) |
| `tests/orchestration/test_crash_report.py` | 1/1 | prepared file, byte copy (`config_snapshot` reader updated) |
| `tests/orchestration/test_f146_package_pipeline_e2e.py` | 2/2 | prepared file, byte copy (`list_projects_readonly` reader updated) |
| `tests/orchestration/test_paths_text.py` | 15/0 | NEW FILE, prepared file, byte copy (the two `home_relative_text` tests, moved from `test_self_health.py`) |
| `tests/orchestration/test_project_resolution.py` | 3/3 | prepared file, byte copy (`list_projects_readonly` import and reader updated) |
| `tests/orchestration/test_self_health.py` | 0/9 | prepared file, byte copy (the two `home_relative_text` tests moved out to `test_paths_text.py`) |
| `tests/test_project_registry.py` | 3/3 | prepared file, byte copy (`list_projects_readonly` reader updated) |

### 2fc84e75d F307 R5 C3: doctor health reports an operations log it cannot write (R-1292)
| Path | +/- | Reason |
|---|---|---|
| `docs/system/self-health-v1.md` | 6/3 | prepared file, byte copy (the `logs` check documented, check count updated to ten) |
| `packages/orchestration/self_health.py` | 36/1 | prepared file, byte copy (the `logs` check added, run last in `run_health_checks`) |
| `tests/cli/test_doctor_health_cmd.py` | 3/3 | prepared file, byte copy (line-count and check-count pins updated from nine to ten) |
| `tests/orchestration/test_self_health.py` | 52/2 | prepared file, byte copy (four new tests for the `logs` check; the order test updated to ten checks) |
| `tests/ui_server/test_public_api.py` | 2/2 | prepared file, byte copy (check-count pins updated from nine to ten) |

### (this commit) F307 R5 C4: handback
| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | rewritten | this handback |

## Item status

| Item | Status | Reason |
|---|---|---|
| C0 | done | base confirmed: HEAD `0c0e290db` equal to `origin/feature/f307-findings-paydown-v9`, tree clean |
| C1 | done | records commit `ecd158b3b` |
| C2 | done | R-1290 refactor commit `e607a8d72` |
| C3 | done | R-1292 behaviour commit `2fc84e75d` |
| C4 | done | this handback commit |
| Gate 1 | done | `git status --porcelain` empty; `verify.py` printed `True` on every counted line, `absent C4` (not yet counted), last line `ALL True` |
| Gate 2 | done | `ruff check` over 22 files printed `All checks passed!`, exit 0 |
| Gate 3 | done | 86 paths, exit 0, `4046 passed, 2 skipped in 56.13s`, two SKIPPED lines, no FAILED, ERROR or `process(es) behind` line |
| Gate 4 | done | `fail_count` 0, all six checks pass |
| Gate 5 | done | open findings count printed `42` |
| Push | pending | runs after this commit; reported in the session reply |

## External actions

No push, PR or `gh` command before this commit; the push follows it and is reported in the session reply. No worktree of my own, no provider call, no rotation.

## Verification

1. Digests: a python check over the 35 lines of `digests.txt` — every prepared file's sha256 read `OK` (printed as per-file EQUAL after copy, plus a dedicated pre-check) against the listed digest, last line `ALL_OK`. `block.md` and `digests.txt` themselves were also hashed first and matched the values given in the delivering prompt.
2. C0: `git branch --show-current` read `feature/f307-findings-paydown-v9`; `git rev-parse HEAD` and `git rev-parse origin/feature/f307-findings-paydown-v9` both read `0c0e290db5cf2432bc3b7ff55a8a8221a76faa28`; `git status --porcelain` was empty before any write.
3. Gate 1: `git status --porcelain` (through `git -C`) — empty. `python3 .remedy-wt/f307-r5/prep/verify.py .` — every counted line `True` (single-parent checks on all three commits, the Cn-subject count 3 of 3, the branch check, every C1, C2 and C3 path-set and per-path equality check, and "the saved block equals block.md"); one line `absent C4` (not yet counted, C4 did not exist when the gate ran); last line `ALL True`.
4. Gate 2: `python3 .remedy-wt/f307-r5/prep/ruff_touched.py .`, run from the primary checkout — `ruff over 22 files: exit 0`, `All checks passed!`.
5. Gate 3: `python3 .remedy-wt/f307-r5/prep/run_selection.py . .remedy-wt/f307-r5-worker/selection-output.txt` — `paths 86`, `exit 0`, `4046 passed, 2 skipped in 56.13s`. SKIPPED lines: `tests/test_agent_tooling.py:43` (D12 quarantine, F252) and `tests/test_install_smoke.py:175` (install smoke is opt-in). No FAILED, no ERROR, no `process(es) behind` line.
6. Gate 4: `python3 -m apps.cli.main integrity check --json` exit 0 — `fail_count` 0; all six checks pass: `handler_import` ("handlers=194"), `live_review_verdict` ("last Gate verdict PASS"), `plan_consistency` ("unchecked=0, context_complete=False"), `relevant_untracked` ("untracked=0, relevant=0"), `repo_root_hygiene` ("no reviewer scratch, evidence dir or archive at the root"), `high_blockers_open` ("no open blocker/high findings").
7. Gate 5: `python3 -c "import scripts.rotate_live_review as r; print(len(r.open_finding_ids(open('.agent/live_review.md').read())))"` — `42`.

## Authored-text proofs

C1's four prepared files, C2's twenty-one prepared files and C3's five prepared files are byte copies of the prepared files; each was proved equal by a `filecmp.cmp` comparison right after the copy, before staging, and `verify.py` re-proved every one of them (`True`). `.agent/authored/f307-r5.md` equals `block.md`: 115 lines, sha256 `6f86db451ac6e0ed4ad301cf01f8a0f6c119ba986500a326224faca8cac303e4` on both sides.

## Deviations & assumptions

One disclosed deviation, with no effect on any gate's result: the C1 commit was created with `cd <repository root> && git commit -m "..."`, a shell shape the block's constraints ask this worker to avoid (`cd` joined to another command by `&&`); it ran without error and produced the correct commit. From C2 onward this worker switched to `git -C <repo> commit -F <message file>` to stay inside the named shapes; no other commit used the disallowed form.

No other deviation. The commit sequence, paths and gate commands followed the block exactly; no file outside the named paths per commit was touched; each gate ran exactly once; no mutation or full-suite run was attempted; `.data` was not read.

## For the operator, in plain sentences

This round booked the previous round's closing verdict and its five resolutions into the running record, and recorded a decision covering two further repairs. First, a small helper that turns a pasted path under the operator's home folder into a short, shareable form moved out of the health-check module into a module of its own, because two other parts of the program already relied on it being there; and four names that four different parts of the program had to reach around a leading underscore to use lost that underscore, both where they are defined and everywhere they are read. Second, the self-check command gained one more check: it now also confirms that Remedy can still write its own internal operations log, by writing and immediately removing a small probe file, and warns the operator by name if that folder or file cannot be written, since a log that silently stops recording would otherwise go unnoticed. All five required checks ran once each and came back exactly as expected. No question waits for the operator.

## Next

1. Phase 1 rule 1: check `.agent/STOP`.
2. Rule 2: the Open PR Gate.
3. Book round 5's verdict in the next round's first commit.
4. T010, the mission record: R-1285, R-1299, R-1300 and R-1311.

Operator questions open: 0. Open findings count gate 5 printed: 42.
