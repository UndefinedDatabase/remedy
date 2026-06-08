# Context

## Active Branch
feature/steps-940-959-test-failure-repair-loop

## Scope
Steps 940-959: Test Failure Artifact v1 + Repair Loop v0

## Prior Step Status
Steps 895-904: PASS — Review Protocol Repair. PR #47 merged.
Steps 905-924: PASS WITH RISKS — remedy do v1 Cohesive Flow.
Steps 925-939: PASS — remedy do v1 Truth Closure. PR #48 open.

## Current Work
Build TestFailureArtifact + fix task creation + repair loop v0.
First "Remedy keeps working" moment — structured failure evidence, not raw output.

## Builder/Reviewer Handoff Rules
- Before final handoff, builder MUST read `.agent/live_review.md`.
- Every open finding must have `Done: R-XXXX` marker or be listed as remaining risk.
- See `.agent/review_protocol.md` for full finding format and resolution rules.

## Pre-existing Issue
`tests/orchestration/test_project_brain.py::TestFileProvenanceChain::test_full_chain_order` fails on main.

## Resource Safety
Use `scripts/remedy_pytest.sh`. No direct pytest, no background pytest, no `shell=True`.
