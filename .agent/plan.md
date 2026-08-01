# Plan — paydown-0801 (single-session micro-round)

## Goal
Close the closure-candidate carry gap structurally (disk vehicle
.agent/candidates.md) and settle the two F056 candidates that were
dropped (evidence-protocol drift; PR-number reporting). Operator
ruling 2026-08-01, F056-candidate loss. Change set: docs/roadmap/**,
docs/agents/**, .agent/** only — micro-round scope per
planner_reviewer_prompt.md §3.

## Current Step
Apply authored texts paydown0801-r1-1..7 (committed under
.agent/authored/, sha256-verified):
1. STATUS_closure_protocol.md — disk-vehicle rule in
   Closure-candidate findings (r1-1); build-order sentence (r1-2);
   evidence-dir block rewritten to "not committed" (r1-3).
2. planner_reviewer_prompt.md §1 — bootstrap step 4 reads
   .agent/candidates.md (r1-4).
3. handback_template.md — External actions carries the PR number
   (r1-5).
4. Create .agent/candidates.md empty carrier (r1-6).
5. Append the three DECISIONs to .agent/decisions.md (r1-7).

## Next Steps
- Gates: python3 -m pytest tests/docs/ -q + canary
  tests/cli/test_golden_path.py -q.
- Handback per handback_template.md, label single-session
  micro-round; push; PR; merge on PASS (standing approval).
- Then F062 per Rule A5 (fresh Window-1 session bootstrap).

## Risks
Docs-structure pins in tests/docs/ could trip on wording; gate
catches it. No production code touched.
