# Handback — F020 Node lifecycle & glyph language · Round 7

## Session

SESSION 1 of feature F020 · round 7 · rounds so far 7

This round booked round 6's PASS (the one full suite green) into the live review record and
advanced `.agent/plan.md` to the evidence half, then ran the evidence job (A1) and built the
fresh review package (A2). Both commits landed in the block's ordered sequence; the push ran
between C2 and A1 as ordered; all five gates (G1-G5) passed with exact matches to the reviewer's
stated readings, and the package read `READY_FOR_REVIEW`. I had ample context remaining
throughout this round; no session-limit pressure at any point.

## Range

Review of 649661cd..HEAD

## Commits

### 09861d084 F020 R7 C1: copy round 7 block and payloads into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f020-r7-block.md | +170/-0 | copy of this round's block, verbatim |
| .agent/authored/f020-r7-create_f020_evidence.py | +157/-0 | copy of the create_f020_evidence.py payload |
| .agent/authored/f020-r7-ledger.diff | +10/-0 | copy of the ledger.diff payload |
| .agent/authored/f020-r7-plan.md | +28/-0 | copy of the plan.md payload |

365 insertions by `git show --numstat` (block's 170 lines + 195); matches the block's expectation
exactly; under the 500-insertion cap.

### ac75d5d4e F020 R7 C2: book round 6's PASS, the one full suite green
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +2/-0 | F020 R6 Gate entry appended (ledger.diff) |
| .agent/plan.md | +5/-7 | rewritten to the plan.md payload |

`git apply --check` on ledger.diff: exit 0. `git apply`: exit 0. Insertions/deletions by `git show
--numstat`: 2/0 live_review.md, 5/7 plan.md — matches the block's expectation exactly.
**This is the closure's ACCEPTED HEAD: `ac75d5d4ebe6f7aa908ccdfd1dfa504582b2fb5e`.**

### (this commit) F020 R7 C3: rewrite handoff for round 7 with the evidence and package readings
Self-reference exception per the handback template (a handback cannot table the commit that
writes it).
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | rewritten | this handback |

## External actions

- `git push -u origin feature/f020-node-lifecycle-glyph-language` — run after C2, before A1.
  Outcome: `649661cd0..ac75d5d4e  feature/f020-node-lifecycle-glyph-language ->
  feature/f020-node-lifecycle-glyph-language`, branch set to track the remote, real exit 0.
- A1 evidence job — `bash -c 'python3 .remedy-wt/f020-r7-payloads/create_f020_evidence.py >
  .remedy-wt/f020-r7-worker/evidence.log 2>&1; echo "REAL_EXIT=$?"'` — REAL_EXIT=0. Job id
  `f020r7e1001`. Bundle written to `.remedy-wt/f020-r7-evidence/` (gitignored, never committed).
- A2 review package — `bash scripts/make_review_zip.sh --evidence-dir .remedy-wt/f020-r7-evidence`
  (no `REMEDY_REVIEW_DIR` set) — REAL_EXIT=0. Package
  `remedy-review-20260925-013441-READY_FOR_REVIEW.zip`, sha256
  `a069e502d3956af33f4e7dde2ece1dfd47355c68030181dbd5764af6d026d1e0`, archived at
  `/home/decodeux/Repos/remedy-history/zips`.
- `git push origin feature/f020-node-lifecycle-glyph-language` — runs AFTER this commit lands;
  its real outcome is reported in the reply, since this handback cannot contain an outcome that
  happens after it. No `gh pr create`, no `gh pr merge` this round: the block forbids both
  (constraint 5).

## Verification

```
$ ls .agent/STOP
ls: cannot access '.agent/STOP': No such file or directory (absent, as required)

$ pwd
/home/decodeux/Repos/remedy
$ git status --porcelain
(empty)
$ git branch --show-current
feature/f020-node-lifecycle-glyph-language
$ git log --oneline -1
649661cd0 F020 R6 C5: record the closure suite transcript and rewrite handoff for round 6
```
All BEFORE ANYTHING ELSE checks passed at round start.

```
$ wc -l / sha256sum .remedy-wt/f020-r7/block.md
170 lines, sha256=6fc454b48260ef96fb47dd958d7cd8ca19536cfd37c866c423779f31d199a7c2
```
Matches both readings given in the delegation message exactly (R-0954).

```
$ git worktree list
(primary + 39 reviewer worktrees under .remedy-wt/f015-*, f020-*, f284-* + 4 job-* worktrees)
$ git branch --list 'remedy/job-*' | wc -l
41
```

```
$ line count / byte count / sha256 over .remedy-wt/f020-r7-payloads/*
create_f020_evidence.py  lines=157 bytes=7773 sha256=02d2a70b7be67fe397d8a0b91cf45229ecf95d3bd4c7587a281e448da2122fa9
ledger.diff              lines=10  bytes=6861 sha256=e6d7ca1d6933122b0d64d85940582623ecb55252d83c4adf626c5429219d116a
plan.md                  lines=28  bytes=980  sha256=f0892cff3851b40b1c1b6cebbc19d9348e05cb5a13796bc03eb59b4867d03827
```
All 3 match the PAYLOADS table exactly (G1).

```
$ (compare each committed .agent/authored/f020-r7-* blob, read with `git show <C1>:<path>`,
   against its source)
f020-r7-block.md                    @ 09861d084: match=True
f020-r7-create_f020_evidence.py     @ 09861d084: match=True
f020-r7-ledger.diff                 @ 09861d084: match=True
f020-r7-plan.md                     @ 09861d084: match=True
```
All 4 BYTE-IDENTICAL against their sources (G1).

```
$ (sha256/bytes of C2's two files, read with `git show <C2>:<path>`, against the block's G2 table)
.agent/live_review.md: bytes=302572 sha256=d2fe2b2dfc06efd045d8e9a57f832f6f879badc261cf37716852876226ca8e13 match=True
.agent/plan.md:        bytes=980    sha256=f0892cff3851b40b1c1b6cebbc19d9348e05cb5a13796bc03eb59b4867d03827 match=True
```
Both match the block's G2 table exactly.

```
$ git diff 649661cd0 ac75d5d4e -- .agent/live_review.md | grep -c '^+Gate: F020 R6 — '
1
```
Matches the block's stated reading of 1 exactly (G2).

```
$ open_finding_ids(text) from scripts/rotate_live_review.py, over .agent/live_review.md's TEXT
  at 649661cd0 and at ac75d5d4e (C2)
649661cd0 open ids: ['R-1008']
ac75d5d4e (C2) open ids: ['R-1008']
```
Reads R-1008 alone at both, matching the block's stated reading exactly (G2).

```
$ bash -c 'python3 .remedy-wt/f020-r7-payloads/create_f020_evidence.py >
  .remedy-wt/f020-r7-worker/evidence.log 2>&1; echo "REAL_EXIT=$?"'
REAL_EXIT=0
$ cat .remedy-wt/f020-r7-worker/evidence.log
head ac75d5d4ebe6f7aa908ccdfd1dfa504582b2fb5e
ancestry-path count 52
plain count 52
collected node ids 810, deselected 16
red control: unsafe among the real ids 0 []
red control: planted id -> a local absolute path
pytest exit 0, {'passed': 807, 'failed': 0, 'skipped': 3}, output_hash e77229dee7e649ac6b46d700d74e6b9c9a52692ba7b680de221a7ad962cf56e9
validate_verification_tests problems [] passed 807
is_valid_current_run True
validation_errors []
gates written: ['artifact_contract_gate.json', 'change_provenance_gate.json', 'commit_execution_gate.json', 'fresh_evidence_gate.json', 'runtime_integration_gate.json', 'final_verifier_report.json']
{
  "job_id": "f020r7e1001",
  "head_commit": "ac75d5d4ebe6f7aa908ccdfd1dfa504582b2fb5e",
  ...
  "verdict": "PASS_WITH_RISKS",
  ...
}
```
Script exit 0. Ancestry-path count 52, plain count 52 — EQUAL, and both read two more than the
reviewer's dry-run reading of 50 at `649661cd`, exactly as the block states. Collected node ids
810, deselected 16 — matches the reviewer's stated dry-run reading. Red control: 0 unsafe among
real ids; the planted id answered "a local absolute path" — both match. Pytest exit 0, 807 passed,
3 skipped — matches. `validate_verification_tests` problem list EMPTY. `is_valid_current_run` True
with no validation error. Evidence job id `f020r7e1001` (G3).

```
$ ls .remedy-wt/f020-r7-evidence/ | grep -E '_gate\.json$|_integrity\.json$|^final_verifier_report\.json$'
artifact_contract_gate.json
change_provenance_gate.json
commit_execution_gate.json
fresh_evidence_gate.json
human_change_integrity.json
manifest_integrity.json
postmortem_integrity.json
runtime_integration_gate.json
final_verifier_report.json
```
9 files (G3).

```
$ git status --porcelain
(empty)
$ bash scripts/make_review_zip.sh --evidence-dir .remedy-wt/f020-r7-evidence
...
{"member_count": 5731, "authoritative_count": 34, "symlink_count": 0, "tombstone_count": 0,
 "final_path": "/home/decodeux/Repos/remedy-history/zips/remedy-review-20260925-013441-READY_FOR_REVIEW.zip",
 "final_sha256": "a069e502d3956af33f4e7dde2ece1dfd47355c68030181dbd5764af6d026d1e0",
 "publication_capability": "SUPPORTED", "package_status": "READY_FOR_REVIEW",
 "evidence_authoritative": true, "review_subject_alignment": "PASS",
 "manifest_sha256": "ee6f79e6c9fe8207796f1c1f95b7afd7c39c99d59d60d40a65cf264f0a64b2b9"}
============================================
REVIEW_PACKAGE_CREATED=true
PACKAGE_STATUS=READY_FOR_REVIEW
EVIDENCE_AUTHORITATIVE=true
REVIEW_PACKAGE_DIR=/home/decodeux/Repos/remedy-history/zips
ZIP_PATH=/home/decodeux/Repos/remedy-history/zips/remedy-review-20260925-013441-READY_FOR_REVIEW.zip
============================================
REAL_EXIT=0
```
`PACKAGE_STATUS=READY_FOR_REVIEW`, `EVIDENCE_AUTHORITATIVE=true` (G4).

```
$ python3 -c "import zipfile; z=zipfile.ZipFile(...); print(zipfile.is_zipfile(path), z.testzip())"
is_zipfile: True
testzip(): None
```
(G4)

```
$ .review_zip_manifest.json → committed_review_subject, read INSIDE the package
{
  "base_commit": "955a6240d53fcc88f4480e57a89c0ef702f7c6b9",
  "base_is_ancestor": true,
  "commit_count": 52,
  "file_count": 108,
  "head_commit": "ac75d5d4ebe6f7aa908ccdfd1dfa504582b2fb5e",
  "tombstones": []
}
```
`head_commit` equals C2's full sha exactly; `base_commit` equals the fork point
`955a6240d53fcc88f4480e57a89c0ef702f7c6b9` exactly (G4).

```
$ python3 -m apps.cli.main integrity check --json
{"check_count": 6, "checks": [
  {"name": "handler_import", "status": "pass", "message": "handlers=157"},
  {"name": "live_review_verdict", "status": "pass", "message": "last Gate verdict PASS"},
  {"name": "plan_consistency", "status": "pass", "message": "unchecked=0, context_complete=False"},
  {"name": "relevant_untracked", "status": "pass", "message": "untracked=0, relevant=0"},
  {"name": "repo_root_hygiene", "status": "pass", "message": "no reviewer scratch, evidence dir or archive at the root"},
  {"name": "high_blockers_open", "status": "pass", "message": "no open blocker/high findings"}
], "fail_count": 0, "ok": true, "passed": true, "schema_version": 1, "version": 1}
REAL_EXIT=0
$ git status --porcelain
(empty)
$ git worktree list
(unchanged from round start: primary + 39 reviewer worktrees + 4 job-* worktrees)
```
All six checks `pass`, `fail_count` 0; tree clean after A2 (G5).

## Authored-text proofs

All 4 authored copies under `.agent/authored/f020-r7-*` (the block copy plus the three payload
copies) were built by `shutil.copyfile` from source to destination — never retyped, never edited.
Each was read back with `git show <C1>:<path>` and compared byte for byte against its source: all
4 BYTE-IDENTICAL (G1 above). `ledger.diff` was applied with `git apply` after `git apply --check`
passed (exit 0 both), never retyped or edited; the resulting `.agent/live_review.md` was verified
by byte count and sha256 against the block's G2 table — MATCH. `.agent/plan.md` was rewritten
whole via `shutil.copyfile` from the payload source — never retyped — and confirmed MATCH against
both the PAYLOADS table and the G2 table. `create_f020_evidence.py` was run unmodified from its
payload path (never applied, per the block's own instruction) as a tool for A1, not a text
application.

## Deviations & assumptions

None. Every commit and action landed in the block's stated order C1, C2 (then push), A1, A2, G1
through G5, then C3, exactly as ordered. No payload was edited, retyped or repaired. The round's
tracked path set through C2 matched constraint 3 exactly (`git diff --name-only 649661cd0 HEAD`
before C3: the four `.agent/authored/f020-r7-*` copies, `.agent/live_review.md`, `.agent/plan.md`
— six paths, all named by constraint 3, nothing under `apps/`, `packages/`, `tests/` or `docs/`, no
edit to `docs/roadmap/STATUS.md`, `README.md` or `scripts/self_use_queue.json`); C3 adds exactly
the one remaining named path, `.agent/handoff.md`. No evidence directory was committed — A1's
bundle stayed under the gitignored `.remedy-wt/f020-r7-evidence/`. The package read
`READY_FOR_REVIEW`, so no blocker condition (constraint 4) applied. Nothing was merged or closed
this round: no `gh pr merge`, no `gh pr create`, no checkout of `main`, no STATUS edit, no README
edit, no ledger rotation — per constraint 5. The reviewer's worktrees, the
`f015-r*`/`f284-r*`/`f020-r*` worktrees and the `job-*` worktrees/branches were left untouched —
per constraint 6 (`git worktree list` unchanged from round start, `remedy/job-*` branch count 41
unchanged).

## Item-status table

| Item | Status | Reason |
|---|---|---|
| C1 | done | 365 insertions, matches block's expectation (170+195) exactly; under the 500-insertion cap |
| C2 | done | ledger.diff apply --check and apply both exit 0; 2/0, 5/7 insertions, matches exactly; PUSHED |
| A1 | done | evidence job exit 0; ancestry counts 52/52 equal, two more than the reviewer's 50; all readings matched |
| A2 | done | package READY_FOR_REVIEW, EVIDENCE_AUTHORITATIVE true; manifest base/head match fork point and C2 |
| G1 | done | all 3 payload digests and 4 authored-copy comparisons matched |
| G2 | done | both named file digests matched; gate-line count 1; open set R-1008 alone at both |
| G3 | done | script exit 0; all readings matched; 9 gate/integrity/final-verifier files present |
| G4 | done | READY_FOR_REVIEW, authoritative true, zip valid (testzip None), manifest base/head match |
| G5 | done | integrity check 6/6 pass, fail_count 0; tree clean; worktree list unchanged |
| G6 | pending | runs after this commit (tree/log check, push, `gh pr list`); reported in the reply |
| PUSH | pending | `git push origin feature/f020-node-lifecycle-glyph-language`, reported in the reply |

## Next

Phase 1 rule 1: read `.agent/STOP` from disk. Then the review of round 7. Then the closing round:
the booking of round 7, the ledger rotation, the STATUS line with the README counters in the same
commit, and the pull request. Open findings: 1. Operator questions open: 3.
