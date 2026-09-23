# Handback — F279 Configuration & toolchain truth · Round 10 · The closure sequence's evidence half: the bundle and the package

## Session

SESSION 2 of feature F279 · round 10 · rounds so far 10

This round booked round 9's PASS and its two flaky suite nodes into the
ledger as recurrences of R-0950 and R-1028, built the feature's evidence
bundle against the fork point `c9bc5c2057b57db8e0a6f4505c91374ac364a5f8`,
and built the fresh review package. Nothing closed. Context remaining at
handback: roughly two-thirds of the budget, ample for the reviewer to open
round 11.

## Range

Review of `118b645e`..`9ee2659888d3c30969d102616503cc2898e26e2c`

## Commits

### f97ddad3 F279 R10 C1: copy round 10 block and payloads into .agent/authored/

| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f279-r10-block.md | 167/0 | byte-for-byte copy of this round's block |
| .agent/authored/f279-r10-create_f279_evidence.py | 133/0 | byte-for-byte copy of the A1 evidence tool |
| .agent/authored/f279-r10-ledger.md | 6/0 | byte-for-byte copy of the ledger append payload |
| .agent/authored/f279-r10-plan.md | 29/0 | byte-for-byte copy of the plan rewrite payload |

Measured insertions: 335 (167 + 133 + 6 + 29), matching the block's stated
"this block's line count plus 168" (167 + 168 = 335), per `git commit`'s own
report `4 files changed, 335 insertions(+)`.

### 9ee26598 F279 R10 C2: book round 9's PASS and record the two flaky nodes as recurrences

| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | 6/0 | strict byte-append of ledger.md's Gate + two Recurrence paragraphs |
| .agent/plan.md | 10/12 | rewrite to plan.md payload |

Measured insertions/deletions by `git show --numstat 9ee26598`: `6	0	.agent/live_review.md` and `10	12	.agent/plan.md` — matching the block's expected 6 and 10 exactly. This commit's full sha, `9ee2659888d3c30969d102616503cc2898e26e2c`, is this closure's ACCEPTED HEAD.

