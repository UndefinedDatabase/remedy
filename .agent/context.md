# Context

## Active Branch
feature/steps-247-252-data-honest-contract

## Scope
Steps 313-320: Real-repo autocoder hardening, Ollama reliability, operator-visible stop reasons.

## Completed
- Real small-repo smoke fixtures (missing function, wrong return, repair scenario)
- Ollama structured patch reliability harness (18 mocked failure modes)
- Source context quality (selection, budget, redaction, metadata)
- Opt-in real Ollama smoke (REMEDY_REAL_OLLAMA_SMOKE, graceful skip)
- Builder failure taxonomy (23 canonical stop reasons)
- Real repair loop hardening (repeated patch detection, budget exhaustion)
- CLI stop_reason display + next-command hints
- autocoder-usage.md documentation

## Current Problems
None blocking.

## Constraints
- No mutation endpoints, no shell=True, no 0.0.0.0
- No fake state, no optimistic LIVE
- React 19 + TypeScript + MUI + CSS Modules
- Redaction: no raw content in UI/API surfaces
- UI remains read-only
- source_apply requires job + intent_id (approved) before mutation
- No unittest.mock in production packages
- Dashboard is version 3
- Graph architecture is Canvas/Force (not React Flow)
- Test files use domain directories — no step-numbered files
- Memory: approved-only, bounded, redacted, no raw leaks
- BuilderOutput: structured_patch_text parsed, not trusted raw
- Stop reasons: canonical names in all surfaces

## Remaining Risks
- Real Ollama output quality varies by model
- Structured patch prompt reliability needs iteration
- Parser strictness tradeoffs (first-block-wins vs reject-multiple)

## Recommended Next Block
If real Ollama parse/apply is flaky:
  Steps 321-328 — Builder Prompt Quality Iteration And Parser Hardening
If real Ollama is acceptable:
  Steps 321-328 — Event-Ledger Replay And Checkpoint Resume
UI block after that:
  Steps 329-336 — Operator Cockpit v2
