# Handback — F024 Phase timeline with scrubber · Round 7

## Session

SESSION 1 of feature F024 · round 7 · rounds so far 7

Ample context remained throughout this round; a large majority of the budget remained at the
point this handback was written.

## Range

Review of 6cf991aa..HEAD

## Commits

### b94a09ee5 F024 R7 C1: copy round 7 block and payloads into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f024-r7-block.md | +170/-0 | copy of this round's block, verbatim |
| .agent/authored/f024-r7-create_f024_evidence.py | +169/-0 | copy of the create_f024_evidence.py payload |
| .agent/authored/f024-r7-ledger.diff | +10/-0 | copy of the ledger.diff payload |
| .agent/authored/f024-r7-plan.md | +27/-0 | copy of the plan.md payload |

376 insertions by `git show --numstat` (block's line count 170 + 206) — matches the block's
expectation exactly; well under the 500-insertion STOP threshold.

### b650ced4b F024 R7 C2: book round 6's PASS, the one full suite green
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +2/-0 | round 6's Gate entry appended, via `git apply` of ledger.diff |
| .agent/plan.md | +4/-7 | rewritten to the plan.md payload |

`git apply --check` on ledger.diff: exit 0. `git apply`: exit 0. Insertions/deletions by `git show
--numstat`: 2/0 live_review.md, 4/7 plan.md — matches the block's expected counts (2/0, 4/7)
exactly. **This commit's full sha, `b650ced4b1d0fef4c9156de0b217cbad7a76bef7`, is this closure's
ACCEPTED HEAD.** Pushed to `origin/feature/f024-phase-timeline-scrubber` immediately after, before
A1.

### (this commit) F024 R7 C3: rewrite handoff for round 7 with the evidence and package readings
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | (self-reference) | this handback, rewritten for round 7 |

Per the handback template's self-reference exception: a handback cannot table the commit that
writes it. Insertions reported in the final reply, as measured by `git show --numstat` after the
commit.

## External actions

- `git push origin feature/f024-phase-timeline-scrubber` after C2: `6cf991aaf..b650ced4b
  feature/f024-phase-timeline-scrubber -> feature/f024-phase-timeline-scrubber`, real exit 0.
- A1 — the evidence job: `python3 .remedy-wt/f024-r7-payloads/create_f024_evidence.py >
  .remedy-wt/f024-r7-worker/evidence.log 2>&1`, real exit 0. Bundle written to
  `.remedy-wt/f024-r7-evidence/` (gitignored, not committed).
- A2 — the review package: `bash scripts/make_review_zip.sh --evidence-dir
  .remedy-wt/f024-r7-evidence`, real exit 0. `PACKAGE_STATUS=READY_FOR_REVIEW`,
  `EVIDENCE_AUTHORITATIVE=true`. Package archived to
  `/home/decodeux/Repos/remedy-history/zips/remedy-review-20260925-082755-READY_FOR_REVIEW.zip`.
- No worktree add/remove this round. No `gh pr create`, no merge. The final `git push` (after this
  commit) and its real outcome, plus `gh pr list`, are reported in the final reply per G6, since
  the push ships this handback and cannot be captured before it happens.

## Verification

```
$ ls .agent/STOP; echo "REAL_EXIT=$?"
ls: cannot access '.agent/STOP': No such file or directory
REAL_EXIT=2
(absent, as required)

$ pwd
/home/decodeux/Repos/remedy
$ git status --porcelain
(empty)
$ git branch --show-current
feature/f024-phase-timeline-scrubber
$ git log --oneline -1
6cf991aaf F024 R6 C5: record the closure suite transcript and rewrite handoff for round 6
```
All BEFORE ANYTHING ELSE step 2 checks passed at round start.

```
$ (line count and sha256 of .remedy-wt/f024-r7/block.md, measured)
line_count: 170
sha256: 604db56ae15731c1cfeb9a491702600d2c491cf2c7f6dd1f32920d6e7ffb0434
```
Matches both readings given in the delegation message exactly (170 lines,
604db56ae15731c1cfeb9a491702600d2c491cf2c7f6dd1f32920d6e7ffb0434) — R-0954.

```
$ git worktree list
(primary + 15 f015-*-dry/sim r1-r6, 5 f015-*-sim r7-r9, 16 f020-*-dry/sim r1-r8,
 20 f023-*-dry/sim r1-r9, f023-r10-dry, f023-r10-sim, f024-r1-dry, f024-r1-sim,
 f024-r2-dry, f024-r2-sim, f024-r3-dry, f024-r3-sim, f024-r4-dry, f024-r4-sim,
 f024-r5-dry, f024-r5-sim, f024-r6-dry, f024-r6-sim, f024-r7-dry, f024-r7-sim,
 8 f284-*-dry/sim r1-r4, 4 job-* worktrees)
$ git branch --list 'remedy/job-*' | wc -l
41
```

```
$ (lines/bytes/sha256 of each payload under .remedy-wt/f024-r7-payloads/)
create_f024_evidence.py lines=169 bytes=8547 sha256=80240feb774bb44208f58f4dff74bf84e90787030471e72ab375bf4c8129d0ff
ledger.diff              lines=10  bytes=6830 sha256=57e8f85ce871068f061a484baa3f2f97f5332043a8b43ec58a5a229448b615ec
plan.md                  lines=27  bytes=890  sha256=b9015060d84ca2b37971c639b97f4d2cc56d67201166f303baca3730b9b2c278
```
All 3 match the PAYLOADS table exactly (G1).

```
$ (compare each committed .agent/authored/f024-r7-* blob against its source, via `git show <C1>:<path>`)
f024-r7-block.md                    @ b94a09ee5: IDENTICAL (sha 604db56a...)
f024-r7-create_f024_evidence.py     @ b94a09ee5: IDENTICAL (sha 80240feb...)
f024-r7-ledger.diff                 @ b94a09ee5: IDENTICAL (sha 57e8f85c...)
f024-r7-plan.md                     @ b94a09ee5: IDENTICAL (sha b9015060...)
```
All 4 BYTE-IDENTICAL against their sources (G1).

```
$ git apply --check .remedy-wt/f024-r7-payloads/ledger.diff; echo "REAL_EXIT=$?"
REAL_EXIT=0
$ git apply .remedy-wt/f024-r7-payloads/ledger.diff; echo "REAL_EXIT=$?"
REAL_EXIT=0
```
`git apply --check` ran and exited 0 immediately before the real `git apply`, which also exited 0.
`.agent/plan.md` was rewritten whole with `shutil.copyfile` from the plan.md payload — never
retyped.

```
$ (bytes/sha256 of the files named in the block's G2 table, read at C2 via `git show <C2>:<path>`)
.agent/live_review.md bytes=309410 sha256=c87726f65f1d9a873f4a0a4d0e6ff14e45ee23f1cafd55572b71d19bc475978b match=True
.agent/plan.md         bytes=890    sha256=b9015060d84ca2b37971c639b97f4d2cc56d67201166f303baca3730b9b2c278 match=True
```
Both match the block's G2 table exactly.

```
$ (lines C2's own diff adds to .agent/live_review.md beginning "Gate: F024 R6 — ",
  via `git diff 6cf991aaf b650ced4b -- .agent/live_review.md`)
count=1
```
Matches the block's stated reading of 1 exactly (G2).

```
$ open_finding_ids(text) from scripts/rotate_live_review.py, over .agent/live_review.md's TEXT
  at 6cf991aaf and at b650ced4b (C2)
6cf991aaf open ids: ['R-1008']
b650ced4b (C2) open ids: ['R-1008']
```
Reads R-1008 alone at both, matching the block's stated reading exactly (G2).

```
$ bash -c 'python3 .remedy-wt/f024-r7-payloads/create_f024_evidence.py >
  .remedy-wt/f024-r7-worker/evidence.log 2>&1; echo "REAL_EXIT=$?"'
REAL_EXIT=0
```
Evidence log (A1), through the summary:
```
head b650ced4b1d0fef4c9156de0b217cbad7a76bef7
ancestry-path count 51
plain count 51
collected node ids 922, deselected 6
red control: unsafe among the real ids 0 []
red control: planted id -> a local absolute path
pytest exit 0, {'passed': 922, 'failed': 0, 'skipped': 0}, output_hash 98e425d245621d2ed583390d40be3a3d152a4221e3ea1fb538117ace0a109513
validate_verification_tests problems [] passed 922
is_valid_current_run True
validation_errors []
gates written: ['artifact_contract_gate.json', 'change_provenance_gate.json', 'commit_execution_gate.json', 'fresh_evidence_gate.json', 'runtime_integration_gate.json', 'final_verifier_report.json']
{
  "job_id": "f024r7e1001",
  "head_commit": "b650ced4b1d0fef4c9156de0b217cbad7a76bef7",
  "authority_count": 32,
  "partition": {"T001": 11, "T002": 11, "T003": 10},
  "commit_count": 51,
  "verdict": "PASS_WITH_RISKS",
  "manual_completion": true,
  "operator_attested_tasks": ["T001", "T002", "T003"],
  "total_passed": 922
}
```
The two ancestry counts (51, 51) are equal, and both read exactly two more than the reviewer's
dry-run reading of 49 at `6cf991aa`, exactly as the block states. 922 node ids collected, 6
deselected, matching the reviewer's dry run. Zero unsafe real ids; the planted red-control id
answers `a local absolute path`, matching. pytest exit 0 with 922 passed, 0 skipped, 0 failed,
matching. `validate_verification_tests` problem list EMPTY, `is_valid_current_run` True with no
validation errors — all matching the reviewer's dry-run readings.

The files under `.remedy-wt/f024-r7-evidence/` whose names end `_gate.json`, `_integrity.json` or
`final_verifier_report.json` (9 total, via `Path.iterdir()`):
`artifact_contract_gate.json`, `change_provenance_gate.json`, `commit_execution_gate.json`,
`final_verifier_report.json`, `fresh_evidence_gate.json`, `human_change_integrity.json`,
`manifest_integrity.json`, `postmortem_integrity.json`, `runtime_integration_gate.json`.

```
$ bash -c 'bash scripts/make_review_zip.sh --evidence-dir .remedy-wt/f024-r7-evidence >
  .remedy-wt/f024-r7-worker/package.log 2>&1; echo "REAL_EXIT=$?"'
REAL_EXIT=0
```
Package log (A2), decisive lines:
```
UNCHANGED: runtime_integration_gate.json — rebuilt from source; identical to existing
Evidence refresh completed for staged copy.
Observability index generated from staged bytes: evidence/current/self_run_observability_index.json
{"member_count": 5941, "authoritative_count": 32, "symlink_count": 0, "tombstone_count": 0,
 "final_path": "/home/decodeux/Repos/remedy-history/zips/remedy-review-20260925-082755-READY_FOR_REVIEW.zip",
 "final_sha256": "1c4b4b358b97b54252a665e60acd3eaaedb134b8b3b0cbbe5ee36d80e60289e6",
 "publication_capability": "SUPPORTED", "package_status": "READY_FOR_REVIEW",
 "evidence_authoritative": true, "review_subject_alignment": "PASS",
 "manifest_sha256": "eee877de8c7d8baa0c8b611eabdeab406343706dfefabb59f1c1bfe28a90a4d1"}
============================================
REVIEW_PACKAGE_CREATED=true
PACKAGE_STATUS=READY_FOR_REVIEW
EVIDENCE_AUTHORITATIVE=true
REVIEW_PACKAGE_DIR=/home/decodeux/Repos/remedy-history/zips
ZIP_PATH=/home/decodeux/Repos/remedy-history/zips/remedy-review-20260925-082755-READY_FOR_REVIEW.zip
============================================
29M	/home/decodeux/Repos/remedy-history/zips/remedy-review-20260925-082755-READY_FOR_REVIEW.zip
Included files: 5941
Branch: feature/f024-phase-timeline-scrubber
Commit: b650ced4b1d0fef4c9156de0b217cbad7a76bef7
```
`PACKAGE_STATUS=READY_FOR_REVIEW`. `EVIDENCE_AUTHORITATIVE=true`. Filename
`remedy-review-20260925-082755-READY_FOR_REVIEW.zip`, sha256
`1c4b4b358b97b54252a665e60acd3eaaedb134b8b3b0cbbe5ee36d80e60289e6` (tool's own printed value,
independently reconfirmed by a full-file re-hash in a scratch script: identical). Archived to
`/home/decodeux/Repos/remedy-history/zips`.

```
$ (zipfile.is_zipfile, ZipFile.testzip(), and .review_zip_manifest.json inside the package)
is_zipfile: True
testzip(): None
committed_review_subject.base_commit: 1bb3a35dc9f69e98c651931b5214c30d1558fbd0
committed_review_subject.head_commit: b650ced4b1d0fef4c9156de0b217cbad7a76bef7
committed_review_subject.commit_count: 51
```
`head_commit` equals C2's full sha exactly. `base_commit` equals the fork point exactly.

```
$ python3 -m apps.cli.main integrity check --json; echo "REAL_EXIT=$?"
{"check_count": 6, "checks": [
  {"name": "handler_import", "status": "pass", "message": "handlers=157"},
  {"name": "live_review_verdict", "status": "pass", "message": "last Gate verdict PASS"},
  {"name": "plan_consistency", "status": "pass", "message": "unchecked=0, context_complete=False"},
  {"name": "relevant_untracked", "status": "pass", "message": "untracked=0, relevant=0"},
  {"name": "repo_root_hygiene", "status": "pass", "message": "no reviewer scratch, evidence dir or archive at the root"},
  {"name": "high_blockers_open", "status": "pass", "message": "no open blocker/high findings"}
], "fail_count": 0, "ok": true, "passed": true, "schema_version": 1, "version": 1}
REAL_EXIT=0
```
All six checks `pass`, `fail_count` 0 (G5). `git status --porcelain` empty immediately after, no
relevant untracked file.

```
$ git diff --name-only 6cf991aa HEAD
.agent/authored/f024-r7-block.md
.agent/authored/f024-r7-create_f024_evidence.py
.agent/authored/f024-r7-ledger.diff
.agent/authored/f024-r7-plan.md
.agent/live_review.md
.agent/plan.md
```
Exactly the tracked path set constraint 3 names, through C2 (this handback's own commit adds
`.agent/handoff.md`, the only remaining member of the named set).

## Evidence and package summary

Evidence job id `f024r7e1001`, base commit `1bb3a35dc9f69e98c651931b5214c30d1558fbd0` (the fork
point), head commit `b650ced4b1d0fef4c9156de0b217cbad7a76bef7` (C2, the accepted HEAD), step range
T001-T003, run id `vr-1053`, SCOPED per the script's own docstring. Real exit 0; 922 passed, 0
failed, 0 skipped; `is_valid_current_run` True with no validation errors. Review package
`remedy-review-20260925-082755-READY_FOR_REVIEW.zip`, sha256
`1c4b4b358b97b54252a665e60acd3eaaedb134b8b3b0cbbe5ee36d80e60289e6`, archived to
`/home/decodeux/Repos/remedy-history/zips`, `PACKAGE_STATUS=READY_FOR_REVIEW`,
`EVIDENCE_AUTHORITATIVE=true`, manifest base/head/commit-count all matching. Nothing closed or
merged this round.

## Authored-text proofs

All 4 authored copies under `.agent/authored/f024-r7-*` (the block copy,
`create_f024_evidence.py`, `ledger.diff`, `plan.md`) were built by `shutil.copyfile` from source to
destination — never retyped, never edited. Each was read back with `git show <C1>:<path>` and
compared byte for byte against its source: all 4 BYTE-IDENTICAL (G1 above). `ledger.diff` was
applied with `git apply` after `git apply --check` passed (exit 0, both). `.agent/plan.md` was
rewritten whole via `shutil.copyfile` from the plan.md payload source — never retyped — and
confirmed MATCH against both the PAYLOADS table and the G2 table. `create_f024_evidence.py` was run
unedited, directly from the payload directory, as the block's TOOL designation requires.

## Deviations & assumptions

None. Both content commits landed in the block's stated order — C1, C2 — followed by A1 (the
evidence job) and A2 (the review package), both actions committing nothing, exactly as the block's
BUNDLE ordering "C1, C2, A1, A2, C3" specifies. No payload was edited, retyped or repaired. G1
through G5 ran before C3 was written, per the block's instruction ("G1 to G5 run before C3 is
written"). The package read `READY_FOR_REVIEW` on its first build — no repair or workaround was
needed. No worktree was added or removed this round; every worktree named in constraint 6
(`f015-r*`, `f020-r*`, `f023-r*`, `f284-r*`, `job-*`, and the reviewer's own `f024-r7-sim`/
`f024-r7-dry`, plus rounds 1 through 6's dry/sim worktrees) was left untouched. No `git stash` was
used, nothing was merged, no pull request was created, no force-push occurred, no `STATUS.md` edit,
no README edit, no ledger rotation.

## Item-status table

| Item | Status | Reason |
|---|---|---|
| C1 | done | 376 insertions, matches block's expectation exactly (170+206); well under the 500-insertion STOP threshold |
| C2 | done | ledger.diff apply --check and apply both exit 0; 2/0, 4/7 insertions/deletions match exactly; sha `b650ced4b1d0fef4c9156de0b217cbad7a76bef7` recorded as ACCEPTED HEAD |
| PUSH (post-C2) | done | `6cf991aaf..b650ced4b`, real exit 0, before A1 |
| A1 | done | evidence job real exit 0; ancestry 51/51 equal (two more than the reviewer's 49); 922 collected/6 deselected; 0 unsafe; pytest 922 passed/0 failed/0 skipped; validate_verification_tests EMPTY; is_valid_current_run True |
| A2 | done | package real exit 0; PACKAGE_STATUS=READY_FOR_REVIEW; EVIDENCE_AUTHORITATIVE=true; manifest base/head/commit-count match; testzip() None |
| G1 | done | all 3 payload digests and 4 authored-copy comparisons matched |
| G2 | done | both named file digests matched; Gate-line count 1 and open-id set R-1008 both matched |
| G3 | done | A1's full reading recorded above; 9 gate/integrity/final-verifier files enumerated |
| G4 | done | PACKAGE_STATUS, EVIDENCE_AUTHORITATIVE, filename, sha256, manifest base/head/commit-count, zip checks all recorded above |
| G5 | done | integrity check 6/6 pass, fail_count 0; tree clean after |
| C3 | done | this handback, written together with the evidence and package readings |
| G6 | pending | reported in the final reply, since C3 cannot contain it |

## Next

Phase 1 rule 1: read `.agent/STOP` from disk. Then the review of round 7. Then the closing round:
the booking of round 7, the ledger rotation, the STATUS line with the README counters in the same
commit, and the pull request. Open findings: 1. Operator questions open: 3.
