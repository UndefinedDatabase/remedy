# Handback — F026 Task edit at runtime · Round 7

## Session

SESSION 1 of feature F026 · round 7 · rounds so far 7

A large fraction of the session's context budget remained by the point this handback was
written. This round booked round 6's PASS verdict, resolved R-1062 and R-1063, registered R-1064
for F285, brought the Built State's findings paragraph current, then built the feature's evidence
bundle against the fork point and the fresh review package. Nothing closed this round.

## Range

Review of 436ff8a05..HEAD

## Commits

### df690e7fb F026 R7 C1: copy round 7 block and payloads
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f026-r7-block.md | +137/-0 | copy of this round's block, verbatim (`shutil.copyfile`) |
| .agent/authored/f026-r7-create_f026_evidence.py | +174/-0 | copy of the evidence-job tool payload |
| .agent/authored/f026-r7-plan.md | +29/-0 | copy of the plan.md payload |
| .agent/authored/f026-r7-records.diff | +46/-0 | copy of the records.diff payload |

386 insertions by `git show --numstat` — the block's stated expectation (this block's own line
count, 137, plus 249: 174+29+46 = 249) — matches exactly.

### 3cb0798d2 F026 R7 C2: book round 6, resolve R-1062 and R-1063, register R-1064 for F285
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +8/-0 | records.diff: the F026 R6 gate entry, R-1062's and R-1063's `Done:` paragraphs, and R-1064's registration appended |
| .agent/plan.md | +9/-11 | rewritten whole to the plan.md payload (`shutil.copyfile`) |
| docs/roadmap/features/T2_F285.md | +3/-0 | records.diff: R-1064's Acceptance line appended after R-1058's |
| docs/roadmap/features/T5_F026.md | +8/-0 | records.diff: one paragraph appended after the Built State's findings, naming R-1061/R-1062/R-1063 resolved and R-1064 owned by F285 |

8/0, 9/11, 3/0, 8/0 — matches the block's G2 stated expectation exactly. `git apply --check` on
records.diff: exit 0; `git apply`: exit 0. This commit's full sha, `3cb0798d20a293f9954074ff9b2c4ae32704035c`,
is this closure's ACCEPTED HEAD. Pushed to `origin/feature/f026-task-edit-runtime` immediately
after this commit, before A1, per the block.

### (pending) F026 R7 C3: rewrite handoff for round 7 with the evidence and package readings
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | measured after this commit exists, in the final reply | this handback (self-reference, R-0149 pattern) |

## External actions

- `git push origin feature/f026-task-edit-runtime` after C2 (`3cb0798d2`), before A1 — outcome:
  `436ff8a05..3cb0798d2  feature/f026-task-edit-runtime -> feature/f026-task-edit-runtime`, real
  exit 0.
- A1, the evidence job (`python3 .remedy-wt/f026-r7-payloads/create_f026_evidence.py`) — an action
  committing nothing; wrote `.remedy-wt/f026-r7-evidence/` (gitignored, not committed).
- A2, the review package (`bash scripts/make_review_zip.sh --evidence-dir
  .remedy-wt/f026-r7-evidence`), without `REMEDY_REVIEW_DIR` set — an action committing nothing;
  the package landed in the operator's archive at `/home/decodeux/Repos/remedy-history/zips`.
- `git push origin feature/f026-task-edit-runtime` after C3 — its real outcome is reported in the
  final reply, since the push happens after this commit.
- No `gh pr create` — the branch's pull request opens at F026's closure, per the block.
- No `git stash`, no force-push, no checkout of `main`, no branch deletion, no worktree
  add/remove, no `remedy/job-*` worktree or branch touched by this worker, no
  `npm install`/`npm ci`/`npx`.

## Verification

```
$ ls .agent/STOP
ls: cannot access '.agent/STOP': No such file or directory
(absent, checked before step one)
```

```
$ pwd
/home/decodeux/Repos/remedy
$ git status --porcelain
(empty)
$ git branch --show-current
feature/f026-task-edit-runtime
$ git log --oneline -1
436ff8a05 F026 R6 C5: record the closure suite on the repaired tree and rewrite handoff for round 6
```
All matched the block's stated readings exactly, before any commit of this round.

```
$ wc -l .remedy-wt/f026-r7/block.md; sha256sum .remedy-wt/f026-r7/block.md
line_count: 137
sha256: 4b1afbc2240881109c07fb0891ddcea7c3bcc9c7d7cd39706ebdf78af30f68c4
```
Matches both readings the delegation message gave exactly.

```
$ git worktree list
(reported at step 4: primary checkout + the pre-existing F015/F020/F023/F024/F025/F026-r6-dry/
F026-r6-sim/F026-r7-sim/F284 dry/sim worktrees, and the same remedy/job-* worktrees and branches
already present at session start — no stale/prunable entries observed)
```

