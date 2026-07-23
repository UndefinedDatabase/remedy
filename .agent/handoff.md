# Handoff — latest worker state (rewrite, never append)
Feature: split-workflow-v3-evidence-repair (infra repair, no feature ID)
Round: 3 (final — all findings resolved)
Branch: feature/split-workflow-v3-evidence-repair
Base: 48952c7 (main after PR #136 merge)
Last commits: e2a26bf, f5215a6, f4302ef, this commit

Changed files (full branch):
| File | Change |
|---|---|
| docs/agents/planner_reviewer_prompt.md | v3 content |
| docs/agents/split_workflow.md | v3 + zip-last ordering |
| docs/roadmap/STATUS_closure_protocol.md | v3 + build-order rule + NO_EVIDENCE clause |
| docs/README.md | v1→v3 description |
| docs/system/agent-tooling-audit.md | R-0076 annotation |
| scripts/make_review_zip.sh | stale plan cleanup, deprecated fallback→warning |
| .agent/handoff.md | rewritten each handback |
| .agent/review_protocol.md | zero-write reviewer model (R-0072) |
| .agent/plan.md | full scope |
| .agent/live_review.md | R-0071..R-0076 all Resolved |
| .agent/decisions.md | /build-remedy + legacy subagent decisions |
| .claude/commands/build-remedy.md | Window 1 bootstrap command |
| .claude/README.md | updated contents |
| AGENTS.md | Audience + handoff sections |

Verification:
  zip (round 3, clean tree): remedy-review-20260723-171817-NO_EVIDENCE.zip
  SHA-256: 0031af3154c63e4e846404cefc1d4e76f835eac12db24b3ed0356e6172e78b5a
  manifest dirty_file_count_total: 0
  handoff in zip: round 3 (current)

Open findings: 0
Resolved: R-0071, R-0072, R-0073, R-0074, R-0075, R-0076
Next expected: merge infra PR, then Part C (README redesign)
(Rules: rewritten at every handback; only the latest state lives here;
git history is the archive; ≤60 lines.)
