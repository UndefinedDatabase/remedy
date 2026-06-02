# Context

## Active Branch
feature/steps-247-252-data-honest-contract

## Scope
Steps 321-328: Wire real Ollama into `remedy do`, stop-reason truth, provider-mode hardening.

## Completed
- --builder-provider none|fixture|ollama in command catalog and CLI
- OllamaBuilder wired to autorun via bridge pipeline
- AutorunResult extended with stop_reason and provider fields
- CLI JSON output v2 with stop_reason, provider
- CLI text output shows stop_reason and provider
- Real `remedy do` Ollama smoke opt-in test
- Ollama prompt improved: strict path/shell/format constraints
- Parser handles trailing text after JSON (common Ollama mistake)
- Docs updated with --builder-provider, accurate commands
- All review findings resolved

## Constraints
- No mutation endpoints, no shell=True, no 0.0.0.0
- UI remains read-only
- source_apply requires job + intent_id (approved) before mutation
- No unittest.mock in production packages
- Ollama only runs when explicitly requested via --builder-provider ollama
- Default provider is none (safe, deterministic)

## Remaining Risks
- Model quality varies by Ollama model
- Structured patch prompt may need further iteration
- Parser strictness: first-block-wins vs reject-multiple (documented)

## Recommended Next Block
If real Ollama outputs are poor:
  Steps 329-336 — Builder Prompt Quality And Parser Hardening
If real Ollama path is acceptable:
  Steps 329-336 — Operator Cockpit v2
Alternative:
  Steps 329-336 — Event-Ledger Replay And Checkpoint Resume
