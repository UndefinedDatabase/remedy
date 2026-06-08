# Plan — Steps 895-904: Parallel Review Protocol Repair

## Goal
Restore live-review finding ledger workflow. Add grouped CLI runtime tests. Document risks honestly.

## Current Step
Complete — awaiting reviewer verdict

## Steps
- [x] 895: Define live review protocol (`.agent/review_protocol.md`)
- [x] 896: Repair live review section (finding ledger format)
- [x] 897: Builder/reviewer checklist in `.agent/context.md`
- [x] 898: Grouped CLI runtime test (5 subprocess tests)
- [x] 899: Runtime missing task test (2 tests)
- [x] 900: Runtime event target test (3 tests)
- [x] 901: Fast lane risk entry (documented in context.md)
- [x] 902: Targeted tests — 108 passed + 4670 fast lane
- [x] 903: Final review section (verdict PENDING, not claiming PASS)
- [x] 904: Final handoff

## Risks
- Pre-existing failure `test_full_chain_order` deselected (documented as known risk)
- Budget trimming deferred; wording fix is honest alternative
- R-0003 open — reviewer must verify before merge-ready
