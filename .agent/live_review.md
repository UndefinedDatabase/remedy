# Live Review — Steps 1573-1608: Expensive Builder Routing v0

Reviewer: parallel reviewer (independent; owns verdict — builder self-report does not set verdict, protocol §5)
Scope: Local-first, budgeted, anti-loop ROUTING/POLICY for when Remedy should use deterministic
logic, local advisory, local candidate generation, or expensive external builder generation.
Routing/policy/planning ONLY. Must NOT: execute any builder/model/provider, call network/
subprocess/cloud/SDK, generate candidates, apply/approve, create Patch Intents/ProposedTasks
directly, create PRs/git, leak raw prompt/response/source/diff/log/secrets/tracebacks/abs paths,
treat model output as truth, recommend external builder without request package + Trust Gate +
Verification + budget + low loop risk + no pending approval/intent, loop on repeated failed
generation, or emit fake next actions. NO PR unless user asks (Step 1608).
Timestamp: 2026-06-15

## Verdict (reviewer-owned)
PENDING — block in progress.

## Check Matrix — to fill
| Check | Status | Note |
|---|---|---|
| 1. Mainline reconciliation (verification PR #64 merged; clean branch; residuals carried) | PASS | off clean main d22e1dd |
| 2. Routing models + tiers + policy (no raw content fields) | PENDING | |
| 3. Routing inputs (safe summaries only; unknown stays unknown) | PENDING | |
| 4. Candidate-generation need detector (suppress on pending/blocker/budget/loop/missing) | PENDING | |
| 5. Local-first decision rules (deterministic→advisor→local-gen→external) | PENDING | |
| 6. Expensive builder justification codes + hard preconditions | PENDING | |
| 7. Budget model (unknown cost blocks external; local≠external) | PENDING | |
| 8. Loop governor (no repeated expensive route without new evidence) | PENDING | |
| 9. Routing selector (exactly one tier / no_safe_route / human_review) | PENDING | |
| 10. Trace persistence (atomic; safe; idempotent by fingerprint) | PENDING | |
| 11. CLI decide/report + catalog + run_contract | PENDING | |
| 12. Orchestrator / local-advisor / verification / self-dogfood integration | PENDING | |
| 13. Progress/Feature/Review-bundle/Cockpit | PENDING | |
| 14. Redaction (no raw in any surface) | PENDING | |
| 15. Architecture guards (no exec/SDK/net/subprocess/apply/approval/PR/intent) | PENDING | |
| (tests) Targeted + full pytest once | PENDING | |
| (handoff) Changed-files table present | PENDING | |

## Findings — Steps 1573-1608
(none yet) — Next id: R-0088.

## Reviewer audit log
- Branch off clean main d22e1dd (PR #64 merged Provider Trust Verification v1; prior block NIT
  _INTENT_OK_RE resolved pre-merge). Prior block zero open findings — nothing to carry.
- Verified: PTV v1 merged to main via PR #64 → main `d22e1dd`; prior-block NIT `_INTENT_OK_RE`
  resolved @ `c29a6bf` (pre-merge). New branch `feature/steps-1573-1608-expensive-builder-routing-v0`
  off `d22e1dd`. `git log d22e1dd..HEAD` empty → no drift, no block code yet. Check 1 PASS.
- Reviewer runs targeted `scripts/remedy_pytest.sh` independently once tests land; relies on
  builder full-suite count for the full run. Reviewer findings beat builder self-report (§5).
