# Handback — F060 round 6: the evidence job and the review package

## Session

SESSION 1 of feature F060 · round 6 · rounds so far 6

Context self-assessment: this worker verified every prepared digest, copied C1 and C2 by byte copy, ran the evidence job and the package build through the launcher once each, and wrote this handback with ample context margin left.

Fortschritt: ~97 % (everything but the closing round is done) — Schätzung

## Range

Review of `55e7873d7`..`HEAD` on `feature/f060-long-run-certificate`.

## Commits

### ffa5c1cad F060 R6 C1: book round 5, resolve R-1406, the plan and the block
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f060-r6.md` | 118/0 | this round's block, byte-saved (118 lines, sha256 `88dd8878e11fe0ecbab846c1056f3715811ef57e7fb8df25d5721a7e05a8ae3e`, equal to `block.md`) |
| `.agent/live_review.md` | 4/0 | round 5 booked, R-1406 resolved (prepared file, byte copy) |
| `.agent/plan.md` | 5/7 | rewritten (prepared file, byte copy) |

### c9b3cbc4b F060 R6 C2: the evidence script
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f060-r6-create_f060_evidence.py` | 452/0 | the evidence script, prepared file, byte copy |

### C3 F060 R6 C3: handback (this commit)
| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | edited | this handback |

## External actions

- `git push -u origin feature/f060-long-run-certificate` after C2: `55e7873d7..c9b3cbc4b`, no retry needed.
- `git push origin feature/f060-long-run-certificate` follows this commit; its outcome is reported in the session reply.
- No pull request was opened. No worktree was added or removed. No provider call.

## Verification

Preconditions: `block.md` (118 lines), `verify.py`, `launch.py`, `wait.py`, `digests.txt` matched the digests in the prompt; the four `c1-`/`c2-` files matched `digests.txt`. Before the first write `HEAD` read `55e7873d7`, equal to `origin/feature/f060-long-run-certificate`, the tree was clean and `.agent/STOP` absent.

1. Gate 1: after C2 `git status --porcelain` empty; `python3 .remedy-wt/f060-r6/prep/verify.py .` — every line `True`, C3 `absent`, last line `ALL True`.
2. Gate 2: A2 and A3 readings below, as ordered.
3. Gate 3: `python3 -m apps.cli.main integrity check --json` — exit 1, `fail_count` 1, only `high_blockers_open`: `12 open blocker/high: R-1335, R-1336, R-1337, R-1338, R-1345, R-1346, R-1348, R-1349, R-1359, R-1360, R-1361, R-1362`; `open_finding_ids` over `.agent/live_review.md` — `88`; `git status --porcelain` empty.

## Authored-text proofs

C1 (three paths) and C2: the prepared files are byte copies, proven equal over bytes at copy time and again by `verify.py` (every `equals` line `True`).

## Evidence and package

Evidence job id: `f060r6e1001`. `git reflog -n 3 --date=iso` before the job: `c9b3cbc4b` C2, `ffa5c1cad` C1, `55e7873d7` R5 C7 (the job did not move HEAD).

A2, quoted from the log (exit line `exit 0 wall 1503.3`):

```
head c9b3cbc4b82312d9c3c2b5180ced6dbb45673a08
ancestry-path count 28
first-parent count 28
collected node ids 10975, deselected 182
red control: unsafe among the real ids 0 []
red control: planted id -> a local absolute path
pytest exit 0, {'passed': 10969, 'failed': 0, 'skipped': 6}, output_hash a90df590dc89bf793c441db472cd8e97ceb4ba4af1a25d4c5ea432b95515cbdb
validate_verification_tests problems [] passed 10969
is_valid_current_run True
validation_errors []
```

Summary JSON: `verdict` PASS_WITH_RISKS, `authority_count` 23, `commit_count` 28, `manual_completion` true, `total_passed` 10969.

A3, quoted from the package build (exit line `exit 0 wall 15.5`):

```
PACKAGE_STATUS=READY_FOR_REVIEW
REVIEW_SUBJECT_ALIGNMENT=PASS
EVIDENCE_AUTHORITATIVE=true
REVIEW_PACKAGE_DIR=~/Repos/remedy-history/zips
ZIP_PATH=~/Repos/remedy-history/zips/remedy-review-20261021-150936-READY_FOR_REVIEW.zip
```

- Package name: `remedy-review-20261021-150936-READY_FOR_REVIEW.zip`; directory `~/Repos/remedy-history/zips`.
- SHA-256 (Python over the file): `97f5c525bc0d5a06a9935df49fbc999ea26913d8789c047561ac86aff4569cec`.
- `.review_zip_manifest.json` inside the package, `committed_review_subject`: base `646c4b1d7aebe171d9e8a14ea235161c192b286c`, head `c9b3cbc4b82312d9c3c2b5180ced6dbb45673a08` (C2), `commit_count` 28, `base_is_ancestor` true.
- `zipfile.is_zipfile` True; `testzip()` None. The first build attempt in the default directory succeeded; no second attempt was needed.

## Staging reclaim

A1 preview (`data reclaim --orphans`): `Reclaimable: nothing`; `Would free 0 B in 0 paths`; no candidate and no refused path (the listed classes are all durable and not addressed by reclaim). The apply step was skipped as ordered; the empty reading is recorded.

## Deviations & assumptions

None.

## Next

In order: Phase 1 rule 1 (`.agent/STOP`); rule 2 (Open PR Gate; no pull request is open for this branch yet); the reviewer reviews round 6 and books its verdict in the next round's first commit; the closing round: the Built State's closure facts, the rotation or its recorded skip, SU-071's consumed_by, the STATUS flip with the README sync, and the pull request, left unmerged.

Operator questions open: 3
Open findings: 88 (gate 3: `open_finding_ids` over `.agent/live_review.md`, at commit `c9b3cbc4b`; the integrity check names only the twelve findings of DECISION F310 D7)

## For the operator, in plain sentences

The evidence for this feature was collected and checked: the test run behind it passed in full, with none failing, and the checks on that evidence came back clean. The review package was built, it is marked ready for review, and it sits in the review folder under your home directory, in the zips folder of the history repository.
