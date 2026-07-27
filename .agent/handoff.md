# Handoff — F047 Checkpoint & resume (kill-proof) — CLOSED

Branch: feature/f047-checkpoint-resume · PR #153 (ready for review, NOT merged
— the Open PR Gate merges it at the next feature's start; the gap is the
operator's manual-review window)
Closure range: `3b257f6..HEAD` · Feature range: `89c4ef0..HEAD`
accepted HEAD: `8e870062feb3487f890232d659ef569cf3aa326e` (Commit B — the
pre-zip head the package and verdicts cover)
LAST_REVIEWED_SHA: `3b257f6` · Open findings: 0 (R-0146 Resolved)
Next expected action: reviewer closure verdict / end of Window 1.

## Closure facts

- Evidence job: `29fbc2fe-60d6-4bb2-a7bb-05dc59dd40d7`
- Evidence dir: `.data/evidence_exports/29fbc2fe-60d6-4bb2-a7bb-05dc59dd40d7`
- Package: `remedy-review-20260727-101857-READY_FOR_REVIEW.zip`
- SHA-256: `b6f96e888d7e8a6d5494f213b845a644be34538e6fc17df9d469712efe98b380`
- PACKAGE_STATUS=READY_FOR_REVIEW · REVIEW_SUBJECT_ALIGNMENT=PASS ·
  EVIDENCE_AUTHORITATIVE=true

## Item status

| Item | Status | Reason |
|------|--------|--------|
| Commit A — gate verdict | done | own commit, first action |
| Commit B — Built State | done | pushed; pre-zip HEAD |
| Preconditions | done | raw below |
| Evidence job | done | attempt 1 FAILED and was deleted; attempt 2 clean |
| Review zip | done | READY, all three flags green |
| Commit C — STATUS + state | done | last commit on the branch (A4) |
| PR #153 finalize | done | `gh pr ready` + `gh pr edit`; NOT merged |

## External actions taken

| Action | Detail |
|--------|--------|
| Pushed Commit B | `git push` → `3b257f6..8e87006` |
| Pushed Commit C | `git push` → `8e87006..<Commit C sha>` |
| `gh pr ready 153` | draft → ready for review |
| `gh pr edit 153 --title --body` | closure description applied |

No merge. No STATUS edit before the zip existed. Evidence dir committed only
in Commit C, after the READY zip was built (F147 lesson).

## Commits in the closure range

**29335a2** chore(f047): persist gate verdict; open closure

| File | +/- |
|------|-----|
| .agent/live_review.md | +19 / −1 |

**8e87006** docs(f047): built state in the feature file

| File | +/- |
|------|-----|
| docs/roadmap/features/T1_F047.md | +159 / −0 |

**Commit C** chore(f047): close F047 — STATUS line, evidence job, review package

