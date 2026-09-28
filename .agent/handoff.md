# Handoff — F035, round 9 (the closure sequence's evidence round: book round 8, read the
self-use generator, build the evidence bundle and the review package at the accepted head)

## Session

SESSION 2 of feature F035 · round 9 · rounds so far 9. Context remaining at handback: a
comfortable majority of the budget is left — this round read AGENTS.md, the block, the three
payloads, the previous round's `.agent/handoff.md` and `docs/agents/handback_template.md` once
each; ran the payload-verification commands once, the pytest booking subset once, the evidence
tool once, the review-zip script once, `integrity check` once, and the independent zip/manifest
re-verification (zipfile, sha256) once.

## Range

Review of `43927119..HEAD` (`HEAD` is this handback's own commit, `F035 R9 C3`, on
`feature/f035-ownership-ledger`).

## Commits

### 8b371f848 F035 R9 C1: copy round 9 block and payloads
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f035-r9-block.md | 164/0 | verbatim copy of this round's block, by `shutil.copyfile` |
| .agent/authored/f035-r9-booking.diff | 31/0 | verbatim copy of the booking.diff payload |
| .agent/authored/f035-r9-create_f035_evidence.py | 159/0 | verbatim copy of the create_f035_evidence.py payload |
| .agent/authored/f035-r9-plan.md | 28/0 | verbatim copy of the plan.md payload |

Measured insertions: 382 (164+31+159+28). Block expected the block's own line count (164) plus
218 = 382. Match, under the 500-line cap.

### 7f25c03bd F035 R9 C2: book round 8, resolve R-1085 and R-1086, name the allowlist lines
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | 4/2 | round 8's PASS Gate entry appended; R-1085's and R-1086's `Landed:` lines replaced by `Done:` lines |
| .agent/plan.md | 7/8 | rewritten to the plan.md payload, by `shutil.copyfile` |
| docs/roadmap/features/T5_F035.md | 5/0 | "Guards widened on purpose" paragraph naming the reachability allowlist's three new lines (closure precondition 7) |

Measured numstat: 4/2, 7/8, 5/0 — equal to the block's G1 expectation exactly (all three files'
sha256 also matched the reviewer's simulation-tree reading; see Verification). This commit's
full sha, `7f25c03bddca1d9c08b58821288b7eed42d1e3cb`, is the closure's ACCEPTED HEAD. Pushed
immediately after, before A0 (see External actions).

### This commit F035 R9 C3: rewrite handoff for round 9 with the evidence and package readings
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | rewritten | this handback, per `docs/agents/handback_template.md` |

## External actions

- `git apply --check .remedy-wt/f035-r9-payloads/booking.diff` — exit 0; `git apply` the same —
  exit 0.
- `shutil.copyfile` of the plan.md payload onto `.agent/plan.md` at C2, from a script in the
  gitignored `.remedy-wt/f035-r9-worker/`.
- `git push -u origin feature/f035-ownership-ledger` at C2 (`7f25c03bd`) — succeeded:
  `439271197..7f25c03bd feature/f035-ownership-ledger -> feature/f035-ownership-ledger`.
- A0 the self-use reading, at C2, from a script in `.remedy-wt/f035-r9-worker/`:
  `packages.orchestration.self_use_generator.generate_and_append_if_empty()` → `None`;
  `packages.orchestration.self_use_queue.next_self_use_item()` → `None`; `git status --porcelain`
  after — empty. No queue file was touched, so nothing needed restoring; closure precondition 6
  reads "self-use NONE (queue exhausted)".
- A1 the evidence job: `bash -c 'python3 .remedy-wt/f035-r9-payloads/create_f035_evidence.py >
  .remedy-wt/f035-r9-worker/evidence.log 2>&1; echo "REAL_EXIT=$?"'` — REAL_EXIT=0. Bundle written
  to the gitignored `.remedy-wt/f035-r9-evidence/`, not committed. Job id `f035r9e1001`, run id
  `vr-0351`, step range `T001-T003`, feature `f035`, base `a0b287a552f4630e64122188c28bd0a965441864`.
