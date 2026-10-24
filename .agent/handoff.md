# Handoff — F157 round 10 (C1/C2 landed, evidence job and review package both green)

## Session

SESSION 3 of feature F157 · round 10 · rounds so far 10. This round booked round 9's PASS verdict,
found the staging reclaim had nothing to free, ran the closure's evidence job to a clean exit 0 and
built the review package to `READY_FOR_REVIEW`, so closure algorithm steps 1 and 2 both now hold
for F157.

Fortschritt: ~95 % (everything but the closing round is done) — Schätzung.

## Range

Review of `4fed10f19`..`ce081c649`.

## Commits

### 6a2186efc F157 R10 C1: book round 9, the plan, the block
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f157-r10.md` | +123/-0 | NEW FILE — this round's block, the authored-text proof |
| `.agent/live_review.md` | +2/-0 | books round 9's PASS verdict (Gate: F157 R9) |
| `.agent/plan.md` | +5/-6 | rewritten: Current Step → round 10's evidence/package sequence, Next Steps → the closing round |

### ce081c649 F157 R10 C2: the evidence script
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f157-r10-create_f157_evidence.py` | +313/-0 | NEW FILE — the evidence script (adapted from F314's), run once by A2 |

### (this commit) F157 R10 C3: handback
| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | rewritten | this file |

## External actions

`gh pr list --state open --json number,headRefName,baseRefName,isDraft` (precondition check,
before any write) → `[]`. `git push -u origin feature/f157-capability-matrix` — run once
immediately after C2, succeeded on the first attempt (no HTTP 500, no retry needed). No PR
created, edited, or merged this round, per the block's constraint. No worktree created or removed.
`git push` runs again once immediately after this commit.

## Verification

**Gate 1.** `git status --porcelain` (run after C2) → empty output, exit 0. Then
`python3 .remedy-wt/f157-r10/prep/verify.py .` → every check line `True` except `absent	C3`
(expected — C3 had not been committed yet when the gate ran), last line `ALL True`. Full output:

```
True	6a2186efc single parent equal to the commit before it
True	ce081c649 single parent equal to the commit before it
True	every commit carries a F157 R10 Cn subject: 2 of 2
True	on feature/f157-capability-matrix
True	C1 paths exactly ['.agent/authored/f157-r10.md', '.agent/live_review.md', '.agent/plan.md']: ['.agent/authored/f157-r10.md', '.agent/live_review.md', '.agent/plan.md']
True	C1 .agent/authored/f157-r10.md equals c1-.agent__authored__f157-r10.md
True	C1 .agent/live_review.md equals c1-.agent__live_review.md
True	C1 .agent/plan.md equals c1-.agent__plan.md
True	C2 paths exactly ['.agent/authored/f157-r10-create_f157_evidence.py']: ['.agent/authored/f157-r10-create_f157_evidence.py']
True	C2 .agent/authored/f157-r10-create_f157_evidence.py equals c2-.agent__authored__f157-r10-create_f157_evidence.py
absent	C3
True	the saved block equals block.md
ALL True
```

**Gate 2 — A2 (evidence job).** Launch:
`python3 .remedy-wt/f157-r10/prep/launch.py evidence .remedy-wt/f157-r10-worker` →
`started evidence: pid 3775688, log .remedy-wt/f157-r10-worker/evidence.log`. One
`python3 .remedy-wt/f157-r10/prep/wait.py evidence .remedy-wt/f157-r10-worker 50` call was enough
(nothing else ran meanwhile); exit code read from `.remedy-wt/f157-r10-worker/evidence.exit`:
`exit 0 wall 1860.1`. Printed lines:

```
head ce081c649130009560b1cfc9c3ccd26b16641cfb
ancestry-path count 36
plain count 36
collected node ids 12858, deselected 253
red control: unsafe among the real ids 0 []
red control: planted id -> a local absolute path
pytest exit 0, {'passed': 12852, 'failed': 0, 'skipped': 6}, output_hash dbf70356ff49191525c369d9b18532cafcd38438dcf9d272207d4212f38e8764, duration 1828.719s
validate_verification_tests problems [] passed 12852
is_valid_current_run True
validation_errors []
gates written: ['artifact_contract_gate.json', 'change_provenance_gate.json', 'commit_execution_gate.json', 'fresh_evidence_gate.json', 'runtime_integration_gate.json', 'final_verifier_report.json']
{
  "job_id": "f157r10e1001",
  "head_commit": "ce081c649130009560b1cfc9c3ccd26b16641cfb",
  "authority_count": 22,
  "partition": {"T001": 8, "T002": 8, "T003": 6},
  "commit_count": 36,
  "verdict": "PASS_WITH_RISKS",
  "manual_completion": true,
  "operator_attested_tasks": ["T001", "T002", "T003"],
  "total_passed": 12852
}
```

Every expected reading matched the block: head equal to C2's full sha, both ancestry counts equal
(36), collected node ids 12858 with deselected 253, red control unsafe count 0 with the planted id
reading `a local absolute path`, pytest exit 0 with failed 0 and duration above zero,
`validate_verification_tests` problems `[]`, `is_valid_current_run` `True`, `validation_errors`
`[]`, process exit 0.

**Gate 2 — A3 (review package).** Launch:
`python3 .remedy-wt/f157-r10/prep/launch.py zip .remedy-wt/f157-r10-worker` →
`started zip: pid 4020041, log .remedy-wt/f157-r10-worker/zip.log`. One
`python3 .remedy-wt/f157-r10/prep/wait.py zip .remedy-wt/f157-r10-worker 50` call was enough; exit
code read from `.remedy-wt/f157-r10-worker/zip.exit`: `exit 0 wall 21.3`. This machine's home
folder is written as `~` below, never as its real absolute path, per the block's own instruction
for the package directory and the C3 no-machine-path constraint. Printed lines:

```
UNCHANGED: runtime_integration_gate.json — rebuilt from source; identical to existing
Evidence refresh completed for staged copy.
Observability index generated from staged bytes: evidence/current/self_run_observability_index.json
Review reports packaged: 4 (newest first; see review_reports/INDEX.md)
Review reports read from: ~/Repos/remedy/.data/review_reports
{"member_count": 2117, "authoritative_count": 22, "symlink_count": 0, "tombstone_count": 0, "final_path": "~/Repos/remedy-history/zips/remedy-review-20261024-070450-READY_FOR_REVIEW.zip", "final_sha256": "9486e587f096ea0811f1d4b65439c0b4ee1bbc648e623f4a037dd73adff72403", "publication_capability": "SUPPORTED", "package_status": "READY_FOR_REVIEW", "evidence_authoritative": true, "review_subject_alignment": "PASS", "manifest_sha256": "ee21f4dd9298ed0bdb821e7cb693d5344344cbe9681ddff0b936a65ad5ea35f0"}

REVIEW_PACKAGE_CREATED=true
PACKAGE_STATUS=READY_FOR_REVIEW
PACKAGING_CWD=~/Repos/remedy
EVIDENCE_DIR=.remedy-wt/f157-r10-evidence
REVIEW_SUBJECT_ALIGNMENT=PASS
EVIDENCE_AUTHORITATIVE=true
REVIEW_PACKAGE_DIR=~/Repos/remedy-history/zips
ZIP_PATH=~/Repos/remedy-history/zips/remedy-review-20261024-070450-READY_FOR_REVIEW.zip
```

Independent checks, run after the build: `python3 -c` sha256 over the package file ==
`9486e587f096ea0811f1d4b65439c0b4ee1bbc648e623f4a037dd73adff72403` (matches the tool's own
`final_sha256`); `zipfile.is_zipfile(...)` → `True`; `ZipFile.testzip()` → `None`; the manifest's
`committed_review_subject` inside the package → `base_commit`
`0f811a7131031c67b2beb537e6afd79d0d626c98`, `head_commit`
`ce081c649130009560b1cfc9c3ccd26b16641cfb` (both exactly as the block ordered); top-level
`package_status` `READY_FOR_REVIEW`.

**Gate 3.** `python3 -m apps.cli.main integrity check --json` →
`{"check_count": 6, "checks": [{"message": "handlers=201", "name": "handler_import", "status":
"pass"}, {"message": "last Gate verdict PASS", "name": "live_review_verdict", "status": "pass"},
{"message": "unchecked=0, context_complete=False", "name": "plan_consistency", "status": "pass"},
{"message": "untracked=0, relevant=0", "name": "relevant_untracked", "status": "pass"},
{"message": "no reviewer scratch, evidence dir or archive at the root", "name":
"repo_root_hygiene", "status": "pass"}, {"message": "no open blocker/high findings", "name":
"high_blockers_open", "status": "pass"}], "fail_count": 0, "ok": true, "passed": true,
"schema_version": 1, "version": 1}`.
Then `python3 -c "import scripts.rotate_live_review as r; print(r.open_finding_ids(open('.agent/live_review.md').read()))"`
→ `['R-1246', 'R-1281', 'R-1351', 'R-1353', 'R-1426', 'R-1428', 'R-1448', 'R-1450']` — exactly the
eight ids the block names. `git status --porcelain` (after A3, before C3) → empty, exit 0.

## Authored-text proofs

C1's byte copy (`.remedy-wt/f157-r10-worker/c1_copy.py`) read `bytes_equal=True` disk-to-disk for
all three targets immediately after copying: `.agent/authored/f157-r10.md`,
`.agent/live_review.md`, `.agent/plan.md`. `block.md` read `line_count=123`,
`sha256=1ba58efab04718df3216314958f5ca6ef186ff9ed2ad789a75c6ee1a43d77c9b`. `verify.py`'s gate-1 run
independently re-confirmed all three `C1 <path> equals c1-<path>` lines `True`, and
`the saved block equals block.md` `True`.
C2's byte copy (`.remedy-wt/f157-r10-worker/c2_copy.py`) read `bytes_equal=True` disk-to-disk for
`.agent/authored/f157-r10-create_f157_evidence.py`, independently reconfirmed by `verify.py`'s
`C2 ... equals c2-...` line `True`.

## Evidence and package

Job id `f157r10e1001`. A2's decisive lines are quoted in full in Verification above: head equal to
C2's full sha `ce081c649130009560b1cfc9c3ccd26b16641cfb`, ancestry-path count and plain count both
36, 12858 node ids collected with 253 deselected, red control unsafe count 0 with planted id
`a local absolute path`, pytest exit 0 with 12852 passed / 0 failed / 6 skipped over 1828.719s,
`validate_verification_tests` problems `[]`, `is_valid_current_run` `True`, `validation_errors`
`[]`, process exit 0. Package: `remedy-review-20261024-070450-READY_FOR_REVIEW.zip`, SHA-256
`9486e587f096ea0811f1d4b65439c0b4ee1bbc648e623f4a037dd73adff72403` (independently computed, matches
the tool's own `final_sha256`), directory `~/Repos/remedy-history/zips`. `PACKAGE_STATUS`
`READY_FOR_REVIEW`, `REVIEW_SUBJECT_ALIGNMENT` `PASS`, `EVIDENCE_AUTHORITATIVE` `true`. Accepted
head inside the package's manifest: `ce081c649130009560b1cfc9c3ccd26b16641cfb`, base
`0f811a7131031c67b2beb537e6afd79d0d626c98` — both exactly as the block ordered.

## Staging reclaim

A1 preview (`python3 -m apps.cli.main data reclaim --orphans`) → `Reclaimable: nothing`;
`Would free 0 B in 0 paths — nothing deleted; re-run with --apply`. Every listed path was refused
with reason `durable`: `api`, `autonomy`, `control`, `crash`, `evidence_exports`,
`job_apply_records`, `job_evidence_index`, `job_logs`, `jobs`, `logs`, `memory`, `missions`,
`projects`, `review_reports`, `roadmap`, `runs`, `serve`. The preview listed no candidate, so
`--apply` was skipped per the block and this empty reading is the final one for A1.

## Deviations & assumptions

None from the ordered commit/action sequence: C1, C2, A1, A2, A3 ran exactly as the block orders,
in order, each gated by the commands it names, and all three gates read green on the first and
only run; the push after C2 succeeded on the first attempt, so no HTTP 500 retry was exercised. One
note, not a deviation: A3's own printed transcript and this handback both write this machine's home
folder as `~` in place of the real absolute path, exactly as the block's A3 instruction and the C3
no-machine-path constraint require; the unredacted values were read and checked directly in the
session before the substitution.

## Item status

| Item | Status | Reason |
|---|---|---|
| C1 | done | |
| C2 | done | pushed immediately after; no HTTP 500 retry needed |
| A1 | done | preview found nothing reclaimable; apply skipped (no candidate listed) |
| A2 | done | exit 0; every expected reading matched the block exactly |
| A3 | done | `PACKAGE_STATUS` `READY_FOR_REVIEW`; `REVIEW_SUBJECT_ALIGNMENT` `PASS`; `EVIDENCE_AUTHORITATIVE` `true` |
| C3 | done | this handback |
| Gate 1 | done | `git status --porcelain` empty; `verify.py` `ALL True` (C3 `absent` at gate time, expected) |
| Gate 2 | done | A2 and A3 both exit 0 per their `.exit` files; every decisive reading matched |
| Gate 3 | done | `fail_count` 0; eight open finding ids match exactly; `git status --porcelain` empty |

## Next

1. Phase 1 rule 1: check `.agent/STOP` before any new work.
2. Phase 1 rule 2: run the Open PR Gate before starting anything unrelated; no pull request is
   open for this branch yet.
3. The reviewer reviews round 10 and books its verdict in the next round's first commit.
4. Then the closing round: the Built State, the rotation, SU-081's `consumed_by`, the STATUS flip
   with the README sync, and the pull request, left unmerged.
5. Operator questions open: 2.
6. Open findings count (gate 3): 8 — `R-1246`, `R-1281`, `R-1351`, `R-1353`, `R-1426`, `R-1428`,
   `R-1448`, `R-1450`.

## For the operator, in plain sentences

This round collected and checked this feature's evidence: every test file the evidence job
packages ran once, 12,852 tests passed and none failed, and all of the evidence job's own checks
came back clean. The review package was then built and is ready for review, saved in the zips
folder under this machine's home directory. From the previous rounds: the paid self-use run that
wrote the first tests for the part of Remedy that hides secrets in public text was reviewed and
passed, and that work is still kept on its own branch, not yet applied to this one.
