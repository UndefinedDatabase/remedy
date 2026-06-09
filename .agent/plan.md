# Plan — Steps 1030-1044: Integrity Gate + Review Zip Closure

## Goal
Make review bundles and handoffs trustworthy. No PASS over broken bundle.

## Current Step
1044 — Final handoff

## Steps
- [x] 1030: Handoff truth — track files, update agent state
- [x] 1031: Fix review zip script syntax error
- [x] 1032-1036: Script contract tests (removed — manual script, not remedy)
- [x] 1037: Integrity gate helper (integrity_gate.py)
- [x] 1038: CLI: integrity check
- [x] 1039: Handoff gate rule (review_protocol.md)
- [x] 1040: Review bundle integration (integrity_summary.json section)
- [x] 1041: Runtime / script tests — 129 pass
- [x] 1042: Generate real review zip — verified clean
- [x] 1043: Live review protocol — findings updated
- [ ] 1044: Final handoff

## Pre-existing Issue
`test_project_brain.py::TestFileProvenanceChain::test_full_chain_order` fails on main.

## Known Risks
- R-0017 (Medium): ctx_says_complete heuristic matches "done" in prior block status text
