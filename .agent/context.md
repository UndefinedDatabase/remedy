# Context

## Active Branch
feature/steps-247-252-data-honest-contract

## Scope
Steps 460-469: Worker real work closure — complete.

## Completed
- Fixture missing job: catches JobNotFoundError → blocked, no crash
- Ollama missing job: catches JobNotFoundError → blocked, no fake approval
- Unified provider path: both fixture/ollama use same autorun try/catch
- Approval truth: waiting_for_approval only with real intent_id
- No placeholder commands: <intent_id> filtered in both backend and UI
- WorkerStatusMini: filters commands containing < before rendering
- 7 regression tests: fixture crash, ollama fake approval, placeholder intent, completed-requires-work

## Resource-Safety Rules (permanent)
- Never run pytest in background
- Always use scripts/remedy_pytest.sh for pytest execution
- Worker processes one job at a time

## Constraints
- UI remains read-only
- waiting_for_approval requires real intent_id
- completed requires real work
- source_apply requires permission + approved intent

## Recommended Next Block
Steps 470-479 — Real Ollama Trial Round And Prompt Selection
