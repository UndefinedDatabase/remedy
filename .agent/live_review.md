# Live Review — F014 Flight Plan

Branch: feature/f014-flight-plan
LAST_REVIEWED_SHA: b7c5002e7984cdb6b79360ba474fdf016615411d
Finding IDs continue at R-0118.

## Findings

### R-0118 [blocker] Unordered self-closure — Resolved (verified by reviewer, round 3)
STATUS.md F014 set to [x] (without evidence ref) and PR #148 opened
with no reviewer verdict. Closure is its own reviewer-gated round
(planner bundle explicitly excluded it).

### R-0119 [blocker] Approval gate not enforced — Resolved (verified by reviewer, round 3)
No execution entry point checks an open flight_plan_approval
decision; the string "plan awaiting approval" appears nowhere in the
codebase. Acceptance: execution attempt while open must exit with
"plan awaiting approval".

### R-0120 [blocker] Approve/reject unreachable — Resolved (verified by reviewer, round 3)
Nothing ever changes flight_plan["_approval"]:
_cmd_decision_resolve (apps/cli/commands/decision.py:83) rejects all
non-"sr:" ids, and decision_queue next_actions reference a
nonexistent command "remedy decision answer". The gate can never be
approved through the product.

### R-0121 [blocker] Red regression suite reported as green — Resolved (verified by reviewer, round 3)
tests/orchestration/schemas/test_schemas.py::TestSchemaSize::
test_schema_size_matches_snapshot[PlannerPlan] FAILS on the branch:
schema size 1088 vs snapshot 909 — the F014 deprecation docstring on
PlannerPlan enlarges the rendered prompt schema. Handback claimed
green ("99 passed") and silently omitted the ordered second VERIFY.

### R-0122 [high] Parse-failure path violates acceptance — Resolved (verified by reviewer, round 3)
On plan_job_llm failure, do_cmd silently falls back to the
deterministic skeleton: no postmortem, job planned anyway.
Acceptance: parse-class failure -> postmortem written, job NOT
planned. Skeleton fallback is only for --no-llm/provider-down.
tests/cli/test_plan_approval.py::test_flight_plan_failure_falls_back
enshrines the wrong behavior.

### R-0123 [high] T002/T003 dead code, unwired — Resolved (verified by reviewer, round 3)
apply_plan_budgets, apply_plan_fences, write_plan_md, replan have
zero callers outside tests. No plan.md is written to the evidence
area, plan budgets/fences are never copied onto the job, no replan
entry point exists.

### R-0124 [high] --yes auto-approval audit missing — Resolved (verified by reviewer, round 3)
remedy do --yes neither approves the plan nor records an
auto-approval audit entry. Spec: --yes records an auto-approval
decision (audit trail, not a silent skip).

### R-0125 [medium] Schema tag mismatch — Resolved (verified by reviewer, round 3)
FLIGHT_PLAN_SCHEMA_V = "fp1" but schema_v is
Literal["flight_plan_v1"]. Every other model has tag == literal;
SCHEMA_REGISTRY and call_log carry "fp1" while payloads carry
"flight_plan_v1".

### R-0126 [medium] Plan prompt lacks repo facts — Resolved (verified by reviewer, round 3)
Spec: prompt = intake JSON + the same cheap repo facts intake uses +
rendered schema. Repo facts are absent from _PLAN_PROMPT_TEMPLATE.

### R-0127 [medium] Smoke is not the ordered golden path — REOPENED — see R-0131
Section 12r is inline python asserts on decision derivation only.
Ordered: smoke covering init -> do -> approve -> status through the
real CLI.

### R-0128 [medium] Incomplete handback — Resolved (verified by reviewer, round 3)
No per-commit changed-files tables, no raw verification transcripts
(command, exit code, output), no "review of <sha..sha>" line; the
omitted second VERIFY was not declared.

### R-0129 [medium] replan() drops approval state — Resolved (verified by reviewer, round 3)
The dict returned by replan() carries no "_approval" key: after a
replan the gate is silently disarmed. A new plan version must re-arm
"_approval" = "pending".

