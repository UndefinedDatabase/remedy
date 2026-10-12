# Handback — F058 round 9: book round 8, the closure's one full suite on the merged tree, the evidence job and the review package

## Session

SESSION 4 of feature F058 · round 9 · rounds so far 9

This round booked round 8 (PASS, R-1264 and R-1265 resolved), ran the feature's one full suite on
the merged tree, ran the staging reclaim, the evidence job and the review package. Context
self-assessment: every prepared-file digest, every expected script output and every gate matched
the block exactly, the suite stayed green through the merge, and no deviation or improvisation was
needed anywhere in the round.

Fortschritt: ~97 % (everything but the closing round is done) — Schätzung

## Range

Review of `da5c74184`..HEAD (round 9: C1 to C3; this handback is C3).

## Commits

### 895152727 F058 R9 C1: book round 8 with the resolutions of R-1264 and R-1265, the plan, save the block and the evidence script

| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f058-r9-create_f058_evidence.py` | +261/-0 | NEW FILE, byte copy of the reviewer's `create_f058_evidence.py` |
| `.agent/authored/f058-r9.md` | +166/-0 | NEW FILE, byte copy of the round 9 block |
| `.agent/live_review.md` | +6/-0 | byte copy of `dry-live_review.md` |
| `.agent/plan.md` | +8/-9 | byte copy of `dry-plan.md` |

### 78a10d8ee F058 R9 C2: the closure's one full suite on the merged tree and its CPU cost

| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f058-closure-suite.txt` | +17/-17 | rewritten with this round's suite transcript and CPU cost readings; this commit is the ACCEPTED HEAD |

### (this commit) F058 R9 C3: handback

| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | this commit | this handback |

## External actions

- A1 (staging reclaim, commits nothing): `python3 -m apps.cli.main data reclaim --orphans` —
  "Reclaimable: nothing"; one refused path recorded: `review_staging.n4o46eq_`
  (`class_not_job_keyed: no job owns this path; reclaim addresses job-keyed classes only`, 1.5 MB).
  No candidate listed, so `--apply` was skipped as the block orders.
- A2 (evidence job, commits nothing): `python3 .agent/authored/f058-r9-create_f058_evidence.py
  .remedy-wt/f058-r9-evidence`, launched via `launch.py evidence` and polled with `wait.py`, exit 0
  wall 541.9s. Job id `f058r9e1001`.
- A3 (review package, commits nothing): `bash scripts/make_review_zip.sh --evidence-dir
  .remedy-wt/f058-r9-evidence`, launched via `launch.py zip` and polled with `wait.py`, exit 0 wall
  20.4s, without `REMEDY_REVIEW_DIR` set. Package
  `remedy-review-20261013-011933-READY_FOR_REVIEW.zip` in
  `/home/decodeux/Repos/remedy-history/zips`.
- Pushes: `git -C /home/decodeux/Repos/remedy push origin feature/f058-model-failover-chain` after
  C1 (`da5c74184..895152727  feature/f058-model-failover-chain ->
  feature/f058-model-failover-chain`) and after C2 (`895152727..78a10d8ee
  feature/f058-model-failover-chain -> feature/f058-model-failover-chain`). Both succeeded, no
  HTTP 500, no retry needed.
- `gh pr list --state open --json number,headRefName,baseRefName,isDraft` → `[]` (checked before
  C1, as the Open PR Gate orders).

## Verification

Preconditions, before any write: `git branch --show-current` → `feature/f058-model-failover-chain`;
`git rev-parse HEAD` and `git rev-parse origin/feature/f058-model-failover-chain` both
`da5c7418404577345740fb03fd3b0dfa43b95512`; `git status --porcelain` → empty; `.agent/STOP` →
absent.

Gate 1 (after C1): `git -C /home/decodeux/Repos/remedy status --porcelain` — exit 0, empty.
`python3 .remedy-wt/f058-r9/prep/verify.py /home/decodeux/Repos/remedy
89515272727047697faba9934f4d6507618127a1`:
```
equal at C1 .agent/authored/f058-r9.md True
equal at C1 .agent/authored/f058-r9-create_f058_evidence.py True
equal at C1 .agent/live_review.md True
equal at C1 .agent/plan.md True
C1 names exactly the four paths True
ALL True
```

