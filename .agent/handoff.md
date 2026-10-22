# Handback — F307 round 27: book round 26 with R-1330; `doctor_core_report`'s step (1); R-1291, one doctor report shape

## Session

SESSION 6 of feature F307 · round 27 · rounds so far 27

Context self-assessment: this worker verified every prepared digest before any write, applied C1 by a byte-proof script, applied C2 and C3 by `git apply` from the reviewer's cut patches with no hand-retyping, read each staged diff in full against its patch before committing, and ran each gate once; context is ample and nothing was lost.

Fortschritt: ~96 % (T001 to T020, R-1280, R-1290, R-1292, R-1297, R-1298, R-1301, R-1330, R-1381, R-1403, R-1411, R-1414 to R-1417, R-1419 landed, R-1281's writer part landed, R-1291 under review · the rest open) — Schätzung

## Range

Review of `256b4d021`..`HEAD` on `feature/f307-findings-paydown-v9`.

## Commits

### f3d13d2e0 F307 R27 C1: book round 26 with R-1330, DECISION F307 D27, the plan
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f307-r27.md` | 85/0 | NEW FILE, this round's block, byte copy (85 lines, sha256 `dc29aa1e5b8ee6375ad09a9a71130f8ce1f88c7961a2cfc986bb6ec310d50647`, equal to `block.md`) |
| `.agent/decisions.md` | 12/0 | prepared slice appended (DECISION F307 D27) |
| `.agent/live_review.md` | 4/0 | prepared slice appended (round 26's Gate verdict PASS; R-1330 RESOLVED) |
| `.agent/plan.md` | 7/7 | replaced with the prepared file |

108 insertions, 7 deletions over 4 files (`git show --shortstat`).

### acf26b369 F307 R27 C2: the dead-model helpers of doctor core move to the module, structural step (1)
| Path | +/- | Reason |
|---|---|---|
| `apps/cli/commands/worker_facade_cmd.py` | 55/55 | `_dead_origin`, `_dead_provenance_short`, `_dead_provenance` moved unchanged from nested helpers to module level, taking the shipped entries as an argument (`doctor_core_report`'s boundary, step (1)) |
| `docs/system/structure-ledger-v1.md` | 3/1 | step (1) recorded done; `doctor_core_report` row lowered 355 → 305 |
| `tests/test_structure_ratchet.py` | 1/1 | `MAX_FUNCTION_LINES` lowered 28661 → 28611, the ratchet following the drop |

61 insertions, 57 deletions over 3 files (`git show --shortstat`); applied from `c2.patch` via `git apply --check --index` then `git apply --index`, never hand-retyped; the staged diff matched the patch exactly before commit.

### 46bfed19b F307 R27 C3: both doctor commands answer one check shape through one table and one scrubber (R-1291)
| Path | +/- | Reason |
|---|---|---|
| `apps/cli/commands/doctor_health_cmd.py` | 4/3 | `_cmd_doctor_health` prints through the shared `health_check_lines` |
| `apps/cli/commands/worker_facade_cmd.py` | 18/26 | `checks` now built as `HealthCheckResult.as_json()`; `_safe_err` deleted, replaced by `report_safe_text`; `blockers` read `level == HEALTH_FAIL`; `_cmd_doctor_core` prints through `health_check_lines` |
| `docs/system/self-health-v1.md` | 7/0 | documents `remedy doctor core`'s shared shape, table and scrubber (R-1291) |
| `docs/system/structure-ledger-v1.md` | 1/1 | `doctor_core_report` row lowered 305 → 295 |
| `packages/orchestration/paths_text.py` | 20/0 | `report_safe_text`, the one scrubber: home folders `~`, secret values `***`, a path under `/mnt/` or `/tmp/` named as it is |
| `packages/orchestration/self_health.py` | 13/4 | `health_check_lines` added (shared table renderer); `_result` now scrubs through `report_safe_text` |
| `tests/cli/test_worker_facade_cmd.py` | 28/9 | new test for the shared shape/table/scrubber; `ok`-key assertions become `level`-key; the `/mnt/`/`/tmp/` test renamed and reads the truthful (unscrubbed-to-home) behaviour |
| `tests/test_structure_ratchet.py` | 1/1 | `MAX_FUNCTION_LINES` lowered 28611 → 28601, the ratchet following the drop |

94 insertions, 42 deletions over 8 files (`git show --shortstat`); applied from `c3.patch` via `git apply --check --index` then `git apply --index`, never hand-retyped; the staged diff matched the patch exactly before commit.

### (this commit) F307 R27 C4: handback
| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | rewritten | this handback |

## Item status

| Item | Status | Reason |
|---|---|---|
| C0 | done | HEAD and `origin/feature/f307-findings-paydown-v9` both `256b4d0218a692711d8f039b03ea74a6133ad3ed`, tree clean, no pull run, no `.agent/STOP`, no open PR (`gh pr list` empty) |
| C1 | done | commit `f3d13d2e0`, 108 insertions/7 deletions, byte proofs all held |
| C2 | done | commit `acf26b369`, 61 insertions/57 deletions over 3 files, applied from `c2.patch` |
| C3 | done | commit `46bfed19b`, 94 insertions/42 deletions over 8 files, applied from `c3.patch` |
| C4 | done | this handback commit |
| Gate 1 | done | `git status --porcelain` empty |
| Gate 2 | done | `ruff over 6 files: exit 0`, `All checks passed!` |
| Gate 3 | done | `paths 89`, `exit 0`, `4396 passed, 2 skipped in 49.06s` |
| Gate 4 | done | `fail_count` 0, all six checks pass |
| Gate 5 | done | `7` |
| Gate 6 | done | `git diff --stat e39bbc988 HEAD -- packages apps scripts tests docs` empty |
| Push | pending | runs after this commit; reported in the session reply |

## External actions

`gh pr list --state open --json number,headRefName,baseRefName,isDraft` — `[]`, no open PR (Open PR Gate passed, no merge needed). Push follows this commit and is reported in the session reply. `.remedy-wt/f307-r27-worker/` (created this round) holds the digest-verification script, the C1 byte-proof script, the gate-4 integrity script, the two commit-message files for C1/C2/C3, and the selection output.

## Verification

1. Digests, before any write: `digests.txt` sha256 `75dd08ee385af7d687a10224c5d7dd3b7dd518da66f097d8843337a2368e7f57` and `block.md` sha256 `dc29aa1e5b8ee6375ad09a9a71130f8ce1f88c7961a2cfc986bb6ec310d50647` (85 lines) both equal the delivering prompt; the seven other listed entries (`c1-.agent__plan.md`, `c1-decisions-append.txt`, `c1-live_review-append.txt`, `c2.patch`, `c3.patch`, `ruff_touched.py`, `run_selection.py`, `selection.txt`) matched (by a python3 script, since `digests.txt` is tab-separated).
2. C0: branch `feature/f307-findings-paydown-v9`; HEAD equals `origin/feature/f307-findings-paydown-v9` at `256b4d0218a692711d8f039b03ea74a6133ad3ed`; tree clean; `gh pr list --state open ...` returned `[]`.
3. Gate 1: `git -C <root> status --porcelain` — empty (read after C3, before C4).
4. Gate 2: `python3 .remedy-wt/f307-r27/prep/ruff_touched.py <root>` — `files:` lists 6 Python files changed since the base, `ruff over 6 files: exit 0`, `All checks passed!`.
5. Gate 3: `python3 .remedy-wt/f307-r27/prep/run_selection.py <root> .remedy-wt/f307-r27-worker/selection-output.txt` — `paths 89`, `exit 0`, `4396 passed, 2 skipped in 49.06s`. SKIPPED: `tests/test_agent_tooling.py:43` (D12 quarantine, F252), `tests/test_install_smoke.py:175` (opt-in, `REMEDY_INSTALL_SMOKE=1`). No FAILED, ERROR, `process(es) behind`, `R-1411:` or `R-0803:` line.
6. Gate 4: `python3 -m apps.cli.main integrity check --json` via a python3 script with `cwd=<root>` — exit 0, `fail_count` 0; `handler_import`, `live_review_verdict`, `plan_consistency`, `relevant_untracked`, `repo_root_hygiene`, `high_blockers_open` all pass.
7. Gate 5: `python3 .remedy-wt/f307-r10/open_count.py <root>` — `7`.
8. Gate 6: `git -C <root> diff --stat e39bbc988 HEAD -- packages apps scripts tests docs` — empty output, confirming the committed product bytes equal the reviewer's dry run.

## Authored-text proofs

`.agent/authored/f307-r27.md` equals `block.md`: 85 lines, sha256 `dc29aa1e5b8ee6375ad09a9a71130f8ce1f88c7961a2cfc986bb6ec310d50647` on both sides. The `.agent/live_review.md` and `.agent/decisions.md` appends (each equal to pre-image plus slice) and the `.agent/plan.md` replacement were each proved byte for byte by one script right after writing, in the same run that applied them. C2 and C3 were the reviewer's cut patches (`c2.patch`, `c3.patch`) applied with `git apply --check --index` then `git apply --index`, never retyped; each staged diff was read in full before its commit and matched its patch exactly, with no file added or changed outside the patch.

## Deviations & assumptions

None. The commit sequence landed exactly as ordered (C1 to C3), each touching only its named paths. No mutation red-proof, no full suite outside the selection, `REMEDY_TEST_MAX_WORKERS` never set, `.data` never read, no amend, rebase, force-push or `--no-verify`, no PR; each gate ran once and never concurrently.

## For the operator, in plain sentences

Remedy's two health commands now report in the same way and print the same kind of list, and a temporary folder in an error message is shown where it really is; private folders and secret values stay hidden in both.

## Next

1. Phase 1 rule 1: check `.agent/STOP`.
2. Rule 2: the Open PR Gate.
3. Review round 27's handback and book its verdict, with R-1291, in the next round's first commit.
4. R-1326, the `[roles]` table, or its carry.

Operator questions open: 0. Open findings count gate 5 printed: 7.
