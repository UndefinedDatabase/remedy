# Handback — F312 round 6 (closure's evidence round)

## Session

SESSION 1 of feature F312 · round 6 · rounds so far 6

Context self-assessment: this session verified all seven prepared-file digests with a Python
sha256 reader before using any of them, executed C1 exactly as the block ordered, ran A1 to A3
with no deviation, and all three gates passed on the first run.

State block:
Feature F312 (`[~]` in STATUS since round 1's C1), branch `feature/f312-scope-kinds`, base
`b74b07336` (round 5's handback, reviewed PASS). Head: this commit (C2), after C1.
Fortschritt: ~95 % (everything but the closing round is done) — Schätzung

## Range

Review of `b74b07336`..HEAD (C1 below, then this commit, C2, which also carries this handback).

## Commits

### a667ae7c4 F312 R6 C1: book round 5, register R-1381, the plan, the evidence script
518 insertions, 5 deletions.
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f312-r6.md` | +113 (new file) | byte copy of `block.md` |
| `.agent/authored/f312-r6-create_f312_evidence.py` | +397 (new file) | byte copy of the reviewer-authored evidence script |
| `.agent/plan.md` | +4/-5 | byte copy of the prepared plan |
| `.agent/live_review.md` | +4 | byte append: round 5's `Gate:` entry and R-1381 (self-use run's two defects, owned by F307) |

### this commit (C2) F312 R6 C2: handback
1 file.
| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | rewritten | this file (a handoff cannot table its own commit) |

## External actions

`gh pr list --state open --json number,headRefName,baseRefName,isDraft` before C1: `[]`, no open
PR — the Open PR Gate passes trivially. No other `gh` command this round. No worktree add/remove
of my own. Push after C1: `git push -u origin feature/f312-scope-kinds` →
`b74b07336..a667ae7c4  feature/f312-scope-kinds -> feature/f312-scope-kinds`, succeeded on the
first attempt, no HTTP 500, no retry needed. The push after this commit is run after C2, so its
outcome is reported in the final reply only.

## Verification

Gates run once each, after C1/A3 and before this commit.

1. After C1: `git status --porcelain` → empty (no output).
   `python3 .remedy-wt/f312-r6/prep/verify.py .`:
   ```
   True	a667ae7c4 single parent equal to the commit before it
   True	every commit carries an F312 R6 Cn subject: 1 of 1
   True	C1 paths exactly ['.agent/authored/f312-r6-create_f312_evidence.py', '.agent/authored/f312-r6.md', '.agent/live_review.md', '.agent/plan.md']: [same]
   absent	C2
   True	C1 .agent/authored/f312-r6.md equals block.md
   True	C1 .agent/authored/f312-r6-create_f312_evidence.py equals create_f312_evidence.py
   True	C1 .agent/plan.md equals dry-plan.md
   True	C1 the ledger is the base plus src-ledger.md
   ALL True
   ```
2. A2 (the evidence job), via `launch.py evidence` then `wait.py evidence … 50`, ended on the first
   wait call:
   ```
   exit 0 wall 1298.9
   head a667ae7c44fad44d84224d946b325d2fd168859e
   ancestry-path count 26
   plain count 26
   collected node ids 9070, deselected 170
   red control: unsafe among the real ids 0 []
   red control: planted id -> a local absolute path
   pytest exit 0, {'passed': 9064, 'failed': 0, 'skipped': 6}, output_hash 4017dfe3f1ee1f86071f63629632169af2b985829659c99f48672b49e5ab5844
   validate_verification_tests problems [] passed 9064
   is_valid_current_run True
   validation_errors []
   ```
   `head` equals C1's full sha; both ancestry counts equal (26 = 26); collected node ids 9070 with
   deselected 170, matching the reviewer's collect-only precheck at `b74b07336` exactly; red
   control unsafe count 0, planted id read as "a local absolute path"; pytest exit 0 with failed 0;
   `validate_verification_tests` problems `[]`; `is_valid_current_run` True; `validation_errors`
   `[]`; job exit 0.
3. A3 (the review package), via `launch.py zip` then `wait.py zip … 50`, ended on the first wait
   call, exit 0, wall 15.1s:
   - `PACKAGE_STATUS=READY_FOR_REVIEW`
   - `REVIEW_SUBJECT_ALIGNMENT=PASS`
   - `EVIDENCE_AUTHORITATIVE=true`
   - package file name: `remedy-review-20261021-011120-READY_FOR_REVIEW.zip`
   - SHA-256 (tool's own reading): `6794d8c3eea4f31999f98681d9a1b080fd8b48ce427fcc101fbcff54fddcf3ac`;
     re-computed independently with a Python `hashlib.sha256` reader over the file: same digest.
   - `committed_review_subject` inside `.review_zip_manifest.json`: base
     `0eda402feab1a4f5a883f825425e22d0f8d243da`, head `a667ae7c44fad44d84224d946b325d2fd168859e`
     (C1's full sha).
   - `zipfile.is_zipfile(...)` → `True`; `testzip()` → `None`.
   - directory: `~/Repos/remedy-history/zips`.
   - No sandbox refusal; the fallback second-location attempt was not needed.
4. After A3, before this commit: `python3 -m apps.cli.main integrity check --json` →
   `fail_count` 1, the one failing check `high_blockers_open` naming the same thirteen ids as
   DECISION F310 D7: `R-1335, R-1336, R-1337, R-1338, R-1345, R-1346, R-1348, R-1349, R-1359,
   R-1360, R-1361, R-1362, R-1369`. Then
   `python3 -c "import scripts.rotate_live_review as r; print(len(r.open_finding_ids(open('.agent/live_review.md').read())))"`
   → `88` (round 5's base of 87, plus the one newly registered R-1381). `git status --porcelain` →
   empty.

## Authored-text proofs

C1's three byte copies (`.agent/authored/f312-r6.md` ← `block.md`;
`.agent/authored/f312-r6-create_f312_evidence.py` ← `create_f312_evidence.py`; `.agent/plan.md` ←
`dry-plan.md`) and the one byte append (`.agent/live_review.md` ← `src-ledger.md`) were each
proved equal by a Python bytes-equality script before the commit
(`.remedy-wt/f312-r6-worker/c1_apply.py`, `ALL True`), and `verify.py`'s "C1" lines above confirm
it again. All seven prepared-file digests named in the block (`block.md`, `verify.py`,
`create_f312_evidence.py`, `dry-plan.md`, `src-ledger.md`, `launch.py`, `wait.py`) matched before
any file was used.

## Evidence and package

- Evidence job id: `f312r6e1001` (A2's `create_manual_completion_bundle` summary names it; also
  printed as `"job_id": "f312r6e1001"` in A2's JSON summary line).
- A2's lines: quoted verbatim in `## Verification` item 2 above.
- Package name: `remedy-review-20261021-011120-READY_FOR_REVIEW.zip` (A3's own
  `ZIP_PATH=~/Repos/remedy-history/zips/remedy-review-20261021-011120-READY_FOR_REVIEW.zip` line,
  rewritten with this machine's home folder as `~`).
- SHA-256: `6794d8c3eea4f31999f98681d9a1b080fd8b48ce427fcc101fbcff54fddcf3ac` (A3's own
  `"final_sha256": "6794d8c3eea4f31999f98681d9a1b080fd8b48ce427fcc101fbcff54fddcf3ac"` line,
  confirmed by an independent Python sha256 read over the file).
- Directory: `~/Repos/remedy-history/zips` (A3's own `REVIEW_PACKAGE_DIR=~/Repos/remedy-history/zips`
  line, rewritten with this machine's home folder as `~`).
- Accepted head: `a667ae7c44fad44d84224d946b325d2fd168859e` (A3's own `Commit:
  a667ae7c44fad44d84224d946b325d2fd168859e` line, which is C1's full sha).

## Staging reclaim

`python3 -m apps.cli.main data reclaim --orphans` (preview, run once): "Reclaimable: nothing";
every listed class (`api`, `control`, `crash`, `evidence_exports`, `job_apply_records`,
`job_evidence_index`, `job_logs`, `jobs`, `logs`, `memory`, `missions`, `projects`,
`review_reports`, `roadmap`, `runs`, `serve`) read "durable" — none refused as a candidate because
none was a candidate; previewed total "Would free 0 B in 0 paths". No candidate was listed, so the
`--apply` run was skipped per the block's instruction, and this empty reading is the recorded one.

## Deviations & assumptions

None. C1 was not amended and landed on its first attempt; `create_f312_evidence.py`, `launch.py`
and `wait.py` were run unedited, as ordered. A1's preview listed no reclaim candidate, so the
`--apply` step was skipped exactly as the block anticipates for that outcome — not a deviation.
A2 and A3 each completed on their first `wait.py` call, so no re-run of `wait.py` was needed beyond
the one call per action; the block's "re-run wait.py until it prints its exit line" clause did not
need to be exercised more than once per action. The A3 fallback (second evidence/zip directory
attempt) was not needed because the first attempt was not refused.

## For the operator, in plain sentences

The evidence of this feature was collected and checked: a fresh evidence job ran the feature's
full declared test set with no unsafe test-id leakage and no failures, and every automated check
on that evidence passed. The review package was built on the first attempt and is ready for
review; it is sitting in this machine's `~/Repos/remedy-history/zips` folder.

## Next

In order: Phase 1 rule 1 (`.agent/STOP`) — absent, no action needed; rule 2, the Open PR Gate — no
pull request is open for this branch yet; the reviewer reviews round 6 and books its verdict in
the next round's first commit; then the closing round: R-1369's resolution line, the rotation or
its recorded skip, SU-066's `consumed_by`, the STATUS flip with the README sync, and the pull
request, left unmerged.
Operator questions open: 1. Open findings: 88 (gate 3, `open_finding_ids`, rule: round 5's base of
87 plus the one R-1381 registered at C1 of this round).

## Item status

| Item | Status | Reason |
|---|---|---|
| C1 | done | a667ae7c4 |
| A1 | done | no candidate; apply skipped per block instruction |
| A2 | done | exit 0, see `## Verification` item 2 |
| A3 | done | `READY_FOR_REVIEW`, see `## Evidence and package` |
| Gate 1 | done | `ALL True` |
| Gate 2 | done | A2 and A3 readings as recorded |
| Gate 3 | done | `fail_count` 1 on the standing thirteen; 88 open findings |
| C2 | done | this commit |
