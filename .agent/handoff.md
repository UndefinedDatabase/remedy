# Handback — F015 Interactive plan editing · Round 8 (evidence bundle + review package built)

## Session

SESSION 1 of feature F015 · round 8 · rounds so far 8

This round books round 7's PASS (C1, C2), then runs the closure-protocol
evidence job (A1) and builds the review package (A2) against the fork
point and the fresh C2 head. Nothing closes this round. A1 and A2 both
matched the reviewer's simulated readings exactly, and the package read
`PACKAGE_STATUS=READY_FOR_REVIEW`. A large majority of this session's
working-context budget remained at the point this handback was written.

## Range

Review of a7c7e942..HEAD

## Commits

### f70035d0 F015 R8 C1: copy round 8 block and payloads into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f015-r8-block.md | +167/-0 | copy of this round's block, verbatim |
| .agent/authored/f015-r8-ledger.diff | +10/-0 | copy of the ledger.diff payload |
| .agent/authored/f015-r8-plan.md | +28/-0 | copy of the plan.md payload |
| .agent/authored/f015-r8-create_f015_evidence.py | +149/-0 | copy of the evidence-script payload |

Total 354 insertions, matching the block's own formula (block line count
167 plus 187 = 354) exactly; under the 500-insertion cap.

### 15aec144 F015 R8 C2: book round 7's PASS, the repaired suite green
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +2/-0 | `Gate: F015 R7 — ` entry appended, via ledger.diff |
| .agent/plan.md | +5/-9 | rewritten to the plan.md payload |

Matches the block's expected 2/0 and 5/9 insertions exactly. This
commit's full SHA, `15aec1449745c1843ad4096e44974b8710b0756c`, is this
closure's ACCEPTED HEAD.

### (this commit) F015 R8 C3: rewrite handoff for round 8 with the evidence and package readings
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | rewrite | this handback |

## External actions

- `git apply --check` then `git apply` for `ledger.diff` — real exit 0,
  0.
- `git push origin feature/f015-interactive-plan-editing` after C2 —
  real outcome `a7c7e942..15aec144  feature/f015-interactive-plan-editing
  -> feature/f015-interactive-plan-editing`.
- `bash -c 'python3 .remedy-wt/f015-r8-payloads/create_f015_evidence.py
  > .remedy-wt/f015-r8-worker/evidence.log 2>&1; echo "REAL_EXIT=$?"'`
  (A1) — real exit 0.
- `bash scripts/make_review_zip.sh --evidence-dir
  .remedy-wt/f015-r8-evidence` (A2) — real exit 0.
- `git push origin feature/f015-interactive-plan-editing` runs after
  this handback is written; its real outcome is reported in the reply,
  not here, per G6.
- No `gh pr create`, no merge, no checkout of `main`, no branch
  deletion, no force-push, no `git stash`, no evidence directory
  committed.

## Verification

G1 TRANSPORT — each of the 3 payloads' lines/bytes/sha256 measured
against the PAYLOADS table, all matched exactly:
```
ledger.diff              lines=10  bytes=5297  sha256=651dabd88e9e52bf5abb6a9fb1305103c9f83b85027860af09ec529584f15d87
plan.md                  lines=28  bytes=950   sha256=2a63e2309cffd31b21ee8791a57c41da901f8164a9d7858ad3959e103bc91b3e
create_f015_evidence.py  lines=149 bytes=7114  sha256=acc16829b06b12e45734005d52002dd96fcbed5088a45c3321ed8788efae7339
```
The block file itself measured 167 lines, sha256
`b5b734189dd356f3fab8c2ef866fa65fca1f376ec0a8f7f2e2502a6de95b856d` —
equal to the delegation message's two readings.
Each committed `.agent/authored/f015-r8-*` blob, read with `git show
f70035d0:<path>`, compared byte for byte (sha256) against its source —
all 4 matched exactly:
```
f015-r8-block.md                  byte_identical=True
f015-r8-ledger.diff               byte_identical=True
f015-r8-plan.md                   byte_identical=True
f015-r8-create_f015_evidence.py   byte_identical=True
```

