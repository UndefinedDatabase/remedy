# Handback — Amendment round amend0805-v3

## Round
Operator-relayed amendment amend0805-v3 (replaces amend0804 v1/v2 —
neither ran). Boundary-agnostic, before F079's claim; NOT a feature
claim, candidates block condition did not fire. Single-session per §3.
Docs/planning only — no product code, no order/template edits.

## Branch
feature/amend0805-v3 (from main after PR #179 merge at Open PR Gate).

## Commits
| SHA | Scope | Files |
|---|---|---|
| d6409c15 | Part B roadmap | STATUS.md, T2_F254.md (new), T12_F253.md, T17_F243.md, T2_F103.md, plan.md |
| e8deb6a6 | Part C reviewer rule | docs/agents/reviewer_conventions.md |
| e4ecd200 | Part D doc drift | scripts/self_run_gauntlet.py, packages/providers/claude_agent/__init__.py |
| a155a886 | Part E workflow | docs/agents/planner_reviewer_prompt.md, .agent/candidates.md |

## Item status
| Item | Status | Reason |
|---|---|---|
| B1 | done | F254 registered in Tier 2 (before F086) + T2_F254.md per F080 grammar |
| B2 | done | MCP facet section appended to T12_F253.md |
| B3 | done | Proof-or-Stop benchmark candidate appended to T17_F243.md |
| B4 | done | Milestone R1 line after Tier 2 heading |
| B5 | done | credit-pool scope note appended to T2_F103.md |
| C1 | done | specified-route-exercised rule added; relationship note below |
| D1 | done | preflight paragraph now matches SUPPORTED_INJECTIONS (none blocked) |
| D2 | done | Step 33+ wording replaced with roadmap + pingpong_provider reference |
| E1 | done | Laufzeit row + definition; grep found no .claude/commands restatement |
| E2 | done | R-0199 operator-priority HIGH note appended |

All presence checks came back ABSENT; no SKIPPED(present), no
ANCHOR-DRIFT.

## C1 relationship (record per order)
C1 is the reviewer-practice HALF of the first closure candidate in
.agent/candidates.md (F070/R-0184). The gate-tooling half — closure
evidence proving a specified verb was CALLED — stays with that
candidate for F079 R1 to order. The candidate's landing should cite
the new reviewer_conventions.md rule.

## Verification
- tests/orchestration/test_self_run_gauntlet.py: 21 passed (D1 is
  docstring-only; no behavior change).
- grep: "Three of the four" and "Bis zum Self-Run" gone repo-wide.
- Out-of-scope drift observed, NOT touched: docs/system/
  architecture.md:2481 restates the stale "(Step 33+)" wording for
  claude_agent — candidate for a future hygiene item.

## Next expected action
F079 (Context handoffs) per Rule A5, fresh session. Its first
reviewed round must empty .agent/candidates.md (4 entries, R-0199
now marked operator-priority HIGH). ADR-0001 still awaits a human.