### G1 — payload transport

```
$ wc -l/wc -c/sha256sum .remedy-wt/f026-r7-payloads/{create_f026_evidence.py,plan.md,records.diff}
create_f026_evidence.py  174 lines  9018 bytes  bdc953617bbd8e18053ecbd5156025fb9a7c3a342a4f70475f3fc0e49c7a255e
plan.md                   29 lines  1004 bytes  08df88f775293582011de55caf8d9d399b5c84aa5c4f13cee153aa819f94a4ca
records.diff               46 lines 10021 bytes  4c578b00a139df283acf34fa480fb08934df299ac481d797adc366454477f9a3
```
All three payloads' measured lines/bytes/sha256 matched the block's table exactly.

```
$ git show df690e7fb:.agent/authored/f026-r7-block.md | cmp -  .remedy-wt/f026-r7/block.md
BLOCK_EQUAL
$ git show df690e7fb:.agent/authored/f026-r7-create_f026_evidence.py | cmp - .remedy-wt/f026-r7-payloads/create_f026_evidence.py
EVID_EQUAL
$ git show df690e7fb:.agent/authored/f026-r7-plan.md | cmp - .remedy-wt/f026-r7-payloads/plan.md
PLAN_EQUAL
$ git show df690e7fb:.agent/authored/f026-r7-records.diff | cmp - .remedy-wt/f026-r7-payloads/records.diff
RECORDS_EQUAL
```
Each `.agent/authored/f026-r7-*` copy, read back with `git show df690e7fb:<path>`, is
byte-identical to its `.remedy-wt/f026-r7(-payloads)/` source.

### G2 — the booking

```
$ git show 3cb0798d2:.agent/live_review.md | wc -c; sha256sum
344410  44dc95efbfdf4b6b4b6da4c0dc48d80bf997c9164f528d4f3ed854002f06e4e5
$ git show 3cb0798d2:.agent/plan.md | wc -c; sha256sum
1004    08df88f775293582011de55caf8d9d399b5c84aa5c4f13cee153aa819f94a4ca
$ git show 3cb0798d2:docs/roadmap/features/T5_F026.md | wc -c; sha256sum
10951   d57d3a775006ed6ea8eedaa832442b6ebdec7d43e91a02d4f5918502dcf0a431
$ git show 3cb0798d2:docs/roadmap/features/T2_F285.md | wc -c; sha256sum
3337    7624be55be8c172809a578e31ab09ccfe51b3a00488864c10c3c54338a01e45f
```
All four equal the block's stated G2 table exactly.

```
$ python3 -c "from rotate_live_review import open_finding_ids; print(open_finding_ids(open('.agent/live_review.md').read()))"
['R-1008', 'R-1055', 'R-1057', 'R-1058', 'R-1064']
```
Matches the block's stated reading exactly (read at C2, `3cb0798d2`).

```
$ python3 -m pytest -q -p no:cacheprovider tests/docs/ tests/cli/test_golden_path.py
369 passed in 36.30s
REAL_EXIT=0
```
Matches the block's stated reading of `369 passed` exactly.

### G3 — the bundle, at A1

```
$ bash -c 'python3 .remedy-wt/f026-r7-payloads/create_f026_evidence.py > .remedy-wt/f026-r7-worker/evidence.log 2>&1; echo "REAL_EXIT=$?"'
REAL_EXIT=0
```
Log, up to the summary:
```
head 3cb0798d20a293f9954074ff9b2c4ae32704035c
ancestry-path count 48
plain count 48
collected node ids 1543, deselected 5
red control: unsafe among the real ids 0 []
red control: planted id -> a local absolute path
pytest exit 0, {'passed': 1543, 'failed': 0, 'skipped': 0}, output_hash 668b2fedf0ab5070a57bcfecdde92a7b677ed453bcf68500677bf3dbc89bcb0b
validate_verification_tests problems [] passed 1543
is_valid_current_run True
validation_errors []
gates written: ['artifact_contract_gate.json', 'change_provenance_gate.json', 'commit_execution_gate.json', 'fresh_evidence_gate.json', 'runtime_integration_gate.json', 'final_verifier_report.json']
```
Ancestry-path count and plain count are equal (48 = 48), two more than the reviewer's dry-run
reading of 46 at `436ff8a05`, exactly as the block predicted. Collected node ids 1543 with 5
deselected, matching the reviewer's dry run exactly. The red control found 0 unsafe among the real
ids and the planted id still answers "a local absolute path". Pytest exit 0 with 1543 passed, 0
failed, 0 skipped, matching the reviewer's dry-run counts exactly.
`validate_verification_tests` returned an empty problem list; `is_valid_current_run` True with no
validation errors. The evidence directory holds (beyond the gate files the tool prints):
`artifact_contract_gate.json`, `change_provenance_gate.json`, `commit_execution_gate.json`,
`context_strategy.json`, `current_change_content_proof.json`, `execution_config.json`,
`final_job_review.json`, `final_verifier_report.json`, `fresh_evidence_gate.json`,
`human_change_integrity.json`, `job_report.json`, `job_timeline.json`, `manifest_integrity.json`,
`manifest.json`, `postmortem_integrity.json`, `prompt_trace_summary.json`,
`review_commit_chain.json`, `review_commit_patches/`, `review_subject.json`,
`runtime_integration_gate.json`, `scratch_file_guard.json`, `target_guard.json`, `task_runs/`,
`tasks.json`, `token_truth.json`, `verification_tests.json`, `workspace_apply.json`,
`workspace.diff`.

