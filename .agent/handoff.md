# Handback — F043 round 8: the closure sequence's evidence round — book round 7, complete the
Built State with the closure suite, reclaim staging copies, and build the evidence bundle and the
review package at the accepted head

## Session

SESSION 1 of feature F043 · round 8 · rounds so far 8. Context self-assessment: a large majority of
the session's context window remained when this handback was written, after both commits and gates
G1 through G5.

## Range

Review of `0e1329230`..HEAD (this round's final commit, C3 — the push's real outcome and
`gh pr list` are reported in the worker's reply, since this file is committed as part of C3 and
cannot name a push that follows it).

## Commits

### `86cefdc52` F043 R8 C1: copy round 8 block and payloads
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f043-r8-block.md | +170/-0 | this round's block, copied verbatim via `shutil.copyfile` |
| .agent/authored/f043-r8-create_f043_evidence.py | +160/-0 | payload copy |
| .agent/authored/f043-r8-plan.md | +28/-0 | payload copy |
| .agent/authored/f043-r8-records.diff | +23/-0 | payload copy |

Total 381 insertions, matching the block's stated formula exactly (block's 170 lines + 211).

### `79137914f` F043 R8 C2: book round 7 and complete the Built State with the closure suite
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +2/-0 | `git apply records.diff`: round 7's Gate entry appended |
| .agent/plan.md | +6/-6 | rewrite := plan.md payload |
| docs/roadmap/features/T5_F043.md | +3/-0 | `git apply records.diff`: the closure-suite paragraph |

