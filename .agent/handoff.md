# Handback — F039, round 12: the closure sequence's evidence round

## Session

SESSION 2 of feature F039 · round 12 · rounds so far 12. This session ran round 12 only: copying
the block and its three payloads into `.agent/authored/`, booking round 11's PASS verdict with
R-1104's registration (owned by F286) and the self-use run's Built State paragraph, then running
the closure protocol's algorithm steps 1 and 2 — the evidence job and the review package — at the
accepted head. Context self-assessment: a comfortable margin remained through the whole round —
the block and AGENTS.md were read whole before any edit, every payload was verified before use,
`booking.diff` applied clean on the first try, the numstat and hash gates all matched their tables
on the first read, the evidence job and the package build each completed in well under a minute
with no repair needed, and the integrity check read clean on the first run; the work was not near
its limit.

For the operator, in plain words: round 12 booked round 11's PASS verdict, registered R-1104 (Low,
owned by F286 — the staleness catalog's config-key check misreads the guide's backticked file name
`story.html` as an unregistered config key) and recorded the closure's self-use run in F039's Built
State. It then built the evidence bundle and the review package at the accepted head, `da3d5430`.
Both gates read clean: the evidence job's two ancestry counts agreed at 90, its red controls read
correctly, and pytest passed all 1073 collected node ids; the package read
`PACKAGE_STATUS=READY_FOR_REVIEW` with `EVIDENCE_AUTHORITATIVE=true`. Nothing was merged and no PR
was created, per the block's constraint 5.

## Range

Review of 3b1f27e8a..HEAD

## Commits

### a3c8bf02b F039 R12 C1: copy round 12 block and payloads
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f039-r12-block.md | +159/-0 | verbatim copy of this round's block |
| .agent/authored/f039-r12-booking.diff | +45/-0 | verbatim copy of the booking payload |
| .agent/authored/f039-r12-create_f039_evidence.py | +170/-0 | verbatim copy of the evidence-tool payload |
| .agent/authored/f039-r12-plan.md | +27/-0 | verbatim copy of the plan payload |

Measured insertions: 401 (159 + 45 + 170 + 27), matching the block's expectation of "this block's
line count plus 242" (159 + 242 = 401) exactly. Under the 500-line cap; no split needed.

### da3d54306 (da3d5430681239aff3419da447abbb75f2105112) F039 R12 C2: book round 11, register R-1104 for F286, add the self-use run to the Built State
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +4/-0 | F039 R11 gate entry (PASS) and R-1104's registration, owned by F286 |
| .agent/plan.md | +3/-3 | rewritten to round 12's current step (this evidence round) |
| docs/roadmap/features/T2_F286.md | +3/-0 | R-1104's Acceptance line |
| docs/roadmap/features/T5_F039.md | +8/-0 | the self-use run's Built State paragraph |

Measured: 4/0, 3/3, 3/0, 8/0 — matching the block's expectation exactly. This is the closure's
ACCEPTED HEAD: `da3d5430681239aff3419da447abbb75f2105112`. Pushed immediately after this commit,
before A1, per the block's instruction.

### (this commit) F039 R12 C3: rewrite handoff for round 12 with the evidence and package readings
| Path | Reason |
|---|---|
| .agent/handoff.md | rewritten per the template (self-reference exception, R-0149 pattern) |

## External actions

- `git push -u origin feature/f039-story-replay-mode` (after C2) — outcome:
  `3b1f27e8a..da3d54306  feature/f039-story-replay-mode -> feature/f039-story-replay-mode`, branch
  set to track the remote, real exit 0.
- A1: `python3 .remedy-wt/f039-r12-payloads/create_f039_evidence.py`, an action committing nothing,
  writing the evidence bundle to `.remedy-wt/f039-r12-evidence/` (gitignored). Real exit 0.
- A2: `bash scripts/make_review_zip.sh --evidence-dir .remedy-wt/f039-r12-evidence`, an action
  committing nothing, without `REMEDY_REVIEW_DIR` set, writing the package to the operator's
  archive at `/home/decodeux/Repos/remedy-history/zips/`. Real exit 0.
- No PR created, no merge, no force-push, no amend, no checkout of another branch, no stash — all
  forbidden by the block and none attempted. `git worktree list | wc -l` read 61 before and after
  the round, unchanged; nothing was deleted that this worker did not create. The final `gh pr list`
  reading goes in the reply per the block (G6 cannot appear in this file since C3 cannot contain
  it).

## Verification

