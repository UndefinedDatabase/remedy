# Handback — Amendment round amend0805-v3 (+ repair amend0805-v3-fix)

## Repair round amend0805-v3-fix (2026-08-05)
Cause: B1 registration missed reg0803 ledger-count atomicity (count
pin + README totals move with a registration). One commit, this
branch, PR #180 stays open.
| Edit | File | Change |
|---|---|---|
| 1 | tests/docs/test_docs_consistency.py | TOTAL_FEATURES 253 -> 254, comment lists F254 |
| 2 | README.md:19 | 36 of 253 -> 36 of 254 registered items |
| 3 | README.md tier table | Tier 2 total 13 -> 14 |
| 4 (opt) | docs/system/architecture.md:2481 | stale "(Step 33+)" row reworded to D2's roadmap reference |
Gates: tests/docs 293 passed (was 2 failed/291); test_golden_path.py
42 passed. Both exit 0.
Process note (round record): the amendment round ran only
test_self_run_gauntlet.py while touching docs/roadmap/** — the
docs-round gate rule applies to amendment rounds exactly as to
feature rounds; relayed prompts must list their gates explicitly.

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
