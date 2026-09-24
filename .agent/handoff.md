# Handback — F282 Findings paydown v2 · Round 12 · The closure sequence's evidence half: book round 11, build the bundle and the package

## Session

SESSION 2 of feature F282 · round 12 · rounds so far 12

This round booked round 11's PASS into the ledger (`.agent/live_review.md`
gains the `Gate: F282 R11 —` entry; `.agent/plan.md` rewritten to round
12's plan), then ran the evidence job (A1) against the fork point
`b8fa02bad0ae82c18b7d9805b5c2d15b9a44532d` and built the fresh review
package (A2). The evidence job read `is_valid_current_run True` with no
validation errors, and the package read `PACKAGE_STATUS=READY_FOR_REVIEW`
with `EVIDENCE_AUTHORITATIVE=true`. Nothing closes this round. Well over
99% of this session's working-context budget remained at handback.

## Range

Review of `f757fbca`..`HEAD`.

## Commits

### ae85339c F282 R12 C1: copy round 12 block and payloads into .agent/authored/

| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f282-r12-block.md | +167/-0 | Bookkeeping copy of this round's step block (R-0954 transport) |
| .agent/authored/f282-r12-create_f282_evidence.py | +146/-0 | Payload copy (the evidence-job TOOL, never edited) |
| .agent/authored/f282-r12-ledger.diff | +10/-0 | Payload copy |
| .agent/authored/f282-r12-plan.md | +29/-0 | Payload copy |

Measured insertions by `git show --numstat`: 352 (167+146+10+29),
matching the block's stated formula "this block's line count plus 185"
exactly (167+185=352, and 146+10+29=185). Under the 500 cap.

### 3d7afae1 F282 R12 C2: book round 11's PASS, the closure suite green after one repair

| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +2/-0 | `ledger.diff` applied: the `Gate: F282 R11 —` entry appended |
| .agent/plan.md | +7/-8 | Rewritten to the round-12 `plan.md` payload (via `shutil.copyfile`) |

Measured insertions/deletions by `git diff --numstat` before commit:
2/0 live_review.md, 7/8 plan.md — matching the block's expected numbers
exactly. Under the 500 cap. C2's full sha,
`3d7afae1a51b89fc039d44801991ce6390347402`, is this closure's ACCEPTED
HEAD.

### (this commit) F282 R12 C3: rewrite handoff for round 12 with the evidence and package readings

| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | rewritten | This handback, per `docs/agents/handback_template.md` — a handback cannot table the commit that writes it (R-0149 self-reference exception) |

## External actions

- `git push origin feature/f282-findings-paydown-v2` after C2 — real
  outcome: `f757fbca..3d7afae1  feature/f282-findings-paydown-v2 ->
  feature/f282-findings-paydown-v2`, real exit 0.
- A1 (the evidence job) and A2 (the review package) are ACTIONS ordered
  by the block that commit nothing; their full readings are under
  Verification (G3, G4) below. A1 wrote
  `.remedy-wt/f282-r12-evidence/` (gitignored, uncommitted). A2 wrote
  the package to `/home/decodeux/Repos/remedy-history/zips/` (outside
  the repository, the operator's archive; `REMEDY_REVIEW_DIR` was not
  set).
- No worktree add/remove this round; `git worktree list` before and
  after this round's work is unchanged — the primary checkout plus
  `f282-r11-dry`, `f282-r11-sim`, `f282-r12-sim` and the four
  `job-*` worktrees, exactly as constraint 6 requires.
- No `gh pr create`, no `gh pr merge`, no checkout of `main`, no branch
  deletion, no force-push, no `git stash` in any form.
- `git push origin feature/f282-findings-paydown-v2` after C3 — real
  outcome reported in the worker's final reply (G6 readings, per the
  block, do not live in this committed file).

## Verification