### BEFORE ANYTHING ELSE (block steps 1-4)
```
$ ls .agent/STOP
ls: cannot access '.agent/STOP': No such file or directory
REAL_EXIT=2
$ pwd
/home/decodeux/Repos/remedy
$ git status --porcelain
(empty)
$ git branch --show-current
feature/f039-story-replay-mode
$ git log --oneline -1
3b1f27e8a F039 R11 C4: rewrite handoff for round 11
```
Block bytes: measured line count (newline count) 159 / given 159; measured sha256
`d3e4f29a285a8804a7605e21e90937fd0fc288fd235cdf8d9f8b8d83415999a0` / given the same — MATCH.
`git worktree list | wc -l` at step 4: 61.

### PAYLOADS table
| file | lines measured/given | bytes measured/given | sha256 match |
|---|---|---|---|
| booking.diff | 45/45 | 9499/9499 | match |
| create_f039_evidence.py | 170/170 | 8244/8244 | match |
| plan.md | 27/27 | 913/913 | match |

### G1 TRANSPORT
- booking.diff: 45 lines, 9499 bytes, sha256 `d73f49c6052a8eea00a0cb7790b997aa2c9711cd48259d8f3b204d155c5dfd6c` — matches PAYLOADS table.
- create_f039_evidence.py: 170 lines, 8244 bytes, sha256 `e5c44627b7ee018e063ce97014210c1efcfbc6a5d54b740a365c5b3a7f185280` — matches PAYLOADS table.
- plan.md: 27 lines, 913 bytes, sha256 `bcf9fb66b49cc11ec03026a82f746ab0851bc2c1e0578dc2dacd81d32224475e` — matches PAYLOADS table.
- `git show a3c8bf02b:.agent/authored/f039-r12-block.md` sha256 `d3e4f29a285a8804a7605e21e90937fd0fc288fd235cdf8d9f8b8d83415999a0` == `.remedy-wt/f039-r12/block.md`: byte-identical.
- `git show a3c8bf02b:.agent/authored/f039-r12-booking.diff` sha256 `d73f49c6052a8eea00a0cb7790b997aa2c9711cd48259d8f3b204d155c5dfd6c` == `.remedy-wt/f039-r12-payloads/booking.diff`: byte-identical.
- `git show a3c8bf02b:.agent/authored/f039-r12-create_f039_evidence.py` sha256 `e5c44627b7ee018e063ce97014210c1efcfbc6a5d54b740a365c5b3a7f185280` == `.remedy-wt/f039-r12-payloads/create_f039_evidence.py`: byte-identical.
- `git show a3c8bf02b:.agent/authored/f039-r12-plan.md` sha256 `bcf9fb66b49cc11ec03026a82f746ab0851bc2c1e0578dc2dacd81d32224475e` == `.remedy-wt/f039-r12-payloads/plan.md`: byte-identical.

### G2 THE BOOKING
At C2 (`da3d5430681239aff3419da447abbb75f2105112`):
| path | bytes | sha256 | matches table |
|---|---|---|---|
| .agent/live_review.md | 370530 | 9f76064aa4acafaf43c2e889d4e6e3b30e9f6363877cb8a446a751cfdb3db9bc | yes |
| .agent/plan.md | 913 | bcf9fb66b49cc11ec03026a82f746ab0851bc2c1e0578dc2dacd81d32224475e | yes |
| docs/roadmap/features/T2_F286.md | 2779 | 682fd256a4a747c5c14b49b01abdcfc33ab123bca2e009427279eb77bbec0c10 | yes |
| docs/roadmap/features/T5_F039.md | 10457 | 3235a4439563ef84027ad5d51fa42bb0ed4877b35c3a08072a01e0dfcf2945b9 | yes |

`open_finding_ids(text)` over the ledger at C2 = `['R-1104']`; `latest_gate_verdict(text)` = `PASS`
— both match the block's stated readings exactly (read via `scripts/rotate_live_review.py` with
`scripts` on `sys.path`, over `.agent/live_review.md` at C2).

```
$ bash -c 'python3 -m pytest -q -p no:cacheprovider tests/docs/ tests/cli/test_golden_path.py 2>&1 | tail -3; echo "REAL_EXIT=${PIPESTATUS[0]}"'
........................................................................ [ 97%]
.........                                                                [100%]
369 passed in 58.20s
REAL_EXIT=0
```
Exactly the reviewer's own stated reading of 369 passed at exit 0.

