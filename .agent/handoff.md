# Handoff — latest worker state (rewrite, never append)
Feature: split-workflow-v3-evidence-repair (infra repair, no feature ID)
Round: 2 (finalization after R-0071..R-0074)
Branch: feature/split-workflow-v3-evidence-repair
Base: 48952c7 (main after PR #136 merge)
Last commits: 453285c, 219dd32, 3708792 + this commit

Changed files:
| File | Change |
|---|---|
| docs/agents/planner_reviewer_prompt.md | v3 content |
| docs/agents/split_workflow.md | v3 content |
| docs/roadmap/STATUS_closure_protocol.md | v3 + canonical zip sequence + NO_EVIDENCE clause |
| docs/README.md | v1→v3 in split_workflow description |
| scripts/make_review_zip.sh | stale plan cleanup, deprecated fallback→warning |
| .agent/handoff.md | rewritten (R-0071 proof) |
| .agent/review_protocol.md | title + wording aligned with zero-write model (R-0072) |
| .agent/plan.md | rewritten to full scope (R-0073) |
| .agent/live_review.md | R-0071..R-0074 persisted + Done markers |
| .agent/decisions.md | /build-remedy + legacy subagent decisions |
| .claude/agents/remedy-reviewer.md | deleted (R-0074) |
| .claude/commands/build-remedy.md | new — Window 1 bootstrap command |
| .claude/README.md | updated contents list |
| AGENTS.md | Audience section, handoff.md section, handoff trigger |

Verification:
  zip (round 2): remedy-review-20260723-165711-NO_EVIDENCE.zip
  SHA-256: f8030e0efb0420e9869cf7deaf3afd26eed16e556d2b283a8c6444a6cfcd7f50
  deprecated fallback: warns, ignores, proceeds as code-only

Open findings: 4 (R-0071..R-0074, all with Done markers, awaiting reviewer resolution)
Next expected: Window 1 reviews bd93397..HEAD
(Rules: rewritten at every handback; only the latest state lives here;
git history is the archive; ≤60 lines.)