**G1 — transport**: each of the three payloads' lines/bytes/sha256
measured against the block's PAYLOADS table — all three rows matched
exactly (ledger.diff 10/3591, plan.md 29/1023, create_f282_evidence.py
146/6648 — all sha256 digests equal to the table). The block itself:
167 lines (newline count), sha256
`9031e4856290fe78eeea33ddf59f03737a8e539d902b0a255487b7ea5a3a6317`,
matching the delegation message's two stated readings exactly (R-0954).
Every committed `.agent/authored/f282-r12-*` blob read with `git show
ae85339c:<path>` compared byte-for-byte against its
`.remedy-wt/f282-r12-payloads/` (or block) source: all four pairs
byte-identical = True (11662, 3591, 1023, 6648 bytes respectively).

**G2 — the booking**: at C2 (`3d7afae1`), `.agent/live_review.md`
436392 bytes, sha256
`2a8e5366d042e810420ae1ef8917bae233cb8b2401d6df11e62aa0a1188e9638`;
`.agent/plan.md` 1023 bytes, sha256
`46c9242f6f8f9e31aa03d5ea3b00c458e0fa64109aa14baea2c5bff9fd807bed` —
both equal to the block's table exactly. Among the lines C2's diff
ADDS, those beginning `Gate: F282 R11 — `: 1 (the entire ledger
paragraph is one such line). Open finding ids via
`scripts/rotate_live_review.py`'s `open_finding_ids(text)`: 3 at
`f757fbca` (`R-0499`, `R-0950`, `R-1008`), 3 at C2 (`3d7afae1`), same
three ids; both set differences (`base - head`, `head - base`) empty —
matching the block's reading exactly.

**G3 — the bundle (A1)**: `bash -c 'python3
.remedy-wt/f282-r12-payloads/create_f282_evidence.py >
.remedy-wt/f282-r12-worker/evidence.log 2>&1; echo "REAL_EXIT=$?"'`,
real exit 0. Log:
```
head 3d7afae1a51b89fc039d44801991ce6390347402
ancestry-path count 67
plain count 67
collected node ids 696
red control: unsafe among the real ids 0 []
red control: planted id -> a local absolute path
pytest exit 0, {'passed': 696, 'failed': 0, 'skipped': 0}, output_hash 6b5e10862dfec7fb75cba166cea4a761e42b58377d9246b6011b3eaa88c9eefc
validate_verification_tests problems [] passed 696
is_valid_current_run True
validation_errors []
gates written: ['artifact_contract_gate.json', 'change_provenance_gate.json', 'commit_execution_gate.json', 'fresh_evidence_gate.json', 'runtime_integration_gate.json', 'final_verifier_report.json']
```
Ancestry-path count (67) equals the plain count (67) — the two ancestry
counts are equal, one more than the reviewer's simulation's 66 because
this tree also holds C1, as the block predicted. Collected count: 696
node ids, equal to `len(node_ids)`. Red control: 0 unsafe among the 696
real ids; the planted unsafe id answered `a local absolute path`.
Pytest exit 0, 696 passed / 0 failed / 0 skipped — 2 more passed than
the reviewer's simulation's 694 passed/2 skipped, because this primary
checkout carries the UI toolchain, so
`tests/ui_contracts/test_ui_lint.py`'s two tests run instead of
skipping, exactly as the block predicted. `output_hash`
`6b5e10862dfec7fb75cba166cea4a761e42b58377d9246b6011b3eaa88c9eefc`.
`validate_verification_tests` problem list: empty (`[]`).
`is_valid_current_run`: `True`, `validation_errors`: empty (`[]`).
Evidence job id: `f282r12e1001`. Files under
`.remedy-wt/f282-r12-evidence/` whose names end `_gate.json`,
`_integrity.json` or `final_verifier_report.json` (9, read directly
from the directory listing, wider than the script's own print which
only globs `*_gate.json` and `final_verifier_report.json`):
`artifact_contract_gate.json`, `change_provenance_gate.json`,
`commit_execution_gate.json`, `fresh_evidence_gate.json`,
`runtime_integration_gate.json`, `final_verifier_report.json`,
`human_change_integrity.json`, `manifest_integrity.json`,
`postmortem_integrity.json`.

