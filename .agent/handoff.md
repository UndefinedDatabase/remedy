# Handback — F079 R4 (CLOSURE PART 1: evidence job + review zip)

Branch: feature/f079-context-handoffs. Range a11d1f74..abc33f79, 4 commits
(+ this handoff). No STATUS edit, no README edit, no PR — that is part 2.

## THE FOUR VALUES FOR THE STATUS LINE
    Evidence job a7f0791c4d6b2e58
    package remedy-review-20260806-203747-READY_FOR_REVIEW.zip
    SHA-256 f30d540afec921aa76aef40d754abc7d00f4026eb2a755aa53bf99e241a88eec
    accepted HEAD abc33f79aac937d3504dddef7a72bdb22d4aa2d1
`accepted HEAD` is the content HEAD the manifest records
(committed_review_subject.head_commit) and the tree the zip was built from.
This handoff commit moves the branch tip past it — the tip after this commit
is NOT the accepted HEAD; use abc33f79 verbatim.

## Changed files per commit
| Commit | Path | +/- | Reason |
|---|---|---|---|
| ecde4e2e | .agent/last_block.md | +160/-146 | R4 block saved verbatim (rides alone) |
| 3873f31f | .agent/authored/f079-r4-{1,2,3}.md | +185/-0 | three texts, sha256 verified |
| cc03063c | .agent/live_review.md · plan.md | +105/-102 | R3 gate PASS persisted, closure plan |
| abc33f79 | docs/roadmap/features/T1_F079.md | +56/-0 | Built State section (precondition 4) |

Authored hashes matched their BEGIN markers before any application:
f883c986… (r4-1) · 16bce73d… (r4-2) · ae6e99fe… (r4-3).

## Raw transcripts
| Command | Exit | Tail |
|---|---|---|
| `pytest tests/docs/ -q` (docs gate, after commit D) | 0 | `293 passed in 0.26s` |
| `pytest tests/cli/test_golden_path.py -q` (canary, after commit D) | 0 | `42 passed in 19.37s` |
| `remedy integrity check --json` | 0 | `"passed": true, "fail_count": 0, "check_count": 5` — handler_import pass (handlers=323) · live_review_verdict pass · plan_consistency pass (unchecked=0) · relevant_untracked pass (untracked=0, relevant=0) · high_blockers_open pass (no open blocker/high findings). Raw JSON in the session scratch; reproduced in full in the handback message. |
| `git status --porcelain` (before zip) | 0 | (empty) |
| `git push` | 0 | `a11d1f74..abc33f79` |
| `pytest tests/orchestration/test_handoff.py -q` (vr-0001) | 0 | `39 passed in 0.32s` |
| `pytest tests/orchestration/test_gauntlet_runner.py -q` (vr-0002) | 0 | `45 passed in 0.55s` |
| `pytest tests/cli/test_mission_cmd.py -q` (vr-0003) | 0 | `83 passed in 36.73s` |
| `pytest tests/cli/test_golden_path.py -q` (vr-0004) | 0 | `42 passed in 19.31s` |
| `pytest tests/docs/ -q` (vr-0005) | 0 | `293 passed in 0.25s` |
| `git status --porcelain` (final) | 0 | (empty; both zips are `.gitignore`d — `remedy-review-*`) |

## Evidence job (producer invocation + stdout)
`packages.orchestration.job_evidence.create_manual_completion_bundle(...)`,
run from a throwaway script in the session scratchpad, writing into
`<scratch>/closure/remedy-job-evidence-f079-closure-2` — OUTSIDE the repo,
never committed. Arguments: `repo_root=<repo>`,
`base_commit=38854f6034f1abff6f2c1e85e4d21752d33d66b6` (full length),
`head_commit=abc33f79aac937d3504dddef7a72bdb22d4aa2d1`,
`job_id=a7f0791c4d6b2e58`, `step_range=T001-T003`, `prior_job_ids=[]`,
`review_feature_id="f079"`, five verification_runs (vr-0001..vr-0005,
`^vr-\d{4,}$`), each with real `--collect-only` node ids
(`len(node_ids) == selected`: 39/45/83/42/293), sha256-hex `output_hash`
computed over that run's own captured stdout, and `test_files` that are
FILES (tests/docs/ expanded to `tests/docs/test_docs_consistency.py`).