C3 (this handoff's own commit) carries no table of its own: a handoff
cannot table the commit that writes it (R-0149 pattern, self-reference
exception).

## External actions

- `git push origin feature/f279-configuration-toolchain-truth` after C2: real outcome `118b645e..9ee26598  feature/f279-configuration-toolchain-truth -> feature/f279-configuration-toolchain-truth`.
- `git push origin feature/f279-configuration-toolchain-truth` after C3: to ship this handback (outcome reported in the worker's final reply, not repeated here per write-once).
- No `gh pr` command was run. No worktree add/remove.

## Verification

**A1 — the evidence job**, from repo root: `bash -c 'python3 .remedy-wt/f279-r10-payloads/create_f279_evidence.py > .remedy-wt/f279-r10-scratch/evidence.log 2>&1; echo "REAL_EXIT=$?"'` → `REAL_EXIT=0`.

Evidence log (`.remedy-wt/f279-r10-scratch/evidence.log`), full contents:

```
head 9ee2659888d3c30969d102616503cc2898e26e2c
ancestry-path count 52
plain count 52
collected node ids 149
red control: unsafe among the real ids 0 []
red control: planted id -> a local absolute path
pytest exit 0, {'passed': 149, 'failed': 0, 'skipped': 0}, output_hash b60a824effd8c9038ea6b819826c5bb6675e3a639c9e81ea5055e5351b7607a7
validate_verification_tests problems [] passed 149
is_valid_current_run True
validation_errors []
gates written: ['artifact_contract_gate.json', 'change_provenance_gate.json', 'commit_execution_gate.json', 'fresh_evidence_gate.json', 'runtime_integration_gate.json', 'final_verifier_report.json']
{
  "job_id": "f279r10e1001",
  "head_commit": "9ee2659888d3c30969d102616503cc2898e26e2c",
  "authority_count": 37,
  "partition": {"T001": 13, "T002": 13, "T003": 11},
  "commit_count": 52,
  "verdict": "PASS_WITH_RISKS",
  "manual_completion": true,
  "operator_attested_tasks": ["T001", "T002", "T003"],
  "total_passed": 149
}
```

Both ancestry counts equal at 52; collected node ids 149 equal the pytest
pass count 149; the red control's planted id answered `a local absolute
path` with 0 unsafe among the real ids; pytest exit 0 with 149 passed, 0
failed, 0 skipped; `validate_verification_tests` problem list empty over
149 passed; `is_valid_current_run` True with an empty validation_errors
list. Every count reads exactly one more than the reviewer's simulation (51
ancestry/plain, 148 node ids, 148 passed) because this round's C1 block copy
joins the parametrized block test of `test_block_lint.py`, matching the
block's own prediction. Evidence job id: `f279r10e1001`.

`.remedy-wt/f279-r10-evidence/` (gitignored) holds, among others, the files
named `*_gate.json`, `*_integrity.json` and `final_verifier_report.json`:
`artifact_contract_gate.json`, `change_provenance_gate.json`,
`commit_execution_gate.json`, `fresh_evidence_gate.json`,
`runtime_integration_gate.json`, `final_verifier_report.json`,
`manifest_integrity.json`, `postmortem_integrity.json` — all eight required
names present (`ls` of the directory).

**A2 — the review package**: tree clean and branch pushed first (`git
status --porcelain` empty; local HEAD `9ee26598` = `origin/...` HEAD
`9ee26598`). `bash scripts/make_review_zip.sh --evidence-dir
.remedy-wt/f279-r10-evidence` → final JSON line:
`{"member_count": 5299, "authoritative_count": 37, "symlink_count": 0,
"tombstone_count": 0, "final_path":
"/home/decodeux/Repos/remedy-history/zips/remedy-review-20260923-091251-READY_FOR_REVIEW.zip",
"final_sha256":
"c59772f93dab75c9a8aa9da3624fa48f45fcc9afe0a372958ce74c2663640224",
"publication_capability": "SUPPORTED", "package_status":
"READY_FOR_REVIEW", "evidence_authoritative": true,
"review_subject_alignment": "PASS", "manifest_sha256":
"b5c4af1d211845acf5cfe52e98712b59782c66ccb4f4ee047833873be420e1dd"}` and the
summary block: `PACKAGE_STATUS=READY_FOR_REVIEW`,
`EVIDENCE_AUTHORITATIVE=true`,
`ZIP_PATH=/home/decodeux/Repos/remedy-history/zips/remedy-review-20260923-091251-READY_FOR_REVIEW.zip`.

Package filename: `remedy-review-20260923-091251-READY_FOR_REVIEW.zip`.
SHA-256 (independently recomputed with Python's `hashlib.sha256` over the
file, matching the script's own `final_sha256`):
`c59772f93dab75c9a8aa9da3624fa48f45fcc9afe0a372958ce74c2663640224`. Archived
directory: `/home/decodeux/Repos/remedy-history/zips`.

`committed_review_subject` read from `.review_zip_manifest.json` inside the
package: `"base_commit": "c9bc5c2057b57db8e0a6f4505c91374ac364a5f8"`,
`"head_commit": "9ee2659888d3c30969d102616503cc2898e26e2c"` — head equals
C2's full sha, base equals the fork point. The package's own
`package_status` field (read from the same manifest) reads
`"READY_FOR_REVIEW"`.

Zip import check: `zipfile.is_zipfile(path)` → `True`; `zf.testzip()` →
`None`.

**G5 — the tree, after A2**: `python3 -m apps.cli.main integrity check
--json` → `{"check_count": 5, "checks": [{"name": "handler_import",
"status": "pass"}, {"name": "live_review_verdict", "status": "pass"},
{"name": "plan_consistency", "status": "pass"}, {"name":
"relevant_untracked", "status": "pass"}, {"name": "high_blockers_open",
"status": "pass"}], "fail_count": 0, "ok": true, "passed": true}` — all
five checks `pass`, `fail_count` 0. `git status --porcelain` empty, no
relevant untracked file. `git worktree list` unchanged: the primary
checkout plus the three pre-existing `job-*` worktrees
(`job-129b3ad7206d4f8d`, `job-e7268925db3a4831`, `job-e7a145761bf04f86`),
none added or removed.

## Authored-text proofs

- `.agent/authored/f279-r10-block.md` (C1) == `.remedy-wt/f279-r10-block.md`: equal, sha256 `333a773ba2f9b2d0478b4b2c94fec409b3acd46301b4f44b104573d3f079ac8d` both sides.
- `.agent/authored/f279-r10-create_f279_evidence.py` (C1) == `.remedy-wt/f279-r10-payloads/create_f279_evidence.py`: equal, sha256 `bac2fe446f8e3017ee98c09663bec053600187965f3cbd5d178c2f83709c70da` both sides.
- `.agent/authored/f279-r10-ledger.md` (C1) == `.remedy-wt/f279-r10-payloads/ledger.md`: equal, sha256 `787102b238cb87dfba93c90ccbde50666f22364fc42ef00a6543b386ad05de7d` both sides.
- `.agent/authored/f279-r10-plan.md` (C1) == `.remedy-wt/f279-r10-payloads/plan.md`: equal, sha256 `04d6e1514f50fae0b28c61acdabaac3b1fe0284cdd960b907e7db10076deb4fa` both sides.
- APPLIED text: the bytes C2 appended to `.agent/live_review.md` (the tail after round 9's ending) compared byte-for-byte to the committed `.agent/authored/f279-r10-ledger.md` blob: equal.
- APPLIED text: `.agent/plan.md` as rewritten by C2 compared byte-for-byte to the committed `.agent/authored/f279-r10-plan.md` blob: equal.

## Deviations & assumptions

None. The round followed C1, C2, A1, A2, C3 in the block's exact order,
with the push placed after C2 and before A1 as ordered.

## Next

Phase 1 rule 1 (read `.agent/STOP` from disk), then the review of round 10.
After that, the closing round: the ledger rotation, the STATUS line with
the README counters and the self-use item's `consumed_by` in the same
commit, and the pull request. Open findings after this round: the same set
as at `118b645e` (28 by distinct id, both differences empty per G2).
Operator-questions count: 0.