**G4 — the package (A2)**: tree clean and branch pushed before running
`bash scripts/make_review_zip.sh --evidence-dir
.remedy-wt/f282-r12-evidence` (no `REMEDY_REVIEW_DIR` set), real exit
0. Tool's own JSON line:
```
{"member_count": 5299, "authoritative_count": 46, "symlink_count": 0, "tombstone_count": 0, "final_path": "/home/decodeux/Repos/remedy-history/zips/remedy-review-20260924-025907-READY_FOR_REVIEW.zip", "final_sha256": "87eccda52d816efd0f352f40decbb30139a11fdb1eb9554d80a5c1489faa2c44", "publication_capability": "SUPPORTED", "package_status": "READY_FOR_REVIEW", "evidence_authoritative": true, "review_subject_alignment": "PASS", "manifest_sha256": "8130ce803616949a8f96d627ba0adb3f66b7ac5bb322d7e9c7e96da66840b194"}
```
And the tool's summary block:
```
REVIEW_PACKAGE_CREATED=true
PACKAGE_STATUS=READY_FOR_REVIEW
PACKAGING_CWD=/home/decodeux/Repos/remedy
EVIDENCE_DIR=.remedy-wt/f282-r12-evidence
REVIEW_SUBJECT_ALIGNMENT=PASS
EVIDENCE_AUTHORITATIVE=true
REVIEW_PACKAGE_DIR=/home/decodeux/Repos/remedy-history/zips
ZIP_PATH=/home/decodeux/Repos/remedy-history/zips/remedy-review-20260924-025907-READY_FOR_REVIEW.zip
```
`PACKAGE_STATUS`: `READY_FOR_REVIEW`. `EVIDENCE_AUTHORITATIVE`: `true`.
Package filename: `remedy-review-20260924-025907-READY_FOR_REVIEW.zip`.
SHA-256 (independently recomputed by streaming the file through
`hashlib.sha256`, matching the tool's own `final_sha256`):
`87eccda52d816efd0f352f40decbb30139a11fdb1eb9554d80a5c1489faa2c44`.
`.review_zip_manifest.json` inside the package,
`committed_review_subject`: `base_commit`
`b8fa02bad0ae82c18b7d9805b5c2d15b9a44532d` (equal to the fork point),
`head_commit` `3d7afae1a51b89fc039d44801991ce6390347402` (equal to C2's
full sha), `commit_count` 67. Zip's own check: `zipfile.is_zipfile`
`True`, `testzip()` answering `None`. Archived directory (absolute):
`/home/decodeux/Repos/remedy-history/zips`.

**G5 — the tree (after A2)**: `python3 -m apps.cli.main integrity
check --json`, real exit 0:
```
{"check_count": 6, "checks": [{"message": "handlers=148", "name": "handler_import", "status": "pass"}, {"message": "last Gate verdict PASS", "name": "live_review_verdict", "status": "pass"}, {"message": "unchecked=0, context_complete=False", "name": "plan_consistency", "status": "pass"}, {"message": "untracked=0, relevant=0", "name": "relevant_untracked", "status": "pass"}, {"message": "no reviewer scratch, evidence dir or archive at the root", "name": "repo_root_hygiene", "status": "pass"}, {"message": "no open blocker/high findings", "name": "high_blockers_open", "status": "pass"}], "fail_count": 0, "ok": true, "passed": true, "schema_version": 1, "version": 1}
```
All six checks `pass`, `fail_count` 0. `git status --porcelain`: empty,
no relevant untracked file. `git worktree list`: primary checkout plus
`f282-r11-dry`, `f282-r11-sim`, `f282-r12-sim` and the four `job-*`
worktrees — unchanged from before the round, no leftover.

**G6**: reported in the worker's final reply only, per the block (not
in this committed handback).

