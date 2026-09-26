# Handoff — F289, round 6

## Session

SESSION 1 of feature F289 · round 6 · rounds so far 6. Context remaining at
handback: ample — the round is a mechanical booking-plus-evidence round with
no repair needed, and closed comfortably inside a single session.

## Range

Review of `ba713c34`..`HEAD` (`HEAD` is this handback's own commit, `F289 R6
C3`, on `feature/f289-self-use-sources`).

## Commits

### 34a801f11 F289 R6 C1: copy round 6 block and payloads
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f289-r6-block.md | 133/0 | copy of this round's block (`shutil.copyfile`) |
| .agent/authored/f289-r6-create_f289_evidence.py | 148/0 | copy of the evidence-job tool payload |
| .agent/authored/f289-r6-plan.md | 26/0 | copy of the plan.md payload |
| .agent/authored/f289-r6-records.diff | 10/0 | copy of the records.diff payload |

Measured insertions: 317 (133+148+26+10), matching the block's expectation
(block's own line count 133 plus 184).

### 32013a054 F289 R6 C2: book round 5 — ACCEPTED HEAD
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | 2/0 | `git apply records.diff` — appends round 5's gate entry |
| .agent/plan.md | 6/7 | rewritten to the plan.md payload |

Expected by the block: 2/0, 6/7 — measured identically. C2's full sha,
`32013a054ea65dce679cc65fe2cd01fe8d73a76d`, is this closure's ACCEPTED HEAD.

### (this commit) F289 R6 C3: rewrite handoff for round 6 with the evidence and package readings
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | rewritten | this handback |

## External actions

- `git push` after C2, before A1 — real outcome: `ba713c342..32013a054
  feature/f289-self-use-sources -> feature/f289-self-use-sources`, real exit 0.
- A1 evidence job — `python3 .remedy-wt/f289-r6-payloads/create_f289_evidence.py
  > .remedy-wt/f289-r6-worker/evidence.log 2>&1`, `REAL_EXIT=0`. Wrote the
  bundle to `.remedy-wt/f289-r6-evidence/` (gitignored under `.remedy-wt/`,
  nothing committed).
- A2 review package — `bash scripts/make_review_zip.sh --evidence-dir
  .remedy-wt/f289-r6-evidence`, no `REMEDY_REVIEW_DIR` set, `REAL_EXIT=0`.
  Produced
  `/home/decodeux/Repos/remedy-history/zips/remedy-review-20260926-225640-READY_FOR_REVIEW.zip`.
- `git push` after C3 — real outcome reported in the reply (G6), since this
  file cannot contain the reading of its own commit.
- No PR created, no PR merged, no branch checkout, no force-push, no stash —
  none were ordered and none were done. No worktree was added or removed.

## Verification

BEFORE ANYTHING ELSE:
- `ls .agent/STOP` → `No such file or directory` (does not exist).
- `pwd` → `/home/decodeux/Repos/remedy`. `git status --porcelain` → empty.
  `git branch --show-current` → `feature/f289-self-use-sources`. `git log
  --oneline -1` → `ba713c342 F289 R5 C5: record the closure suite and
  rewrite handoff for round 5` — all three matched the delegation message
  (`ba713c34`) exactly.
- Block bytes: measured 133 lines, sha256
  `72c63e13a3f9a5471f18b83636d8d39b51fdc1af1dc150ee1169aeb5baef6336` against
  `.remedy-wt/f289-r6/block.md` — both matched the delegation message
  exactly.

PAYLOADS (measured against the table, before use, all three matched):
| file | lines | bytes | sha256 match |
|---|---|---|---|
| create_f289_evidence.py | 148 | 7143 | yes |
| plan.md | 26 | 812 | yes |
| records.diff | 10 | 7930 | yes |

CONSTRAINT 1 — `git apply --check` real exit 0 for `records.diff` before the
real `git apply`, also real exit 0. No payload was edited or retyped.

G1 TRANSPORT — every `.agent/authored/f289-r6-*` copy read back with `git
show 34a801f11:<path>` compared byte-for-byte (sha256) against its source:
all four byte-identical (block.md, create_f289_evidence.py, plan.md and
records.diff all matched — see the PAYLOADS table above and the block's own
table).

G2 THE BOOKING — read with `git show 32013a054:<path>`:
| path | bytes | sha256 match |
|---|---|---|
| .agent/live_review.md | 333667 | yes (`349153378594733fe465cf272d9f9791ac834972af0b06027edba524848d1023`) |
| .agent/plan.md | 812 | yes (`7703244cbc2cc4664a196e7a3905c000d874e05b26b812b843a8859611b5b729`) |

`open_finding_ids` (via `scripts/rotate_live_review.py`) over `.agent/live_review.md`
at C2 → `[]`, matching the reviewer's simulation exactly.

`python3 -m pytest -q -p no:cacheprovider tests/docs/ tests/cli/test_golden_path.py`
serially at C2:
```
369 passed in 38.81s
REAL_EXIT=0
```
Matches the reviewer's simulation reading of 369 passed at real exit 0
exactly.

G3 THE BUNDLE, at A1 (`.remedy-wt/f289-r6-worker/evidence.log`, real exit 0):
```
head 32013a054ea65dce679cc65fe2cd01fe8d73a76d
ancestry-path count 34
plain count 34
collected node ids 634, deselected 2
red control: unsafe among the real ids 0 []
red control: planted id -> a local absolute path
pytest exit 0, {'passed': 634, 'failed': 0, 'skipped': 0}, output_hash 046a7d43af4dcc4a1491765ca785a99ca6935a7bfe8fc6401938039e4fe6cd40
validate_verification_tests problems [] passed 634
is_valid_current_run True
validation_errors []
gates written: ['artifact_contract_gate.json', 'change_provenance_gate.json', 'commit_execution_gate.json', 'fresh_evidence_gate.json', 'runtime_integration_gate.json', 'final_verifier_report.json']
```
Both ancestry counts equal at 34 (two more than the reviewer's dry-run
reading of 32 at `ba713c34`, matching the block's "at C2 both ancestry
counts read two more"); collected/deselected 634/2 matches the reviewer's
dry run exactly; the red control found zero unsafe real ids and the planted
id answered "a local absolute path", matching; pytest exit 0 with 634
passed and 0 skipped matches; `validate_verification_tests` problem list
empty; `is_valid_current_run` True with an empty validation-error list.
Script's own overall `REAL_EXIT=0`. The evidence directory holds the six
named gate files plus `manifest.json`, `verification_tests.json`,
`workspace.diff`, `review_subject.json`, `review_commit_chain.json` and the
`task_runs/` and `review_commit_patches/` subdirectories (27 top-level
entries total) — gitignored under `.remedy-wt/`, nothing committed.

G4 THE PACKAGE, at A2 (`bash scripts/make_review_zip.sh --evidence-dir
.remedy-wt/f289-r6-evidence`, real exit 0):
```
PACKAGE_STATUS=READY_FOR_REVIEW
EVIDENCE_AUTHORITATIVE=true
REVIEW_PACKAGE_DIR=/home/decodeux/Repos/remedy-history/zips
ZIP_PATH=/home/decodeux/Repos/remedy-history/zips/remedy-review-20260926-225640-READY_FOR_REVIEW.zip
```
Package filename: `remedy-review-20260926-225640-READY_FOR_REVIEW.zip`.
SHA-256 (measured independently with `hashlib.sha256` over the file, matching
the tool's own reported `final_sha256`):
`7044a4959459a9144a0b3030453ed74944ab4edad8125fd67c2eb2e6cc488a62`.
`.review_zip_manifest.json` inside the package, read via `zipfile`:
`committed_review_subject.base_commit` = `d0239fa348ca0685470d98549628a689ed288dc9`
(the fork point), `committed_review_subject.head_commit` =
`32013a054ea65dce679cc65fe2cd01fe8d73a76d` (equal to C2's full sha),
`base_is_ancestor` true, `commit_count` 34. `zipfile.is_zipfile(path)` →
`True`; `ZipFile.testzip()` → `None`. Archived directory:
`/home/decodeux/Repos/remedy-history/zips`.

G5 THE TREE, after A2:
`python3 -m apps.cli.main integrity check --json` →
```
{"check_count": 6, "checks": [
  {"name": "handler_import", "status": "pass", "message": "handlers=161"},
  {"name": "live_review_verdict", "status": "pass", "message": "last Gate verdict PASS"},
  {"name": "plan_consistency", "status": "pass", "message": "unchecked=0, context_complete=False"},
  {"name": "relevant_untracked", "status": "pass", "message": "untracked=0, relevant=0"},
  {"name": "repo_root_hygiene", "status": "pass", "message": "no reviewer scratch, evidence dir or archive at the root"},
  {"name": "high_blockers_open", "status": "pass", "message": "no open blocker/high findings"}
], "fail_count": 0, "ok": true, "passed": true}
```
Six of six `pass`, `fail_count` 0. `git status --porcelain` → empty.
`git worktree list | wc -l` → `62`.

G6 TREE AND PUSH (after C3): reported in full in the reply, since this file
cannot contain the reading of its own commit.

## Authored-text proofs

The block copy and the three payload copies (`create_f289_evidence.py`,
`plan.md`, `records.diff`), read back at `34a801f11`, equal the reviewer's
originals byte for byte (see G1 above, all four sha256 matches).
`records.diff` was applied with `git apply` unedited (constraint 1),
confirmed byte-identical by the G2 sha256 reading of `.agent/live_review.md`;
`.agent/plan.md` was rewritten to the `plan.md` payload verbatim via
`shutil.copyfile`, also confirmed byte-identical by the G2 sha256 reading.
`create_f289_evidence.py` was run unedited as a tool, never applied as a
diff or copied into a tracked path other than its `.agent/authored/` record.

## Item-status table

| Item | Status | Reason |
|---|---|---|
| BEFORE ANYTHING ELSE 1–3 | done | |
| PAYLOADS verification | done | |
| C1 | done | |
| C2 | done | accepted head `32013a054ea65dce679cc65fe2cd01fe8d73a76d` |
| A1 (evidence job) | done | `REAL_EXIT=0`, all readings match the reviewer's dry run |
| A2 (review package) | done | `PACKAGE_STATUS=READY_FOR_REVIEW`, `EVIDENCE_AUTHORITATIVE=true` |
| C3 (this handoff) | done | |
| G1 | done | |
| G2 | done | |
| G3 | done | |
| G4 | done | |
| G5 | done | |
| G6 | done | reported in the reply |
| Constraint 1 (no retype, `git apply --check` first) | done | |
| Constraint 2 (every commit under 500 insertions) | done | largest was C1 at 317 |
| Constraint 3 (tracked path set) | done | matches exactly, see reply |
| Constraint 4 (package not READY, or any gate red → stop) | done | package read READY_FOR_REVIEW, no gate was red, so no stop/hand-back path was needed |
| Constraint 5 (nothing merged, nothing closed) | done | no PR, no merge, no STATUS/README edit, no ledger rotation, no `consumed_by` edit |
| Constraint 6 (delete nothing not created; worktrees/branches stay) | done | `git worktree list` count reported at G5 (62); nothing removed |
| Constraint 7 (a tool-output statement quotes its own output line) | done | all quoted lines above are verbatim tool output |

## Deviations & assumptions

None. Every gate read exactly what the block and the reviewer's dry run
predicted; no repair, no split commit, and no hand-back path was triggered.

## Next

Phase 1 rule 1 (read `.agent/STOP` from disk), then the review of round 6,
then the closing round — the booking of round 6, the ledger rotation,
SU-033's `consumed_by`, the STATUS line with the README counters in the
same commit, and the pull request. Open findings at C2 (as
`open_finding_ids` reads the ledger): 0. Operator questions open: 0.