Every numstat reading equals the block's expected table exactly (2/0, 6/6, 3/0). `git apply
--check` on records.diff read exit 0 before the real apply, which also read exit 0. This commit's
full sha, `79137914f113d510ecdef140dfecc8b0e49a76e3`, is this closure's ACCEPTED HEAD.

### `<this commit>` F043 R8 C3: rewrite handoff for round 8 with the evidence and package readings
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | rewrite | this file, per `docs/agents/handback_template.md` |

## External actions

- `git push -u origin feature/f043-explanation-layer` after C2 — remote updated
  `0e1329230..79137914f`, real exit 0 (fast-forward, tracking already set from round 7).
- `python3 -m apps.cli.main data reclaim --orphans` (A0, no commit) — preview only, no `--apply`
  (see Verification).
- `python3 .remedy-wt/f043-r8-payloads/create_f043_evidence.py` (A1, no commit) — wrote
  `.remedy-wt/f043-r8-evidence/`, gitignored, not committed.
- `bash scripts/make_review_zip.sh --evidence-dir .remedy-wt/f043-r8-evidence` (A2, no commit,
  `REMEDY_REVIEW_DIR` not set) — wrote the package to the operator's archive, not committed.
- `git push` after C3 — reported in the worker's reply, since it runs after this commit.
- No `gh pr create`, no `gh pr merge`, no checkout of `main`, no branch deletion, no force-push, no
  `git stash`, no self-use run, no STATUS/README edit, no ledger rotation, no queue edit.

## Verification

**BEFORE ANYTHING ELSE** —
- `ls .agent/STOP` → `ls: cannot access '.agent/STOP': No such file or directory` (absent).
- `pwd` → `/home/decodeux/Repos/remedy`. `git status --porcelain` → empty. `git branch
  --show-current` → `feature/f043-explanation-layer`. `git log --oneline -1` → `0e1329230 F043 R7
  C7: record the closure suite transcript and rewrite handoff for round 7` — all three match the
  block's stated readings.
- Block bytes (R-0954): measured line count (newline count) 170, sha256
  `e5554b3ab4cdfb340b38abb35b4c536524fb5ee022f99b03c4522d35e85620f4`, both equal the two readings
  the delegation message stated.
- `git worktree list | wc -l` → 11.

**PAYLOADS TABLE** — every reading measured before use, all three exact matches against the block's
table:
| file | lines | bytes | sha256 |
|---|---|---|---|
| records.diff | 23 | 6011 | `b9b90c21fa9b532e40971170ddc6a7287386bb72e6ecbd82619917acd478d8c4` |
| plan.md | 28 | 965 | `18faa259158bda7867c0f15a37f2c68de934a60c677196880d583a2bbdc04b21` |
| create_f043_evidence.py | 160 | 7765 | `cf7f0878b36f87e801cc18914d13aa73a1d8b5ea510aeca23673922daadb0ed2` |

**G1 TRANSPORT** — every `.agent/authored/f043-r8-*` copy, read back with `git show 86cefdc52:<path>`
from C1, was byte-for-byte identical to its source: block.md against `.remedy-wt/f043-r8/block.md`,
create_f043_evidence.py/plan.md/records.diff against their payloads — 4 pairs, all `byte_equal: True`,
confirmed by both `diff -q` and `sha256sum`.

**G2 THE BOOKING** — every committed file's bytes and sha256 at `79137914f` equaled the block's
given values exactly:
- `.agent/live_review.md` @ C2 (135097 bytes, `04a3725abe586965fdf088cef9b83e0be6a2de854eeda11e86a99d8400d3fe0f`) — match
- `.agent/plan.md` @ C2 (965 bytes, `18faa259158bda7867c0f15a37f2c68de934a60c677196880d583a2bbdc04b21`) — match
- `docs/roadmap/features/T5_F043.md` @ C2 (8407 bytes, `bf74bb52f4d0cd17e964057d5a104dea9269c4f320e11b7bd4149cc951bcc6b6`) — match

`open_finding_ids` (from `scripts/rotate_live_review.py`) over the ledger text at C2 read `[]`,
`latest_gate_verdict` read `PASS` — both matching the reviewer's stated reading exactly.

Serially at C2:
```
$ bash -c 'python3 -m pytest -q -p no:cacheprovider tests/docs/ tests/cli/test_golden_path.py 2>&1 | tail -3; echo "REAL_EXIT=${PIPESTATUS[0]}"'
........................................................................ [ 97%]
.........                                                                [100%]
369 passed in 53.35s
REAL_EXIT=0
```
Matches the reviewer's stated reading exactly (`369 passed`), exit 0.

**G3 THE BUNDLE** (A1, tool: `create_f043_evidence.py`) — real exit code 0. Full log:
```
head 79137914f113d510ecdef140dfecc8b0e49a76e3
ancestry-path count 58
plain count 58
collected node ids 748, deselected 2
red control: unsafe among the real ids 0 []
red control: planted id -> a local absolute path
pytest exit 0, {'passed': 748, 'failed': 0, 'skipped': 0}, output_hash c68d56c66eb7cfd5a92350a4f8eb46ecc01c5d647d383eb028758b72ed84e8aa
validate_verification_tests problems [] passed 748
is_valid_current_run True
validation_errors []
gates written: ['artifact_contract_gate.json', 'change_provenance_gate.json', 'commit_execution_gate.json', 'fresh_evidence_gate.json', 'runtime_integration_gate.json', 'final_verifier_report.json']
```
The two ancestry counts are equal (58 = 58), each one more than the reviewer's dry-run reading of 57
— the block states this is expected, for C1. Collected 748 node ids with 2 deselected, matching the
reviewer's reading exactly. The red control found 0 unsafe among the real ids; the planted id
answered `a local absolute path`, matching the reviewer's reading. Pytest exit 0, 748 passed, 0
skipped, `output_hash c68d56c66eb7cfd5a92350a4f8eb46ecc01c5d647d383eb028758b72ed84e8aa`.
`validate_verification_tests` returned an EMPTY problem list. `is_valid_current_run` True, no
validation errors. Six gate files written: `artifact_contract_gate.json`,
`change_provenance_gate.json`, `commit_execution_gate.json`, `fresh_evidence_gate.json`,
`runtime_integration_gate.json`, `final_verifier_report.json`. The job's own summary JSON:
`job_id f043r8e1001`, `head_commit 79137914f113d510ecdef140dfecc8b0e49a76e3`, `authority_count 46`,
`commit_count 58`, `verdict PASS_WITH_RISKS`, `total_passed 748`.

**A0 THE STAGING RECLAIM** — real exit 0. Full log:
```
Data root: /home/decodeux/Repos/remedy/.data
  Reclaimable: nothing
  Refused (kept, with the reason):
    review_staging.n4o46eq_  class_not_job_keyed: no job owns this path; reclaim addresses job-keyed classes only  1.5 MB
  Not reclaimed — reclaim addresses ephemeral classes only:
    control (durable)  228 B
    evidence (unclassified)  4.1 MB
    evidence_exports (durable)  32.7 MB
    job_evidence_index (durable)  141.6 KB
    job_logs (durable)  16.8 MB
    job_promotions (unclassified)  237.7 KB
    jobs (durable)  158.6 MB
    memory (durable)  3.3 KB
    missions (durable)  8.2 KB
    pingpong_runs (unclassified)  165.5 MB
    projects (durable)  121.1 KB
    proposed_tasks (durable)  1.8 KB
    queue (unclassified)  364 B
    remedy-job-evidence-f013_job_intake_closure (unclassified)  338.1 KB
    roadmap (durable)  148.6 KB
    runs (durable)  138.8 MB
    smoke (durable)  225 B
    task_jobs (unclassified)  44.9 MB
    ui (durable)  0 B
    workspaces (durable)  37.7 MB
  Would free 0 B in 0 paths — nothing deleted; re-run with --apply
