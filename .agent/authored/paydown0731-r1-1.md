# Live Review — Paydown micro-round 2026-07-31 (F052→F053 boundary)

Branch: feature/paydown-0731
Scope: codify the digest fallback for transport proofs and the
practice-requires-pointer rule (planner_reviewer_prompt.md); resolve
the carried VT run_id closure candidate (STATUS_closure_protocol.md);
fix R-0159 (worktree-safe dogfood branch guard) + gate-doc cleanup.
Same-session merge on PASS (standing operator approval, 2026-07-31).

## Steps
- R1: Open PR Gate (#167) → Items 1–3 + candidate pass → gates
  (tests/docs + canary + touched test files) → handback.

## Findings
- Open: R-0159 (process, Low, carried from F052): the 2 ids in
  tests/cli/test_self_dogfood_execution_cli.py cannot pass in ANY
  linked worktree — self_dogfood_execution.current_branch() reads
  Path(".git")/"HEAD", and a worktree's .git is a gitfile pointer,
  so the guard answers main_branch_unsafe/blocked; they land in
  comm -23 on every gate run. Fix: this round's Item 3 (accept both
  .git forms, stdlib-only).
- Open: CANDIDATE (carried from F052 closure, no ID spent): the
  closure protocol's producer-pitfall list lacks the
  VerificationTests run_id shape — `^vr-\d{4,}$`
  (build_review_manifest._VT_RUN_ID_RE); a rejected VT doc yields
  vt_passed = None, failing the final-verifier confirmation.
  Fix: this round's candidate pass (resolve inline as DECISION per
  the STATUS_closure_protocol.md closure-candidate rule).
- Next free ID: R-0160.

## Verdicts
- R1: PENDING (reviewer).