### G3 THE BUNDLE (A1)
```
$ bash -c 'python3 .remedy-wt/f039-r12-payloads/create_f039_evidence.py > .remedy-wt/f039-r12-worker/evidence.log 2>&1; echo "REAL_EXIT=$?"'
REAL_EXIT=0
```
Log contents in full:
```
head da3d5430681239aff3419da447abbb75f2105112
ancestry-path count 90
plain count 90
collected node ids 1073, deselected 2
red control: unsafe among the real ids 0 []
red control: planted id -> a local absolute path
pytest exit 0, {'passed': 1073, 'failed': 0, 'skipped': 0}, output_hash a8f18011f79262980b0a16b35d24fb22ede7ca34bf0f3da98069b3edf03acaa7
validate_verification_tests problems [] passed 1073
is_valid_current_run True
validation_errors []
gates written: ['artifact_contract_gate.json', 'change_provenance_gate.json', 'commit_execution_gate.json', 'fresh_evidence_gate.json', 'runtime_integration_gate.json', 'final_verifier_report.json']
{
  "job_id": "f039r12e1001",
  "head_commit": "da3d5430681239aff3419da447abbb75f2105112",
  "authority_count": 57,
  "partition": {"T001": 19, "T002": 19, "T003": 19},
  "commit_count": 90,
  "verdict": "PASS_WITH_RISKS",
  "manual_completion": true,
  "operator_attested_tasks": ["T001", "T002", "T003"],
  "total_passed": 1073
}
```
The two ancestry counts (ancestry-path 90, plain 90) agree, each exactly two more than the
reviewer's dry-run reading of 88 at `3b1f27e8`, as the block predicted for C2. Collected 1073 node
ids with 2 deselected, matching the reviewer's dry run exactly. Red controls: 0 unsafe among real
ids, the planted id answering "a local absolute path" — both matching. pytest exit 0, 1073 passed,
0 failed, 0 skipped. `output_hash` `a8f18011f79262980b0a16b35d24fb22ede7ca34bf0f3da98069b3edf03acaa7`.
`validate_verification_tests` problem list empty (1073 passed). `is_valid_current_run` True, no
validation errors. Six gate files written:
`artifact_contract_gate.json`, `change_provenance_gate.json`, `commit_execution_gate.json`,
`fresh_evidence_gate.json`, `runtime_integration_gate.json`, `final_verifier_report.json` — all
present under `.remedy-wt/f039-r12-evidence/` alongside the rest of the bundle (28 files/dirs total,
gitignored).

