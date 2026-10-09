# Handoff — F299 round 8: book round 7, the closure's evidence job and review package on the accepted head

## Session

SESSION 1 of feature F299 · round 8 · rounds so far 8

Context self-assessment: the reviewer's context holds; the closing round follows in this session.

Fortschritt: ~98 % (everything but the closing commit and the pull request is done) — Schätzung

## Range

Review of `b2abe592ecec916b0322e3ee800b7137ef5aa192`..HEAD (two commits on
`feature/f299-acceptance-checks-other-repos`: C1 and this handback).

## Commits

### `02f613d86` F299 R8 C1: book round 7, resolve R-1231, the plan, save the block and the evidence script

| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f299-r8.md` | 140/0 | NEW FILE — byte copy of `block.md`; sha256 `969937e9b7f1d81dc64235ef91c1394fb3578d308d3743a37240984b34db677e`, 140 lines, both sides |
| `.agent/authored/f299-r8-create_f299_evidence.py` | 192/0 | NEW FILE — byte copy of `create_f299_evidence.py`; sha256 `a1a96f002bba8647a5c2ec3572b622bfbc69b9499511434dfd5eb8a7d3f33dec`, 192 lines, both sides |
| `.agent/live_review.md` | 4/0 | appends `Gate: F299 R7` (PASS) and `Done: R-1231` resolved; proved equal to the blob at `b2abe592e` + `src/ledger-append.txt`, and to `dry-live_review.md` |
| `.agent/plan.md` | 7/8 | replaced with `dry-plan.md`: round 8's current step, R-1231 removed from the open-findings line |

### This commit (self-reference) — F299 R8 C2: handback with the evidence and package readings

| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | this commit | this file |

## External actions

`git push origin feature/f299-acceptance-checks-other-repos` after C1 — succeeded on the first
attempt (`b2abe592e..02f613d86`). The same push, ordered after this commit, is reported in the
worker's final reply. No `gh pr create`, no `gh pr merge`, no new branch, no stash entry touched,
no `git worktree add`/`remove`.

## Verification

**C1's self-review**: `git diff --cached` read whole (388 lines, 27878 bytes, saved to
`.remedy-wt/f299-r8-worker/c1_diff_cached.txt`); matched the four expected paths exactly; no
unintended edits, no debug leftovers, no unrelated changes.

**Gate 1** (after C1): `git -C /home/decodeux/Repos/remedy status --porcelain` — empty. One Python
script (`gate1.py`) printing `True` for each byte equality, every committed file read with
`git show 02f613d86:<path>`: `.agent/authored/f299-r8.md`==`block.md` **True**;
`.agent/authored/f299-r8-create_f299_evidence.py`==`create_f299_evidence.py` **True**;
`.agent/plan.md`==`dry-plan.md` **True**; `.agent/live_review.md`== blob at `b2abe592e` +
`src/ledger-append.txt` **True**.

**Gate 2** (A1 — the staging reclaim, commits nothing):
```
python3 -m apps.cli.main data reclaim --orphans
```
Exit 0. `Reclaimable: nothing.` Refused (kept, with the reason):
`review_staging.n4o46eq_  class_not_job_keyed: no job owns this path; reclaim addresses job-keyed
classes only  1.5 MB`. `Would free 0 B in 0 paths — nothing deleted; re-run with --apply.` No
candidate was listed, so `--apply` was correctly skipped per the block.

**Gate 3** (A2 — the evidence job, commits nothing): launched detached (PID 2449072) from
`launch_a2_evidence.py`, polled with `poll_a2.py` to completion, output captured whole to
`/home/decodeux/Repos/remedy/.remedy-wt/f299-r8-worker/evidence.log`. Key lines, verbatim:
```
head 02f613d86c169c7ce991ab1163f8eb1b4aa5769f
ancestry-path count 31
plain count 31
collected node ids 2173, deselected 12
red control: unsafe among the real ids 0 []
red control: planted id -> a local absolute path
pytest exit 0, {'passed': 2170, 'failed': 0, 'skipped': 3}, output_hash 24d9813774b459011eee7608dc0423eda9c3f53e14fe0cfdf022882a6549b3ab
validate_verification_tests problems [] passed 2170
is_valid_current_run True
validation_errors []
gates written: ['artifact_contract_gate.json', 'change_provenance_gate.json', 'commit_execution_gate.json', 'fresh_evidence_gate.json', 'runtime_integration_gate.json', 'final_verifier_report.json']
```
Summary JSON: `job_id f299r8e1001`, `head_commit 02f613d86c169c7ce991ab1163f8eb1b4aa5769f`,
`authority_count 36`, `commit_count 31`, `verdict PASS_WITH_RISKS`, `total_passed 2170`. All
expected readings matched exactly: head equal to C1's full sha, both ancestry counts 31,
`2173, deselected 12`, no unsafe id, the planted id answering `a local absolute path`, pytest exit
0, `validate_verification_tests problems []`, `is_valid_current_run True`, `validation_errors []`.
Reflog and branch unchanged before and after the run (`git reflog -n 3 --date=iso` shows the same
three commits with `02f613d86` at tip before and after; `git branch --show-current` reads
`feature/f299-acceptance-checks-other-repos` both times).

**Gate 4** (A3 — the review package, commits nothing):
```
bash scripts/make_review_zip.sh --evidence-dir .remedy-wt/f299-r8-evidence
```
run via a blocking Python wrapper (`a3_zip.py`, `cwd=/home/decodeux/Repos/remedy`), without
setting `REMEDY_REVIEW_DIR`, output captured to
`/home/decodeux/Repos/remedy/.remedy-wt/f299-r8-worker/zip.log`. Exit **0**.
`PACKAGE_STATUS=READY_FOR_REVIEW`, `REVIEW_SUBJECT_ALIGNMENT=PASS`, `EVIDENCE_AUTHORITATIVE=true`.
Package `remedy-review-20261009-192024-READY_FOR_REVIEW.zip`, SHA-256
`6280e0aefab46067a191d9b5806625d6fe008961923ee45139590376583facf9` (re-hashed independently from
disk in `a3_verify_zip.py`; matched the tool's own reported hash). `.review_zip_manifest.json`
inside the package: `committed_review_subject.base_commit` =
`1acd5ac39220fb3a672f2a1027b9fa54b2592f6f` (matches), `committed_review_subject.head_commit` =
`02f613d86c169c7ce991ab1163f8eb1b4aa5769f` (matches C1). `zipfile.is_zipfile` **True**,
`testzip()` **None**. Archived directory: `/home/decodeux/Repos/remedy-history/zips`.

**Gate 5** (after A3, before C2):
```
python3 -m apps.cli.main integrity check --json
```
Exit 0. `"check_count": 6`, `"fail_count": 0`, `"ok": true`, `"passed": true`, all six checks
`"status": "pass"` (`handler_import`, `live_review_verdict` — message "last Gate verdict PASS" —
`plan_consistency`, `relevant_untracked`, `repo_root_hygiene`, `high_blockers_open`).
```
python3 -c "import scripts.rotate_live_review as r; print(r.open_finding_ids(open('.agent/live_review.md').read()))"
```
Output, verbatim:
```
['R-1138', 'R-1139', 'R-1143', 'R-1149', 'R-1156', 'R-1157', 'R-1158', 'R-1160', 'R-1162', 'R-1172', 'R-1176', 'R-1196', 'R-1219', 'R-1220', 'R-1225', 'R-1230']
```
Matches the block's ordered list exactly. `git status --porcelain` empty.

**Gate 6** (after C2's push, reported in the worker's final reply): local tip equal to
`origin/feature/f299-acceptance-checks-other-repos`.

## Authored-text proofs

`.agent/authored/f299-r8.md` (saved block, C1) equals `block.md` byte for byte: sha256
`969937e9b7f1d81dc64235ef91c1394fb3578d308d3743a37240984b34db677e`, 140 lines, both sides.
`.agent/authored/f299-r8-create_f299_evidence.py` equals `create_f299_evidence.py` byte for byte:
sha256 `a1a96f002bba8647a5c2ec3572b622bfbc69b9499511434dfd5eb8a7d3f33dec`, 192 lines, both sides.
`.agent/plan.md` equals `dry-plan.md` byte for byte. `.agent/live_review.md`'s append was proved to
equal the pre-round blob at `b2abe592e` followed by `src/ledger-append.txt`, both at write time and
again read-only against the committed blob at `02f613d86` (gate 1).

## Deviations & assumptions

- **A2's process exit code was not captured via a direct OS-level wait.** The evidence job was
  launched with `subprocess.Popen(..., start_new_session=True)` from a short-lived launcher script
  that printed the child's PID and exited immediately without calling `proc.wait()`. The child was
  thereby orphaned and reparented; by the time polling found it no longer alive, its real exit
  status had already been reaped by its new parent and could not be retrieved from an unrelated
  process. This was a design mistake in the launcher, not a rerun: the evidence pytest itself ran
  exactly once, as the block requires. To compensate without starting a second test run: (a) the
  script's own stdout, captured whole in `evidence.log`, shows `pytest exit 0` for the embedded
  pytest invocation and every other expected reading verbatim; (b) a read-only corroboration script
  (`a2_corroborate.py`) re-read (never re-ran) `verification_tests.json` and re-called
  `validate_verification_tests` and `validate_evidence_candidate` against the evidence directory
  already on disk, reproducing `problems []`, `is_valid_current_run True`, `validation_errors []`
  and `exit_code 0` for the stored run; (c) the script's own `main()` returns
  `0 if not problems and validation['is_valid_current_run'] and run.returncode == 0 else 1`, and all
  three conditions held, so its logical exit code is 0. The job's readings are not in doubt; only
  the direct OS-level capture of the wrapper process's own return code is missing. A3's wrapper was
  written differently (a blocking `subprocess.run()` in one script) specifically to avoid repeating
  this gap, and its exit code (0) was captured directly.
- **An early, discarded shell command used `cd` and `&&`.** Before reading the block, the first
  attempt at the mandatory sha256 check of `block.md` was issued as `cd / && python3 -c "..."`,
  which the sandbox refused outright (`cd` to a non-allowed directory) and which also violated the
  block's "never `cd`, never chain with `&&`" rule. No file was read, no byte was written, and no
  git state changed — the command errored before doing anything. It was immediately replaced with
  `python3 -I -c "..."` run as its own call with an absolute path, and every command for the rest of
  the round followed that form. Flagged here for the same reason earlier rounds flagged their own
  shell-rule slips: so an auditor does not have to find it in a shell-history diff instead.
- No other deviation: C1, A1, A2, A3 and gates 1–5 ran exactly as ordered, each exactly once, in the
  block's sequence; C1 is a single commit at 343 insertions, under the 500-insertion cap; no file
  outside C1's named paths was touched; A1, A2 and A3 committed nothing; the evidence pytest run was
  the round's only test run, with no `-n`, no `REMEDY_TEST_MAX_WORKERS`, and no second pytest
  invocation before or after it; no evidence directory, package or queue file is committed (tracked
  path set is exactly `.agent/authored/f299-r8.md`, `.agent/authored/f299-r8-create_f299_evidence.py`,
  `.agent/live_review.md`, `.agent/plan.md` and, with this commit, `.agent/handoff.md`); nothing was
  merged or closed — no `gh pr merge`, no `gh pr create`, no STATUS/README edit, no ledger rotation,
  no queue edit, no self-use run.

## Round verdicts

Round 6 FAIL (R-1231 registered) and round 7 PASS (R-1231 resolved) are both already booked in the
ledger — round 7 by this round's C1. Round 8's verdict is the reviewer's, to be booked in the next
round's first commit.

## For the operator, in plain sentences

This feature's review package was built: `remedy-review-20261009-192024-READY_FOR_REVIEW.zip`, in
`/home/decodeux/Repos/remedy-history/zips`. The one old scratch item found this round — a staging
copy no job still owns (`review_staging.n4o46eq_`, about 1.5 MB) — was listed but not one the
reclaim tool is allowed to touch automatically (it is not job-keyed), so nothing was deleted and no
space was freed; everything else in the data root is durable or unclassified and the tool leaves it
alone by design. Nothing waits for you.

## Next

1. Phase 1 rule 1 (`.agent/STOP`).
2. Phase 1 rule 2 (Open PR Gate; no pull request is open for this branch yet).
3. The reviewer reviews round 8 and books its verdict in the next round's first commit.
4. The closing round: book round 8, rotate the ledger, the self-use entry SU-051's `consumed_by`,
   the STATUS flip with the README sync, and the pull request, left unmerged.

Operator questions open: 0.
Open findings: 16 (R-1160, Medium; R-1138, R-1139, R-1143, R-1149, R-1156, R-1157, R-1158, R-1162,
R-1172, R-1176, R-1196, R-1219, R-1220, R-1225 and R-1230, Low; all owned by F297).

## Item status

| Item | Status | Reason |
|---|---|---|
| C1: book round 7, resolve R-1231, the plan, save the block and the evidence script | done | all byte proofs True, both at write time and at gate 1; pushed, accepted HEAD `02f613d86c169c7ce991ab1163f8eb1b4aa5769f` |
| A1: the staging reclaim | done | no candidate listed; `--apply` correctly skipped; one refused path recorded with its reason |
| A2: the evidence job | done | all expected readings matched exactly; exit code derived from the log and a read-only corroboration rather than a direct OS-level capture (deviation above) |
| A3: the review package | done | `READY_FOR_REVIEW`, manifest base/head match, zip integrity confirmed, package archived |
| C2: handback | done | this commit |
| Gate 1 | passed | status clean; all four byte proofs True |
| Gate 2 | passed | A1's readings as listed there |
| Gate 3 | passed | A2's readings as listed there |
| Gate 4 | passed | A3's readings as listed there |
| Gate 5 | passed | integrity six checks pass, fail_count 0; open finding ids match exactly; status clean |
| Gate 6 | pending push | to be reported in the worker's final reply after C2's push |
| Push (C1) | done | `b2abe592e..02f613d86`, first attempt |
| Push (C2) | pending | reported in the worker's final reply |
