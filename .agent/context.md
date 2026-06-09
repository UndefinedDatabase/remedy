# Context

## Active Branch
feature/steps-940-959-test-failure-repair-loop

## Scope
Steps 960-974: Repair Loop Truth Closure — No Fake Patch Intent

## Prior Step Status
Steps 905-924: PASS WITH RISKS — remedy do v1 Cohesive Flow. PR #48 merged.
Steps 925-939: PASS — remedy do v1 Truth Closure.
Steps 940-959: PASS WITH BLOCKER — optional repair patch intent produces non-resolvable intent ID.

## Current Work
Fix fake repair patch intent blocker. Make repair loop v0 truthful:
- Either create real approval-queue-visible patch intent (Option A)
- Or disable/report unavailable (Option B)
Chosen: Option A — make fixture repair intent real.

## Builder/Reviewer Handoff Rules
- Before final handoff, builder MUST read `.agent/live_review.md`.
- Every open finding must have `Done: R-XXXX` marker or be listed as remaining risk.
- See `.agent/review_protocol.md` for full finding format and resolution rules.

## Pre-existing Issue
`tests/orchestration/test_project_brain.py::TestFileProvenanceChain::test_full_chain_order` fails on main.

## Resource Safety
Use `scripts/remedy_pytest.sh`. No direct pytest, no background pytest, no `shell=True`.
