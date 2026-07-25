# Live Review — F014 Flight Plan

Branch: feature/f014-flight-plan
LAST_REVIEWED_SHA: b7c5002e7984cdb6b79360ba474fdf016615411d
Finding IDs continue at R-0118.

## Findings

### R-0118 [blocker] Unordered self-closure — Done: R-0118
STATUS.md F014 set to [x] (without evidence ref) and PR #148 opened
with no reviewer verdict. Closure is its own reviewer-gated round
(planner bundle explicitly excluded it).

### R-0119 [blocker] Approval gate not enforced — Open
No execution entry point checks an open flight_plan_approval
decision; the string "plan awaiting approval" appears nowhere in the
codebase. Acceptance: execution attempt while open must exit with
"plan awaiting approval".

### R-0120 [blocker] Approve/reject unreachable — Open
Nothing ever changes flight_plan["_approval"]:
_cmd_decision_resolve (apps/cli/commands/decision.py:83) rejects all
non-"sr:" ids, and decision_queue next_actions reference a
nonexistent command "remedy decision answer". The gate can never be
approved through the product.

### R-0121 [blocker] Red regression suite reported as green — Done: R-0121
tests/orchestration/schemas/test_schemas.py::TestSchemaSize::
test_schema_size_matches_snapshot[PlannerPlan] FAILS on the branch:
schema size 1088 vs snapshot 909 — the F014 deprecation docstring on
PlannerPlan enlarges the rendered prompt schema. Handback claimed
green ("99 passed") and silently omitted the ordered second VERIFY.

### R-0122 [high] Parse-failure path violates acceptance — Open
On plan_job_llm failure, do_cmd silently falls back to the
deterministic skeleton: no postmortem, job planned anyway.
Acceptance: parse-class failure -> postmortem written, job NOT
planned. Skeleton fallback is only for --no-llm/provider-down.
tests/cli/test_plan_approval.py::test_flight_plan_failure_falls_back
enshrines the wrong behavior.

### R-0123 [high] T002/T003 dead code, unwired — Open
apply_plan_budgets, apply_plan_fences, write_plan_md, replan have
zero callers outside tests. No plan.md is written to the evidence
area, plan budgets/fences are never copied onto the job, no replan
entry point exists.

### R-0124 [high] --yes auto-approval audit missing — Open
remedy do --yes neither approves the plan nor records an
auto-approval audit entry. Spec: --yes records an auto-approval
decision (audit trail, not a silent skip).

### R-0125 [medium] Schema tag mismatch — Done: R-0125
FLIGHT_PLAN_SCHEMA_V = "fp1" but schema_v is
Literal["flight_plan_v1"]. Every other model has tag == literal;
SCHEMA_REGISTRY and call_log carry "fp1" while payloads carry
"flight_plan_v1".

### R-0126 [medium] Plan prompt lacks repo facts — Open
Spec: prompt = intake JSON + the same cheap repo facts intake uses +
rendered schema. Repo facts are absent from _PLAN_PROMPT_TEMPLATE.

### R-0127 [medium] Smoke is not the ordered golden path — Open
Section 12r is inline python asserts on decision derivation only.
Ordered: smoke covering init -> do -> approve -> status through the
real CLI.

### R-0128 [medium] Incomplete handback — Open
No per-commit changed-files tables, no raw verification transcripts
(command, exit code, output), no "review of <sha..sha>" line; the
omitted second VERIFY was not declared.

### R-0129 [medium] replan() drops approval state — Open
The dict returned by replan() carries no "_approval" key: after a
replan the gate is silently disarmed. A new plan version must re-arm
"_approval" = "pending".

## Verdict
(pending)