## Authored-text proofs

- `.agent/authored/f282-r12-block.md` (C1) ==
  `.remedy-wt/f282-r12-block.md`: byte-identical True (11662 bytes, 167
  lines, sha256
  `9031e4856290fe78eeea33ddf59f03737a8e539d902b0a255487b7ea5a3a6317`).
- `.agent/authored/f282-r12-ledger.diff`, `-plan.md`,
  `-create_f282_evidence.py` (C1) == their
  `.remedy-wt/f282-r12-payloads/` sources: byte-identical True, all
  three (3591, 1023, 6648 bytes respectively).
- `ledger.diff` was applied at C2 with `git apply --check` then
  `git apply` directly from the payload's own bytes under
  `.remedy-wt/f282-r12-payloads/` — never retyped, both real exit 0.
- `.agent/plan.md` at C2 == its payload source verbatim (rewrite by
  `shutil.copyfile`): byte-identical True (confirmed by the G2 sha256
  reading above and by the payload table reading for plan.md).
- `create_f282_evidence.py` was run from the payload directory at A1,
  never applied or edited, per the block's own description of it as a
  TOOL.
- No payload was edited or retyped anywhere this round; every copy used
  `shutil.copyfile` and the one diff was applied by `git apply` reading
  the payload file directly.

## Item-status table

| Item | Status | Reason |
|---|---|---|
| C1 | done | 352 insertions, matches block formula (167+185) exactly |
| C2 | done | 2/0, 7/8 insertions/deletions by `git diff --numstat`, matches block exactly |
| A1 (evidence job) | done | real exit 0; `is_valid_current_run True`, no validation errors, no problems |
| A2 (review package) | done | `PACKAGE_STATUS=READY_FOR_REVIEW`, `EVIDENCE_AUTHORITATIVE=true`, manifest base/head match fork point / C2 exactly |
| C3 | done | this handback |
| Round 11 booking | done | `Gate: F282 R11 —` entry appended to `.agent/live_review.md` via `ledger.diff` |
| G1 | done | all readings match; all four authored copies byte-identical |
| G2 | done | both sha256/byte readings match; open-set 3 at both, both differences empty; the added-line count is 1 |
| G3 | done | script real exit 0; ancestry=plain=67; 696 collected; 0 unsafe; pytest 696 passed/0 failed/0 skipped exit 0; validation clean |
| G4 | done | READY_FOR_REVIEW; authoritative true; manifest base/head correct; zip valid; archived under remedy-history/zips |
| G5 | done | integrity check all six pass, fail_count 0; tree clean; worktree list unchanged |
| G6 | done | readings reported in the final reply only, per the block |
| Push after C2 | done | `f757fbca..3d7afae1` |
| Push after C3 | done | reported in the final reply |

## Deviations & assumptions

None. Every measured number matched the block's stated expectation
exactly (the +1 commit and +2 passed adjustments in A1's counts were
themselves predicted by the block, not deviations), and the commit/
action sequence landed in the block's exact order C1-C2-A1-A2-C3. The
package read `READY_FOR_REVIEW` on the first build, so constraint 4's
STOP path was not needed. No payload was edited or retyped; every copy
used `shutil.copyfile` and the one diff was applied via `git apply`
reading the payload file directly. This round is SESSION 2 of F282,
its twelfth round. Nothing closed, nothing merged, no PR opened, per
constraint 5.

## Next

Phase 1 rule 1 (read `.agent/STOP` from disk), then the review of
round 12, then the closing round: the ledger rotation, the ownership
step for R-0499, R-0950 and R-1008, the next paydown's registration,
the STATUS line with the README counters in the same commit, and the
pull request. Open findings count: 3. Operator-questions count: 0.
