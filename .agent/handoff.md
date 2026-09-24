# Handback — F019 Live node materialization · Round 8 (closure sequence, evidence half)

## Session

SESSION 2 of feature F019 · round 8 · rounds so far 8

This round books round 7's PASS (whose one full suite was green), then
builds the feature's evidence bundle against the fork point and the fresh
review package. Nothing closes this round. I had ample context remaining
throughout this round; no session-limit pressure at any point.

## Range

Review of 38c988ba3..HEAD

## Commits

### 0c5b54fd6 F019 R8 C1: copy round 8 block and payloads into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f019-r8-block.md | +170/-0 | copy of this round's block, verbatim |
| .agent/authored/f019-r8-ledger.diff | +10/-0 | copy of the ledger.diff payload |
| .agent/authored/f019-r8-plan.md | +31/-0 | copy of the plan.md payload |
| .agent/authored/f019-r8-create_f019_evidence.py | +154/-0 | copy of the create_f019_evidence.py payload |

365 insertions by `git show --numstat` (block's 170 lines + 195); matches
the block's expectation exactly; under the 500-insertion cap.

### d581b6667 F019 R8 C2: book round 7's PASS, the one full suite green
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +2/-0 | `Gate: F019 R7 —` entry appended |
| .agent/plan.md | +6/-8 | rewritten to the plan.md payload (round 8 scope) |

`git apply --check` on ledger.diff: exit 0. `git apply`: exit 0.
Insertions/deletions by `git show --numstat`: 2/0 live_review.md, 6/8
plan.md — matches the block's expectation exactly. This commit's full sha,
`d581b6667a9e29a1d276a39555b9038adb82a92b`, is this closure's ACCEPTED
HEAD. Pushed immediately after (`38c988ba3..d581b6667` to
`feature/f019-live-node-materialization`), before A1.

### (this commit) F019 R8 C3: rewrite handoff for round 8 with the evidence and package readings
Self-reference exception per the handback template (a handback cannot
table the commit that writes it).
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | rewritten | this handback |

## External actions

- `git push origin feature/f019-live-node-materialization` after C2 — real
  outcome: `38c988ba3..d581b6667  feature/f019-live-node-materialization ->
  feature/f019-live-node-materialization`, `REAL_EXIT=0`.
- A1 — `python3 .remedy-wt/f019-r8-payloads/create_f019_evidence.py >
  .remedy-wt/f019-r8-worker/evidence.log 2>&1` — `REAL_EXIT=0`. Bundle
  written to `.remedy-wt/f019-r8-evidence/` (gitignored, not committed).
  Job id `f019r8e1001`.
- A2 — `bash scripts/make_review_zip.sh --evidence-dir
  .remedy-wt/f019-r8-evidence` — `REAL_EXIT=0`. Package
  `remedy-review-20260924-204836-READY_FOR_REVIEW.zip`, sha256
  `d0340a1a2ed77a6472e2d3f3469a4e5bf590674fd21e4d229b9c4d52d01263ff`,
  archived to `/home/decodeux/Repos/remedy-history/zips`.
- `git push origin feature/f019-live-node-materialization` runs after this
  handback is committed; its real outcome is reported in the reply only,
  per G6.
- No `gh pr` command of any kind this round. No checkout of `main`, no
  branch deletion, no force-push, no `git stash`, no worktree add/remove
  (constraint 6 leaves every existing worktree alone).

## Verification

G1 TRANSPORT — all 3 payloads measured against the block's PAYLOADS table,
all matched (line count, byte count, sha256):
```
ledger.diff              lines=10  bytes=6809 sha256=0eb7324a3bfb7a4a86644ee40119dbc2341760a22f56e9d3af43c075b74ef0a0
plan.md                  lines=31  bytes=1158 sha256=f6c823ede98916ca0ebe0c041012161d492379b742991bdd5239ebfcc9d5da25
create_f019_evidence.py  lines=154 bytes=7457 sha256=d6e004262d9b164ec5b02eac8e2901596b297dca6044d4d519e973cf669fccf4
ALL PAYLOAD DIGESTS MATCH: True
```
Each `.agent/authored/f019-r8-*` copy, read back with `git show
0c5b54fd6:<path>` from C1, matched its source byte for byte (4
comparisons: the block copy against `.remedy-wt/f019-r8/block.md`, plus
the 3 payload copies) — `ALL_TRANSPORT_OK: True`.

G2 THE BOOKING — at C2 (`d581b6667`), `.agent/live_review.md` read 322254
bytes, sha256
`1929360eddaf4005f803333a5bb5cba7b5da0e08b4dc54e3be4fcbd76fc23f60`
(MATCH); `.agent/plan.md` read 1158 bytes, sha256
`f6c823ede98916ca0ebe0c041012161d492379b742991bdd5239ebfcc9d5da25`
(MATCH, equal to the plan.md payload). The count of lines C2's diff adds
to the ledger beginning `Gate: F019 R7 — ` is 1 (measured over C2's diff
of `.agent/live_review.md`). `open_finding_ids`
(`scripts/rotate_live_review.py`) over `.agent/live_review.md`: at
`38c988ba` → `['R-0499', 'R-0950', 'R-1008', 'R-1046']`; at C2
(`d581b6667`) → the same four — matches the reviewer's simulated reading
exactly at both.

G3 THE BUNDLE — at A1, real transcript:
```
head d581b6667a9e29a1d276a39555b9038adb82a92b
ancestry-path count 57
plain count 57
collected node ids 718, deselected 4
red control: unsafe among the real ids 0 []
red control: planted id -> a local absolute path
pytest exit 0, {'passed': 718, 'failed': 0, 'skipped': 0}, output_hash 3cdf64d19dea9cfc5f8ea25c5a6060e10a8a915e614a891c6dafb29e85adaf29
validate_verification_tests problems [] passed 718
is_valid_current_run True
validation_errors []
gates written: ['artifact_contract_gate.json', 'change_provenance_gate.json', 'commit_execution_gate.json', 'fresh_evidence_gate.json', 'runtime_integration_gate.json', 'final_verifier_report.json']
REAL_EXIT=0
```
Script exit code 0. The two ancestry counts (ancestry-path 57, plain 57)
are equal, and each reads two more than the reviewer's dry-run reading of
55 at `38c988ba` (55 + 2 = 57, expected). Collected node ids 718,
deselected 4 — matches the reviewer's dry-run reading exactly. Red
control: 0 unsafe ids among the real set (`[]`), planted id answered "a
local absolute path" — matches. pytest exit 0, 718 passed / 0 failed / 0
skipped, output_hash
`3cdf64d19dea9cfc5f8ea25c5a6060e10a8a915e614a891c6dafb29e85adaf29`.
`validate_verification_tests` problem list: `[]` (EMPTY, matches).
`is_valid_current_run`: `True`, `validation_errors`: `[]` (matches). Job
id: `f019r8e1001`. Files under `.remedy-wt/f019-r8-evidence/` ending
`_gate.json`: `artifact_contract_gate.json`, `change_provenance_gate.json`,
`commit_execution_gate.json`, `fresh_evidence_gate.json`,
`runtime_integration_gate.json`; ending `_integrity.json`:
`human_change_integrity.json`, `manifest_integrity.json`,
`postmortem_integrity.json`; and `final_verifier_report.json` — all 9
present.

G4 THE PACKAGE — at A2, real transcript (trailer block):
```
REVIEW_PACKAGE_CREATED=true
PACKAGE_STATUS=READY_FOR_REVIEW
EVIDENCE_DIR=.remedy-wt/f019-r8-evidence
REVIEW_SUBJECT_ALIGNMENT=PASS
EVIDENCE_AUTHORITATIVE=true
REVIEW_PACKAGE_DIR=/home/decodeux/Repos/remedy-history/zips
ZIP_PATH=/home/decodeux/Repos/remedy-history/zips/remedy-review-20260924-204836-READY_FOR_REVIEW.zip
REAL_EXIT=0
```
`PACKAGE_STATUS` reads `READY_FOR_REVIEW`. `EVIDENCE_AUTHORITATIVE`:
`true`. Package filename:
`remedy-review-20260924-204836-READY_FOR_REVIEW.zip`. Its SHA-256,
measured independently with `sha256sum` against the archived file, is
`d0340a1a2ed77a6472e2d3f3469a4e5bf590674fd21e4d229b9c4d52d01263ff`
(matches the script's own `final_sha256` reading). `.review_zip_manifest.json`
read from INSIDE the package: `committed_review_subject.base_commit` =
`92b7f5f18943ba7a22b748687d1c565bec7e752a` (the fork point),
`committed_review_subject.head_commit` =
`d581b6667a9e29a1d276a39555b9038adb82a92b` (equal to C2's full sha),
`commit_count` 57. The zip's own check: `zipfile.is_zipfile()` → `True`,
`testzip()` → `None`. Archived directory:
`/home/decodeux/Repos/remedy-history/zips` (absolute; not `NOT ARCHIVED`).

G5 THE TREE — after A2:
```
$ python3 -m apps.cli.main integrity check --json
{"check_count": 6, "checks": [{"message": "handlers=157", "name": "handler_import", "status": "pass"}, {"message": "last Gate verdict PASS", "name": "live_review_verdict", "status": "pass"}, {"message": "unchecked=0, context_complete=False", "name": "plan_consistency", "status": "pass"}, {"message": "untracked=0, relevant=0", "name": "relevant_untracked", "status": "pass"}, {"message": "no reviewer scratch, evidence dir or archive at the root", "name": "repo_root_hygiene", "status": "pass"}, {"message": "no open blocker/high findings", "name": "high_blockers_open", "status": "pass"}], "fail_count": 0, "ok": true, "passed": true, "schema_version": 1, "version": 1}
REAL_EXIT=0
```
All six checks `pass`, `fail_count` 0. `git status --porcelain`: empty, no
relevant untracked file. `git worktree list`: unchanged from before this
round — no worktree added or removed (the round's own `.remedy-wt/f019-r8`,
`.remedy-wt/f019-r8-payloads`, `.remedy-wt/f019-r8-sim` and
`.remedy-wt/f019-r8-worker` directories are not `git worktree add`
worktrees and do not appear in that list).

G6 — reported in the reply per the block's own instruction (measured
after this handback is written, committed and pushed).

## Authored-text proofs

All 4 authored copies under `.agent/authored/f019-r8-*` (the block copy
plus the 3 payload copies) were built by reading each source's bytes with
`shutil.copyfile` and writing them unedited — never retyped, never
edited. Each was read back from C1 (`0c5b54fd6`) with `git show
0c5b54fd6:<path>` and compared byte for byte against its source: all 4
`BYTE-IDENTICAL` (G1 above). `ledger.diff` was applied with `git apply`
after `git apply --check` passed (exit 0 both), never retyped or edited;
its resulting file contents (`.agent/live_review.md`) were verified by
byte count and sha256 against the reviewer's own simulated reading at C2
(G2 above) — `MATCH`; `.agent/plan.md` was separately rewritten whole via
`shutil.copyfile` from its payload and also confirmed `MATCH`.
`create_f019_evidence.py` was run unedited from the payload directory as
a TOOL (A1) and never applied to a tracked file.

## Deviations & assumptions

None. Every commit landed in the block's stated order (C1, C2, then A1,
A2, C3), C2 was pushed before A1 as ordered, G1–G5 ran before C3 was
written as ordered, and no payload was edited, retyped or repaired. The
round's whole tracked path set matches constraint 3 exactly: `git diff
--name-only 38c988ba3 HEAD` (measured through C2, before this handback
commit) named exactly the four `.agent/authored/f019-r8-*` copies,
`.agent/live_review.md` and `.agent/plan.md`; this handback adds
`.agent/handoff.md` in C3 as the constraint allows. No evidence directory
was ever committed (`.remedy-wt/f019-r8-evidence/` is gitignored and
untracked throughout). Nothing under `packages/`, `apps/`, `tests/` or
`docs/` was touched, and none of `README.md`, `docs/roadmap/STATUS.md`,
`scripts/self_use_queue.json`, `.agent/decisions.md`,
`.agent/prose_slips.md`, `.agent/candidates.md` or
`.agent/operator_questions.md` was touched. The package read
`READY_FOR_REVIEW` on the first attempt, so constraint 4's stop-and-report
branch was not needed. Nothing was merged and nothing was closed: no `gh
pr merge`, no `gh pr create`, no checkout of `main`, no branch deletion,
no force-push, no STATUS edit, no README edit, no ledger rotation.

## Item-status table

| Item | Status | Reason |
|---|---|---|
| C1 | done | 365 insertions, matches (170 block + 195) |
| C2 | done | git apply --check and apply both exit 0; 2/0, 6/8 insertions, matches both files; pushed before A1 |
| A1 | done | evidence job exit 0, job id f019r8e1001, all readings matched the reviewer's dry-run shape |
| A2 | done | package READY_FOR_REVIEW, EVIDENCE_AUTHORITATIVE true, manifest base/head matched |
| C3 | done | handoff rewritten per template |
| G1 | done | all 3 payload digests and 4 authored-copy comparisons matched |
| G2 | done | both named file digests matched at C2; 1 new Gate line; open_finding_ids correct at both commits |
| G3 | done | script exit 0; ancestry counts 57/57 equal (two more than the reviewer's 55); 718 collected/4 deselected; pytest 718 passed/0 failed/0 skipped exit 0; validate_verification_tests empty; is_valid_current_run True |
| G4 | done | PACKAGE_STATUS READY_FOR_REVIEW; EVIDENCE_AUTHORITATIVE true; manifest base=fork point, head=C2's sha; zip valid, testzip None |
| G5 | done | integrity check all 6 pass, fail_count 0; tree clean; worktree list unchanged |
| G6 | done | reported in the reply (tree/push/PR state after C3) |

## Next

Phase 1 rule 1: read `.agent/STOP` from disk. Then the review of round 8.
Then the closing round: the booking of round 8, the ledger rotation, the
STATUS line with the README counters in the same commit, and the pull
request. Open findings: 4. Operator questions open: 3.