### G4 — the package, at A2

```
$ bash scripts/make_review_zip.sh --evidence-dir .remedy-wt/f026-r7-evidence
...
{"member_count": 6089, "authoritative_count": 49, "symlink_count": 0, "tombstone_count": 0,
 "final_path": "/home/decodeux/Repos/remedy-history/zips/remedy-review-20260925-224758-READY_FOR_REVIEW.zip",
 "final_sha256": "8a9aa2d963b00ecad738490efc6df69df72dc782252a2c0f9f16d6cfb9cd6bc8",
 "publication_capability": "SUPPORTED", "package_status": "READY_FOR_REVIEW",
 "evidence_authoritative": true, "review_subject_alignment": "PASS",
 "manifest_sha256": "c07df3c85273182dc21ad124803a74acb1a1f3c01e3ec33c36d98fe8339806cc"}
============================================
REVIEW_PACKAGE_CREATED=true
PACKAGE_STATUS=READY_FOR_REVIEW
EVIDENCE_AUTHORITATIVE=true
REVIEW_PACKAGE_DIR=/home/decodeux/Repos/remedy-history/zips
ZIP_PATH=/home/decodeux/Repos/remedy-history/zips/remedy-review-20260925-224758-READY_FOR_REVIEW.zip
============================================
REAL_EXIT=0
```
`PACKAGE_STATUS=READY_FOR_REVIEW` (the reading, not merely exit 0); `EVIDENCE_AUTHORITATIVE=true`.
Package filename `remedy-review-20260925-224758-READY_FOR_REVIEW.zip`; independently re-hashed:
`sha256sum` → `8a9aa2d963b00ecad738490efc6df69df72dc782252a2c0f9f16d6cfb9cd6bc8` (equal to the
tool's own `final_sha256`).

```
$ python3 -c "import zipfile,json; z=zipfile.ZipFile(...); print(zipfile.is_zipfile(p), z.testzip()); d=json.loads(z.read('.review_zip_manifest.json')); print(d['committed_review_subject'])"
is_zipfile True
testzip None
base 905558493f1ff6570493a8b212a741ab59242a4a
head 3cb0798d20a293f9954074ff9b2c4ae32704035c
```
`committed_review_subject` inside the package: base `905558493f1ff6570493a8b212a741ab59242a4a`
(the fork point) and head `3cb0798d20a293f9954074ff9b2c4ae32704035c` (equal to C2's full sha, the
accepted head). `zipfile.is_zipfile` True, `testzip()` None.

The archived directory: `/home/decodeux/Repos/remedy-history/zips` (not `NOT ARCHIVED` — the tool
moved the package there itself).

### G5 — the tree, after A2

```
$ python3 -m apps.cli.main integrity check --json
{"check_count": 6, "checks": [
  {"name": "handler_import", "status": "pass", "message": "handlers=160"},
  {"name": "live_review_verdict", "status": "pass", "message": "last Gate verdict PASS"},
  {"name": "plan_consistency", "status": "pass", "message": "unchecked=0, context_complete=False"},
  {"name": "relevant_untracked", "status": "pass", "message": "untracked=0, relevant=0"},
  {"name": "repo_root_hygiene", "status": "pass", "message": "no reviewer scratch, evidence dir or archive at the root"},
  {"name": "high_blockers_open", "status": "pass", "message": "no open blocker/high findings"}
], "fail_count": 0, "ok": true, "passed": true}
```
Six `pass`, `fail_count` 0.

```
$ git status --porcelain
(empty)
$ git worktree list
(primary checkout + the pre-existing worktrees, unchanged from the pre-round reading; none added
or removed this round)
```

## Authored-text proofs

`.agent/authored/f026-r7-block.md`, `f026-r7-create_f026_evidence.py`, `f026-r7-plan.md` and
`f026-r7-records.diff` (at C1) were built with `shutil.copyfile` from the reviewer's payload
files — never retyped, never edited — and G1 compared every one byte for byte, read back with
`git show df690e7fb:<path>`, against its source: all four BYTE-IDENTICAL. `.agent/plan.md` was
REWRITTEN whole (verbatim to the `plan.md` payload) at C2; `records.diff` was applied verbatim
with `git apply --check` then `git apply`, never retyped or hand-edited — G2's byte/sha256 table
on the resulting `.agent/live_review.md`, `.agent/plan.md`, `docs/roadmap/features/T5_F026.md` and
`docs/roadmap/features/T2_F285.md` confirms the applied result matches the reviewer's own target
state exactly. `create_f026_evidence.py` was run unedited from the payload directory at A1 (never
copied into the working tree and executed from there, never retyped).

## Deviations & assumptions

None. Every commit followed the block's ordered bundle exactly (C1, C2, A1, A2, then C3, inside
which this handback lives); no payload was edited or retyped; `git apply --check` read exit 0
before `git apply`; both commits stayed under the 500-insertion cap; no commit touched a path
outside constraint 3's tracked set (confirmed by `git diff --name-only 436ff8a05` below); no gate
went red; no evidence directory was committed; nothing was merged or closed; no STATUS, README or
`consumed_by` edit; no worktree or `remedy/job-*` branch touched.