| File | +/- |
|------|-----|
| docs/roadmap/STATUS.md | +1 / −1 (one line, proven by `git diff --numstat`) |
| .agent/plan.md | rewritten — checklist complete |
| .agent/handoff.md | rewritten — this file |
| remedy-review-20260727-101857-READY_FOR_REVIEW.zip | added |
| .data/evidence_exports/29fbc2fe-…/** | added (force-added; ignored path) |

## Byte-identity proofs (reviewer-authored text applied verbatim)

    ### PROOF 1 — verdict text byte-identical
    authored block present verbatim in live_review.md: True
    authored bytes: 1112  sha256: f25d1097aab34e89d69b011dd11bc657

    ### PROOF 2 — LAST_REVIEWED_SHA header
    4:LAST_REVIEWED_SHA: 3b257f6

    ### PROOF 3 — STATUS line byte-identical
    authored STATUS line present verbatim: True
    authored bytes: 384

    ### PROOF 4 — the five authored risks, substring-checked in the Built State
      OK   1 unknown live worktree head proceeds
      OK   1 documented + tested / copy-mode
      OK   2 job.metadata["checkpoint_error"] + warning log
      OK   3 xdist nondeterminism pre-existing F135/F052
      OK   4 docs/resume.md absent, BACKLOG gap item, not created at closure
      OK   5 integrity check live_review_verdict matcher warn, F046 backlog

    $ git diff --numstat docs/roadmap/STATUS.md
    1	1	docs/roadmap/STATUS.md

## Preconditions (raw)

    $ python3 -m apps.cli.main integrity check --json
    {
      "version": 1,
      "passed": true,
      "fail_count": 0,
      "check_count": 5,
      "checks": [
        { "name": "handler_import",     "status": "pass", "message": "handlers=308" },
        { "name": "live_review_verdict","status": "warn", "message": "no verdict found" },
        { "name": "plan_consistency",   "status": "pass", "message": "unchecked=2, context_complete=False" },
        { "name": "relevant_untracked", "status": "pass", "message": "untracked=0, relevant=0" },
        { "name": "high_blockers_open", "status": "pass", "message": "no open blocker/high findings" }
      ]
    }
    exit 0

    $ git status --short
    (no output — clean)

    $ git log --oneline -1
    8e87006 docs(f047): built state in the feature file

    $ git status -sb
    ## feature/f047-checkpoint-resume...origin/feature/f047-checkpoint-resume

`live_review_verdict` "no verdict found" is the known matcher warn (carried
risk 5, F046 backlog item) — `passed` is still true, so it does not block.
`plan_consistency unchecked=2` was the integration-gate and closure boxes,
both ticked in Commit C.

## Evidence job — BOTH attempts, raw

### Attempt 1 — FAILED, directory DELETED, never patched

Job id `62c47842-1765-4ce5-b8bf-fee93166e5e6`. Producer ran and wrote 27
entries, but the gate matrix refused it:

    gate_matrix ok      : False
    blocking_reasons    : ['final_verifier_report.json test_status.passed cannot be
                           confirmed: the VerificationTests total is missing or invalid',
                           'verification_tests.json runs[0] output_hash does not match
                           sha256(stdout_summary)',
                           'verification_tests.json runs[1] output_hash does not match
                           sha256(stdout_summary)',
                           'verification_tests.json runs[2] output_hash does not match
                           sha256(stdout_summary)']

ONE root cause: the validator requires `output_hash == sha256(stdout_summary)`,
and the first attempt hashed the full stdout while `stdout_summary` held only
the last line. The `final_verifier` message cascades from it —
`ctx["vt_passed"]` is None whenever verification_tests.json has any problem.

Fix: `stdout_summary` now IS the real stdout (all three runs are far under the
4000-char `_VT_MAX_STDOUT` cap, asserted in the builder) and `output_hash`
covers exactly those bytes. Directory deleted with `rm -rf`, confirmed gone,
tree clean. Nothing was patched in place.

### Attempt 2 — clean

    HEAD      = 8e870062feb3487f890232d659ef569cf3aa326e
    BASE_FULL = 89c4ef0e723f89c58956de3964d1653461d273b9
    vr-0001: exit=0 passed=72 failed=0 nodes=72 dur=0.442s  hash=25549f392db1b616…
    vr-0002: exit=0 passed=7  failed=0 nodes=7  dur=1.189s  hash=3a10d5caa7d5558a…
    vr-0003: exit=0 passed=42 failed=0 nodes=42 dur=14.847s hash=fd1fa19af4d2cf7b…

    authority set (11):
        apps/cli/command_catalog.py
        apps/cli/commands/job.py
        docs/roadmap/STATUS.md
        docs/roadmap/features/T1_F047.md
        packages/orchestration/checkpoints.py
        packages/orchestration/config.py
        packages/orchestration/long_run_executor.py
        packages/orchestration/worktrees.py
        tests/orchestration/test_checkpoints.py
        tests/orchestration/test_resume_cli.py
        tests/orchestration/test_resume_kill.py

    partition == authority set: OK

    job_id       = 29fbc2fe-60d6-4bb2-a7bb-05dc59dd40d7
    evidence_dir = .data/evidence_exports/29fbc2fe-60d6-4bb2-a7bb-05dc59dd40d7

    === producer summary ===
    { "authority_count": 11, "commit_count": 17,
      "head_commit": "8e870062feb3487f890232d659ef569cf3aa326e",
      "job_id": "29fbc2fe-60d6-4bb2-a7bb-05dc59dd40d7",
      "manual_completion": true,
      "operator_attested_tasks": ["T001", "T002", "T003"],
      "partition": { "T001": 4, "T002": 4, "T003": 3 },
      "total_passed": 121, "verdict": "PASS_WITH_RISKS" }

    gate_matrix ok      : True
    blocking_reasons    : []
    gate_verdicts       :
        artifact_contract_gate.json      PASS
        change_provenance_gate.json      PASS
        commit_execution_gate.json       NEEDS_HUMAN_APPROVAL
        final_verifier_report.json       PASS_WITH_RISKS
        fresh_evidence_gate.json         PASS
        manifest_integrity.json          ok=true
        postmortem_integrity.json        ok=true
        runtime_integration_gate.json    PASS

**Verification runs** are v1.1.0 with exactly the 14 fields, ids matching
`^vr-\d{4,}$`, node_ids collected via `pytest --collect-only -q` with
`selected == len(node_ids)` asserted in the builder, full-length SHAs, and no
`base_commit` inside the runs. Each was executed fresh and its real stdout
hashed.

**Task partition** was derived from `resolve_review_subject(".", "89c4ef0")`
filtered by `is_attestable_source`, and asserted equal to the authority set
BEFORE the producer call (the assert is in the builder, not a post-hoc check).
**Stated openly:** T003 is the docs-carrying slice — it holds
`tests/orchestration/test_resume_kill.py` plus BOTH closure docs,
`docs/roadmap/STATUS.md` and `docs/roadmap/features/T1_F047.md`. STATUS.md is
in the authority set at Commit B because the setup commit already moved its
F047 line from `[ ]` to `[~]`.

## Review zip (raw)

    $ git status --short          # clean, Commit B pushed
    $ bash scripts/make_review_zip.sh --evidence-dir .data/evidence_exports/29fbc2fe-60d6-4bb2-a7bb-05dc59dd40d7
    UNCHANGED: runtime_integration_gate.json — rebuilt from source; identical to existing
    Evidence refresh completed for staged copy.
    Observability index generated from staged bytes: evidence/current/self_run_observability_index.json
    {"member_count": 1468, "authoritative_count": 11, "symlink_count": 0,
     "tombstone_count": 0,
     "final_path": "remedy-review-20260727-101857-READY_FOR_REVIEW.zip",
     "final_sha256": "b6f96e888d7e8a6d5494f213b845a644be34538e6fc17df9d469712efe98b380",
     "publication_capability": "SUPPORTED", "package_status": "READY_FOR_REVIEW",
     "evidence_authoritative": true, "review_subject_alignment": "PASS",
     "manifest_sha256": "ba33c1b306c2b0f9368cd3a2719e48087d50ce980ab9d820a66532764a0e258e"}

    ============================================
    REVIEW_PACKAGE_CREATED=true
    PACKAGE_STATUS=READY_FOR_REVIEW
    PACKAGING_CWD=/home/decodeux/Repos/remedy
    EVIDENCE_DIR=.data/evidence_exports/29fbc2fe-60d6-4bb2-a7bb-05dc59dd40d7
    REVIEW_SUBJECT_ALIGNMENT=PASS
    EVIDENCE_AUTHORITATIVE=true
    ZIP_PATH=/home/decodeux/Repos/remedy/remedy-review-20260727-101857-READY_FOR_REVIEW.zip
    ============================================
    8.0M  remedy-review-20260727-101857-READY_FOR_REVIEW.zip
    Included files: 1468
    Branch: feature/f047-checkpoint-resume
    Commit: 8e870062feb3487f890232d659ef569cf3aa326e
    exit 0

SHA-256 **re-run, not copied**:

    $ sha256sum remedy-review-20260727-101857-READY_FOR_REVIEW.zip
    b6f96e888d7e8a6d5494f213b845a644be34538e6fc17df9d469712efe98b380  remedy-review-20260727-101857-READY_FOR_REVIEW.zip

`committed_review_subject` read back OUT of the built zip
(`.review_zip_manifest.json`):

    base_commit    : 89c4ef0e723f89c58956de3964d1653461d273b9
    head_commit    : 8e870062feb3487f890232d659ef569cf3aa326e
    base_is_ancestor: True
    commit_count   : 17
    file_count     : 15
    tombstones     : []
    package_status : READY_FOR_REVIEW

It spans `89c4ef0..8e87006` (Commit B) exactly as required.

## Canary — fresh, after the STATUS edit

    $ python3 -m pytest tests/cli/test_golden_path.py -q
    42 passed in 14.86s
    exit 0

## Runtime actuals (observed only)

| Metric | Value |
|---|---|
| Rounds | 4 (Setup+T001+T002 · R-0146 repair+T003 · integration gate · closure) |
| Findings | 1 (R-0146, Medium) — Resolved |
| Verdicts | Round 2 PASS · Integration gate PASS |
| Production files changed | 5 (checkpoints.py new, long_run_executor.py, config.py, worktrees.py, job.py, command_catalog.py) |
| Tests added | 79 (test_checkpoints 37, test_resume_cli 35, test_resume_kill 7) |
| Provider calls | 0 — zero-provider feature |
| Tokens / cost | not-measured; token truth is `character_heuristic` |
| Models | none invoked |

## Notes for the reviewer

- Zero F047-attributable regressions at the gate. The one gate finding was in
  an F047-authored state file and was fixed by MEETING the contract, not by
  editing the test.
- `commit_execution_gate` is NEEDS_HUMAN_APPROVAL by design — the final
  verifier verdict is PASS_WITH_RISKS, which is what the closure line records.
- The five carried risks live in the Built State section of
  `docs/roadmap/features/T1_F047.md`, byte-checked above.
- `docs/resume.md` was deliberately NOT created at closure: the gap spans
  commands beyond F047 and belongs in the BACKLOG, not in this feature's diff.
- PR #153 is ready and NOT merged.
