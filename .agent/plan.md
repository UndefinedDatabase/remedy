# Plan — Steps 305-312

## Goal
Structured builder pipeline, Ollama patch bridge, bounded autocoder E2E.

## Current Step
All steps complete. Ready for commit + push.

## Steps
- [x] Step 305: Stop writing raw prompt/memory into planning artifact, replace with safe metadata
- [x] Step 306: Extend BuilderOutput with structured patch fields, add parser bridge with safety checks
- [x] Step 307: Update Ollama builder prompt to request structured patch format
- [x] Step 308: Connect builder → parse → intent → approval → source_apply → proof → tests
- [x] Step 309: Fixture smoke for CI, opt-in real Ollama smoke test
- [x] Step 310: Bounded repair loop with structured patch (pyc cache fix)
- [x] Step 311: Operator visibility for structured patch pipeline in CLI/dashboard
- [x] Step 312: Full baseline 3773 passed, 2 skipped. Vitest 21 passed. TypeScript clean. Build OK.
