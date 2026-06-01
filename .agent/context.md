# Context

## Active Branch
feature/steps-247-252-data-honest-contract

## Scope
Steps 305-312: Structured builder pipeline, Ollama patch bridge, bounded autocoder E2E.

## Completed
- Prompt redaction (raw prompt → [redacted] hash/length in planning artifact)
- BuilderOutput v2 (structured_patch_text + structured_patch_format fields)
- BuilderPatchResult model + parse_builder_patch() with safety checks
- Structured patch parser: plain JSON + fenced JSON + unified diff detection
- Ollama builder prompt: requests structured patch file_ops JSON
- Builder bridge: BuilderOutput → parse → intent → approval → source_apply → test → proof
- Fixture smoke tests for CI, opt-in real Ollama smoke
- Bounded repair loop: build → bridge → test → repair_context → rebuild (max_cycles)
- .pyc cache fix (PYTHONDONTWRITEBYTECODE=1) for repair loop test reliability
- Dashboard: builder_patch_parsed, repair_loop_cycle, repair_loop_max_cycles
- CLI: events displayed in text output, cycles shown

## Current Problems
- R-7001: Duplicate imports in 15/24 domain test files (cosmetic)

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
- Test files use domain directories — no step-numbered files or class names
- Memory: approved-only, bounded, redacted, no raw leaks
- BuilderOutput: structured_patch_text parsed, not trusted raw

## Recommended Next Block
Steps 313-320 — Event-Ledger Replay And Checkpoint Resume
