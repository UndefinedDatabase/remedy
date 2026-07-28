# Plan — F251 closure round (protocol v3)

## Goal
Close F251 per STATUS_closure_protocol.md v3 under Ruling A: evidence
job, fresh READY review zip, authored STATUS line, PR into main (NOT
merged — the next feature's Open PR Gate merges it).

## Checklist
- [x] Commit A: R5 verdict persisted (f251-r5-1, sha256 + cmp 0) — b375b32
- [x] Commit B: Built State in docs/roadmap/features/T1_F251.md —
      ACCEPTED_HEAD = ab2258933944cd3ab3280646d1aa00fb062ecb36
- [x] Preconditions: porcelain empty · integrity check --json passed=true,
      fail_count=0 (live_review_verdict warn = known matcher backlog)
- [x] Evidence job 1cadf9c8-0052-4fe8-91a9-efe08c315a00 — 8 green runs,
      683 passed, evidence_authoritative=true, is_valid_current_run=true,
      0 issues, validated BEFORE packaging. create_manual_completion_bundle(
      review_feature_id="f251", ...) — sha256-hex output_hash from
      the stored stdout_summary, full-length base_commit, node_ids
      from the same selection (F048 pitfalls)
- [x] Review zip: READY_FOR_REVIEW on attempt 3; attempts 1 and 2
      failed and are recorded in the handback, not hidden
- [x] Commit C (LAST, A4): authored STATUS line, four slots filled,
      blank-back byte-proof green + evidence dir + final .agent state
- [ ] PR into main created, NOT merged; description: what/why, key
      decisions incl. Ruling A, changed-files table, verdict, open
      findings 0, runtime actuals (models not-measured)

## Current Step
PR into main (NOT merged). Closure complete otherwise.

## Risks
- The D4 ids read live .agent files; their state at evidence time is
  recorded as observed, never adjusted (F252 item 7).
- No D-class edits; the 154-catalog baseline stays untouched.
- Ledger and pin: no feature-file or STATUS count changes this round
  beyond the [~]→[x] swap (line count unchanged).
- The churn-gate runs (154 failures each) are NOT in verification_runs:
  the producer refuses any run with exit_code != 0. They are evidence of
  churn-freedom, recorded in .agent/f251_baseline/ and Built State, not
  a green-suite claim.
