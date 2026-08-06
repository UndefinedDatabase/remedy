# Live Review — F079 Context handoffs (Tier 1)

Branch: feature/f079-context-handoffs
Scope: handoff artifact (handoff.json + rendered handoff.md) composed
from dossier, checkpoint reference, open decisions and next intent;
triggers + loop consumption; measured recall eval. The F075 candidate
sweep (4 entries) is registered/resolved in R1 per
docs/roadmap/STATUS_closure_protocol.md ("Closure-candidate findings").

## Steps
- R1 (SPLIT, LARGE): Open PR Gate (#180) + STATUS claim + candidate
  sweep + R-0199 measured diagnosis + reuse inspection + T001 (schema
  + composer + idempotence + unit tests). Awaiting handback.
- R2 (planned): T002 triggers + loop consumption + reference
  verification; R-0199 fix order once the diagnosis numbers are in.
- R3 (planned): T003 boundary recall eval + threshold. Then the
  integration gate round, then closure (its own round, never bundled).

## Findings
- R-0199 (harness perf, Medium — carried from F075, ID spent there):
  the attempt-03 campaign read ~872 GB while writing ~2 MB.
  Hypothesis, unverified: gauntlet_runner.data_root_digest full-scans
  the operator's real data root before and after every run. Operator
  priority HIGH. R1 orders the MEASURED diagnosis (raw numbers in the
  handback); the fix order follows in R2 on those numbers.
- R-0200 (process/gate-tooling, Medium) 2026-08-06, registered from
  candidates: F070 was accepted with a specified execution step
  unbuilt — its zero-provider closure evidence never proved the
  specified verb was CALLED. The reviewer-practice half is landed
  (docs/agents/reviewer_conventions.md, specified-route-exercised
  rule, amend0805-v3). The gate-tooling half (closure evidence proves
  a specified verb actually ran) stays OPEN here. DECISION: deferred —
  no build inside F079 scope (alternatives considered: build it now —
  rejected as scope creep; drop it — rejected, the F070 gap was real).
  Reversal: any later relay may order the build; if unbuilt at F079
  closure it rolls to candidates per protocol.
- R-0201 (roadmap routing) 2026-08-06, resolved from candidates: the
  move schema has no resume kind — a paused job's only forward path is
  re-dispatch, and a job that ended max_cycles_reached cannot be
  continued (F075 R5/R6 evidence). DECISION: routed to F106 — a scope
  note is appended to docs/roadmap/features/T3_F106.md in this round
  (alternative considered: F045 — rejected, loops are declarative
  config, not continuation of interrupted state). Reversal: move or
  reword the note in any later round. Resolved by routing.
- R-0202 (gate tooling, Low) 2026-08-06, registered from candidates:
  the mid-run UI rebuild recurred in the F075 R12 base gate despite
  REMEDY_UI_NO_AUTO_BUILD=1 (same class as R-0169, F069 R2); suspect a
  spawned server/build path not honoring the env var.
  docs/agents/integration_gate.md already carries the operational
  mitigation (dist hash check + per-id attribution). DECISION:
  deferred, OPEN — the env-var hunt is its own ordered round when
  prioritized; rolls to candidates at closure if unbuilt.
- Next free ID: R-0203.

## Verdicts
- (none yet — R1 handback awaited)
