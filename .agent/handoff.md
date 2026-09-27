# Handoff — F029, round 10

## Session

SESSION 2 of feature F029 · round 10 · rounds so far 10. Context remaining
at handback: ample — the round verified three payloads, applied one small
diff, ran the evidence job and the review-package build (both single-pass,
no repair), verified all five gates and wrote this handoff, all in one pass.

## Range

Review of `03e0998e6`..`HEAD` (`HEAD` is this handback's own commit, `F029
R10 C3`, on `feature/f029-subtree-rerun`).

## Commits

### 207bb0533 F029 R10 C1: copy round 10 block and payloads
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f029-r10-block.md | 149/0 | copy of this round's block |
| .agent/authored/f029-r10-booking.diff | 10/0 | copy of the booking.diff payload |
| .agent/authored/f029-r10-create_f029_evidence.py | 166/0 | copy of the evidence-job tool payload |
| .agent/authored/f029-r10-plan.md | 28/0 | copy of the plan payload |

Measured insertions: 353 (block's own line count 149 + 204), matching the
block's expectation exactly, under the 500-line cap.

### e56e82f73 F029 R10 C2: book round 9
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | 2/0 | round 9's Gate entry appended (booking.diff) |
| .agent/plan.md | 5/9 | rewrite from the plan payload |

Matches the block's expected numstat (2/0, 5/9) exactly. Applied via
`git apply --check` (exit 0) then the real apply (exit 0) of `booking.diff`,
followed by the `.agent/plan.md` rewrite via `shutil.copyfile`. This
commit's full sha, `e56e82f733ec51609598590eda05aa1b2b7329ca`, is this
closure's ACCEPTED HEAD. Pushed immediately after this commit, before A1,
per the block's order.

### (pending) F029 R10 C3: rewrite handoff for round 10 with the evidence and package readings
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | rewrite | this file, carrying the evidence job id, the package name, its SHA-256, its archived directory, the accepted head and every gate reading |

## External actions

`git push origin feature/f029-subtree-rerun` after C2 — real outcome:
`03e0998e6..e56e82f73  feature/f029-subtree-rerun -> feature/f029-subtree-rerun`
(fast-forward, exit 0). `git push origin feature/f029-subtree-rerun` again
after C3 (this handoff) — its real outcome is reported to the delegator,
since C3 cannot contain it. No PR opened, no merge, no branch checked out
or deleted, no force-push, no stash, no worktree added or removed this
round (`git worktree list | wc -l` read 62 both before and after).

## Verification

**BEFORE ANYTHING ELSE**
- `ls .agent/STOP` → `No such file or directory` (absent).
- `pwd` → `/home/decodeux/Repos/remedy`; `git status --porcelain` → empty;
  `git branch --show-current` → `feature/f029-subtree-rerun`; `git log
  --oneline -1` → `03e0998e6`.
- Block bytes: measured 149 lines, sha256
  `e63cfe85f556cbf7906d7a3843e56e7dd81f9fc86d906c3d25c63d785724aecd` — both
  match the delegation message's readings exactly.
- `git worktree list | wc -l` → 62.

**PAYLOADS** — all three matched the table exactly:
`booking.diff` 10 lines / 7952 bytes /
`11efb3efa18e243a43e7da982da283f24dad81252ba09092824554e042014b65`;
`create_f029_evidence.py` 166 lines / 8329 bytes /
`e7a5a5f35fe4dbdd8805be3a27aab5428d880322ecc0b5b32ad179628301baf9`;
`plan.md` 28 lines / 880 bytes /
`902310d2909ced67d1b90bec212b1c2d7f35b7b00c42d02f49186b6d4ab7fbf8`.

**G1 TRANSPORT** — each `.agent/authored/f029-r10-*` copy read via `git show
207bb0533:<path>` equals its source byte for byte (sha256, all four):
block copy `e63cfe85f556cbf7906d7a3843e56e7dd81f9fc86d906c3d25c63d785724aecd`
== `.remedy-wt/f029-r10/block.md`; booking.diff copy
`11efb3efa18e243a43e7da982da283f24dad81252ba09092824554e042014b65` ==
`.remedy-wt/f029-r10-payloads/booking.diff`; create_f029_evidence.py copy
`e7a5a5f35fe4dbdd8805be3a27aab5428d880322ecc0b5b32ad179628301baf9` ==
`.remedy-wt/f029-r10-payloads/create_f029_evidence.py`; plan.md copy
`902310d2909ced67d1b90bec212b1c2d7f35b7b00c42d02f49186b6d4ab7fbf8` ==
`.remedy-wt/f029-r10-payloads/plan.md`.

**G2 THE BOOKING** — sha256/bytes of each file read via `git show
e56e82f733ec51609598590eda05aa1b2b7329ca:<path>` equals the reviewer's
table exactly: `.agent/live_review.md`: 337275 bytes,
`b264d9d690f51788e016890d93805ed5224a06b1e589edee9909bb2bee5cf81f` — match.
`.agent/plan.md`: 880 bytes,
`902310d2909ced67d1b90bec212b1c2d7f35b7b00c42d02f49186b6d4ab7fbf8` — match.
`open_finding_ids` (`scripts/rotate_live_review.py`) over
`.agent/live_review.md` at C2 → `[]`, matching the reviewer's stated
reading. Then, serially at C2:
```
bash -c 'python3 -m pytest -q -p no:cacheprovider tests/docs/ tests/cli/test_golden_path.py 2>&1 | tail -3; echo "REAL_EXIT=${PIPESTATUS[0]}"'
```
→ `369 passed in 35.56s`, `REAL_EXIT=0` — matches the reviewer's simulation
reading of 369 passed, exit 0 exactly.

**G3 THE BUNDLE (A1)** — command:
```
bash -c 'python3 .remedy-wt/f029-r10-payloads/create_f029_evidence.py > .remedy-wt/f029-r10-worker/evidence.log 2>&1; echo "REAL_EXIT=$?"'
```
→ `REAL_EXIT=0`. Log through the summary:
```
head e56e82f733ec51609598590eda05aa1b2b7329ca
ancestry-path count 67
plain count 67
collected node ids 1286, deselected 6
red control: unsafe among the real ids 0 []
red control: planted id -> a local absolute path
pytest exit 0, {'passed': 1286, 'failed': 0, 'skipped': 0}, output_hash b2db3c2b36e2aef554a594e3bf6cc4f7944585bf20906469485d15f9389ef910
validate_verification_tests problems [] passed 1286
is_valid_current_run True
validation_errors []
gates written: ['artifact_contract_gate.json', 'change_provenance_gate.json', 'commit_execution_gate.json', 'fresh_evidence_gate.json', 'runtime_integration_gate.json', 'final_verifier_report.json']
```
The two ancestry counts are equal (67 = 67), each exactly two more than the
reviewer's dry-run reading of 65 at `03e0998e`, as the block predicted for
C2. Collected/deselected (1286/6), the empty unsafe list, and the planted
id's answer all match the reviewer's dry-run readings exactly. `job_id
f029r10e1001`, base `b2863af4e1560305f771fb9b82c745e7cfe9ae9b`, step range
`T001-T003`, feature `f029`, run id `vr-0291` — all as the block specifies.
Trailing summary JSON: `verdict "PASS_WITH_RISKS"`, `commit_count 67`,
`total_passed 1286`, `authority_count 48`.

**G4 THE PACKAGE (A2)** — command:
```
bash -c 'bash scripts/make_review_zip.sh --evidence-dir .remedy-wt/f029-r10-evidence > .remedy-wt/f029-r10-worker/zip.log 2>&1; echo "REAL_EXIT=$?"'
```
(no `REMEDY_REVIEW_DIR` set) → `REAL_EXIT=0`. Log's tail:
```
PACKAGE_STATUS=READY_FOR_REVIEW
EVIDENCE_AUTHORITATIVE=true
ZIP_PATH=/home/decodeux/Repos/remedy-history/zips/remedy-review-20260927-201630-READY_FOR_REVIEW.zip
```
Package filename: `remedy-review-20260927-201630-READY_FOR_REVIEW.zip`.
SHA-256 (measured independently with `hashlib.sha256` over the file, and
matching the script's own reported `final_sha256`):
`9a0d0eb2ac1576e96149aca426e6aec301eedc6247c9ee0fb0b4a8eb01e9bf4b`.
`zipfile.is_zipfile` → `True`; `testzip()` → `None`. Inside the package,
`.review_zip_manifest.json`'s `committed_review_subject`: `base_commit
b2863af4e1560305f771fb9b82c745e7cfe9ae9b` (equal to the fork point),
`head_commit e56e82f733ec51609598590eda05aa1b2b7329ca` (equal to C2's full
sha, the accepted head), `base_is_ancestor true`, `commit_count 67`.
Archived directory: `/home/decodeux/Repos/remedy-history/zips` (absolute).

**G5 THE TREE (after A2)** —
`python3 -m apps.cli.main integrity check --json` →
```
{"check_count": 6, "checks": [{"message": "handlers=165", "name": "handler_import", "status": "pass"}, {"message": "last Gate verdict PASS", "name": "live_review_verdict", "status": "pass"}, {"message": "unchecked=0, context_complete=False", "name": "plan_consistency", "status": "pass"}, {"message": "untracked=0, relevant=0", "name": "relevant_untracked", "status": "pass"}, {"message": "no reviewer scratch, evidence dir or archive at the root", "name": "repo_root_hygiene", "status": "pass"}, {"message": "no open blocker/high findings", "name": "high_blockers_open", "status": "pass"}], "fail_count": 0, "ok": true, "passed": true, "schema_version": 1, "version": 1}
```
All six checks read `pass`, `fail_count 0`. `git status --porcelain` →
empty. `git worktree list | wc -l` → 62 (unchanged).

**Constraint 3** — `git diff --name-only 03e0998e6` after C2 lists exactly:
`.agent/authored/f029-r10-block.md`, `.agent/authored/f029-r10-booking.diff`,
`.agent/authored/f029-r10-create_f029_evidence.py`,
`.agent/authored/f029-r10-plan.md`, `.agent/live_review.md`,
`.agent/plan.md` — 6 paths, all in the block's tracked path set. No evidence
directory and no package is tracked (the evidence directory is gitignored;
the zip lives in the operator's archive outside the repository). After C3
this list additionally carries `.agent/handoff.md` itself, matching the
tracked path set exactly with no path outside it.

## Authored-text proofs

`.agent/authored/f029-r10-block.md`, `f029-r10-booking.diff`,
`f029-r10-create_f029_evidence.py` and `f029-r10-plan.md` (C1, `207bb0533`):
each read back via `git show` equals its source
(`.remedy-wt/f029-r10/block.md`, `.remedy-wt/f029-r10-payloads/booking.diff`,
`.remedy-wt/f029-r10-payloads/create_f029_evidence.py`,
`.remedy-wt/f029-r10-payloads/plan.md`) byte for byte — see G1 above.
`.agent/plan.md` at C2 (`e56e82f733ec51609598590eda05aa1b2b7329ca`) equals
the `plan.md` payload byte for byte — see G2 above. `booking.diff`'s effect
on `.agent/live_review.md` was verified by `git apply --check` (exit 0)
before the real apply (exit 0), then the resulting file's bytes/sha256 were
matched against the reviewer's table (G2) rather than retyped.

## Deviations & assumptions

None. Every reading matched the block's stated expectation exactly on the
first attempt: both payload tables, the C1 insertion count, both C2
numstats, the G2 file hashes and pytest count, the G3 bundle's ancestry
equality (67/67, two more than the reviewer's 65 as predicted), collected/
deselected counts, red control, pytest count and validation readings, the
G4 package's `READY_FOR_REVIEW`/`EVIDENCE_AUTHORITATIVE`/manifest subject
readings, and the G5 integrity/tree readings. No commit was split,
reordered or dropped from the block's ordered C1-A1-A2-C3 sequence; no
gate went red; no repair round was needed.

## Item-status table

| Item | Status | Reason |
|---|---|---|
| C1 | done | copy of block + 3 payloads, 353 insertions matching block's own count + 204 |
| C2 | done | booking.diff applied (2/0 live_review.md), plan.md rewritten (5/9) — matches expected numstat; full sha is the accepted head; pushed |
| A1 | done | evidence job real exit 0; ancestry 67=67 (two more than dry-run's 65); 1286 collected/6 deselected; 0 unsafe; pytest 1286 passed/0 skipped exit 0; validate_verification_tests problems []; is_valid_current_run True |
| A2 | done | review package real exit 0; PACKAGE_STATUS READY_FOR_REVIEW; EVIDENCE_AUTHORITATIVE true; manifest head/base match C2/fork point; zip valid, testzip None |
| C3 | done | this handoff, carrying every gate reading, the evidence job id, the package name/SHA-256/directory and the accepted head |
| G1 transport | done | PASS — all four copies byte-identical by sha256 |
| G2 the booking | done | PASS — both file reads, open_finding_ids and the pytest gate match the reviewer's table exactly |
| G3 the bundle | done | PASS — every A1 reading matches the reviewer's dry-run expectation |
| G4 the package | done | PASS — every A2 reading matches; package archived outside the repo |
| G5 the tree | done | PASS — integrity check 6/6 pass, tree clean, worktree count unchanged |

## Next

Phase 1 rule 1 (read `.agent/STOP` from disk), then the review of round 10,
then the closing round — the booking of round 10, the ledger rotation, the
STATUS line with the README counters in the same commit, and the pull
request. Open findings: 0 (per `open_finding_ids` at C2). Operator
questions open: 0.