- A2 the review package: `bash -c 'bash scripts/make_review_zip.sh --evidence-dir
  .remedy-wt/f035-r9-evidence > .remedy-wt/f035-r9-worker/zip.log 2>&1; echo "REAL_EXIT=$?"'` —
  REAL_EXIT=0, `REMEDY_REVIEW_DIR` not set. Package written to
  `/home/decodeux/Repos/remedy-history/zips/remedy-review-20260928-050815-READY_FOR_REVIEW.zip`
  (the operator's archive, outside the repo).
- No `git worktree add`/`remove` this round — only the gitignored, non-worktree
  `.remedy-wt/f035-r9-worker/` directory was created for scripts and logs.
- No PR created or merged — the block orders none, and none was created.
- `git push` at C3 — reported in the reply per the block (G6 cannot go in this file, written
  before the push).

## Verification

G1 TRANSPORT — payloads measured against the PAYLOADS table before use:
```
booking.diff:              31 lines, 6891 bytes, sha256 fbdc8f8570011da356772e541465919ec4dab8966a785dde8202c9a3be269c3b — MATCH
create_f035_evidence.py:   159 lines, 7727 bytes, sha256 3da17a80dbdec62ccd31263a8ceb460e87098a7fca97f8b46976be68d9e415c7 — MATCH
plan.md:                   28 lines, 981 bytes, sha256 3aa54d1a8426d83faea0af946e8748f380edd47f0f48ad0c4b6aabb3540cb9b0 — MATCH
```
Block's own bytes verified before anything else (R-0954): 164 lines, sha256
`e61a9f0bf487a9a0a25c4709e3712931774e7c34044db1643600713431050e748` — MATCH against the
delegation message's stated table.

Copies at C1, read back with `git show <C1>:<path>` and compared byte-for-byte against the
source: `.agent/authored/f035-r9-block.md` (12736 bytes,
`e61a9f0bf487a9a0a25c4709e3712931774e7c34044db1643600713431050e748`),
`.agent/authored/f035-r9-booking.diff` (6891 bytes,
`fbdc8f8570011da356772e541465919ec4dab8966a785dde8202c9a3be269c3b`),
`.agent/authored/f035-r9-create_f035_evidence.py` (7727 bytes,
`3da17a80dbdec62ccd31263a8ceb460e87098a7fca97f8b46976be68d9e415c7`),
`.agent/authored/f035-r9-plan.md` (981 bytes,
`3aa54d1a8426d83faea0af946e8748f380edd47f0f48ad0c4b6aabb3540cb9b0`) — all IDENTICAL to their
sources and to the block's own stated table.

G2 THE BOOKING — at C2 (`7f25c03bd`), `git show <C2>:<path>` read and hashed:
```
.agent/live_review.md              334919 bytes  c1e7297c58a5e25ae631569e82a2d0c9fb8b23cf96d965bf6f25b2740db8b87d — MATCH
.agent/plan.md                     981 bytes     3aa54d1a8426d83faea0af946e8748f380edd47f0f48ad0c4b6aabb3540cb9b0 — MATCH
docs/roadmap/features/T5_F035.md   11761 bytes   f5693dfa2440b8805ebde2d6c542c7a0a9b6b3a44a61d051af173cb701e8f57a — MATCH
```
`scripts.rotate_live_review.open_finding_ids` over the ledger text at C2: `[]` — equal to the
reviewer's simulation reading. Lines beginning `Landed: R-1085` or `Landed: R-1086`: 0 — equal.
Then, serially, at C2:
```
$ python3 -m pytest -q -p no:cacheprovider tests/docs/ tests/cli/test_golden_path.py
369 passed in 56.55s
REAL_EXIT=0
```
Equal to the reviewer's simulation (369 passed, exit 0).

G3 THE BUNDLE — at A1, the tool's own report:
```
head 7f25c03bddca1d9c08b58821288b7eed42d1e3cb
ancestry-path count 58
plain count 58
collected node ids 1068, deselected 3
red control: unsafe among the real ids 0 []
red control: planted id -> a local absolute path
pytest exit 0, {'passed': 1068, 'failed': 0, 'skipped': 0}, output_hash 984ca7c4e691e8d1c8dd988c8f0ae57a02efff43ae67ff42179744e8be5e8bbe
validate_verification_tests problems [] passed 1068
is_valid_current_run True
validation_errors []
gates written: ['artifact_contract_gate.json', 'change_provenance_gate.json', 'commit_execution_gate.json', 'fresh_evidence_gate.json', 'runtime_integration_gate.json', 'final_verifier_report.json']
REAL_EXIT=0
```
Ancestry and plain counts equal, at 58 — two more than the reviewer's dry-run reading of 56, per
the block's own stated expectation ("At C2 both ancestry counts read two more"). Collected 1068
node ids with 3 deselected — equal to the reviewer's dry run (1068 collected, 3 deselected). Zero
unsafe among the real ids; the planted id answers "a local absolute path" — equal. Pytest exit 0,
1068 passed, 0 skipped — equal. `validate_verification_tests` problem list EMPTY — equal.
`is_valid_current_run` True with no validation error — equal. Six gate files written.

G4 THE PACKAGE — at A2, the script's own report:
```
UNCHANGED: runtime_integration_gate.json — rebuilt from source; identical to existing
Evidence refresh completed for staged copy.
Observability index generated from staged bytes: evidence/current/self_run_observability_index.json
{"member_count": 6590, "authoritative_count": 39, "symlink_count": 0, "tombstone_count": 0, "final_path": "/home/decodeux/Repos/remedy-history/zips/remedy-review-20260928-050815-READY_FOR_REVIEW.zip", "final_sha256": "9b3e3841d2c11725c8a03579fa2a7d5dcb963aac3386faeb5a6ab5517ac2b8aa", "publication_capability": "SUPPORTED", "package_status": "READY_FOR_REVIEW", "evidence_authoritative": true, "review_subject_alignment": "PASS", "manifest_sha256": "10d056cb61ee44fd1da7f205b64a861bd88b7a909867874b7e570bc9fc2e44e7"}
REVIEW_PACKAGE_CREATED=true
PACKAGE_STATUS=READY_FOR_REVIEW
PACKAGING_CWD=/home/decodeux/Repos/remedy
EVIDENCE_DIR=.remedy-wt/f035-r9-evidence
REVIEW_SUBJECT_ALIGNMENT=PASS
EVIDENCE_AUTHORITATIVE=true
REVIEW_PACKAGE_DIR=/home/decodeux/Repos/remedy-history/zips
ZIP_PATH=/home/decodeux/Repos/remedy-history/zips/remedy-review-20260928-050815-READY_FOR_REVIEW.zip
REAL_EXIT=0
```
`PACKAGE_STATUS` reads `READY_FOR_REVIEW` (the reading, not merely exit 0). `EVIDENCE_AUTHORITATIVE`
reads `true`. Package filename `remedy-review-20260928-050815-READY_FOR_REVIEW.zip`, sha256
`9b3e3841d2c11725c8a03579fa2a7d5dcb963aac3386faeb5a6ab5517ac2b8aa` — independently re-hashed from
the file on disk with the same result. `.review_zip_manifest.json` INSIDE the package:
`committed_review_subject` reads `base_commit` `a0b287a552f4630e64122188c28bd0a965441864` (the
fork point) and `head_commit` `7f25c03bddca1d9c08b58821288b7eed42d1e3cb` (C2's full sha, the
accepted head) — both equal. `zipfile.is_zipfile` → True; `testzip()` → None. Archived directory:
`/home/decodeux/Repos/remedy-history/zips` (absolute, outside the repository).

G5 THE TREE — after A2:
```
$ python3 -m apps.cli.main integrity check --json
{"check_count": 6, "checks": [{"message": "handlers=167", "name": "handler_import", "status": "pass"}, {"message": "last Gate verdict PASS", "name": "live_review_verdict", "status": "pass"}, {"message": "unchecked=0, context_complete=False", "name": "plan_consistency", "status": "pass"}, {"message": "untracked=0, relevant=0", "name": "relevant_untracked", "status": "pass"}, {"message": "no reviewer scratch, evidence dir or archive at the root", "name": "repo_root_hygiene", "status": "pass"}, {"message": "no open blocker/high findings", "name": "high_blockers_open", "status": "pass"}], "fail_count": 0, "ok": true, "passed": true, "schema_version": 1, "version": 1}
```
All six checks read `pass`, `fail_count` 0. `git status --porcelain` — empty. `git worktree list |
wc -l` — 61, unchanged from step 4's reading and from the count after C1/C2.

G6 AFTER C3 AND THE PUSH — reported in the final reply only, per the block; not this file.

## Authored-text proofs

`.agent/authored/f035-r9-block.md`, `.agent/authored/f035-r9-booking.diff`,
`.agent/authored/f035-r9-create_f035_evidence.py` and `.agent/authored/f035-r9-plan.md`, each
compared byte-for-byte at C1 against its payload source — all IDENTICAL (see G1 above, also
equal to the block's own stated table). `booking.diff`'s effect on `.agent/live_review.md`,
`.agent/plan.md` and `docs/roadmap/features/T5_F035.md`, read at C2 by size and sha256 — all
equal to the reviewer's own simulation reading (see G2 above).

## Deviations & assumptions

None. The bundle ran in the block's own order (C1, C2, A0, A1, A2, C3), no splits and no extra
commits, both commits under the 500-line cap, and every gate's measured reading matched the
block's stated expectation exactly — including the block's own explicit prediction that the
ancestry counts at C2 would read two more than the reviewer's dry-run 56.

## Next

Per AGENTS.md Phase 1 rule 1 (read `.agent/STOP` from disk) and the block's own ordering: the
review of round 9, then the closing round — the booking of round 9, the ledger rotation, the
STATUS line with the README counters in the same commit, and the pull request. Open findings: 0
(`open_finding_ids` reads `[]` at C2). Operator questions open: 0.

## Item status

| Item | Status | Reason |
|---|---|---|
| Step 1 (`.agent/STOP` check) | done | absent |
| Step 2 (primary checkout, branch, HEAD) | done | |
| Step 3 (block byte verification) | done | |
| Step 4 (worktree/branch count) | done | 61 |
| Payload verification (3 payloads) | done | |
| C1 | done | |
| C2 | done | pushed immediately after |
| A0 self-use reading | done | `None`, `None`; queue file untouched |
| A1 evidence job | done | exit 0, all readings equal to the reviewer's expectations |
| A2 review package | done | `READY_FOR_REVIEW`, exit 0 |
| C3 | done | this handback |
| G1 Transport | done | |
| G2 The booking | done | |
| G3 The bundle | done | |
| G4 The package | done | |
| G5 The tree | done | |
| G6 Tree and push | done | reported in the reply, not this file (block: it cannot go in C3) |