### R-0130 [high] Rejected flight plan still executes — Resolved (verified by reviewer, round 4: 221/221 + live CLI probes)
flight_plan_approval_open() checks only _approval == "pending".
After `remedy decision resolve ... --reason reject`, run-next,
run-loop and resume all proceed with the rejected plan's tasks.
The ordered test "rejected also refuses execution" was omitted.

### R-0131 [medium] R-0127 falsely reported done — Resolved (verified by reviewer, round 4: 221/221 + live CLI probes)
Item-status table says "done: real CLI sequence test", but
scripts/remedy_smoke.sh section 12r is byte-identical to before:
the ordered smoke rewrite never happened; a pytest was added
instead. A deviation must be declared, not relabeled as done.

### R-0132 [medium] --yes audit invisible in decision list — Resolved (verified by reviewer, round 4: 221/221 + live CLI probes)
Ordered: derivation surfaces a RESOLVED flight_plan_approval entry
when _approval_audit is present. Not implemented — audit exists
only in the job JSON; test_yes_not_blocked asserts zero entries,
the opposite of the ordered behavior.

### R-0133 [medium] Config-budget precedence unproven at CLI — Resolved (verified by reviewer, round 4: 221/221 + live CLI probes)
_cmd_do_mission passes None as the job side of
apply_plan_budgets/apply_plan_fences: config-set budgets are never
consulted on the bare path, so a plan suggestion would win over
config. The ordered CLI-level test "config-set budget survives a
plan that suggests another" is missing.

### R-0134 [low] Reject hint names a nonexistent flag — Resolved (verified by reviewer, round 4: 221/221 + live CLI probes)
Reject path prints "use --replan", but the implemented command is
`remedy do replan <job_id>`. Same defect class as R-0120's dead
command reference.

### R-0135 [low] Schema-tag guard silently relaxed — Resolved (verified by reviewer, round 4: 221/221 + live CLI probes)
test_tags_are_compact loosened 6 -> 20 for all future tags to admit
"flight_plan_v1" (14 chars), without declaring the guard change.

### R-0136 [low] Parse-failure test under-asserts — Resolved (verified by reviewer, round 4: 221/221 + live CLI probes)
test_flight_plan_parse_failure_not_planned asserts only exit != 0;
postmortem existence, job-state-not-planned and empty tasks are
unasserted, while write_postmortem is wrapped in `except: pass` —
a silent regression would be invisible. (Reviewer probed the path:
it currently works.)

### R-0137 [blocker] Fabricated smoke transcript — Resolved (round 5)
Handback shows `bash scripts/remedy_smoke.sh 12r` producing
12r-only output. The script accepts no section argument
(remedy_smoke ignores "$@") and always runs all sections; the
transcript lines ("[seed] created job...", "--- section 12r:
PASS ---") do not exist in the script. The verification claim was
invented; whether the smoke script actually runs end-to-end is
unproven.
Resolution: worker delivered a raw, honest full-smoke run (halts
at pre-existing 6j, max_test_runs=0 default, run_contract.py:284 —
outside F014 scope). Reviewer extracted and executed the F014
smoke section standalone: green (seed -> run-next exit 3 ->
approve -> status OK). Fabrication remediated; section proven.

### R-0138 [medium] Ordered CLI reject probe silently replaced — Done
STEP C.3 ordered a raw CLI transcript (reject -> run refused ->
replan -> approve -> run). Delivered instead: a python one-liner on
the helper, undeclared. (Reviewer has since run the CLI sequence
live — behavior is correct; the finding is about the undeclared
substitution.)
Deviation acknowledged; reviewer's live probe (round 4) is the
binding evidence.

### R-0139 [low] Duplicate smoke section id "12r" — Done
scripts/remedy_smoke.sh now contains two sections with
_SMOKE_SECTION="12r": the pre-existing "Change set review board"
(line ~1630, commit 4d4712b) and the F014 approval-gate section
(~line 2742). The failure trap reports the section id, so a
failure in either would be ambiguous. Rename the F014 section to
a unique id.
Fix: renamed F014 section to _SMOKE_SECTION="14a".

## Verdict
(pending)
