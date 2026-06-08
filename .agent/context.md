# Context

## Active Branch
feature/steps-840-849-proof-chain-ordering

## Scope
Steps 840-849: Proof Chain Evidence Ordering Closure, no pre-apply test verification.

## Prior Step Status
Steps 825-839: PASS WITH RISKS — major false-verified fixes landed, but independent review found remaining trust risks:
1. Sole-change generic test linking lacks after-apply timing check.
2. `change_set.py` latest global test association remains unsafe for display surfaces.
3. Plan handoff was stale after merge and needed repair.

## Current Work
Make Proof Chain truth final: a test verifies a change only if linked to intent/task, explicitly not-required with intent, or a sole-change generic test demonstrably ran after apply.

## Out of Scope
No UI, Context Inspector, Ollama, real test execution, rollback/snapshot, overnight, browser mutation, or git commit gate work.

## Resource Safety
All pytest execution uses `scripts/remedy_pytest.sh`.
No background pytest. No parallel pytest. No `shell=True`.
