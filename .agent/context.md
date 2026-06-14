# Context

## Active Branch
feature/steps-1275-1304-bounded-overnight-executor-v0 (forked from clean main at
9c59ad1 after PR #55 merged Bounded Overnight Preparation v0). No drift.

## Mainline reconciliation (Step 1275)
- PR #55 MERGED → main. Current main commit: 9c59ad1.
- Bounded Overnight Prep v0 landed: overnight_readiness.py (readiness/plan/report),
  `remedy overnight readiness|plan|report`, capability matrix, stop-reason taxonomy,
  morning checklist, budget/risk summaries, progress/feature/review-bundle/cockpit
  integrations. Default policy report-only. NO executor built. can_run_unattended
  intentionally false in prep v0.
- Last full suite (prep v0): 5470 passed, 8 skipped, 1 deselected.

## Scope
Steps 1275-1304: Bounded Overnight Executor v0 — foreground, explicitly-invoked,
AT MOST ONE bounded reviewable step. Builds on readiness/plan/report from prep v0.

## Carried residual risks
- Review-findings source was explicit-unknown in prep v0 (R-0080). Step 1285 closes
  it for the executor: parse .agent/live_review.md verdict + open finding counts;
  PENDING/FAIL or open blocker/high blocks execution; unknown blocks unattended.
- Executor enabling must NOT ignore review blocker/high findings.
- Provider-backed source repair remains future (no provider this block).
- Fixture repair builder is docs-only by design.
- UI `npm run lint` pre-existing TS parser/dependency blocker (no deps allowed).
- Pre-existing deselected `test_project_brain.py::...::test_full_chain_order`
  (always `-k "not test_full_chain_order"`).

## Executor v0 constraints
- FOREGROUND, explicitly invoked ONLY. No daemon/scheduler/watch/background/loop.
- Default report-only; execution requires --allow-one-cycle + explicit action flag.
- max_cycles == 1; exactly one allowed service action per invocation.
- Allowed actions: inspect/readiness/report; do_continue (approved intent, if
  policy allow_apply/allow_repair_apply); repair_propose (existing FailureArtifact,
  if policy allow_repair_propose). No provider, no auto-approval, no auto-revert,
  no git commit.
- No subprocess/CLI to execute Remedy commands — call central services directly.
- No shell=True. No background pytest.
- Idempotent: retry never double-applies/tests/proposes or duplicates reports.
- Re-validate catalog entry + entity existence + policy + RunContract/permissions
  via the central service that executes; never bypass service gates.
- No raw stdout/stderr/source/diff/artifact-body/secrets/tracebacks/abs paths in
  any public surface (Result/record/CLI/report/Progress/Feature/Review/Cockpit).

## Foundation reused
- overnight_readiness.build_overnight_readiness/plan/report + select_overnight_next_action.
- do_continue.run_do_continue (one safe cycle: snapshot→apply→test→proof→stop; idempotent).
- repair_loop.run_repair_attempt (propose only; idempotent; no apply).
- run_contract (evaluate_run_action/ContractAction), permissions (is_allowed/Capability).
- do_run.validate_next_safe_action_command (catalog-backed check).
- Review Bundle REQUIRED_SECTIONS currently 15; add overnight_run_summary.json → 16.

## Active Constraints
- No shell=True anywhere. No background pytest (scripts/remedy_pytest.sh).
- No destructive Git (reset/checkout/clean/commit/push from executor).
- No automatic repair loop, no multi-cycle, no real provider/Ollama, no UI mutation,
  no browser automation, no MCP activation, no dependency upgrades.
- Do not weaken permission/approval/RunContract/snapshot/test gates.
- Gates live in central services — executor calls them, never reimplements/bypasses.

## Product readiness — Bounded Overnight Executor v0 (Step 1301)
CAN: from an explicit `remedy overnight run <job>` invocation, run one readiness
check, select one catalog+entity-backed safe action, and — only with
`--allow-one-cycle` + an explicit action flag and all gates passing — execute
exactly ONE central-service action (do_continue apply OR docs-only repair propose),
persist an append-only run record + durable per-phase checkpoints, recompute
readiness, and emit a morning report. Foreground; report-only by default.
CANNOT (deferred/by design): no daemon/scheduler/watch/background/multi-cycle loop;
no provider/Ollama; no auto-approval/auto-revert/contract-relax/budget-raise; no
git commit; no source-rewriting repair (fixture builder docs-only); no UI mutation;
no subprocess/CLI for command execution.
Provider still deferred: trust/verification + no-cloud gating not built; source
repair needs a verified provider path first.
Before a real scheduled overnight: a bounded executor LOOP with budget/runtime
caps, provider-backed source repair, and review-findings automation hardening.

## Next block
Provider-backed Repair Builder v0 OR Provider Trust Verification.