stdout:

    {
      "authority_count": 13,
      "commit_count": 26,
      "head_commit": "abc33f79aac937d3504dddef7a72bdb22d4aa2d1",
      "job_id": "a7f0791c4d6b2e58",
      "manual_completion": true,
      "operator_attested_tasks": ["T001", "T002", "T003"],
      "partition": {"T001": 5, "T002": 5, "T003": 3},
      "total_passed": 502,
      "verdict": "PASS_WITH_RISKS"
    }

PASS_WITH_RISKS is the operator-attested profile, not a defect: every gate
reads PASS (artifact_contract, change_provenance, fresh_evidence,
missing_tests, runtime_integration, scratch_file_guard, spec_compliance,
final_job_review), `missing_evidence` is empty, and the only non-PASS
entries are `commit_execution_gate: NEEDS_HUMAN_APPROVAL` plus the two
model-actuals-unavailable warnings that a zero-provider manual completion
always carries.

## Review zip
FIRST ATTEMPT — recorded because the protocol requires the attempt's outcome,
not just the successful one:
`remedy-review-20260806-203619-BLOCKED_EVIDENCE.zip`
(sha256 b2ad0fc52944033e0953bd3e5a99eb96f47d690f4c92019c69fe35fd51b1b787).
Cause, diagnosed from the manifest's `current_evidence.validation`
(not guessed, and not retried blind): that bundle also recorded the R3
full-suite run with its node ids enumerated, and the suite's own
redaction/traversal tests carry parametrized ids that literally contain
secret-like strings and absolute paths —
`test_public_surfaces_never_expose[sk-ABCDEFGHIJKLMNOPQRSTUVWX]`,
`[password=hunter2]`,
`test_absolute_and_traversing_refs_are_rejected[/home/someone/.data/raw_stream.jsonl]`
— 605 such ids. The packaging privacy validator rejected those fields, which
is correct behaviour, so enumerating the whole suite's ids can never pass.
The full-suite numbers therefore stay where they already are and where they
belong: `.agent/gate_f079_r3/` (committed, inside the review subject) and the
Built State section. Recording per-file scoped runs is also the established
precedent of previous closures.

SECOND ATTEMPT — the recorded package:

    package_status  READY_FOR_REVIEW
    ZIP_PATH        remedy-review-20260806-203747-READY_FOR_REVIEW.zip
    final_sha256    f30d540afec921aa76aef40d754abc7d00f4026eb2a755aa53bf99e241a88eec
    manifest_sha256 9ba12144776eddff1215d8f4c8603ba2377cbffeb5a4524d662bee4507e222bd
    member_count 2031 · authoritative_count 13 · symlink_count 0 · 9.0M
    EVIDENCE_AUTHORITATIVE=true · REVIEW_SUBJECT_ALIGNMENT=PASS

Verified in the packaged manifest:
`committed_review_subject.base_commit = 38854f6034f1abff6f2c1e85e4d21752d33d66b6`,
`head_commit = abc33f79aac937d3504dddef7a72bdb22d4aa2d1` — the required span;
`current_evidence.validation.is_valid_current_run = true` with
`validation_errors: []`; `final_verifier_reproducibility = VERIFIED_EQUAL`;
`token_truth_authority = VERIFIED_EQUAL`; `publication_capability = SUPPORTED`.
Integrity of the archive itself: `zipfile.testzip()` → None over all 2031
members. `sha256sum` of the file on disk reproduces the printed hash exactly.

## Item status
| Item | Status | Reason |
|---|---|---|
| 1 state commits | done | A/B/C in order, all three hashes verified before applying |
| 2 Built State | done | appended to T1_F079.md; docs gate 293 + canary 42, both exit 0 |
| 3 preconditions | done | integrity check PASS (5/5), porcelain empty, branch pushed |
| 4 evidence job | done | a7f0791c4d6b2e58, canonical producer, evidence dir outside the repo |
| 5 review zip | deviated | READY_FOR_REVIEW on the second attempt; the first was BLOCKED_EVIDENCE and both are recorded above with the diagnosed cause |
| 6 handback | done | canary green at the content HEAD, porcelain empty, values reported verbatim |