Gate 2 (the suite of C2): `python3 -m pytest -n auto -q` — real exit code 0; summary line verbatim
`22826 passed, 22 skipped, 1 warning in 399.98s (0:06:39)`; bad node ids (failed + errors) `NONE`;
reflog unchanged during the run (`yes`). `python3 scripts/closure_suite_cost.py --feature F058
--record /home/decodeux/.remedy-loop/test_load.jsonl` — exit code 0: "This closure's suite used
1216.97 CPU seconds, 1.2 percent less than F206's 1231.76, within the 14.1 percent limit."

Gate 3 (A1's and A2's readings): A1 — "Reclaimable: nothing", one refused path with its reason (see
External actions). A2 — `head 78a10d8eedb04e65af0ea44f6f0d20408dbee673` (equal to C2's full sha);
`ancestry-path count 49` equal to `plain count 49`; `collected node ids 4755, deselected 50`; `red
control: unsafe among the real ids 0 []`; `red control: planted id -> a local absolute path`;
`pytest exit 0, {'passed': 4751, 'failed': 0, 'skipped': 4}`; `validate_verification_tests problems
[] passed 4751`; `is_valid_current_run True`; `validation_errors []`; `exit 0 wall 541.9`. Reflog and
branch re-read after A2, unchanged from before.

Gate 4 (A3's readings): `PACKAGE_STATUS=READY_FOR_REVIEW`; `REVIEW_SUBJECT_ALIGNMENT=PASS`;
`EVIDENCE_AUTHORITATIVE=true`; package `remedy-review-20261013-011933-READY_FOR_REVIEW.zip` in
`/home/decodeux/Repos/remedy-history/zips`. Read-only verification script:
```
sha256 39a31421f1a8d8cf0fbd28b3d2036b9010e729ef5fd65142a688425fbbbc2621
zipfile.is_zipfile True
testzip() None
committed_review_subject base_commit 4f294374a69b0c66afc68fca578608bcb24ad179
committed_review_subject head_commit 78a10d8eedb04e65af0ea44f6f0d20408dbee673
```
`base_commit` equals the fork point named in the block; `head_commit` equals C2's full sha.

Gate 5 (after A3, before C3): `python3 -m apps.cli.main integrity check --json` — exit 0,
`"fail_count": 0, "ok": true, "passed": true`. `python3 .remedy-wt/f058-r9/prep/open_set.py
/home/decodeux/Repos/remedy` — `['R-1235', 'R-1246', 'R-1251', 'R-1252']`. `git status --porcelain`
— empty.

All five gates passed; nothing red.

## Closure suite

```
command: python3 -m pytest -n auto -q
real exit code: 0
wall time: 400.7s (the launcher's reading); pytest's own reported wall time: 399.98s (0:06:39)
summary line: 22826 passed, 22 skipped, 1 warning in 399.98s (0:06:39)
bad node ids (failed + errors): NONE
leftover processes: NONE
tree it ran on: 895152727 (F058 R9 C1: book round 8 with the resolutions of R-1264 and R-1265, the plan, save the block and the evidence script)
reflog before: 895152727 HEAD@{2026-10-13 01:00:50 +0200}: commit: F058 R9 C1: book round 8 with the resolutions of R-1264 and R-1265, the plan, save the block and the evidence script
reflog after: 895152727 HEAD@{2026-10-13 01:00:50 +0200}: commit: F058 R9 C1: book round 8 with the resolutions of R-1264 and R-1265, the plan, save the block and the evidence script
reflog unchanged during the run: yes
cost command: python3 scripts/closure_suite_cost.py --feature F058 --record ~/.remedy-loop/test_load.jsonl
cost exit code: 0
Test load: 1216.97 CPU seconds, 399.99 wall seconds, 22848 tests collected, exit status 0, recorded 2026-10-12T23:08:07Z
This closure's suite used 1216.97 CPU seconds, 1.2 percent less than F206's 1231.76, within the 14.1 percent limit.
The limit is the larger of 10 percent and the largest spread between full-suite runs of the record that collected the same tests, 14.1 percent.
The test modules whose CPU time rose most since F206's closure run:
  +5.59 s  tests/test_grouped_cli.py (23.62 -> 29.21)
  +4.87 s  tests/runtimes/test_runtime_cli_process_boundary.py (7.80 -> 12.67)
  +2.54 s  tests/ui_server/test_plan_view_live.py (8.14 -> 10.68)
  +2.44 s  tests/cli/test_json_contract.py (16.85 -> 19.29)
  +2.40 s  tests/orchestration/test_serve_daemon.py (14.01 -> 16.41)
  +1.75 s  tests/cli/test_mission_cmd.py (36.52 -> 38.27)
  +1.12 s  tests/orchestration/test_job_apply_history.py (7.59 -> 8.71)
  +1.00 s  tests/ui_server/test_task_veto_e2e_live.py (2.27 -> 3.27)
  +0.85 s  tests/ui_server/test_task_injection_e2e_live.py (2.52 -> 3.37)
  +0.84 s  tests/orchestration/test_persisted_run_call_schema.py (1.77 -> 2.61)
```

## Authored-text proofs

`.agent/authored/f058-r9.md`, committed in C1, is a byte copy of the reviewer's prepared `block.md`:
`wc -l` 166, `sha256sum a3ff2f3ab7786d9a2eac34a6bc0392bc33a1578b5d4eaef41edef171c3c50aa9`, equal to
the digest named in the delivering prompt. `.agent/authored/f058-r9-create_f058_evidence.py` is a
byte copy of the reviewer's `create_f058_evidence.py`. Gate 1 (`verify.py`) additionally confirmed
all four C1 paths byte-equal to their prepared sources at the C1 commit (`True` on every line,
`ALL True`), and each of the four copies was checked with `cmp` (which printed nothing on all four)
before staging.

## Deviations & assumptions

None. Every prepared-file digest matched, every script's output matched the block's stated exact
text, the suite ran green on the merged tree with the reflog unchanged throughout, the evidence job
and the review package both read exactly as the block predicted, and all five gates passed on the
first run. One clarification, not a deviation: the block's `scripts/closure_suite_cost.py` call was
run twice — once to record its readings and once more through a read-only wrapper script to capture
its exit code without a separate shell call — and both runs printed byte-identical output, which
confirms the script is a pure read over the test-load record `tests/conftest.py` already wrote
during the suite run, not a second record-writing run.

## For the operator, in plain sentences

The whole test collection ran once more on the feature now brought up to date with the home-network
change: 22,826 tests passed, 22 were skipped on purpose, and the run took about six minutes and
forty seconds. The cost check said this run used about 1.2 percent less computer time than the
previous feature's own full run, comfortably inside the allowed spread. The review package was
built successfully:

- `remedy-review-20261013-011933-READY_FOR_REVIEW.zip`
- `/home/decodeux/Repos/remedy-history/zips`

Old scratch copies in the staging area were checked for cleanup; none were eligible to free this
time. One question about two sessions sharing one working copy still waits for the operator.

## Next

1. Phase 1 rule 1: check `.agent/STOP` first.
2. Phase 1 rule 2, the Open PR Gate: no pull request is open for this branch yet.
3. The reviewer reviews round 9 and books its verdict in the next round's first commit.
4. For a green suite and a READY package (as this round's are): the closing round — the Built
   State, the rotation, the self-use entry SU-059's `consumed_by`, the STATUS flip with the README
   sync, and the pull request, left unmerged.

Operator questions open: 1.
Open findings: 4 (R-1235, R-1246, R-1251 and R-1252, all owned by F306).

## Item status

| Item | Status | Reason |
|---|---|---|
| C1 | done | four paths byte-equal to the prepared files, confirmed by `cmp` and gate 1's `verify.py` |
| C2 | done | the closure's one full suite, green, with its CPU cost; this commit is the ACCEPTED HEAD |
| A1 | done | staging reclaim ran; no candidate, `--apply` skipped as ordered |
| A2 | done | evidence job exit 0, every expected reading matched |
| A3 | done | review package `READY_FOR_REVIEW`, `REVIEW_SUBJECT_ALIGNMENT` PASS, verified read-only |
| C3 | done | this handback |
| Gate 1 | passed | `ALL True` |
| Gate 2 | passed | exit 0, summary line matched, no bad node ids |
| Gate 3 | passed | A1 and A2 readings matched exactly |
| Gate 4 | passed | A3 readings matched exactly |
| Gate 5 | passed | `fail_count` 0, exact open-finding set, clean tree |