### G4 THE PACKAGE (A2)
```
$ bash -c 'bash scripts/make_review_zip.sh --evidence-dir .remedy-wt/f039-r12-evidence > .remedy-wt/f039-r12-worker/zip.log 2>&1; echo "REAL_EXIT=$?"'
REAL_EXIT=0
```
Log's summary block:
```
REVIEW_PACKAGE_CREATED=true
PACKAGE_STATUS=READY_FOR_REVIEW
PACKAGING_CWD=/home/decodeux/Repos/remedy
EVIDENCE_DIR=.remedy-wt/f039-r12-evidence
REVIEW_SUBJECT_ALIGNMENT=PASS
EVIDENCE_AUTHORITATIVE=true
REVIEW_PACKAGE_DIR=/home/decodeux/Repos/remedy-history/zips
ZIP_PATH=/home/decodeux/Repos/remedy-history/zips/remedy-review-20260929-031523-READY_FOR_REVIEW.zip
```
`PACKAGE_STATUS=READY_FOR_REVIEW` (the required reading, not merely exit 0); `EVIDENCE_AUTHORITATIVE=true`.
Package filename `remedy-review-20260929-031523-READY_FOR_REVIEW.zip`, SHA-256
`e9097684c735ec44a6b33f4bc409de252280e7294e3d2d142b4197684f9dee7d` (re-measured directly with
`sha256sum` against the archived file — matches the log's `final_sha256`). Archived directory
`/home/decodeux/Repos/remedy-history/zips`.

Manifest inside the package (`.review_zip_manifest.json`), `committed_review_subject`:
`base_commit` `4d60eb84ede7ec3371d18ccf0782a9e34eea8787` (the FORK POINT), `head_commit`
`da3d5430681239aff3419da447abbb75f2105112` (== C2's full sha), `base_is_ancestor` true,
`commit_count` 90, `file_count` 137, `tombstones` `[]`.
`zipfile.is_zipfile(path)` → `True`; `zf.testzip()` → `None`.

### G5 THE TREE (after A2)
```
$ bash -c 'python3 -m apps.cli.main integrity check --json 2>&1; echo "REAL_EXIT=$?"'
{"check_count": 6, "checks": [
  {"name": "handler_import", "status": "pass", "message": "handlers=169"},
  {"name": "live_review_verdict", "status": "pass", "message": "last Gate verdict PASS"},
  {"name": "plan_consistency", "status": "pass", "message": "unchecked=0, context_complete=False"},
  {"name": "relevant_untracked", "status": "pass", "message": "untracked=0, relevant=0"},
  {"name": "repo_root_hygiene", "status": "pass", "message": "no reviewer scratch, evidence dir or archive at the root"},
  {"name": "high_blockers_open", "status": "pass", "message": "no open blocker/high findings"}
], "fail_count": 0, "ok": true, "passed": true, "schema_version": 1, "version": 1}
REAL_EXIT=0
```
All six checks read `pass`, `fail_count` 0, exit 0.
```
$ git status --porcelain
(empty)
$ git worktree list | wc -l
61
```

## Authored-text proofs

| payload | committed at | disk-to-disk vs source | result |
|---|---|---|---|
| block.md copy | a3c8bf02b | `.agent/authored/f039-r12-block.md` vs `.remedy-wt/f039-r12/block.md` | byte-identical |
| booking.diff copy | a3c8bf02b | `.agent/authored/f039-r12-booking.diff` vs `.remedy-wt/f039-r12-payloads/booking.diff` | byte-identical |
| create_f039_evidence.py copy | a3c8bf02b | `.agent/authored/f039-r12-create_f039_evidence.py` vs `.remedy-wt/f039-r12-payloads/create_f039_evidence.py` | byte-identical |
| plan.md copy | a3c8bf02b | `.agent/authored/f039-r12-plan.md` vs `.remedy-wt/f039-r12-payloads/plan.md` | byte-identical |
| booking.diff application | da3d54306 | `git apply --check` then `git apply`, both exit 0; C2's four files' bytes/sha256 vs the G2 table | all match |
| plan.md rewrite | da3d54306 | `.agent/plan.md` := payload plan.md via `shutil.copyfile`, bytes/sha256 vs the PAYLOADS/G2 table | match |
| create_f039_evidence.py execution | A1 | run verbatim, unedited, from `.remedy-wt/f039-r12-payloads/create_f039_evidence.py`; no line retyped | N/A (tool run, not applied as text) |

## Item Status

| Item | Status | Reason |
|---|---|---|
| C1 | done | |
| C2 | done | pushed immediately after; is the ACCEPTED HEAD |
| A1 (evidence job) | done | exit 0; ancestry 90/90; 1073 passed; PASS_WITH_RISKS |
| A2 (review package) | done | exit 0; PACKAGE_STATUS=READY_FOR_REVIEW |
| C3 | done | this handback |
| G1 transport | done | |
| G2 the booking | done | open_finding_ids=['R-1104'], latest_gate_verdict=PASS; 369 passed |
| G3 the bundle | done | see above |
| G4 the package | done | READY_FOR_REVIEW, EVIDENCE_AUTHORITATIVE=true, head==C2 |
| G5 the tree | done | integrity 6/6 pass; tree clean; worktrees 61 |
| G6 push and PR gate | done | reported in the reply |
| R-1104 | done (registered) | Owner F286, Acceptance line added at C2 |

## Deviations & assumptions

None. Every commit and action ran in the block's ordered sequence (C1, C2, A1, A2, C3); no commit
reached the 500-line cap, so none was split; the tracked path set after this commit matches
constraint 3 exactly (the `.agent/authored/f039-r12-*` copies, `.agent/live_review.md`,
`.agent/plan.md`, `docs/roadmap/features/T2_F286.md`, `docs/roadmap/features/T5_F039.md` and
`.agent/handoff.md` — no evidence directory, no package, no queue file); nothing was merged, no PR
was created, no STATUS or README edit was made, and no worktree or branch that this worker did not
itself create as scratch was touched or deleted. One incidental note: while checking that C1's copy
script was idempotent, this worker re-ran it a second time before staging; it re-wrote the same four
files with byte-identical content (verified: `git status --porcelain` read empty immediately after),
so it left no trace on the committed state — recorded here for completeness, not because it changed
anything.

## Next

Phase 1 rule 1: read `.agent/STOP` from disk before anything else. Then the review of round 12 —
the booking of round 11 with R-1104 (owned by F286) and the self-use run's Built State paragraph,
and the evidence bundle and review package built at the accepted head `da3d5430`. Then the closing
round: the booking of round 12, the ledger rotation, the STATUS line with the README counters in
the same commit, the self-use item's `consumed_by`, and the pull request. Open-findings count: 1
(`['R-1104']`, as `open_finding_ids` reads it at C2). Operator questions open: 1.
