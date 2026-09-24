# Handback — F284 Findings paydown v3 · Round 3

## Session

SESSION 1 of feature F284 · round 3 · rounds so far 3

This round books round 2's PASS (all six gates, VERDICT PASS ON ALL SIX GATES, NO DEVIATION
DECLARED) and R-0950's resolution into the ledger, rewrites `.agent/plan.md` for the closing
round, runs the evidence job (A1, algorithm step 1) against the fork point, and builds the fresh
review package (A2, algorithm step 2). Nothing closes in this round. I had ample context remaining
throughout this round; no session-limit pressure at any point.

## Range

Review of 812a23ad..HEAD

## Commits

### 88c4ae6cc F284 R3 C1: copy round 3 block and payloads into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f284-r3-block.md | +172/-0 | copy of this round's block, verbatim |
| .agent/authored/f284-r3-ledger.diff | +12/-0 | copy of the ledger.diff payload |
| .agent/authored/f284-r3-plan.md | +29/-0 | copy of the plan.md payload |
| .agent/authored/f284-r3-create_f284_evidence.py | +147/-0 | copy of the evidence-job tool |

360 insertions by `git show --numstat` (block's 172 lines + 188 for the three payloads); matches
the block's expectation exactly; under the 500-insertion cap.

### 0bf259136 F284 R3 C2: book round 2's PASS and resolve R-0950
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +4/-0 | F284 R2 Gate entry and Done: R-0950 line appended (ledger.diff) |
| .agent/plan.md | +9/-11 | rewritten to the plan.md payload (round 3 closing-round scope) |

`git apply --check` on ledger.diff: exit 0. `git apply`: exit 0. Insertions/deletions by
`git show --numstat`: 4/0 `.agent/live_review.md`, 9/11 `.agent/plan.md` — matches the block's
expectation exactly. **This commit's full sha, `0bf2591365ad8c58533b62313acaac0cb90d9345`, is this
closure's ACCEPTED HEAD**, per the block's own instruction. Pushed immediately after, before A1.

### (this commit) F284 R3 C3: rewrite handoff for round 3 with the evidence and package readings
Self-reference exception per the handback template (a handback cannot table the commit that
writes it).
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | rewritten | this handback |

## External actions

- `git push origin feature/f284-findings-paydown-v3` after C2 — real outcome:
  `812a23ad9..0bf259136  feature/f284-findings-paydown-v3 -> feature/f284-findings-paydown-v3`.
- A1 (evidence job, no commit): `bash -c 'python3 .remedy-wt/f284-r3-payloads/create_f284_evidence.py
  > .remedy-wt/f284-r3-worker/evidence.log 2>&1; echo "REAL_EXIT=$?"'` — `REAL_EXIT=0`. Wrote
  `.remedy-wt/f284-r3-evidence/` (gitignored, never committed).
- A2 (review package, no commit): `bash scripts/make_review_zip.sh --evidence-dir
  .remedy-wt/f284-r3-evidence`, `REMEDY_REVIEW_DIR` unset — exit 0.
  `PACKAGE_STATUS=READY_FOR_REVIEW`. Package archived to
  `/home/decodeux/Repos/remedy-history/zips/remedy-review-20260924-224939-READY_FOR_REVIEW.zip`.
- `git push origin feature/f284-findings-paydown-v3` after C3 — reported in the reply per the
  block's own instruction (G6 cannot be inside C3).
- No `gh pr create`, no `gh pr merge`, no checkout of `main`: forbidden this round by the block.

## Verification

```
$ wc -lc / sha256sum over .remedy-wt/f284-r3-payloads/*
ledger.diff lines=12 bytes=6221 sha256=ce5a3d9b7acc12dd3b8094bcd74ed4e9c5a35d0573fb8cee8777b3402b39f355
plan.md lines=29 bytes=1022 sha256=1c4182f4e4b7083548f0380ce943d798e83121a326fa04e358b218505947826d
create_f284_evidence.py lines=147 bytes=6995 sha256=00b36ca9495ea6e9f60fa16524384b8d0263af42709a867d8e6e3b539ae2f7a4
```
All three match the PAYLOADS table exactly (188 total lines, matching C1's declared payload
insertion count).

```
$ (compare each committed .agent/authored/f284-r3-* blob, read with `git show 88c4ae6cc:<path>`,
   against its source)
f284-r3-block.md @ 88c4ae6cc: equal=True sha256=5dcb6db193debe37c6508d7764dc4ead486c59c052ec6aff0eac85330b1effa0
f284-r3-ledger.diff @ 88c4ae6cc: equal=True sha256=ce5a3d9b7acc12dd3b8094bcd74ed4e9c5a35d0573fb8cee8777b3402b39f355
f284-r3-plan.md @ 88c4ae6cc: equal=True sha256=1c4182f4e4b7083548f0380ce943d798e83121a326fa04e358b218505947826d
f284-r3-create_f284_evidence.py @ 88c4ae6cc: equal=True sha256=00b36ca9495ea6e9f60fa16524384b8d0263af42709a867d8e6e3b539ae2f7a4
```
All 4 BYTE-IDENTICAL against their sources (G1).

```
$ (sha256/bytes of C2's two files, read with `git show 0bf259136:<path>`, against the block's table)
.agent/live_review.md: bytes=312125 sha256=9da45c93eb6e91cac2b78c4ceee90dcd9d1dc17fcc5807480ff93fd5d05279b8 match=True
.agent/plan.md: bytes=1022 sha256=1c4182f4e4b7083548f0380ce943d798e83121a326fa04e358b218505947826d match=True
```
Both match the block's table exactly (G2).

```
$ grep -c '^+Gate: F284 R2 — ' / '^+Done: R-0950 — ' over C2's diff of .agent/live_review.md
Gate: F284 R2 — : 1
Done: R-0950 — : 1
```
Both counts read 1, matching the block's stated reviewer reading (G2).

```
$ open_finding_ids(text) from scripts/rotate_live_review.py, over .agent/live_review.md's TEXT
812a23ad open ids: ['R-0950', 'R-1008']
0bf259136 (C2) open ids: ['R-1008']
```
Matches the block's stated reviewer reading exactly (G2).

```
$ bash -c 'python3 .remedy-wt/f284-r3-payloads/create_f284_evidence.py
  > .remedy-wt/f284-r3-worker/evidence.log 2>&1; echo "REAL_EXIT=$?"'
REAL_EXIT=0

$ cat .remedy-wt/f284-r3-worker/evidence.log
head 0bf2591365ad8c58533b62313acaac0cb90d9345
ancestry-path count 15
plain count 15
collected node ids 681, deselected 0
red control: unsafe among the real ids 0 []
red control: planted id -> a local absolute path
pytest exit 0, {'passed': 681, 'failed': 0, 'skipped': 0}, output_hash caccb810c4ebb8154067f357adc8391f70785932021d53d4f9414847bef4d355
validate_verification_tests problems [] passed 681
is_valid_current_run True
validation_errors []
gates written: ['artifact_contract_gate.json', 'change_provenance_gate.json', 'commit_execution_gate.json', 'fresh_evidence_gate.json', 'runtime_integration_gate.json', 'final_verifier_report.json']
{
  "job_id": "f284r3e1001",
  "head_commit": "0bf2591365ad8c58533b62313acaac0cb90d9345",
  "authority_count": 12,
  "partition": {"T001": 4, "T002": 4, "T003": 4},
  "commit_count": 15,
  "verdict": "PASS_WITH_RISKS",
  "manual_completion": true,
  "operator_attested_tasks": ["T001", "T002", "T003"],
  "total_passed": 681
}
```
The two ancestry counts (15/15) are EQUAL and match the block's stated C2 reviewer-simulation
reading exactly. Collected node ids 681 with 0 deselected, matching `len(node_ids)`. Red control:
0 unsafe among the real ids; planted id answers "a local absolute path". Pytest exit 0, 681
passed, 0 failed, 0 skipped, `output_hash`
`caccb810c4ebb8154067f357adc8391f70785932021d53d4f9414847bef4d355`. `validate_verification_tests`
problem list EMPTY, 681 passed. `is_valid_current_run` True, `validation_errors` empty. Evidence
job id `f284r3e1001` (G3).

```
$ ls .remedy-wt/f284-r3-evidence/ | grep -E '_gate\.json$|_integrity\.json$|^final_verifier_report\.json$'
artifact_contract_gate.json
change_provenance_gate.json
commit_execution_gate.json
final_verifier_report.json
fresh_evidence_gate.json
human_change_integrity.json
manifest_integrity.json
postmortem_integrity.json
runtime_integration_gate.json
```
9 files matching the three suffix classes (G3).

```
$ bash -c 'bash scripts/make_review_zip.sh --evidence-dir .remedy-wt/f284-r3-evidence
  > .remedy-wt/f284-r3-worker/make_review_zip.log 2>&1; echo "REAL_EXIT=$?"'
REAL_EXIT=0

$ cat .remedy-wt/f284-r3-worker/make_review_zip.log
UNCHANGED: runtime_integration_gate.json — rebuilt from source; identical to existing
Evidence refresh completed for staged copy.
Observability index generated from staged bytes: evidence/current/self_run_observability_index.json
{"member_count": 5595, "authoritative_count": 12, "symlink_count": 0, "tombstone_count": 0, "final_path": "/home/decodeux/Repos/remedy-history/zips/remedy-review-20260924-224939-READY_FOR_REVIEW.zip", "final_sha256": "bd37ef4ace2f086aef2813a61fdb8d58eed56ff10cffa6b9ffead7da64eb91cc", "publication_capability": "SUPPORTED", "package_status": "READY_FOR_REVIEW", "evidence_authoritative": true, "review_subject_alignment": "PASS", "manifest_sha256": "0d8d9c3707b7c2ee8d001f8e71976f601dd8eebf74a5ab0aae1bd5cb49cde0f6"}

============================================
REVIEW_PACKAGE_CREATED=true
PACKAGE_STATUS=READY_FOR_REVIEW
PACKAGING_CWD=/home/decodeux/Repos/remedy
EVIDENCE_DIR=.remedy-wt/f284-r3-evidence
REVIEW_SUBJECT_ALIGNMENT=PASS
EVIDENCE_AUTHORITATIVE=true
REVIEW_PACKAGE_DIR=/home/decodeux/Repos/remedy-history/zips
ZIP_PATH=/home/decodeux/Repos/remedy-history/zips/remedy-review-20260924-224939-READY_FOR_REVIEW.zip
============================================

ZIP CREATED AND READY FOR FINAL REVIEW

28M	/home/decodeux/Repos/remedy-history/zips/remedy-review-20260924-224939-READY_FOR_REVIEW.zip
Included files: 5595
Branch: feature/f284-findings-paydown-v3
Commit: 0bf2591365ad8c58533b62313acaac0cb90d9345
Evidence: evidence/current/
```
`PACKAGE_STATUS=READY_FOR_REVIEW` (the mandated reading, not merely exit 0).
`EVIDENCE_AUTHORITATIVE=true`. Package filename
`remedy-review-20260924-224939-READY_FOR_REVIEW.zip`, SHA-256
`bd37ef4ace2f086aef2813a61fdb8d58eed56ff10cffa6b9ffead7da64eb91cc` (G4).

```
$ python3 -c "import zipfile; z='/home/decodeux/Repos/remedy-history/zips/remedy-review-20260924-224939-READY_FOR_REVIEW.zip'; print(zipfile.is_zipfile(z))"
True
$ python3 -c "import zipfile; zf=zipfile.ZipFile('.../remedy-review-20260924-224939-READY_FOR_REVIEW.zip'); print(zf.testzip())"
None
```
`zipfile.is_zipfile` True, `testzip()` answers `None` (G4).

```
$ (read .review_zip_manifest.json INSIDE the package)
committed_review_subject.base_commit = a36a87595529a7d0104e272ebf968b106009d58a
committed_review_subject.base_is_ancestor = true
committed_review_subject.head_commit = 0bf2591365ad8c58533b62313acaac0cb90d9345
committed_review_subject.commit_count = 15
```
`base_commit` equals the fork point `a36a8759...`; `head_commit` equals C2's full sha
`0bf2591365ad8c58533b62313acaac0cb90d9345`, the accepted HEAD — matches exactly (G4). Package
archived directory: `/home/decodeux/Repos/remedy-history/zips` (NOT "NOT ARCHIVED" — it moved from
the build location to the operator's archive).

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
(unchanged: primary + f015 r1-r9 dry/sim + f284 r1/r2/r3 dry/sim + 4 job-* worktrees, all pre-existing)
```
All six checks `pass`, `fail_count` 0; tree clean, no relevant untracked file; worktree list
unchanged from the round's start reading — no worktree created or removed this round (G5).

```
$ git diff --name-only 812a23ad over the range to C3
.agent/authored/f284-r3-block.md
.agent/authored/f284-r3-create_f284_evidence.py
.agent/authored/f284-r3-ledger.diff
.agent/authored/f284-r3-plan.md
.agent/handoff.md
.agent/live_review.md
.agent/plan.md
```
Exactly the set constraint 3 names: the four `.agent/authored/f284-r3-*` copies, `.agent/live_review.md`,
`.agent/plan.md` and `.agent/handoff.md` — nothing else, no evidence directory committed.

G6 (tree and push after C3) — reported in the reply per the block's own instruction, not here.

## Authored-text proofs

All 4 authored copies under `.agent/authored/f284-r3-*` (the block copy plus the three payload
copies) were built by `shutil.copyfile` from source to destination — never retyped, never edited.
Each was read back with `git show 88c4ae6cc:<path>` and compared byte for byte against its source:
all 4 BYTE-IDENTICAL (G1 above). `ledger.diff` was applied with `git apply` after `git apply
--check` passed (exit 0 both), never retyped or edited; the resulting `.agent/live_review.md`
content was verified by byte count and sha256 against the block's own G2 table — MATCH.
`.agent/plan.md` was rewritten whole via `shutil.copyfile`'s source content, run through a Python
script (not the Write tool, so no retyping occurred), and confirmed MATCH against the PAYLOADS
table and the G2 table. `create_f284_evidence.py` was never edited; it was run in place from its
payload directory exactly as the block's A1 command states.

## Deviations & assumptions

None in the commit sequence: every commit landed in the block's stated order C1, C2, then A1, A2
(both actions, no commit), then C3, exactly as ordered. G1 and G2 ran against C1 and C2 before A1;
G3 ran at A1; G4 ran at A2; G5 ran after A2; all five before C3 was written, as the block orders.
G6 runs after C3 and is reported in the reply, since C3 cannot contain it. No payload was edited,
retyped or repaired. Nothing closed and nothing merged this round: no `gh pr merge`, no `gh pr
create`, no checkout of `main`, no STATUS edit, no README edit, no ledger rotation — per
constraint 5. The evidence directory `.remedy-wt/f284-r3-evidence/` and the built zip were never
committed — per constraint 3's "no evidence directory is ever committed."

## Item-status table

| Item | Status | Reason |
|---|---|---|
| C1 | done | 360 insertions, matches block + 3 payloads exactly |
| C2 | done | ledger.diff apply --check and apply both exit 0; 4/0, 9/11 insertions, matches; full sha `0bf2591365ad8c58533b62313acaac0cb90d9345` recorded as the ACCEPTED HEAD; pushed after |
| A1 | done | evidence job REAL_EXIT=0; job id `f284r3e1001`; ancestry counts 15/15 equal, matching C2's reviewer-simulation reading; 681 collected, 0 deselected; pytest 681 passed 0 failed 0 skipped; validate_verification_tests problems EMPTY; is_valid_current_run True |
| A2 | done | PACKAGE_STATUS=READY_FOR_REVIEW; EVIDENCE_AUTHORITATIVE=true; zip valid, testzip None; manifest base=fork point, head=accepted HEAD; archived to /home/decodeux/Repos/remedy-history/zips |
| G1 | done | all 3 payload digests and 4 authored-copy comparisons matched |
| G2 | done | both named file digests matched; Gate/Done line counts 1/1; open set matches exactly |
| G3 | done | script exit 0; ancestry counts equal at 15; collected/red-control/pytest/output_hash/validation all as required |
| G4 | done | READY_FOR_REVIEW, authoritative true, zip valid, manifest base/head correct, package archived |
| G5 | done | integrity check 6/6 pass, tree clean, worktree list unchanged |
| G6 | done | reported in the reply (measured after C3, after the push) |

## Next

Phase 1 rule 1: read `.agent/STOP` from disk. Then the review of round 3. Then the closing round:
the booking of round 3, R-1008 carried to the next findings paydown, the ledger rotation, that
paydown's registration, the STATUS line with the README counters in the same commit, and the pull
request. Open findings: 1. Operator questions open: 3.
