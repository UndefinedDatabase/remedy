# Plan — Steps 2446-2505 Closure: R-0135..R-0140

## Goal
Fix 6 findings from independent review of Run Replay to Self-Repair Proposal v0.

## Steps
- [x] R-0135: Restrict approval to awaiting_operator/edited; require non-empty evidence, prompt, criteria, tests; re-check safety in convert
- [x] R-0136: Add secret marker scrubbing (sk-ant-*, api_key=*, etc.) to to_dict() and all public exports; sanitize edited prompts
- [x] R-0137: Add signal_collection_warnings/errors fields to _gather_replay_signals; blocked proposal on collection errors
- [x] R-0138: Wire self_repair_progress_summary into progress_ledger.py (extract/merge/build_progress_ledger)
- [x] R-0139: Add CLI subprocess tests for all 7 commands with isolated REMEDY_DATA_DIR (12 tests)
- [x] R-0140: Simple-language explanation in final handoff
- [x] Tests: 68 proposal tests + 12 CLI tests + 121 progress/bundle tests + 6759 full suite (0 failures, 8 skipped)
- [ ] Commit + push + PR

## Hard rules
No provider execution; no auto-apply/approve/PR/git; no shell=True; no secret storage;
no raw log/prompt/transcript leaks; no MemPalace/embeddings.
