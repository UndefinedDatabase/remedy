# Handback — F305 round 4: book round 3, the recurrence of R-1252 and the resolution of R-1248, the closure's evidence job and review package

## Session

SESSION 1 of feature F305 · round 4 · rounds so far 4

Context self-assessment: the session verified the block's own line count and sha256 and all four
Bundle-listed prepared files' digests before any write, byte-copied and re-hashed every C1 target
against its prepared source before staging, confirmed the exact path set and numstat before the
commit, ran the detached evidence job and the review package build each exactly once with the
command's own exit code captured in the launching script, and closed every gate green on the first
pass; context remains comfortable at handback.

Fortschritt: ~95 % (everything but the closing round is done) — Schätzung

## Range

Review of `abe4e45f3`..HEAD.

## Commits

### 5132e4873 F305 R4 C1: book round 3, the recurrence of R-1252 and the resolution of R-1248, the plan, save the block and the evidence script

| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f305-r4-create_f305_evidence.py` | +255/-0 | NEW FILE, byte copy of `prep/create_f305_evidence.py` (reviewer-authored, adapted from `.agent/authored/f297-r13-create_f297_evidence.py`) |
| `.agent/authored/f305-r4.md` | +140/-0 | NEW FILE, byte copy of `block.md` (140 lines, sha256 `2ebb3d988b794db335f5aba15f351384dd69c1c973796e3db7042460d5dd323f`, matching both values the session was given) |
| `.agent/live_review.md` | +6/-0 | byte copy of base `abe4e45f3:.agent/live_review.md` plus `prep/append-live_review.txt`: the `Gate: F305 R3` entry, the `Recurrence: R-1252` entry and the `Done: R-1248` entry appended |
| `.agent/plan.md` | +7/-12 | rewritten in full for F305 round 4, byte copy of `prep/dry-plan.md` |

### this commit F305 R4 C2: handback with the evidence and package readings

| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | this commit | this file (self-reference rule, `docs/agents/handback_template.md`) |

## External actions

`git push -u origin feature/f305-multi-repo-chain-band` after C1 → `abe4e45f3..5132e4873
feature/f305-multi-repo-chain-band -> feature/f305-multi-repo-chain-band`, tracking set up. The
same push command follows this commit (C2), per the block's push-after-C2 instruction; its outcome
is reported in the final reply, not in this file. No pull request opened, edited or merged this
round (none is open for this branch; the block forbids opening one). No other `gh` command run. No
`git worktree add`/`remove` performed; the worker's own scratch directory
`.remedy-wt/f305-r4-worker/` (gitignored) held the launch/poll/inspect scripts and logs.

## Verification

**Preconditions (before C1):** `git rev-parse HEAD` read `abe4e45f35e5d2da8b96245feff0aa369a486226`,
equal to `origin/feature/f305-multi-repo-chain-band`; `git status --porcelain` empty; `.agent/STOP`
absent; `git branch --show-current` read `feature/f305-multi-repo-chain-band`.

**Block and Bundle digests (before any write):** `wc -l block.md` read `140`, its sha256 read
`2ebb3d988b794db335f5aba15f351384dd69c1c973796e3db7042460d5dd323f` — both equal to the values the
prompt delivered. All four digest-bearing prepared files (`append-live_review.txt`, `dry-plan.md`,
`create_f305_evidence.py`, `verify.py`) were hashed and matched the block's stated digests exactly
before use:
```
2ad7e2a0f2d4f68c759b0b93b363484bc4736202400964e98d4b6bf580c1c00f  append-live_review.txt
11cfd180678e9a7bbf6ef6409d1861558be795859d6afc132dd74609108aca2e  dry-plan.md
d177898eb6903aebe2952e632d93983f1a9b6c11c00cee1bb3fdd10ae1d68d8f  create_f305_evidence.py
44e0e36f8bbb0f407b52e6dc3e7cc59153259911b2c37963a788d0de0c5382c5  verify.py
```

**C1:** `c1_prepare.py` byte-copied `block.md`, `create_f305_evidence.py` and `dry-plan.md` to
their destinations and appended `append-live_review.txt`'s bytes to `.agent/live_review.md`,
printing each write's own sha256; the `.agent/authored/f305-r4.md` write's sha256 read
`2ebb3d988b794db335f5aba15f351384dd69c1c973796e3db7042460d5dd323f` with `lines=140`, matching the
block exactly. `git add` then `git status --porcelain` showed exactly the four Bundle paths, no
other path. `git diff --stat --cached` read `4 files changed, 408 insertions(+), 12 deletions(-)`.
`git branch --show-current` read `feature/f305-multi-repo-chain-band` immediately before the
commit.

**A1 (staging reclaim, commits nothing):** `python3 -m apps.cli.main data reclaim --orphans` →
exit 0:
```
Data root: /home/decodeux/Repos/remedy/.data
  Reclaimable: nothing
  Refused (kept, with the reason):
    review_staging.n4o46eq_  class_not_job_keyed: no job owns this path; reclaim addresses job-keyed classes only  1.5 MB
  Would free 0 B in 0 paths — nothing deleted; re-run with --apply
