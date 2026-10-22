# Handback — F307 round 31: book round 30 and R-1420, the evidence job and the review package

## Session

SESSION 7 of feature F307 · round 31 · rounds so far 31

Context self-assessment: this worker verified every prepared digest before any write, copied each prepared file by a script that proved equality over bytes, ran the evidence job and the package once each through the launcher and each gate once; context is ample and nothing was lost.

Fortschritt: ~99 % (everything but the closing round is done) — Schätzung

## Range

Review of `f3d693a87`..`HEAD` on `feature/f307-findings-paydown-v9`.

## Commits

### 5a9030360 F307 R31 C1: book round 30 and R-1420, the plan, the block
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f307-r31.md` | new | NEW FILE, this round's block, byte copy (115 lines, sha256 `4ada4e14242fe8d537c3dfe9e72ee3f34b9747409020ccb0922a121f2e4b4ebb`) |
| `.agent/live_review.md` | appended | prepared file copied (equals pre-image plus `append-live_review.txt`) |
| `.agent/plan.md` | rewritten | prepared file copied |

124 insertions, 8 deletions over 3 files (`git show --shortstat`).

### a100201f3 F307 R31 C2: the evidence script
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f307-r31-create_f307_evidence.py` | new | NEW FILE, byte copy of the prepared script |

293 insertions over 1 file (`git show --shortstat`).

### (this commit) F307 R31 C3: handback
| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | rewritten | this handback |

## Item status

| Item | Status | Reason |
|---|---|---|
| C1 | done | commit `5a9030360`, byte proofs held, ledger equals pre-image plus slice |
| C2 | done | commit `a100201f3`, byte proof held, pushed |
| A1 | done | preview read nothing reclaimable; apply skipped |
| A2 | done | exit 0, wall 1816.5 s, `PASS_WITH_RISKS` as the script's own verdict line |
| A3 | done | `READY_FOR_REVIEW`, exit 0, wall 62.1 s |
| C3 | done | this handback commit |
| Gate 1 | done | status empty; verify.py `ALL True` |
| Gate 2 | done | A2 exit 0 and A3 exit 0 from the launcher's exit files |
| Gate 3 | done | `fail_count` 0; open set of 6 ids as ordered; status empty |

## External actions

`git push -u origin feature/f307-findings-paydown-v9` after C2: `f3d693a87..a100201f3`, accepted on the first try. The push after this commit is reported in the session reply. No `gh` command, no pull request, no fetch or pull, no provider call. The scratch folder `.remedy-wt/f307-r31-worker/` holds the digest checker, the copy scripts, the commit messages, the launcher logs and exit files.

## Verification

1. Digests before any write: `block.md` (115 lines), `verify.py` and `digests.txt` equal the prompt's; every file `digests.txt` lists matched (checker run with `python3 -I`).
2. Preconditions: HEAD `f3d693a87` equal to `origin/feature/f307-findings-paydown-v9`, `git status --porcelain` empty, `.agent/STOP` absent. `git branch --show-current` read `feature/f307-findings-paydown-v9` before each of C1 to C3.
3. Gate 1: `git status --porcelain` empty; `verify.py` printed `True` on every line, `absent` for C3, last line `ALL True`.
4. Gate 2: see Evidence and package.
5. Gate 3: `python3 -m apps.cli.main integrity check --json` exit 0, `fail_count` 0 (six checks, all pass). `open_finding_ids` printed `['R-1246', 'R-1281', 'R-1326', 'R-1351', 'R-1353', 'R-1418']`. `git status --porcelain` empty.

## Authored-text proofs

Applied this round, each proved equal over bytes by a copy script right after writing and again by `verify.py` against the committed blobs: `.agent/authored/f307-r31.md`, `.agent/live_review.md`, `.agent/plan.md` (C1) and the evidence script (C2). `.agent/live_review.md` equals its pre-image followed by `append-live_review.txt`.

## Evidence and package

Evidence job id `f307r31e1001`. `git reflog -n 3` before the run: `a100201f3 HEAD@{2026-10-22 05:40:44 +0200}: commit: F307 R31 C2: the evidence script`, then C1, then `f3d693a87` (R30 C4). A2 printed, exit `exit 0 wall 1816.5`:

```
head a100201f3a40b1f07ac02abd470836c336e843f1
ancestry-path count 122
plain count 122
collected node ids 11507, deselected 251
red control: unsafe among the real ids 0 []
red control: planted id -> a local absolute path
pytest exit 0, {'passed': 11501, 'failed': 0, 'skipped': 6}, output_hash 52c6cbc2d78282fbbfd1e717ff529ba8ef62453df83aa3bf3aa8032e38741a31
validate_verification_tests problems [] passed 11501
is_valid_current_run True
validation_errors []
```

The script's JSON summary: `verdict` `PASS_WITH_RISKS`, `authority_count` 289, `commit_count` 122, `total_passed` 11501.

A3 (exit 0, wall 62.1 s): `PACKAGE_STATUS=READY_FOR_REVIEW`, `REVIEW_SUBJECT_ALIGNMENT=PASS`, `EVIDENCE_AUTHORITATIVE=true`. Package `remedy-review-20261022-061118-READY_FOR_REVIEW.zip`, SHA-256 `e49aa6fde92a4f6c69f5994c3a58e9b7734acef64713a9ee14d118db988dbfd8` (a Python sha256 over the file, equal to the tool's `final_sha256`), directory `~/Repos/remedy-history/zips`. `committed_review_subject` in `.review_zip_manifest.json` inside the package: base `eeed13064c44173c7565f6a8900d049b339176ab`, head `a100201f3a40b1f07ac02abd470836c336e843f1`, 122 commits. `zipfile.is_zipfile` True, `testzip()` None. The tool's closing lines: `Commit: a100201f3a40b1f07ac02abd470836c336e843f1`, `Included files: 2139`.

## Staging reclaim

`python3 -m apps.cli.main data reclaim --orphans` preview: `Reclaimable: nothing`, `Would free 0 B in 0 paths`; no refused path other than the durable classes the tool lists as not reclaimed. The apply was skipped as ordered; freed total 0 B.

## Deviations & assumptions

None. The commit sequence landed exactly as ordered (C1, C2, then this C3), each touching only its named paths. No amend, rebase, force-push or `--no-verify`, no pull request, `.data` never read by this worker, no second launch of any action, no suite run other than A2's evidence pytest.

## Next

1. Phase 1 rule 1: check `.agent/STOP`.
2. Rule 2: the Open PR Gate; no pull request is open for this branch yet.
3. The reviewer reviews round 31 and books its verdict in the next round's first commit.
4. The closing round: the Built State, the re-assigned findings, the rotation, the next findings paydown, SU-073's consumed_by, the STATUS flip with the README sync, and the pull request, left unmerged.

Operator questions open: 0. Open findings gate 3 printed: `['R-1246', 'R-1281', 'R-1326', 'R-1351', 'R-1353', 'R-1418']`.

## For the operator, in plain sentences

The evidence for this batch of repairs was collected and checked: the tests it covers all passed and nothing failed.

The review package was built and is ready for review; it sits in the history folder's zips directory under your home folder.
