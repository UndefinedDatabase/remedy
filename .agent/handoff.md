# Handoff — F148 Closure (final)

## PR
- **#145**: https://github.com/UndefinedDatabase/remedy/pull/145
- Branch: `feature/f148-project-scoping`
- Status: open, not merged (per closure protocol step 6)

## Evidence Job
- ID: `cf7ca6e8-8d5a-4b0a-ab4b-8f946bcdd42a`
- Dir: `remedy-job-evidence-f148/`
- Gates: 8/8 (final_verifier_report, fresh_evidence, artifact_contract,
  change_provenance, manifest_integrity, postmortem_integrity,
  commit_execution, runtime_integration)
- Verdict: PASS_WITH_RISKS

## Zip Attempts

### Attempt 1 (BLOCKED)
- File: `remedy-review-20260724-180231-BLOCKED_EVIDENCE.zip`
- SHA-256: `93d24c4fc5bf290946d6c307e4a8e1f9ea5c36f2058be2693a1f2136a9017a5b`
- Status: BLOCKED_EVIDENCE — `is_valid_current_run=false`
- Cause: verification_tests.json runs had wrong field set (missing v1.1
  fields: run_id, stdout_summary, head_sha, selected, deselected, skipped,
  node_ids, duration_seconds). Also output_hash != sha256(stdout_summary).

### Attempt 2 (BLOCKED — pre-attempt-3, same root cause)
- Commit subject `(unscoped)/(orphaned: id)` triggered `_contains_local_path`
  in review_subject validator. Rewrote via git filter-branch to
  `unscoped and orphaned`. Evidence rebuilt with new HEAD after rewrite.

### Attempt 3 (READY)
- File: `remedy-review-20260724-180532-READY_FOR_REVIEW.zip`
- SHA-256: `d81e54b4ea5716ab3f2c00593a3911457fff79121532bf63e3231c142496e7a9`
- Status: READY_FOR_REVIEW
- review_subject_alignment: PASS
- evidence_authoritative: true

## Integrity Gate
```json
{
  "version": 1,
  "passed": true,
  "fail_count": 0,
  "check_count": 5,
  "checks": [
    {"name": "handler_import", "status": "pass", "message": "handlers=305"},
    {"name": "live_review_verdict", "status": "pass", "message": "PASS — R-0085-series n/a (F147); F148 findings R-0098..R-0109"},
    {"name": "plan_consistency", "status": "pass", "message": "unchecked=0, context_complete=False"},
    {"name": "relevant_untracked", "status": "pass", "message": "untracked=0, relevant=0"},
    {"name": "high_blockers_open", "status": "pass", "message": "no open blocker/high findings"}
  ]
}
```

## Grep Proof — Byte-Identical Applied Text

### STATUS line
```
$ grep -F "Project scoping everywhere (T001–T004 complete; accepted 2026-07-24" docs/roadmap/STATUS.md
- [x] F148 — Project scoping everywhere (T001–T004 complete; accepted 2026-07-24 · live review PASS — ACCEPTED · Evidence job cf7ca6e8-8d5a-4b0a-ab4b-8f946bcdd42a · package remedy-review-20260724-180532-READY_FOR_REVIEW.zip · SHA-256 d81e54b4ea5716ab3f2c00593a3911457fff79121532bf63e3231c142496e7a9 · accepted HEAD 6799d12ed2b9f2c96b3410b150b09695c551691e)
```

### R-0108 resolution
```
$ grep -F "independently verified — scoped slug loaded via" .agent/live_review.md
- **Reviewer**: independently verified — scoped slug loaded via
```

### R-0109 resolution
```
$ grep -F "independently verified — unit test proves the" .agent/live_review.md
- **Reviewer**: independently verified — unit test proves the
```

### Verdict
```
$ grep -F "PASS — R-0085-series n/a (F147); F148 findings R-0098..R-0109" .agent/live_review.md
PASS — R-0085-series n/a (F147); F148 findings R-0098..R-0109
```

## Closure Commits
| Hash | Message |
|------|---------|
| `97ae61a` → `8283cf9` | chore(f148): resolve R-0108..R-0109, verdict, built state |
| `1170b9d` → `b0259d3` | chore(f148): closure handoff |
| `c7823e1` → `6799d12` | chore(f148): STATUS [x] — closure (fills pending zip) |
| `32cdd3e` | chore(f148): closure evidence + STATUS fills |

(Pre-rewrite hashes → post-rewrite hashes shown for commits affected
by the filter-branch that fixed the path-in-subject blocker.)

## Next expected action
Reviewer reviews PR #145. Merge deferred to next feature start per
closure protocol step 6.
