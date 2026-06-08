# Context

## Active Branch
feature/steps-905-924-remedy-do-v1

## Scope
Steps 925-939: remedy do v1 Truth Closure

## Prior Step Status
Steps 865-879: PASS — Context Inspector v1.
Steps 880-894: PASS — Context Inspector Truth Closure.
Steps 895-904: PASS — Review Protocol Repair. PR #47 merged.
Steps 905-924: PASS WITH RISKS — remedy do v1 Cohesive Flow. PR #48 open.

## Carried Risks
1. next_safe_action validates group only, not full command_id → Step 926-927
2. DoRunContract duplicates RunContract → Step 930
3. Context exception skipped, flow continues to build → Step 928
4. do.run catalog: may_mutate_repo=True, may_execute_commands=True overclaim → Step 929
5. max_loops stored but not enforced → Step 931
6. Autonomy cap not transparent in output → Step 932

## Builder/Reviewer Handoff Rules
- Before final handoff, builder MUST read `.agent/live_review.md`.
- Every open finding must have `Done: R-XXXX` marker or be listed as remaining risk.
- See `.agent/review_protocol.md` for full finding format and resolution rules.

## Pre-existing Issue
`tests/orchestration/test_project_brain.py::TestFileProvenanceChain::test_full_chain_order` fails on main.

## Resource Safety
Use `scripts/remedy_pytest.sh`. No direct pytest, no background pytest, no `shell=True`.