G2 THE BOOKING — read with `git show 15aec144:<path>`, each equal to
the reviewer's simulation:
```
.agent/live_review.md   305509 bytes  3fc832d03b0d4886b1522eed1bc9805ca13a26ac0b17d0ce7f8f9b189a88120b  MATCH
.agent/plan.md              950 bytes  2a63e2309cffd31b21ee8791a57c41da901f8164a9d7858ad3959e103bc91b3e  MATCH
```
Count of lines C2's diff adds to `.agent/live_review.md` beginning
`Gate: F015 R7 — `: 1 — matches. `open_finding_ids`
(scripts/rotate_live_review.py) over `.agent/live_review.md`'s text: at
`a7c7e942` -> `{R-0499, R-0950, R-1008, R-1046}` (4); at `15aec144` (C2)
-> the same 4; set difference in both directions = `{}` — matches the
reviewer's reading of 4 and 4, both differences empty.

G3 THE BUNDLE — at A1, `.remedy-wt/f015-r8-worker/evidence.log`:
```
head 15aec1449745c1843ad4096e44974b8710b0756c
ancestry-path count 44
plain count 44
collected node ids 922, deselected 18
red control: unsafe among the real ids 0 []
red control: planted id -> a local absolute path
pytest exit 0, {'passed': 922, 'failed': 0, 'skipped': 0}, output_hash 50ebece0a329b04a53868f3cc9af3ea6ada01395eb493657e7df3068b9057953
validate_verification_tests problems [] passed 922
is_valid_current_run True
validation_errors []
gates written: ['artifact_contract_gate.json', 'change_provenance_gate.json', 'commit_execution_gate.json', 'fresh_evidence_gate.json', 'runtime_integration_gate.json', 'final_verifier_report.json']
```
plus the script's own JSON summary: `job_id f015r8e1001`, `head_commit
15aec1449745c1843ad4096e44974b8710b0756c`, `commit_count 44`, `verdict
PASS_WITH_RISKS`, `total_passed 922`. This matches the reviewer's stated
simulation exactly: ancestry 44 = plain 44, 922 collected/18 deselected,
0 unsafe, planted id answering "a local absolute path", pytest exit 0
with 922 passed/0 skipped, empty `validate_verification_tests` problem
list, `is_valid_current_run` True with no validation error.
Files under `.remedy-wt/f015-r8-evidence/` ending `_gate.json`,
`_integrity.json` or `final_verifier_report.json` (9): `artifact_contract_gate.json`,
`change_provenance_gate.json`, `commit_execution_gate.json`,
`fresh_evidence_gate.json`, `runtime_integration_gate.json`,
`human_change_integrity.json`, `manifest_integrity.json`,
`postmortem_integrity.json`, `final_verifier_report.json`.

G4 THE PACKAGE — at A2, `.remedy-wt/f015-r8-worker/make_review_zip.log`:
```
REVIEW_PACKAGE_CREATED=true
PACKAGE_STATUS=READY_FOR_REVIEW
EVIDENCE_AUTHORITATIVE=true
REVIEW_PACKAGE_DIR=/home/decodeux/Repos/remedy-history/zips
ZIP_PATH=/home/decodeux/Repos/remedy-history/zips/remedy-review-20260924-151010-READY_FOR_REVIEW.zip
```
Package filename `remedy-review-20260924-151010-READY_FOR_REVIEW.zip`,
SHA-256 `920b9e1c3763632b86e97cb9724831e9c9e58378bbc71bac4532638e976da840`
(measured with `hashlib.sha256`, matching the script's own reported
`final_sha256`). `.review_zip_manifest.json` inside the package:
`committed_review_subject.base_commit =
fce49ce0789eec07148673ec4e356d28f1eb5fe3` (the fork point),
`head_commit = 15aec1449745c1843ad4096e44974b8710b0756c` (equal to C2's
full sha), `commit_count = 44`. Zip's own check:
`zipfile.is_zipfile` True, `testzip()` None. Archived directory:
`/home/decodeux/Repos/remedy-history/zips` (absolute; `REMEDY_REVIEW_DIR`
was not set, so the package went to the operator's archive — not `NOT
ARCHIVED`).

G5 THE TREE — after A2:
```
$ python3 -m apps.cli.main integrity check --json
{"check_count": 6, "checks": [
  {"name": "handler_import", "status": "pass", "message": "handlers=157"},
  {"name": "live_review_verdict", "status": "pass", "message": "last Gate verdict PASS"},
  {"name": "plan_consistency", "status": "pass", "message": "unchecked=0, context_complete=False"},
  {"name": "relevant_untracked", "status": "pass", "message": "untracked=0, relevant=0"},
  {"name": "repo_root_hygiene", "status": "pass", "message": "no reviewer scratch, evidence dir or archive at the root"},
  {"name": "high_blockers_open", "status": "pass", "message": "no open blocker/high findings"}
], "fail_count": 0, "ok": true, "passed": true}
```
All six checks pass, `fail_count` 0. `git status --porcelain` empty, no
relevant untracked file. `git worktree list` unchanged from before A1/A2
(reported in full in the reply).

G6 TREE AND PUSH — reported in the reply, not here, per the block's own
G6 instruction (C3 cannot contain the post-C3 readings).

## Authored-text proofs

`f015-r8-block.md`, `f015-r8-ledger.diff`, `f015-r8-plan.md` and
`f015-r8-create_f015_evidence.py` copies: each read back with `git show
f70035d0:<path>` and compared against the payload table's own reading —
all 4 matched byte for byte (see G1 above). `ledger.diff` was applied
with `git apply` (never retyped), preceded by a real `git apply --check`
at exit 0 and followed by the real `git apply` at exit 0. `plan.md` was
copied whole with `shutil.copyfile` into `.agent/plan.md`, never
retyped, never edited. `create_f015_evidence.py` was run unchanged from
`.remedy-wt/f015-r8-payloads/` (never copied into a runnable location,
never edited) to produce the evidence bundle.

## Deviations & assumptions

None. Every commit landed in the block's stated order (C1, C2), both
actions ran in the block's stated order (A1, A2) between C2 and C3,
every gate ran before C3 as ordered, and no payload was edited, retyped,
or repaired. A1's and A2's readings matched the reviewer's simulation
exactly with no divergence to record.

## Item-status table

| Item | Status | Reason |
|---|---|---|
| C1 | done | 354 insertions, matches block formula (167+187) exactly |
| C2 | done | live_review + plan advance, matches 2/0 and 5/9 exactly; full sha is the ACCEPTED HEAD |
| A1 | done | evidence job f015r8e1001, all readings matched the reviewer's simulation exactly |
| A2 | done | package READY_FOR_REVIEW, EVIDENCE_AUTHORITATIVE true, manifest base/head/commit_count matched |
| C3 | done | handoff rewritten with all readings, committed alone |
| G1 | done | all 3 payloads and 4 authored copies matched byte for byte |
| G2 | done | both file hashes, Gate-line count and finding-id sets matched |
| G3 | done | bundle readings matched the reviewer's simulation exactly; 9 gate/integrity/verifier files present |
| G4 | done | package READY_FOR_REVIEW, zip valid, manifest base/head/commit_count matched |
| G5 | done | integrity check 6/6 pass, tree clean, worktrees unchanged |
| G6 | done | reported in the reply, not the handback, per the block's own G6 instruction |
| Push | done | reported in the reply, not the handback, per the block's own G6 instruction |

## Next

Phase 1 rule 1: read `.agent/STOP` from disk. Then the review of round
8. Then the closing round: the booking of round 3, the ledger rotation,
the STATUS line with the README counters in the same commit, and the
pull request. Open findings: 4. Operator questions: 1.
