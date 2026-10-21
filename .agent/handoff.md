# Handback — F313 round 5

## Session

SESSION 1 of feature F313 · round 5 · rounds so far 5

Context self-assessment: this session verified every prepared file's digest before use, applied the prepared files as proved byte copies, and ran both long steps once through the launch and wait helpers while running nothing else; no stop condition was met.

Fortschritt: ~95 % (everything but the closing round is done) — Schätzung

## Range

Review of `3cfa11aee`..HEAD (C1, C2, then this commit C3, which carries this handback).

## Commits

### ac7bbe504 F313 R5 C1: book round 4, the plan
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f313-r5.md` | +113 (new) | byte copy of `block.md` (113 lines, sha256 f5aca36b906c0f731ce26779d91f791a6318959c7b9056f5311084e305be6b6d, equal to the prompt's) |
| `.agent/live_review.md` | +2 | base plus `src-ledger.md`, round 4's verdict |
| `.agent/plan.md` | +4/-5 | byte copy of `src-plan.md` |

### da2e6ebe8 F313 R5 C2: the evidence script
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f313-r5-create_f313_evidence.py` | +427 (new) | byte copy of the evidence script, alone |

### C3 (this commit)
| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | rewritten | this handback |

## External actions

- `git push -u origin feature/f313-contract-1-22` after C2: `3cfa11aee..da2e6ebe8`, accepted first time.
- `python3 .remedy-wt/f313-r5/prep/launch.py evidence .remedy-wt/f313-r5-worker` then `wait.py evidence ... 50`: `exit 0 wall 1430.4`.
- `python3 .remedy-wt/f313-r5/prep/launch.py zip .remedy-wt/f313-r5-worker` then `wait.py zip ... 50`: `exit 0 wall 14.4` (first attempt; no second attempt needed).
- The push of this commit follows it. No pull request created or merged.

## Verification

1. Gate 1 (after C2): `git status --porcelain` empty; `python3 .remedy-wt/f313-r5/prep/verify.py .` exit 0, every line `True`, `absent` for C3, last line `ALL True`.
2. Gate 2: A2 and A3 readings in "Evidence and package".
3. Gate 3 (after A3): `python3 -m apps.cli.main integrity check --json` exit 1, `fail_count` 1, the one failing check `high_blockers_open`: `12 open blocker/high: R-1335, R-1336, R-1337, R-1338, R-1345, R-1346, R-1348, R-1349, R-1359, R-1360, R-1361, R-1362`; `open_finding_ids` count printed `87` (R-1246 to R-1381); `git status --porcelain` empty.

## Authored-text proofs

Python byte equality against the prepared file, all `True`: `.agent/authored/f313-r5.md`, `.agent/plan.md`, the appended `.agent/live_review.md` (C1); `.agent/authored/f313-r5-create_f313_evidence.py` (C2). Digests of `block.md`, `verify.py`, `digests.txt` and of every listed prepared file matched before use.

## Evidence and package

Evidence job id: `f313r5e1001`. Reflog before the job: `da2e6ebe8 HEAD@{2026-10-21 05:13:26 +0200}: commit: F313 R5 C2: the evidence script`.

A2 lines verbatim:

```
exit 0 wall 1430.4
head da2e6ebe8e2d53f6f36f13527b259481fdf16029
ancestry-path count 18
plain count 18
collected node ids 9553, deselected 177
red control: unsafe among the real ids 0 []
red control: planted id -> a local absolute path
pytest exit 0, {'passed': 9547, 'failed': 0, 'skipped': 6}, output_hash 74ab3a8c41a3236df4035c5a7340f09c86367c7f6280b39bdcb4f92990ad3771
validate_verification_tests problems [] passed 9547
is_valid_current_run True
validation_errors []
"verdict": "PASS_WITH_RISKS", "commit_count": 18, "authority_count": 26, "total_passed": 9547
```

Package (from the build's own lines):

- `PACKAGE_STATUS=READY_FOR_REVIEW`, `REVIEW_SUBJECT_ALIGNMENT=PASS`, `EVIDENCE_AUTHORITATIVE=true`
- name: `remedy-review-20261021-053728-READY_FOR_REVIEW.zip`
- SHA-256 (Python over the file): `31eee0bfb465651bc3c04ca6c383fd230ba7c1d8ace53fcff3250a7d2fad4848`
- directory: `REVIEW_PACKAGE_DIR=~/Repos/remedy-history/zips`
- manifest `committed_review_subject`: base `25ab7c98bd5c8482c54a3b5d8405daec977fa6d3`, head `da2e6ebe8e2d53f6f36f13527b259481fdf16029`, commit_count 18, base_is_ancestor true
- `zipfile.is_zipfile` True, `testzip()` None; 1983 members

## Staging reclaim

Preview `data reclaim --orphans`: `Reclaimable: nothing`, `Would free 0 B in 0 paths — nothing deleted`; no candidate and no refused path (only the durable classes listed as not addressed). The apply was skipped, as the block orders for an empty preview.

## Deviations & assumptions

None. (The sandbox refused one command carrying an exit-code variable; it was re-run without it. Copies and checks ran as small scripts under `.remedy-wt/f313-r5-worker/`.)

## Next

1. Phase 1 rule 1: check `.agent/STOP`.
2. Phase 1 rule 2: the Open PR Gate; no pull request is open for this branch yet.
3. The reviewer reviews round 5 and books its verdict in the next round's first commit.
4. The closing round: the rotation or its recorded skip, SU-068's consumed_by, the STATUS flip with the README sync, and the pull request, left unmerged.

Operator questions open: 1. Open findings count gate 3 printed: 87 (rule: `open_finding_ids` over `.agent/live_review.md`).

## For the operator, in plain sentences

The evidence for this feature was collected and checked: the test collection of 9553 tests ran once on the code that will ship, 9547 passed, none failed and 6 were skipped, and the evidence checks all read valid. The review package was built and is ready for review as remedy-review-20261021-053728-READY_FOR_REVIEW.zip in the review-history folder under the repository's home directory; it is about 7.8 MB. The staging area had nothing to reclaim.
