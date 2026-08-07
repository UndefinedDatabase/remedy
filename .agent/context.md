# Context — F080 machine-readable roadmap mirror (R3, closure part 1)

## Active Branch
feature/f080-roadmap-mirror — R2 PASS with the integration gate and the
full suite green (LAST_REVIEWED_SHA 84cd2797), cut from main 1da1b07a.
No PR yet: the closure PR is R4's, and it merges at the next feature's
Open PR Gate.

## Scope
F080 R3, closure part 1 per docs/roadmap/STATUS_closure_protocol.md:
persist the R2 verdict, route R-0205's class to T2_F083, append the
Built State to docs/roadmap/features/T1_F080.md (precondition 4),
re-confirm preconditions 1-5, then the evidence job and the fresh review
zip. T001-T003 are landed and unchanged; no product code changes here.

## Constraints
- NOT this round: the STATUS.md [x] edit, the README capability sync
  and the PR. They are R4's single closure commit (Rule A4, R-0154).
- The evidence dir is NEVER committed (closure DECISION 2026-08-01) —
  it lives in session scratch, outside the repo, or the package builds
  BLOCKED_EVIDENCE (F147 attempt-2 lesson).
- The zip is built from a CLEAN tree after all content commits; a
  package built from a dirty tree is invalid. A failing zip build is a
  closure BLOCKER: record the raw error and hand back.
- Evidence producer is create_manual_completion_bundle with
  review_feature_id="f080" — write_runtime_integration_gate alone is
  not a bundle. Producer pitfalls are satisfied at authoring time:
  sha256-hex output_hash, full-length base_commit, non-empty node ids
  with len(node_ids) == selected, test_files that are files not
  directories, VerificationTests run_id matching ^vr-\d{4,}$.
- STATUS.md semantics stay human-owned (A4); no generated artifact is
  ever committed.
- Test runner is pytest; this round re-runs only the scoped
  precondition suites (tests/docs/, tests/cli/test_golden_path.py,
  tests/ui_server/test_dashboard_contract.py,
  tests/regression/test_resource_safety.py). The full `-n auto` gate
  already PASSed in R2 and is re-confirmed from its raw transcripts.

## Steps
Verdict + R-0205 routing (Part A) → Built State (Part B) →
preconditions 1-5 (Part C) → evidence job + fresh zip (Part D) → push +
handoff rewrite carrying the zip name, SHA-256, evidence job id and the
full accepted-HEAD sha for R4.