```
Matches the reviewer's stated preview reading exactly: `Would free 0 B in 0 paths`, one refused
path `review_staging.n4o46eq_` with reason `class_not_job_keyed`. Since the preview also lists no
candidate, `--apply` was SKIPPED and this empty reading is the recorded one.

**G4 THE PACKAGE** (A2, tool: `scripts/make_review_zip.sh`) — real exit 0. Decisive log lines:
```
UNCHANGED: runtime_integration_gate.json — rebuilt from source; identical to existing
Evidence refresh completed for staged copy.
Observability index generated from staged bytes: evidence/current/self_run_observability_index.json
{"member_count": 7235, "authoritative_count": 46, "symlink_count": 0, "tombstone_count": 0, "final_path": "/home/decodeux/Repos/remedy-history/zips/remedy-review-20260930-033441-READY_FOR_REVIEW.zip", "final_sha256": "a9e44274ad032d41fae6741aeaa5f891ecfd983d5af99663208d97f1560da6e1", "publication_capability": "SUPPORTED", "package_status": "READY_FOR_REVIEW", "evidence_authoritative": true, "review_subject_alignment": "PASS", "manifest_sha256": "779305d825986faae1620c885981dcb520eb761459220f2be3c69beddb1eeecd"}
REVIEW_PACKAGE_CREATED=true
PACKAGE_STATUS=READY_FOR_REVIEW
REVIEW_SUBJECT_ALIGNMENT=PASS
EVIDENCE_AUTHORITATIVE=true
REVIEW_PACKAGE_DIR=/home/decodeux/Repos/remedy-history/zips
ZIP_PATH=/home/decodeux/Repos/remedy-history/zips/remedy-review-20260930-033441-READY_FOR_REVIEW.zip
```
`PACKAGE_STATUS=READY_FOR_REVIEW`, `REVIEW_SUBJECT_ALIGNMENT=PASS`,
`EVIDENCE_AUTHORITATIVE=true`. Package filename `remedy-review-20260930-033441-READY_FOR_REVIEW.zip`,
SHA-256 `a9e44274ad032d41fae6741aeaa5f891ecfd983d5af99663208d97f1560da6e1` (recomputed independently
by the worker over the file on disk, matching `final_sha256` from the tool's own JSON line).
`.review_zip_manifest.json` read from INSIDE the package: `committed_review_subject.base_commit =
21bfc1881b81902b267171d0486d82d1ed89fe25` (the FORK POINT, equal to `BASE` in the evidence tool),
`committed_review_subject.head_commit = 79137914f113d510ecdef140dfecc8b0e49a76e3` (equal to C2's
full sha, the accepted head). `zipfile.is_zipfile(path)` → `True`; `ZipFile.testzip()` → `None`
(no bad member). Archived directory: `/home/decodeux/Repos/remedy-history/zips` (not `NOT ARCHIVED`).

**G5 THE TREE** (after A2) —
```
$ python3 -m apps.cli.main integrity check --json
{"check_count": 6, "checks": [{"message": "handlers=171", "name": "handler_import", "status": "pass"}, {"message": "last Gate verdict PASS", "name": "live_review_verdict", "status": "pass"}, {"message": "unchecked=0, context_complete=False", "name": "plan_consistency", "status": "pass"}, {"message": "untracked=0, relevant=0", "name": "relevant_untracked", "status": "pass"}, {"message": "no reviewer scratch, evidence dir or archive at the root", "name": "repo_root_hygiene", "status": "pass"}, {"message": "no open blocker/high findings", "name": "high_blockers_open", "status": "pass"}], "fail_count": 0, "ok": true, "passed": true, "schema_version": 1, "version": 1}
REAL_EXIT=0
```
All six checks read status `pass`, `fail_count` 0. `git status --porcelain` → empty. `git worktree
list | wc -l` → 11 (unchanged throughout the round).

## Authored-text proofs

Every `.agent/authored/f043-r8-*` copy (the block, create_f043_evidence.py, plan.md, records.diff)
was compared byte-for-byte against its source under `.remedy-wt/f043-r8-payloads/` (and the block
itself against `.remedy-wt/f043-r8/block.md`), read back with `git show 86cefdc52:<path>` from C1:
all 4 pairs match (G1 above, `diff -q` silent and sha256 identical each time). `records.diff` was
not edited or retyped; it applied with `git apply --check` (exit 0) then `git apply` (exit 0)
verbatim. `plan.md` was applied only by `shutil.copyfile`, never retyped.

## Item status (AGENTS.md Completion Report)

| Item | Status | Reason |
|---|---|---|
| C1 | done | |
| C2 | done | commit's full sha is the ACCEPTED HEAD |
| A0 | done | preview read no candidate; `--apply` correctly skipped per the block's conditional |
| A1 | done | tool exit 0, all validations passed |
| A2 | done | `PACKAGE_STATUS=READY_FOR_REVIEW`, exit 0 |
| C3 | done | this handoff |
| G1 | done | |
| G2 | done | |
| G3 | done | |
| G4 | done | |
| G5 | done | |
| G6 | done | reported in the worker's reply (runs after C3 and its push) |

## Deviations & assumptions

- None. Every payload applied unedited (`git apply --check` exit 0 before the real apply, which
  also read exit 0), the C1 insertion count (381) equaled the block's stated formula exactly, both
  C2 numstat readings equaled the block's expected table exactly, the docs/CLI test selection at C2
  matched the reviewer's tree reading exactly (`369 passed`), the evidence job's ancestry/plain
  counts, node id count, red control and pytest result all matched the reviewer's dry-run reading
  (with the ancestry counts one higher, as the block itself predicted, for C1), the reclaim preview
  matched the reviewer's stated preview exactly and required no `--apply`, and the package build
  read `READY_FOR_REVIEW`/`PASS`/`true` with a valid, uncorrupted zip whose internal manifest names
  the correct base and head. No departure from the block's ordered sequence C1-C2-A0-A1-A2-C3: every
  step ran in order, none dropped, none added, none reordered. The tracked path set at the tip
  (`git diff --name-only 0e1329230`) contains only the paths constraint 3 names: the four
  `.agent/authored/f043-r8-*` copies, `.agent/live_review.md`, `.agent/plan.md`,
  `docs/roadmap/features/T5_F043.md` and `.agent/handoff.md`. No evidence directory, no package and
  no queue file was committed. `scripts/self_use_queue.json` was not touched.

## Next

Phase 1 rule 1 (read `.agent/STOP` from disk), then the review of round 8, then the closing round —
the booking of round 8, the ledger rotation, the STATUS line with the README and the self-use queue
in the same commit, and the pull request. Open findings: 0 (`open_finding_ids` read `[]` at C2).
Operator questions open: 0.
