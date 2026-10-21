# Handback — F303 round 8: book round 7, R-1411, DECISION F303 D6, the evidence job with its own data root, the review package

## Session

SESSION 2 of feature F303 · round 8 · rounds so far 8

Context self-assessment: this worker verified every prepared digest, byte-copied the prepared files, ran each long command once through the launch and wait helpers and wrote this handback from what it read; context is ample and nothing was lost.

Fortschritt: ~97 % (everything but the closing round is done) — Schätzung

## Range

Review of `1c25b5e8d`..`HEAD` on `feature/f303-face-public-api`.

## Commits

### 289968b65 F303 R8 C1: book round 7, register R-1411, DECISION F303 D6, the plan and the block
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f303-r8.md` | 123/0 | NEW FILE, this round's block, byte copy (123 lines, sha256 `1f763c3e50ab3e94e451b3223bfa112b3fef4cc6884f890b2ff4f0594dcb8ac4`, equal to `block.md`) |
| `.agent/live_review.md` | 4/0 | prepared file, byte copy |
| `.agent/decisions.md` | 10/0 | prepared file, byte copy |
| `.agent/plan.md` | 5/5 | prepared file, byte copy |

### 5727408e0 F303 R8 C2: the evidence script with a data root of its own (DECISION F303 D6)
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f303-r8-create_f303_evidence.py` | NEW FILE | prepared file, byte copy (24304 bytes) |

### (this commit) F303 R8 C3: handback
| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | rewritten | this handback |

## External actions

- `git push -u origin feature/f303-face-public-api` after C2: `1c25b5e8d..5727408e0`, no HTTP error, first try.
- `git push origin feature/f303-face-public-api` follows this commit; its outcome is in the session reply.
- No pull request, no merge, no `gh` command, no worktree of my own, no provider call.

## Verification

Preconditions: the ten prepared digests matched; `HEAD` was `1c25b5e8d`, equal to `origin/feature/f303-face-public-api`, the tree was clean, `.agent/STOP` absent.

1. Gate 1: after C2 `git status --porcelain` empty; `python3 .remedy-wt/f303-r8/prep/verify.py .` — every line `True`, `absent` for C3, last line `ALL True`.
2. A1: `python3 -m apps.cli.main data reclaim --orphans` — `Reclaimable: nothing`, `Would free 0 B in 0 paths`; no refused path (only durable classes listed as not reclaimed). Apply skipped.
3. A2: `git reflog -n 3 --date=iso` before: C2 at 18:37:43, C1 at 18:37:40, `1c25b5e8d` at 18:33:41. `launch.py evidence` then `wait.py evidence ... 50`: `.exit` file reads `exit 0 wall 1373.8`. Verbatim:

```
head 5727408e0926857a7f24363015c1ea96da6dc1a7
ancestry-path count 36
first-parent count 36
data root for the run: .remedy-wt/f303-r8-evidence-data (fresh, empty)
collected node ids 11122, deselected 203
red control: unsafe among the real ids 0 []
red control: planted id -> a local absolute path
guard lines []
pytest exit 0, {'passed': 11116, 'failed': 0, 'skipped': 6}, output_hash ea0fc00ffa5be411bda07b0ef827c494b8b3bf9c598c8d939652f6e2a7ef8750
validate_verification_tests problems [] passed 11116
is_valid_current_run True
validation_errors []
```

   Summary: job_id `f303r8e1001`, head_commit `5727408e0926857a7f24363015c1ea96da6dc1a7`, authority_count 42, commit_count 36, verdict `PASS_WITH_RISKS`, manual_completion true, total_passed 11116.
4. A3: `launch.py zip` then `wait.py zip ... 50`: `.exit` file reads `exit 0 wall 14.1`. `REVIEW_PACKAGE_CREATED=true`, `PACKAGE_STATUS=READY_FOR_REVIEW`, `REVIEW_SUBJECT_ALIGNMENT=PASS`, `EVIDENCE_AUTHORITATIVE=true`, 2038 files, 8.1M. No second attempt was needed.
5. Gate 3: `python3 -m apps.cli.main integrity check --json` exit 1 — `fail_count` 1, the one failing check `high_blockers_open`: "12 open blocker/high: R-1335, R-1336, R-1337, R-1338, R-1345, R-1346, R-1348, R-1349, R-1359, R-1360, R-1361, R-1362", the other five pass. `open_finding_ids` over `.agent/live_review.md` prints `88` (round 7's 87 and R-1411). `git status --porcelain` empty.

## Authored-text proofs

C1's four files and C2's file are byte copies of the prepared files; each was proved equal by a Python equality over bytes right after the copy and `verify.py` re-proved them (`True`). `.agent/authored/f303-r8.md` equals `block.md` (123 lines, sha256 above).

## Staging reclaim

A1 previewed nothing to reclaim: `Reclaimable: nothing`, 0 B in 0 paths, no refused path. The apply was not run.

## Evidence and package

Evidence job id `f303r8e1001`: `head 5727408e0926857a7f24363015c1ea96da6dc1a7`; `data root for the run: .remedy-wt/f303-r8-evidence-data (fresh, empty)`; `pytest exit 0, {'passed': 11116, 'failed': 0, 'skipped': 6}`; `is_valid_current_run True`; `validation_errors []`; exit 0.

Review package: name `remedy-review-20261021-190053-READY_FOR_REVIEW.zip`; SHA-256 `ceeee0c17538832f84c67beafeca5d53861c71a3713205efb27878d46e47d362` (Python sha256 over the file; the builder's `final_sha256` agrees); directory `~/Repos/remedy-history/zips`; `PACKAGE_STATUS=READY_FOR_REVIEW`; accepted head `5727408e0926857a7f24363015c1ea96da6dc1a7` and base `2621bbe2ebf62c394750fee8b06cbdfd357d7f77` from `committed_review_subject` in `.review_zip_manifest.json` inside the package (commit_count 36, base_is_ancestor true); `zipfile.is_zipfile` True, `testzip()` None.

## Deviations & assumptions

None.

## For the operator, in plain sentences

The evidence of this feature was collected and checked: every test ran, none failed, and the checks on the result all came out as expected. It had to be collected twice because a background program of your own wrote into the data folder that a safety check watches, while the check was watching; this time the run used a data folder of its own. The review package was built and is ready for review, in the history folder under your home directory, in its zips subfolder, named remedy-review-20261021-190053-READY_FOR_REVIEW.zip.

## Next

1. Phase 1 rule 1: `.agent/STOP` is absent.
2. Phase 1 rule 2: no pull request is open for this branch yet.
3. The reviewer reviews round 8 and books its verdict in the next round's first commit.
4. The closing round: the rotation or its recorded skip, SU-072's consumed_by, the STATUS flip with the README sync, and the pull request, left unmerged.

Operator questions open: 0. Open findings count gate 3 reads: 88 (`scripts.rotate_live_review.open_finding_ids` over `.agent/live_review.md`, at the commit before this handback, `5727408e0`).
