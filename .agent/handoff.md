# Handback — F141 round 10: book round 9, the evidence job and the review package

## Session

SESSION 2 of feature F141 · round 10 · rounds so far 10

Context self-assessment: this worker verified every prepared digest, made C1 and C2 by byte copy, ran the staging reclaim preview, the evidence job and the package build each once, and wrote this handback with ample context margin left.

Fortschritt: ~97 % (everything but the closing round is done) — Schätzung

## Range

Review of `f2ced46d9`..`HEAD` on `feature/f141-permission-matrix` (base: round 9's handback).

## Commits

### 605f5a1de F141 R10 C1: book round 9, resolve R-1402, the plan and the block
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f141-r10.md` | new | this round's block, byte-saved for the authored-text proof |
| `.agent/live_review.md` | edited | round 9 booked, R-1402 resolved |
| `.agent/plan.md` | edited | re-headed for round 10 |

### 23e8f8244 F141 R10 C2: the evidence script
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f141-r10-create_f141_evidence.py` | new | the evidence script with job id `f141r10e1001`, a byte copy of the prepared file |

C3 (this handback commit) is not tabled: the self-reference exception applies. It touches `.agent/handoff.md` only.

## External actions

- `git push origin feature/f141-permission-matrix` after C2: `f2ced46d9..23e8f8244`, accepted on the first try.
- `git push origin feature/f141-permission-matrix` after C3 follows this commit; its outcome is reported in the session reply.
- No pull request was opened or merged. No worktree was added or removed.

## Verification

Preconditions: `block.md` (117 lines, sha256 `fc17e007...cacc2c`), `verify.py` and `digests.txt` matched the prompt's sha256; every file `digests.txt` listed matched. Start state: HEAD `f2ced46d9` equal to origin, `git status --porcelain` empty, no `.agent/STOP`.

1. Gate 1 (after C2): `git status --porcelain` empty; `python3 .remedy-wt/f141-r10/prep/verify.py .` — every line `True`, C3 `absent`, last line `ALL True`.
2. A1: `python3 -m apps.cli.main data reclaim --orphans` — `Reclaimable: nothing`, `Would free 0 B in 0 paths`; no refused path listed (the durable classes are listed as not reclaimed). The apply was skipped, as the block orders for an empty preview.
3. A2 (reflog before: `23e8f8244 HEAD@{2026-10-21 12:52:58 +0200}: commit: F141 R10 C2: the evidence script`): exit 0, wall 1388.2 s.
4. A3: exit 0, wall 21.6 s, see below.
5. Gate 3: `python3 -m apps.cli.main integrity check --json` — `fail_count` 1, only `high_blockers_open`: `12 open blocker/high: R-1335, R-1336, R-1337, R-1338, R-1345, R-1346, R-1348, R-1349, R-1359, R-1360, R-1361, R-1362`; the open-findings command printed `88`; `git status --porcelain` empty.

## Authored-text proofs

C1: the three prepared `c1-` files are byte copies, proven equal by a Python bytes comparison at copy time and again by `verify.py` (all `True`). C2: the prepared script is a byte copy, proven the same way. C3: none applied.

## Evidence and package

Evidence job id: `f141r10e1001`. A2's lines:

```
head 23e8f8244bc15db7df28c0b1f28086c289a46fcb
ancestry-path count 45
first-parent count 45
collected node ids 10831, deselected 182
red control: unsafe among the real ids 0 []
red control: planted id -> a local absolute path
pytest exit 0, {'passed': 10825, 'failed': 0, 'skipped': 6}, output_hash d25ed90981293e8dd4847a1e416a9bac8cd790ebc5a8e4a1603cc8e93215c8cc
validate_verification_tests problems [] passed 10825
is_valid_current_run True
validation_errors []
```

The job's closing report: `"verdict": "PASS_WITH_RISKS"`, `"authority_count": 42`, `"commit_count": 45`, `"total_passed": 10825`.

Package (A3), each quoting the tool's line:

- `PACKAGE_STATUS=READY_FOR_REVIEW`, `REVIEW_SUBJECT_ALIGNMENT=PASS`, `EVIDENCE_AUTHORITATIVE=true`
- name: `remedy-review-20261021-131628-READY_FOR_REVIEW.zip`
- SHA-256 (Python sha256 over the file; equals `final_sha256`): `c8f302dbefe31863d6d3509858eb3d6fff2abe56c0648b3d78b03cd005611d26`
- directory: `REVIEW_PACKAGE_DIR=~/Repos/remedy-history/zips`
- accepted head: `Commit: 23e8f8244bc15db7df28c0b1f28086c289a46fcb`; manifest `committed_review_subject` base `43e4705604bd33707db741bd1d5ec9679fc9df89`, head `23e8f8244bc15db7df28c0b1f28086c289a46fcb`, `base_is_ancestor` true, `commit_count` 45
- `zipfile.is_zipfile` True, `testzip()` None, `member_count` 2026

## Staging reclaim

Preview: `Reclaimable: nothing`; `Would free 0 B in 0 paths — nothing deleted`. Nothing was refused; the apply was not run (empty reading).

## Deviations & assumptions

None.

## Next

1. Phase 1 rule 1: `.agent/STOP`.
2. Phase 1 rule 2: the Open PR Gate; no pull request is open for this branch yet.
3. The reviewer reviews round 10 and books its verdict in the next round's first commit.
4. The closing round: the Built State, the rotation or its recorded skip, SU-070's consumed_by, the STATUS flip with the README sync, and the pull request, left unmerged.

Operator questions open: 3.
Open findings: 88, read by gate 3's second command (`scripts.rotate_live_review.open_finding_ids` over `.agent/live_review.md`) at commit `23e8f8244` (R-1402 resolved in C1 `605f5a1de`; round 9's 89 less one).

## For the operator, in plain sentences

The evidence for this feature was collected and checked: the test evidence run passed with no failures and the evidence validated as a current, valid run. The review package was built, is marked ready for review, and sits in the review packages folder in the history directory next to the repository.

## Item status

| Item | Status | Reason |
|---|---|---|
| C1 | done | `605f5a1de` |
| C2 | done | `23e8f8244` |
| A1 | done | preview empty, apply skipped as ordered |
| A2 | done | exit 0, every expected line read |
| A3 | done | `READY_FOR_REVIEW`, alignment `PASS`, evidence authoritative |
| C3 | done | this commit |
| Gate 1 | done | `ALL True` |
| Gate 2 | done | A2's and A3's readings as above |
| Gate 3 | done | `fail_count` 1 (`high_blockers_open`, twelve findings); open findings `88`; tree clean |
