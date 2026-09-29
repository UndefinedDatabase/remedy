# Handback — F291 round 5: book round 4 with R-1114's resolution, complete the Built State, reclaim staging copies, build the evidence bundle and the review package at the accepted head

## Session

SESSION 1 of feature F291 · round 5 · rounds so far 5. Context self-assessment: roughly half the
session's context window remained when this handback was written, after both content commits, the
staging reclaim, the evidence job, the review package build and all five in-round gates.

## Range

Review of `d88f85b68`..HEAD (this round's final commit, C3 — the push's real outcome is reported in
the worker's reply, since this file is committed as part of C3 and cannot name its own commit's sha
or anything that follows it).

## Commits

### `6fc445a8d` F291 R5 C1: copy round 5 block and payloads
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f291-r5-block.md | +167/-0 | this round's block, copied verbatim via `shutil.copyfile` |
| .agent/authored/f291-r5-records.diff | +27/-0 | payload copy |
| .agent/authored/f291-r5-plan.md | +26/-0 | payload copy |
| .agent/authored/f291-r5-create_f291_evidence.py | +154/-0 | payload copy (A1's tool) |

Total 374 insertions (block's 167 + 207), matching the block's stated formula exactly; measured
`git diff --cached --stat` before commit: `4 files changed, 374 insertions(+)`, well under the 500
cap.

### `5f4cebf37` F291 R5 C2: book round 4 with R-1114's resolution and complete the Built State
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +4/-0 | `git apply` of records.diff: round 4's Gate entry and R-1114's `Done:` resolution line appended |
| .agent/plan.md | +7/-9 | rewritten via `shutil.copyfile` from the plan.md payload |
| docs/roadmap/features/T5_F291.md | +7/-0 | `git apply` of records.diff: the closure-suite paragraph for rounds 3 and 4 appended to the Built State |

Measured `git diff --cached --numstat` before commit: 4/0, 7/9, 7/0 — equal to the block's expected
numstat table exactly, in the same order. **This is the ACCEPTED HEAD: `5f4cebf3751861d03edf470d2ff3c47c13005279`.**
Pushed immediately after this commit (`d88f85b68..5f4cebf37`), before A0.

### C3 (this commit) — F291 R5 C3: rewrite handoff for round 5 with the evidence and package readings
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | this file | round 5 handback: the reclaim reading, the evidence job id, the package name, its SHA-256, its archived directory, the accepted head and every gate reading |

## External actions

- `git push origin feature/f291-self-use-sources-v2` after C2: succeeded,
  `d88f85b68..5f4cebf37  feature/f291-self-use-sources-v2 -> feature/f291-self-use-sources-v2`.
- A0 (staging reclaim, commits nothing): `python3 -m apps.cli.main data reclaim --orphans` →
  exit 0, preview read `Reclaimable: nothing`, one refused path `review_staging.n4o46eq_`
  (`class_not_job_keyed`), `Would free 0 B in 0 paths`. No candidate listed, so `--apply` was
  skipped per the block's instruction.
- A1 (evidence job, commits nothing): `python3 .remedy-wt/f291-r5-payloads/create_f291_evidence.py`
  → exit 0, wrote `.remedy-wt/f291-r5-evidence/` (gitignored, not committed).
- A2 (review package, commits nothing): `bash scripts/make_review_zip.sh --evidence-dir
  .remedy-wt/f291-r5-evidence` → exit 0, wrote
  `/home/decodeux/Repos/remedy-history/zips/remedy-review-20260929-230028-READY_FOR_REVIEW.zip`
  (the operator's archive, `REMEDY_REVIEW_DIR` unset).
- `git push` after C3: real outcome reported in the worker's reply, since C3 cannot record a push
  that follows it.
- No PR was created (the block orders "No pull request" for this round). No `gh pr merge`, no
  checkout of `main`, no branch deletion, no force-push, no `git stash`, no STATUS/README edit, no
  ledger rotation, no queue edit and no self-use run.

## Verification

**BEFORE ANYTHING ELSE:** step 1 `ls .agent/STOP` — absent (`No such file or directory`, exit 2).
step 2 `pwd` `/home/decodeux/Repos/remedy`; `git status --porcelain` empty; `git branch --show-current`
`feature/f291-self-use-sources-v2`; `git log --oneline -1` `d88f85b68` — all matched exactly. step 3
block measured 167 newlines, sha256
`dd66035128e94ee52a8c6a0f0e8c0d83e67bf0c11d70bafd5b0facd684a98b73` — equal to the delegation
message's two readings exactly. step 4 `git worktree list | wc -l` = 13.

**PAYLOADS:** all three measured exactly against the table — records.diff 27/8498/
`e4825be317af7666d0a8ffc84dd6ee22b5a1223fa3a18f3785e905af8e14f48f`, plan.md 26/851/
`85b502bc9fcbd3b4cb10ef1ba56db7388a94cffb56e78e6f76c06bda5f0bc545`, create_f291_evidence.py
154/7442/`affe04853c45dfc2ad58a273156eb45c982a27e03fc29b168dc657e016e16af0` — full readings match the
block's table digit for digit.

**G1 transport:** all four committed `.agent/authored/f291-r5-*` copies (block, records diff, plan,
the evidence tool) verified byte-identical to their sources with an independent hash-comparison
script (`git show 6fc445a8d:<path>` vs. source bytes) — all four equal, the block copy against
`.remedy-wt/f291-r5/block.md` included.

**G2 the booking, at C2 (`5f4cebf37`):** `git show 5f4cebf37:<path>` byte/hash for each of the three
files, verified with an independent script:
| path | bytes | sha256 | match |
|---|---|---|---|
| .agent/live_review.md | 145504 | `9b7648e7648b0a6d102eb8ed1b3e02131301e82f39363e62733996248181b7a5` | equal |
| .agent/plan.md | 851 | `85b502bc9fcbd3b4cb10ef1ba56db7388a94cffb56e78e6f76c06bda5f0bc545` | equal |
| docs/roadmap/features/T5_F291.md | 7457 | `f65c0d38c43c367f07737e6e5b3c12fc80e9186a1e4f0cdffa1a66fad691baa9` | equal |

All three equal the reviewer's tree exactly. `open_finding_ids` (from `scripts/rotate_live_review.py`
over `.agent/live_review.md` at C2) read `[]`; `latest_gate_verdict` read `PASS` — both equal to the
reviewer's reading. The serial gate,
`bash -c 'python3 -m pytest -q -p no:cacheprovider tests/docs/ tests/cli/test_golden_path.py 2>&1 | tail -3; echo "REAL_EXIT=${PIPESTATUS[0]}"'`,
read `369 passed in 54.57s`, `REAL_EXIT=0`.

**G3 the bundle, at A1 (`create_f291_evidence.py`, run from the repository root at C2):** real exit
code **0**. Full log:
```
head 5f4cebf3751861d03edf470d2ff3c47c13005279
ancestry-path count 31
plain count 31
collected node ids 732, deselected 2
red control: unsafe among the real ids 0 []
red control: planted id -> a local absolute path
pytest exit 0, {'passed': 732, 'failed': 0, 'skipped': 0}, output_hash 8f3ee236836506837aa861108e5c5ffdf87abc89da01bb81c5c0fa1d044fc0eb
validate_verification_tests problems [] passed 732
is_valid_current_run True
validation_errors []
gates written: ['artifact_contract_gate.json', 'change_provenance_gate.json', 'commit_execution_gate.json', 'fresh_evidence_gate.json', 'runtime_integration_gate.json', 'final_verifier_report.json']
```
The two ancestry counts (ancestry-path and plain, both over `aa5defdee6b508a77e0d41fba433f75b7b77d6cf`
(the FORK POINT)..HEAD) read equal at **31** — one more than the reviewer's dry-run reading of 30,
accounting for this round's extra commit, C1 (the reviewer's tree carried C2 but not C1). Collected
732 node ids with 2 deselected (the standing D3 `not legacy` quarantine), matching the reviewer's dry
run exactly. The red control found 0 unsafe ids among the 732 real ones, and the planted unsafe id
(`tests/x.py::test_a[/home/someone/secret]`) answered "a local absolute path" — equal to the
reviewer's reading. pytest exited 0 with 732 passed, 0 failed, 0 skipped — equal to the reviewer's
732 passed, 0 skipped reading. `output_hash`
`8f3ee236836506837aa861108e5c5ffdf87abc89da01bb81c5c0fa1d044fc0eb` over the real pytest output.
`validate_verification_tests` returned an EMPTY problem list; `is_valid_current_run` True with an
empty `validation_errors` list — both equal to the reviewer's reading. The evidence directory holds
six gate files: `artifact_contract_gate.json`, `change_provenance_gate.json`,
`commit_execution_gate.json`, `fresh_evidence_gate.json`, `runtime_integration_gate.json`,
`final_verifier_report.json`. Job id `f291r5e1001`; the summary JSON reports `commit_count: 31`,
`verdict: "PASS_WITH_RISKS"`, `total_passed: 732`.

**G4 the package, at A2 (`scripts/make_review_zip.sh --evidence-dir .remedy-wt/f291-r5-evidence`,
no `REMEDY_REVIEW_DIR` set):** real exit code **0**. Log's decisive lines:
```
{"member_count": 7109, "authoritative_count": 13, "symlink_count": 0, "tombstone_count": 0, "final_path": "/home/decodeux/Repos/remedy-history/zips/remedy-review-20260929-230028-READY_FOR_REVIEW.zip", "final_sha256": "445966ec71a0b64f30be65c8082e7819f43a060bfdb80a8505ca9aa0dc62ca33", "publication_capability": "SUPPORTED", "package_status": "READY_FOR_REVIEW", "evidence_authoritative": true, "review_subject_alignment": "PASS", "manifest_sha256": "1f121364652db9589fad8a0df5d01e17f9e82b3e8cc15855e07306b83e542a48"}
REVIEW_PACKAGE_CREATED=true
PACKAGE_STATUS=READY_FOR_REVIEW
REVIEW_SUBJECT_ALIGNMENT=PASS
EVIDENCE_AUTHORITATIVE=true
REVIEW_PACKAGE_DIR=/home/decodeux/Repos/remedy-history/zips
ZIP_PATH=/home/decodeux/Repos/remedy-history/zips/remedy-review-20260929-230028-READY_FOR_REVIEW.zip
```
`PACKAGE_STATUS` reads `READY_FOR_REVIEW` (the reading, not the exit code); `REVIEW_SUBJECT_ALIGNMENT`
reads `PASS`; `EVIDENCE_AUTHORITATIVE` reads `true`. Package filename
`remedy-review-20260929-230028-READY_FOR_REVIEW.zip`, SHA-256 (independently recomputed, streaming,
over the file on disk) `445966ec71a0b64f30be65c8082e7819f43a060bfdb80a8505ca9aa0dc62ca33`, equal to
the log's `final_sha256`. `zipfile.is_zipfile` → True; `zf.testzip()` → None. The
`.review_zip_manifest.json` INSIDE the package reads `committed_review_subject`:
`base_commit` `aa5defdee6b508a77e0d41fba433f75b7b77d6cf` (the FORK POINT), `base_is_ancestor` true,
`head_commit` `5f4cebf3751861d03edf470d2ff3c47c13005279` (equal to C2's full sha, the accepted head),
`commit_count` 31, `file_count` 59, `tombstones` []. Archived directory:
`/home/decodeux/Repos/remedy-history/zips` (not `NOT ARCHIVED`).

**G5 the tree, after A2:** `python3 -m apps.cli.main integrity check --json` →
```
{"check_count": 6, "checks": [{"message": "handlers=171", "name": "handler_import", "status": "pass"}, {"message": "last Gate verdict PASS", "name": "live_review_verdict", "status": "pass"}, {"message": "unchecked=0, context_complete=False", "name": "plan_consistency", "status": "pass"}, {"message": "untracked=0, relevant=0", "name": "relevant_untracked", "status": "pass"}, {"message": "no reviewer scratch, evidence dir or archive at the root", "name": "repo_root_hygiene", "status": "pass"}, {"message": "no open blocker/high findings", "name": "high_blockers_open", "status": "pass"}], "fail_count": 0, "ok": true, "passed": true, "schema_version": 1, "version": 1}
```
All six checks read `status: "pass"`, `fail_count: 0`, `ok: true`, real exit 0. `git status
--porcelain` empty. `git worktree list | wc -l` = 13, equal to the BEFORE-ANYTHING-ELSE step 4
reading.

**Round's whole tracked path set** (constraint 3), measured with `git diff --name-only d88f85b68`
before C3 is committed: `.agent/authored/f291-r5-block.md`,
`.agent/authored/f291-r5-create_f291_evidence.py`, `.agent/authored/f291-r5-plan.md`,
`.agent/authored/f291-r5-records.diff`, `.agent/live_review.md`, `.agent/plan.md`,
`docs/roadmap/features/T5_F291.md` — every path is a member of the block's stated set (constraint
3's list, `.agent/handoff.md` itself added by C3). No evidence directory, no package and no queue
file is in this list — `.remedy-wt/f291-r5-evidence/` is gitignored
(`git check-ignore -v` → `.gitignore:235:.remedy-wt/`) and the package lives outside the repository
tree entirely, under `/home/decodeux/Repos/remedy-history/zips`.

## Authored-text proofs

Both `.agent/authored/f291-r5-*` payload/block copies verified byte-identical, source to committed
copy, by an independent hash-comparison script comparing `.remedy-wt/f291-r5/block.md` and each
`.remedy-wt/f291-r5-payloads/*` file against `git show 6fc445a8d:<path>` — all four equal (G1,
above). The applied `records.diff` (→ `.agent/live_review.md`, and the rewritten `.agent/plan.md` via
`shutil.copyfile`, and `docs/roadmap/features/T5_F291.md`) reproduced content matching the block's
G2 byte/sha256 table exactly at C2 — this confirms `git apply` and `shutil.copyfile` reproduced the
reviewer-authored text exactly, not only that the source payload itself was uncorrupted.
`create_f291_evidence.py` (A1's tool) ran unedited from the payload directory, as the block requires;
its own file bytes were never touched after the G1 copy.

## Deviations & assumptions

None from the block's ordered commit/action sequence — C1, C2, A0, A1, A2 and C3 landed in the
block's own order, with no payload retyped or edited, and no evidence file hand-edited to make a
validator pass. A0's preview listed no reclaimable candidate (`Reclaimable: nothing`, `Would free 0 B
in 0 paths`, one refused path `review_staging.n4o46eq_`/`class_not_job_keyed` — identical in shape to
the reviewer's own preview reading), so `--apply` was correctly skipped per the block's own
conditional instruction; this is not a deviation, it is the block's stated branch for an empty
preview. Every gate the block ordered (G1 through G5) ran and its real output is reported above; G6
is reported in the worker's final reply only, since it covers C3's own push and cannot be recorded
inside C3. No file outside the round's tracked path set (constraint 3) was touched (verified above).
No `gh pr create` or `gh pr merge`, no checkout of `main`, no branch deletion, no force-push, no
`git stash`, no STATUS/README edit, no ledger rotation, no queue edit and no self-use run.

## Next

Per the block's `## Next` order: Phase 1 rule 1, then the review of round 5, then the closing round —
the booking of round 5, the ledger rotation, the STATUS line with the README and the self-use queue
in the same commit, and the pull request. Open findings: 0, per `open_finding_ids` at C2 (`[]`).
Operator questions open: 0.

## Item-status table

| Item | Status | Reason |
|---|---|---|
| C1 copy round 5 block and payloads | done | 374 insertions, matching block's formula exactly (167+207) |
| C2 book round 4 with R-1114's resolution and complete the Built State | done | numstat matched exactly (4/0, 7/9, 7/0); G2 hashes and ledger readings matched; pushed immediately after |
| A0 the staging reclaim | done | preview read no candidate (`Would free 0 B in 0 paths`), `--apply` skipped per the block's conditional instruction |
| A1 the evidence job | done | exit 0; ancestry counts equal at 31; 732 collected/2 deselected; pytest 732 passed/0 failed/0 skipped; validate_verification_tests empty; is_valid_current_run True |
| A2 the review package | done | exit 0; PACKAGE_STATUS READY_FOR_REVIEW; REVIEW_SUBJECT_ALIGNMENT PASS; EVIDENCE_AUTHORITATIVE true; manifest base/head equal to fork point/accepted head |
| C3 rewrite handoff for round 5 | done | this commit |
| G1 transport | done | all four authored copies byte-identical to source |
| G2 the booking | done | all three C2 files byte/hash-equal to the reviewer's tree; open_finding_ids `[]`, latest_gate_verdict PASS; serial gate 369 passed at exit 0 |
| G3 the bundle | done | all A1 readings equal to or consistent with the reviewer's dry run (ancestry +1 for C1) |
| G4 the package | done | all A2 readings equal to the reviewer's dry run shape; package archived at `/home/decodeux/Repos/remedy-history/zips` |
| G5 the tree | done | integrity check 6/6 pass, fail_count 0; git status clean; worktree count 13 |

Open findings: 0 (`open_finding_ids` at C2 reads `[]`). Operator questions open: 0.
