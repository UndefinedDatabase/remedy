# Plan — Steps 975-994: Review Bundle v1

## Goal
Build safe review bundle command. Close R-0006 repair runtime gap.

## Current Step
994 — Final handoff

## Steps
- [x] 975: Handoff setup — agent files updated
- [x] 976: Close R-0006 — 5 subprocess tests for --fixture-patch-intent
- [x] 977: Review bundle model — dataclasses (ReviewBundleResult, etc.)
- [x] 978: Build safe bundle sections
- [x] 979: Event summary section
- [x] 980: Changed files safe section
- [x] 981: Repair summary section
- [x] 982: Context inspection section
- [x] 983: Trust report section
- [x] 984: CLI command — review.bundle in catalog + handler
- [x] 985: Review zip script hygiene — 3 contract tests
- [x] 986: Bundle safety tests — 8 tests
- [x] 987: CLI runtime tests — 8 subprocess tests
- [x] 988: Bundle determinism tests — 4 tests
- [x] 989: Docs — review-bundle-v1.md
- [x] 990: Agent tooling — review_protocol.md updated
- [x] 991: Review protocol integration
- [x] 992: Targeted tests — 147 pass, 0 fail
- [ ] 993: Live review protocol
- [ ] 994: Final handoff

## Pre-existing Issue
`test_project_brain.py::TestFileProvenanceChain::test_full_chain_order` fails on main.
