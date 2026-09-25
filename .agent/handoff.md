# Handback — F023 Semantic zoom L0–L3 · Round 9

## Session

SESSION 1 of feature F023 · round 9 · rounds so far 9

This round is the closure sequence's evidence half: it booked round 8's PASS (the one full suite
green), then built the evidence bundle against the fork point and the fresh review package. Ample
context remained throughout this round; no session-limit pressure at any point.

## Range

Review of fecd022ad..HEAD

## Commits

### 28be0df00 F023 R9 C1: copy round 9 block and payloads into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f023-r9-block.md | +170/-0 | copy of this round's block, verbatim |
| .agent/authored/f023-r9-create_f023_evidence.py | +167/-0 | copy of the create_f023_evidence.py payload |
| .agent/authored/f023-r9-ledger.diff | +10/-0 | copy of the ledger.diff payload |
| .agent/authored/f023-r9-plan.md | +29/-0 | copy of the plan.md payload |

376 insertions by `git show --numstat` (block's line count 170 + 206) — matches the block's
expectation exactly; well under the 500-insertion STOP threshold and the 500-line commit cap.

### 54e5ffd24 F023 R9 C2: book round 8's PASS, the one full suite green
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +2/-0 | `Gate: F023 R8 —` entry appended |
| .agent/plan.md | +8/-10 | rewritten to the plan.md payload |

`git apply --check` on ledger.diff: exit 0. `git apply`: exit 0. Insertions/deletions by `git show
--numstat`: 2/0 live_review.md, 8/10 plan.md — matches the block's expectation exactly. This
commit's full SHA, `54e5ffd2485bf90c405f5ad662b7d86be8dd3eb9`, is this closure's ACCEPTED HEAD.

## External actions

- `git push origin feature/f023-semantic-zoom-l0-l3` after C2, before A1 — outcome
  `fecd022ad..54e5ffd24  feature/f023-semantic-zoom-l0-l3 -> feature/f023-semantic-zoom-l0-l3`.
- A1 THE EVIDENCE JOB — `bash -c 'python3 .remedy-wt/f023-r9-payloads/create_f023_evidence.py >
  .remedy-wt/f023-r9-worker/evidence.log 2>&1; echo "REAL_EXIT=$?"'`. REAL_EXIT=0. Job id
  `f023r9e1001`. Bundle written to `.remedy-wt/f023-r9-evidence/` (gitignored, uncommitted).
  Committed nothing.
- A2 THE REVIEW PACKAGE — `bash scripts/make_review_zip.sh --evidence-dir
  .remedy-wt/f023-r9-evidence` (no `REMEDY_REVIEW_DIR` set). REAL_EXIT=0. Package
  `remedy-review-20260925-052148-READY_FOR_REVIEW.zip`, sha256
  `6e041624017f41e1644f71f3d8c18ae8dd4d677b1d8df4fe6206f89b6f76b4bb`, archived at
  `/home/decodeux/Repos/remedy-history/zips`. Committed nothing.
- No `git worktree add`/`remove` this round.
- No pull request created, no merge, no checkout of `main`, no branch deletion, no force-push, no
  `git stash` — none performed (constraint 5).

## Verification

```
$ ls .agent/STOP; echo $?
ls: cannot access '.agent/STOP': No such file or directory
2
(absent, as required)

$ pwd
/home/decodeux/Repos/remedy
$ git status --porcelain
(empty)
$ git branch --show-current
feature/f023-semantic-zoom-l0-l3
$ git log --oneline -1
fecd022ad F023 R8 C5: record the closure suite transcript and rewrite handoff for round 8
```
All BEFORE ANYTHING ELSE checks passed at round start.

```
$ wc -l .remedy-wt/f023-r9/block.md
170
$ sha256sum .remedy-wt/f023-r9/block.md
c911b8db6618927a49f1fed99b9a5dbbcf2fd3782178585492668ccca22226b7
```
Matches both readings given in the delegation message exactly (170 lines,
c911b8db6618927a49f1fed99b9a5dbbcf2fd3782178585492668ccca22226b7) — R-0954.

```
$ git worktree list
(primary + 15 f015-*-dry/sim r1-r6, 5 f015-*-sim r7-r9, 16 f020-*-dry/sim r1-r8,
 f023-r1-dry, f023-r1-sim, f023-r2-dry, f023-r2-sim, f023-r3-dry, f023-r3-sim,
 f023-r4-dry, f023-r4-sim, f023-r5-dry, f023-r5-sim, f023-r6-dry, f023-r6-sim,
 f023-r7-dry, f023-r7-sim, f023-r8-dry, f023-r8-sim, f023-r9-dry, f023-r9-sim,
 8 f284-*-dry/sim r1-r4, 4 job-* worktrees)
$ git branch --list 'remedy/job-*' | wc -l
41
```

```
$ (line count, byte count, sha256 of each payload under .remedy-wt/f023-r9-payloads/)
create_f023_evidence.py  lines=167 bytes=8624 sha256=74829a8b4e83c22e03ad74946962e31c38209747540e3c4d6e5d8bb2ff7a2da8
ledger.diff              lines=10  bytes=6581 sha256=ccfb304d084ee7a2608ce8b9a7e5239dc3a2a54089b4305c0c691048ed013520
plan.md                  lines=29  bytes=984  sha256=4baa04bb4c51d70ab1fb5e7c4bffbacdff6a19d1f873f5b62396e183794f0283
```
All 3 match the PAYLOADS table exactly (G1).

```
$ (compare each committed .agent/authored/f023-r9-* blob, read with `git show <C1>:<path>`,
   against its source)
f023-r9-block.md                @ 28be0df00: IDENTICAL (sha c911b8db...)
f023-r9-create_f023_evidence.py @ 28be0df00: IDENTICAL (sha 74829a8b...)
f023-r9-ledger.diff             @ 28be0df00: IDENTICAL (sha ccfb304d...)
f023-r9-plan.md                 @ 28be0df00: IDENTICAL (sha 4baa04bb...)
```
All 4 BYTE-IDENTICAL against their sources (G1).

```
$ git apply --check .remedy-wt/f023-r9-payloads/ledger.diff; echo $?
0
$ git apply .remedy-wt/f023-r9-payloads/ledger.diff; echo $?
0
```

```
$ (bytes/sha256 of the files named in the block's G2 table, read at C2)
C2 .agent/live_review.md: bytes=311433 sha256=f9adecd3b3a2e88f5324495691c207b60727629f69566e95cfc162eaeba4767c match=True
C2 .agent/plan.md: bytes=984 sha256=4baa04bb4c51d70ab1fb5e7c4bffbacdff6a19d1f873f5b62396e183794f0283 match=True
```
Both match the block's G2 table exactly.

```
$ git show 54e5ffd24 -- .agent/live_review.md | grep -c '^+Gate: F023 R8 — '
1
```
Matches the reviewer's stated reading of 1 exactly (G2).

```
$ open_finding_ids(text) from scripts/rotate_live_review.py, over .agent/live_review.md's TEXT
  at fecd022a and at 54e5ffd24 (C2)
fecd022ad open ids: ['R-1008']
54e5ffd24 (C2) open ids: ['R-1008']
```
Reads R-1008 alone at both, matching the block's stated reading exactly (G2).

```
$ bash -c 'python3 .remedy-wt/f023-r9-payloads/create_f023_evidence.py >
  .remedy-wt/f023-r9-worker/evidence.log 2>&1; echo "REAL_EXIT=$?"'
REAL_EXIT=0
```
Log (up to the summary):
```
head 54e5ffd2485bf90c405f5ad662b7d86be8dd3eb9
ancestry-path count 69
plain count 69
collected node ids 706, deselected 5
red control: unsafe among the real ids 0 []
red control: planted id -> a local absolute path
pytest exit 0, {'passed': 706, 'failed': 0, 'skipped': 0}, output_hash 7d72e61864886b9c2edb661948e98807f895a7da5aa4be4316747f9e6f0950fe
validate_verification_tests problems [] passed 706
is_valid_current_run True
validation_errors []
gates written: ['artifact_contract_gate.json', 'change_provenance_gate.json', 'commit_execution_gate.json', 'fresh_evidence_gate.json', 'runtime_integration_gate.json', 'final_verifier_report.json']
{
  "job_id": "f023r9e1001",
  "head_commit": "54e5ffd2485bf90c405f5ad662b7d86be8dd3eb9",
  "authority_count": 49,
  "partition": {"T001": 17, "T002": 17, "T003": 15},
  "commit_count": 69,
  "verdict": "PASS_WITH_RISKS",
  "manual_completion": true,
  "operator_attested_tasks": ["T001", "T002", "T003"],
  "total_passed": 706
}
```
Both ancestry counts read 69, equal — two more than the reviewer's dry-run reading of 67 at
`fecd022a`, exactly as the block predicted (its dry run measured a fork-point-anchored range two
commits shorter than C2's). Collected 706 node ids with 5 deselected, none unsafe, the planted id
answering "a local absolute path" — all equal the reviewer's dry-run readings. pytest exit 0, 706
passed, 0 skipped — equal. `validate_verification_tests` problem list empty, `is_valid_current_run`
True, no validation errors — equal (G3).

```
$ ls .remedy-wt/f023-r9-evidence/ | grep -E '_gate\.json$|_integrity\.json$|final_verifier_report\.json$'
artifact_contract_gate.json
change_provenance_gate.json
commit_execution_gate.json
fresh_evidence_gate.json
runtime_integration_gate.json
human_change_integrity.json
manifest_integrity.json
postmortem_integrity.json
final_verifier_report.json
```
9 files (G3).

```
$ git status --porcelain
(empty — the evidence bundle is gitignored under .remedy-wt/)
```

```
$ bash -c 'bash scripts/make_review_zip.sh --evidence-dir .remedy-wt/f023-r9-evidence >
  .remedy-wt/f023-r9-worker/package.log 2>&1; echo "REAL_EXIT=$?"'
REAL_EXIT=0
```
Decisive lines:
```
{"member_count": 5875, "authoritative_count": 49, "symlink_count": 0, "tombstone_count": 0,
 "final_path": "/home/decodeux/Repos/remedy-history/zips/remedy-review-20260925-052148-READY_FOR_REVIEW.zip",
 "final_sha256": "6e041624017f41e1644f71f3d8c18ae8dd4d677b1d8df4fe6206f89b6f76b4bb",
 "publication_capability": "SUPPORTED", "package_status": "READY_FOR_REVIEW",
 "evidence_authoritative": true, "review_subject_alignment": "PASS",
 "manifest_sha256": "0df659ccb30fb1cbb321fea80230708f26bbdaa693267ffded41067e8fbeb3dd"}
REVIEW_PACKAGE_CREATED=true
PACKAGE_STATUS=READY_FOR_REVIEW
EVIDENCE_AUTHORITATIVE=true
REVIEW_PACKAGE_DIR=/home/decodeux/Repos/remedy-history/zips
ZIP_PATH=/home/decodeux/Repos/remedy-history/zips/remedy-review-20260925-052148-READY_FOR_REVIEW.zip
Commit: 54e5ffd2485bf90c405f5ad662b7d86be8dd3eb9
```
`PACKAGE_STATUS=READY_FOR_REVIEW` (not merely exit 0), `EVIDENCE_AUTHORITATIVE=true` (G4).

```
$ python3 -c "import zipfile; zf=zipfile.ZipFile('/home/decodeux/Repos/remedy-history/zips/remedy-review-20260925-052148-READY_FOR_REVIEW.zip'); print(zipfile.is_zipfile('...'), zf.testzip())"
is_zipfile True
testzip None
```
```
$ (.review_zip_manifest.json inside the package, committed_review_subject)
{
  "base_commit": "441f4e8e3a041ed7db42043ef112176d573c816c",
  "base_is_ancestor": true,
  "commit_count": 69,
  "file_count": 142,
  "head_commit": "54e5ffd2485bf90c405f5ad662b7d86be8dd3eb9",
  "tombstones": []
}
```
`head_commit` equals C2's full sha; `base_commit` equals the fork point `441f4e8e3a041ed7db42043ef112176d573c816c` (G4).

```
$ python3 -c "hashlib.sha256 over the archived zip, computed independently"
6e041624017f41e1644f71f3d8c18ae8dd4d677b1d8df4fe6206f89b6f76b4bb
```
Matches the tool's own reported `final_sha256` exactly (G4). Archived directory:
`/home/decodeux/Repos/remedy-history/zips` (not `NOT ARCHIVED`).

```
$ bash -c 'python3 -m apps.cli.main integrity check --json; echo "REAL_EXIT=$?"'
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
All six checks `pass`, `fail_count` 0 (G5).

```
$ git status --porcelain
(empty, no untracked file)
$ git worktree list
(unchanged from the round-start reading above — no worktree added or removed this round)
```
(G5).

```
$ git diff --name-only fecd022a HEAD
.agent/authored/f023-r9-block.md
.agent/authored/f023-r9-create_f023_evidence.py
.agent/authored/f023-r9-ledger.diff
.agent/authored/f023-r9-plan.md
.agent/live_review.md
.agent/plan.md
```
Exactly the round's tracked path set through C2 (constraint 3); `.agent/handoff.md` is added by
this same commit, C3, which is a self-reference the template exempts from its own diff snapshot.
No evidence directory is committed — the bundle stays under gitignored `.remedy-wt/`.

## Evidence and package summary

- Evidence job id: `f023r9e1001`
- Package filename: `remedy-review-20260925-052148-READY_FOR_REVIEW.zip`
- Package SHA-256: `6e041624017f41e1644f71f3d8c18ae8dd4d677b1d8df4fe6206f89b6f76b4bb`
- Archived directory: `/home/decodeux/Repos/remedy-history/zips`
- Accepted HEAD (C2's full SHA): `54e5ffd2485bf90c405f5ad662b7d86be8dd3eb9`
- PACKAGE_STATUS: `READY_FOR_REVIEW`; EVIDENCE_AUTHORITATIVE: `true`

## Authored-text proofs

All 4 authored copies under `.agent/authored/f023-r9-*` (the block copy plus the three payload
copies) were built by `shutil.copyfile` from source to destination — never retyped, never edited.
Each was read back with `git show <C1>:<path>` and compared byte for byte against its source: all 4
BYTE-IDENTICAL (G1 above). `ledger.diff` was applied with `git apply` after `git apply --check`
passed (exit 0 both), never retyped or edited; the resulting `.agent/live_review.md` was verified by
byte count and sha256 against the block's G2 table — MATCH. `.agent/plan.md` was rewritten whole via
`shutil.copyfile` from the payload source — never retyped — and confirmed MATCH against both the
PAYLOADS table and the G2 table. `create_f023_evidence.py` is a TOOL for A1, run from the payload
directory and never edited; its readings (job id, both ancestry counts, collected/deselected
counts, the red controls, pytest's exit code and counts, `output_hash`, the validation results) all
equal the reviewer's own stated readings, adjusted only where the block itself predicted a
difference (the two-commit-wider ancestry range at C2 versus the dry run's `fecd022a`).

## Deviations & assumptions

None. Both commits and both actions landed in the block's stated order: C1, C2, A1, A2, then C3
(this handback), exactly as ordered. No payload was edited, retyped or repaired. G1 through G5 ran
before C3 was written, per the block's instruction that G1–G5 run before C3. The push after C2 and
before A1 happened exactly where the block placed it. The package read `READY_FOR_REVIEW` on the
first build — no BLOCKED_EVIDENCE handling was needed, so constraint 4's stop-and-handback path did
not apply. Nothing was merged, closed, or rotated this round: no `gh pr merge`, no `gh pr create`,
no checkout of `main`, no STATUS edit, no README edit, no ledger rotation, no `git stash` — per
constraint 5. Every worktree named in constraint 6 (`f015-r*`, `f020-r*`, `f023-r*`, `f284-r*`,
`job-*`) was left untouched — no worktree was added or removed this round; all 41 `remedy/job-*`
branches were left untouched.

## Item-status table

| Item | Status | Reason |
|---|---|---|
| C1 | done | 376 insertions, matches block's expectation exactly (170+206); well under the 500-insertion STOP threshold |
| C2 | done | ledger.diff apply --check and apply both exit 0; 2/0, 8/10 insertions/deletions match exactly; full sha `54e5ffd2485bf90c405f5ad662b7d86be8dd3eb9` recorded as the ACCEPTED HEAD |
| PUSH (post-C2) | done | `fecd022ad..54e5ffd24` pushed to origin before A1 |
| A1 | done | evidence job exit 0; job id f023r9e1001; ancestry counts 69/69 equal; 706 collected, 5 deselected, 0 unsafe; pytest 706 passed/0 skipped exit 0; validation clean |
| A2 | done | package exit 0; PACKAGE_STATUS=READY_FOR_REVIEW; EVIDENCE_AUTHORITATIVE=true; manifest base/head match the fork point and C2; testzip() None; archived at /home/decodeux/Repos/remedy-history/zips |
| G1 | done | all 3 payload digests and 4 authored-copy comparisons matched |
| G2 | done | both named file digests matched; gate-line count 1 matched; open set R-1008 alone at both |
| G3 | done | exit 0; ancestry 69/69 equal; 706/5 collected/deselected, 0 unsafe; pytest 706/0/0 exit 0; validation clean; 9 gate/integrity/verifier files present |
| G4 | done | READY_FOR_REVIEW, EVIDENCE_AUTHORITATIVE true, manifest base=fork point head=C2, zip valid, testzip None, archived |
| G5 | done | integrity check 6/6 pass, fail_count 0; tree clean; worktree list unchanged |
| C3 | done | this handback |
| PUSH (post-C3) | pending | `git push origin feature/f023-semantic-zoom-l0-l3`, reported in the reply |

## Next

Phase 1 rule 1: read `.agent/STOP` from disk. Then the review of round 9. Then the closing round:
the booking of round 9, the ledger rotation, the STATUS line with the README counters in the same
commit, and the pull request. Open findings: 1. Operator questions open: 3.
