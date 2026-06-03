# Plan — Steps 460-469

## Goal
Worker real work closure: no crash on missing job, no fake approval, honest lifecycle.

## Current Step
All steps complete.

## Steps
- [x] Step 460: Clean handoff truth
- [x] Step 461: Fixture missing job blocks safely (catches JobNotFoundError)
- [x] Step 462: No fake ollama approval (blocks without real intent)
- [x] Step 463: Unified fixture/ollama path via real autorun
- [x] Step 464: Approval requires real intent_id (no placeholders)
- [x] Step 465: Lifecycle mapping v2 (approval_required_no_intent → blocked)
- [x] Step 466: CLI worker output truth (no placeholder commands)
- [x] Step 467: UI filters placeholder commands (includes("<") check)
- [x] Step 468: 7 fake-state regression tests
- [x] Step 469: Baseline (4148 passed, 8 skipped, Vitest 35, TS clean, build OK)
