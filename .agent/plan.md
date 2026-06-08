# Plan — Steps 840-849: Proof Chain Evidence Ordering Closure

## Goal
Prevent pre-apply or unrelated generic tests from verifying changes. Keep display surfaces from implying unsafe test associations.

## Current Step
841-844 — implement timestamp-gated linking and safe change-set association

## Steps
- [x] 840: Handoff repair — Steps 825-839 marked PASS WITH RISKS, stale risks carried forward
- [ ] 841: Add proof_chain timestamp helpers
- [ ] 842: Require after-apply ordering for sole-change generic tests
- [ ] 843: Add timing-specific missing links
- [ ] 844: Fix change_set test association
- [ ] 845: Add truth tests for timing
- [ ] 846: Add CLI/text no-overclaim tests
- [ ] 847: Command catalog truth cleanup/test
- [ ] 848: Run targeted tests through wrapper
- [ ] 849: Final handoff

## Risks
- Unknown or invalid timestamps must never verify sole-change generic tests.
- Intent/task-linked tests remain allowed without timestamps.
- Output must not leak raw event data or artifacts.
