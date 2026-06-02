# Plan — Steps 321-328

## Goal
Wire real Ollama into `remedy do`, stop-reason truth, provider-mode hardening.

## Current Step
All steps complete. Ready for commit + push.

## Steps
- [x] Step 321: Verified/closed review gaps from 313-320 (R-9002/R-9004/R-9005 confirmed fixed)
- [x] Step 322: Added --builder-provider none|fixture|ollama to catalog + CLI
- [x] Step 323: Wired OllamaBuilder into autorun via bridge pipeline
- [x] Step 324: stop_reason + provider in AutorunResult, CLI JSON v2, text output
- [x] Step 325: Real `remedy do` Ollama smoke opt-in (REMEDY_REAL_OLLAMA_SMOKE)
- [x] Step 326: Improved Ollama prompt (strict constraints), parser handles trailing text
- [x] Step 327: Updated docs with --builder-provider, command contract tests
- [x] Step 328: Baseline 3869 passed, 7 skipped. Vitest 21. TypeScript clean. Build OK.
