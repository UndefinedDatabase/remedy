# Handoff — latest worker state (rewrite, never append)
Feature: split-workflow-v3-evidence-repair (no feature ID — infra repair)
Round: 1 (single round)
Branch: feature/split-workflow-v3-evidence-repair
Base: 48952c7 (main after PR #136 merge)
Last commits: 72654ef, a6a5c3a, 01e2018, bd93397

Changed files:
| File | Change |
|---|---|
| docs/agents/planner_reviewer_prompt.md | replaced with v3 content |
| docs/agents/split_workflow.md | replaced with v3 content |
| docs/roadmap/STATUS_closure_protocol.md | replaced with v3 + canonical zip sequence |
| docs/README.md | v1→v3 in split_workflow description |
| .agent/handoff.md | created (initial → current state) |
| scripts/make_review_zip.sh | stale plan cleanup + deprecated fallback→warning |

Verification:
  zip build (no evidence): PASS — remedy-review-20260723-161744-NO_EVIDENCE.zip
  SHA-256: af47e29f19b09804e4c58f8a1f75277482a0637c0bd3c3a3ce869f7553fb6dd8
  zip build (old f017 evidence): expected FAIL — Content Proof mismatch (correct)
  deprecated fallback: PASS — warns, ignores, proceeds as code-only

Open findings: 0
Next expected: Window 1 reviews 48952c7..HEAD, then operator decides PR merge
(Rules: rewritten at every handback; only the latest state lives here;
git history is the archive; ≤60 lines.)