```
$ git diff --name-only 436ff8a05
.agent/authored/f026-r7-block.md
.agent/authored/f026-r7-create_f026_evidence.py
.agent/authored/f026-r7-plan.md
.agent/authored/f026-r7-records.diff
.agent/handoff.md
.agent/live_review.md
.agent/plan.md
docs/roadmap/features/T2_F285.md
docs/roadmap/features/T5_F026.md
```
(measured again after C3, before push, in the final reply) Exactly constraint 3's named path set:
the `.agent/authored/f026-r7-*` copies, `.agent/live_review.md`, `.agent/plan.md`,
`docs/roadmap/features/T5_F026.md`, `docs/roadmap/features/T2_F285.md` and `.agent/handoff.md`. No
evidence directory appears; no STATUS, README, `self_use_queue.json` or `candidates.md` edit
appears.

## Item-status table

| Item | Status | Reason |
|---|---|---|
| C1 | done | 386 insertions (137+249), matches the block's expectation exactly; all four copies byte-identical |
| C2 | done | `git apply --check`/`git apply` both exit 0; per-file numstat 8/0, 9/11, 3/0, 8/0 matches the G2 table exactly; open-finding set gains R-1064, loses R-1062 and R-1063; pushed before A1 |
| A1 | done | evidence job exit 0; ancestry/plain counts equal at 48 (two more than the reviewer's dry-run 46); 1543 collected/5 deselected; red control clean; pytest 1543 passed/0 failed/0 skipped; empty validate_verification_tests problem list; is_valid_current_run True |
| A2 | done | `PACKAGE_STATUS=READY_FOR_REVIEW`, `EVIDENCE_AUTHORITATIVE=true`; package `remedy-review-20260925-224758-READY_FOR_REVIEW.zip`, sha256 `8a9aa2d963b00ecad738490efc6df69df72dc782252a2c0f9f16d6cfb9cd6bc8`; archived at `/home/decodeux/Repos/remedy-history/zips`; manifest base/head match the fork point and C2 |
| C3 | done | this handback, rewritten per the template; committed and pushed |
| G1 | done | all four payloads' lines/bytes/sha256 matched the table; every copy byte-identical by `git show` |
| G2 | done | all four files match the stated bytes/sha256 at C2; open-finding set correct; pytest gate `369 passed` at exit 0 |
| G3 | done | evidence job's real exit code 0; every reading matches the reviewer's dry-run pattern with the two ancestry counts two higher, as predicted |
| G4 | done | `READY_FOR_REVIEW`; sha256 independently re-verified; manifest base/head correct; `is_zipfile` True, `testzip()` None; archived directory recorded |
| G5 | done | six `integrity check` pass, `fail_count` 0; tree clean; worktree list unchanged |
| G6 | done | reported in the final reply, after C3 and the push |
| Pull request | skipped | not opened this round — the branch opens one at F026's closure, per the block |

## Next

Phase 1 rule 1: read `.agent/STOP` from disk. Then the review of round 7. Then the closing round:
book round 7's PASS, rotate the ledger, accept F026 in STATUS with its README pins and the
self-use item's `consumed_by` in the same commit, and open the pull request. Open findings: 5 —
`R-1008`, `R-1055`, `R-1057`, `R-1058` and `R-1064`, all owned by F285 — the count the script reads
at C2 (`3cb0798d2`). Operator questions open: 4 — the count of `### Q` headings in
`.agent/operator_questions.md` at C2.