```
The preview lists no candidate, so `--apply` was skipped per the block.

**A2 (evidence job, commits nothing):** `git reflog -n 3 --date=iso` before the run:
```
5132e4873 HEAD@{2026-10-12 03:36:06 +0200}: commit: F305 R4 C1: ...
abe4e45f3 HEAD@{2026-10-12 03:09:23 +0200}: commit: F305 R3 C6: handback
a09a65206 HEAD@{2026-10-12 03:06:30 +0200}: commit: F305 R3 C5: ...
```
`git branch --show-current` read `feature/f305-multi-repo-chain-band`. `a2_launch_evidence.py`
launched `a2_runner.py` detached (`start_new_session=True`), which ran
`python3 .agent/authored/f305-r4-create_f305_evidence.py .remedy-wt/f305-r4-evidence` to
completion, streamed to `evidence.log`, and wrote its exit code to `evidence.exit`. Polled with
`a2_poll_evidence.py` until `DONE exit=0` appeared (about 16 minutes wall). `evidence.log` whole:
```
head 5132e487355b06bca05fc27a1aabafec1b0835d9
ancestry-path count 17
plain count 17
collected node ids 4465, deselected 50
red control: unsafe among the real ids 0 []
red control: planted id -> a local absolute path
pytest exit 0, {'passed': 4461, 'failed': 0, 'skipped': 4}, output_hash 5ff006fe7e47133afb9ed0747543f69c6fce6ede7f200682aa6de99ab96522ce
validate_verification_tests problems [] passed 4461
is_valid_current_run True
validation_errors []
gates written: ['artifact_contract_gate.json', 'change_provenance_gate.json', 'commit_execution_gate.json', 'fresh_evidence_gate.json', 'runtime_integration_gate.json', 'final_verifier_report.json']
{
  "job_id": "f305r4e1001",
  "head_commit": "5132e487355b06bca05fc27a1aabafec1b0835d9",
  "authority_count": 27,
  "partition": {
    "T001": 9,
    "T002": 9,
    "T003": 9
  },
  "commit_count": 17,
  "verdict": "PASS_WITH_RISKS",
  "manual_completion": true,
  "operator_attested_tasks": [
    "T001",
    "T002",
    "T003"
  ],
  "total_passed": 4461
}
```
Head equals C1's full sha; both ancestry counts 17; `collected node ids 4465, deselected 50`; no
unsafe id; the planted id answers `a local absolute path`; pytest exit 0 at 4461 passed and 4
skipped (more passed and fewer skipped than the reviewer's dry run's 4456/9, as the block predicted
for a checkout with the UI toolchain linked in); `validate_verification_tests problems []`,
`is_valid_current_run True`, `validation_errors []`; wrapper exit 0. `git reflog -n 3 --date=iso`
and `git branch --show-current` read identically after the run — neither moved.

**A3 (review package, commits nothing):** from the clean, pushed tree at C1,
`a3_make_zip.py` ran `bash scripts/make_review_zip.sh --evidence-dir .remedy-wt/f305-r4-evidence`
once, `cwd=/home/decodeux/Repos/remedy`, `REMEDY_REVIEW_DIR` explicitly popped from the child's
environment (it was not set to begin with). Exit 0. `zip.log` whole:
```
UNCHANGED: runtime_integration_gate.json — rebuilt from source; identical to existing
Evidence refresh completed for staged copy.
Observability index generated from staged bytes: evidence/current/self_run_observability_index.json
{"member_count": 8165, "authoritative_count": 27, "symlink_count": 0, "tombstone_count": 0, "final_path": "/home/decodeux/Repos/remedy-history/zips/remedy-review-20261012-035421-READY_FOR_REVIEW.zip", "final_sha256": "485bba5edc512dce18320e9c52b8a01afc827c0b439d595b4f5adb6a60804e13", "publication_capability": "SUPPORTED", "package_status": "READY_FOR_REVIEW", "evidence_authoritative": true, "review_subject_alignment": "PASS", "manifest_sha256": "138d1b99ddb2bf5e07e397727ad16b39e6cf38ead34faba716fecb8dbbcaae96"}

