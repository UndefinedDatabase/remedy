# Plan — Steps 329-334

## Goal
Final Ollama CLI truth fix, stop-reason JSON repair, docs contract closure.

## Current Step
All steps complete. Ready for commit + push.

## Steps
- [x] Step 329: Updated docs/autocoder-usage.md — pipeline overview, VRAM free, missing stop reasons, warnings
- [x] Step 330: Fixed stop_reason JSON corruption — _BOOL_EVENTS whitelist, removed stop_reason from events
- [x] Step 331: Fixed memory injection import — correct module, explicit degradation metadata
- [x] Step 332: Added 9 CLI path regression tests exercising real handler path
- [x] Step 333: Docs command contract — all remedy commands catalog-valid, flags validated
- [x] Step 334: Full baseline 3886 passed, 7 skipped. Vitest 21. TypeScript clean. Build OK.