============================================
REVIEW_PACKAGE_CREATED=true
PACKAGE_STATUS=READY_FOR_REVIEW
PACKAGING_CWD=/home/decodeux/Repos/remedy
EVIDENCE_DIR=.remedy-wt/f305-r4-evidence
REVIEW_SUBJECT_ALIGNMENT=PASS
EVIDENCE_AUTHORITATIVE=true
REVIEW_PACKAGE_DIR=/home/decodeux/Repos/remedy-history/zips
ZIP_PATH=/home/decodeux/Repos/remedy-history/zips/remedy-review-20261012-035421-READY_FOR_REVIEW.zip
============================================

ZIP CREATED AND READY FOR FINAL REVIEW

37M	/home/decodeux/Repos/remedy-history/zips/remedy-review-20261012-035421-READY_FOR_REVIEW.zip
Included files: 8165
Branch: feature/f305-multi-repo-chain-band
Commit: 5132e487355b06bca05fc27a1aabafec1b0835d9
Evidence: evidence/current/
```
`PACKAGE_STATUS=READY_FOR_REVIEW`, `REVIEW_SUBJECT_ALIGNMENT=PASS`,
`EVIDENCE_AUTHORITATIVE=true`. `a3_inspect_zip.py` then read, inside the package:
`zipfile.is_zipfile` → `True`; sha256 over the zip bytes →
`485bba5edc512dce18320e9c52b8a01afc827c0b439d595b4f5adb6a60804e13` (matches `final_sha256`
exactly); `testzip()` → `None`; `.review_zip_manifest.json`'s `committed_review_subject.base_commit`
→ `f6004fdf1d75315ca49f748d169c7a60def3b94e` (matches the block's stated base);
`committed_review_subject.head_commit` → `5132e487355b06bca05fc27a1aabafec1b0835d9` (matches C1's
full sha). Archived directory: `/home/decodeux/Repos/remedy-history/zips`.

**Gate 1 (after C1):** `git -C /home/decodeux/Repos/remedy status --porcelain` → empty. Then
`python3 .../prep/verify.py /home/decodeux/Repos/remedy 5132e487355b06bca05fc27a1aabafec1b0835d9`
→
```
equal at C1 True .agent/authored/f305-r4.md
equal at C1 True .agent/authored/f305-r4-create_f305_evidence.py
equal at C1 True .agent/plan.md
base plus slice at C1 True .agent/live_review.md
C1 path set True ['.agent/authored/f305-r4-create_f305_evidence.py', '.agent/authored/f305-r4.md', '.agent/live_review.md', '.agent/plan.md']
ALL True
```
Exit 0, every line `True`, last line `ALL True`.

**Gate 2 (A1's readings):** as recorded above under A1 — `Reclaimable: nothing`, one refused path
with its reason, `Would free 0 B in 0 paths`.

**Gate 3 (A2's readings):** as recorded above under A2 — head, both ancestry counts, collected/
deselected, no unsafe id, planted-id control, pytest exit 0 with counts, validation lines, exit 0.

**Gate 4 (A3's readings):** as recorded above under A3 — `PACKAGE_STATUS`,
`REVIEW_SUBJECT_ALIGNMENT`, `EVIDENCE_AUTHORITATIVE`, filename, SHA-256, manifest base/head,
`is_zipfile`/`testzip()`, directory.

**Gate 5 (after A3, before C2):** `python3 -m apps.cli.main integrity check --json` →
```json
{"check_count": 6, "checks": [{"message": "handlers=184", "name": "handler_import", "status": "pass"}, {"message": "last Gate verdict PASS", "name": "live_review_verdict", "status": "pass"}, {"message": "unchecked=0, context_complete=False", "name": "plan_consistency", "status": "pass"}, {"message": "untracked=0, relevant=0", "name": "relevant_untracked", "status": "pass"}, {"message": "no reviewer scratch, evidence dir or archive at the root", "name": "repo_root_hygiene", "status": "pass"}, {"message": "no open blocker/high findings", "name": "high_blockers_open", "status": "pass"}], "fail_count": 0, "ok": true, "passed": true, "schema_version": 1, "version": 1}
```
Exit 0, all six checks `pass`, `fail_count` 0. Then
`python3 -c "import scripts.rotate_live_review as r; print(r.open_finding_ids(open('.agent/live_review.md').read()))"`
→ `['R-1235', 'R-1246', 'R-1251', 'R-1252']`, matching exactly. `git status --porcelain` → empty.

**Gate 6 (after C2's push):** reported in the final reply, not here (block instruction).

No mutation run (the block forbids it this round). No test run beyond A2's one evidence pytest
command; `REMEDY_TEST_MAX_WORKERS` was never set, no extra `-n` was passed, no two test commands
ran at once. No `npm` or `npx` run. No pull request opened or merged. No provider call made this
round.

## Authored-text proofs

1. `block.md` → `.agent/authored/f305-r4.md` (C1): byte-equal, confirmed by `c1_prepare.py`'s own
   printed sha256 and again by gate 1's `verify.py`.
2. `prep/create_f305_evidence.py` → `.agent/authored/f305-r4-create_f305_evidence.py` (C1):
   byte-equal, confirmed the same way; never edited; this is the exact file A2 ran.
3. The base `abe4e45f3:.agent/live_review.md` + `prep/append-live_review.txt` →
   `.agent/live_review.md` (C1): built by the formula gate 1's `verify.py` checks ("base plus
   slice at C1 True").
4. `prep/dry-plan.md` → `.agent/plan.md` (C1): byte-equal, confirmed by `c1_prepare.py` and gate 1.

## Deviations & assumptions

None. Every commit matched the block's ordered sequence (C1, then A1/A2/A3 which commit nothing,
then C2) with no extra commit, no dropped commit and no reordering. No file was written outside
C1's named path set; A1 recorded the empty reading and the one refused path instead of running
`--apply`, exactly as the block directs when the preview lists no candidate; A2's wrapper ran the
evidence script exactly once, detached, polled rather than waited on inline, with its own exit
code captured in the runner script; A3's wrapper ran the zip script exactly once with
`REMEDY_REVIEW_DIR` absent from the child environment. No mutation was run (none was ordered);
exactly one test command ran this round (A2's evidence pytest); `REMEDY_TEST_MAX_WORKERS` was
never set and no extra `-n` was passed; `npm`/`npx` were never run; `.agent/STOP` did not appear
during the round; no merge, branch create/switch beyond the one feature branch, or force-push was
performed; no pull request was opened or merged. The one deviation from habit, not from the block:
the first A1 attempt used `python3 -I -m apps.cli.main data reclaim --orphans`, which fails the
module lookup in this checkout (`-I`'s stripped `sys.path` drops the cwd that `-m` would otherwise
add, so `apps.cli.main` is unreachable; the module is importable here only via the normal,
non-isolated interpreter, not via an installed package). That attempt exited 1 with
`ModuleNotFoundError: No module named 'apps'`, touched no file and ran no reclaim logic, so it is
not the recorded A1 reading above; the corrected, successful run with a plain `python3` is the one
reported under A1 and Gate 2.

## Next

1. Phase 1 rule 1 (`.agent/STOP`): absent throughout this round; the next session checks it first.
2. Rule 2, the Open PR Gate: no pull request is open for this branch yet.
3. The reviewer reviews round 4 and books its verdict in the next round's first commit.
4. The closing round: the Built State, the rotation, the self-use entry `SU-057`'s `consumed_by`,
   the STATUS flip with the README sync, and the pull request, left unmerged.

Operator questions open: 1.
Open findings: 4 (R-1235, R-1246, R-1251 and R-1252, all owned by F306).

## For the operator, in plain sentences

This feature's review package was built successfully and is ready for review:
- folder: `/home/decodeux/Repos/remedy-history/zips`
- file: `remedy-review-20261012-035421-READY_FOR_REVIEW.zip`

No old scratch copies needed cleaning up this round, so no space was freed. The run on itself from
the previous round met the same small fault as the last feature's did: a task Remedy splits while
it runs leaves the record of that run unwritten, and the repair for that is already set aside for
the next clean-up feature. Nothing new waits for the operator.

## Item status

| Item | Status | Reason |
|---|---|---|
| C1 | done | round 3 booked (VERDICT PASS), the recurrence of R-1252 and the resolution of R-1248 booked, the block and the evidence script saved, `.agent/plan.md` rewritten for round 4; all byte proofs `True` |
| A1 | done | staging reclaim preview lists no candidate; recorded the empty reading and the one refused path; `--apply` skipped per the block |
| A2 | done | evidence job `f305r4e1001` ran to completion detached, exit 0; every expected reading matched |
| A3 | done | review package built once, `PACKAGE_STATUS=READY_FOR_REVIEW`, manifest base/head confirmed, zip integrity confirmed |
| C2 | done | this handback |
| Gate 1 | passed | every line `True`, `ALL True` |
| Gate 2 | passed | A1's readings as recorded |
| Gate 3 | passed | A2's readings as recorded |
| Gate 4 | passed | A3's readings as recorded |
| Gate 5 | passed | integrity `fail_count` 0, all six checks `pass`; open findings list matched exactly; tree clean |
| Gate 6 | pending | runs after the push; reported in the final reply |
