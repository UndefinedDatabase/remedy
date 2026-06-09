# Plan — Steps 960-974: Repair Loop Truth Closure

## Goal
Fix fake repair patch intent blocker from Steps 940-959.
Make Repair Loop v0 truthful — no fake intent IDs, no fake next_safe_actions.

## Design Choice
Option A: Make fixture repair patch intent real via `patch_intent_explanations`.

## Current Step
974 — Final handoff

## Steps
- [x] 960: Handoff truth — update agent files
- [x] 961: Regression test for fake repair intent (confirmed failing)
- [x] 962: Fix repair_loop.py — real patch_intent_explanations
- [x] 963: Validate next_safe_action against actual entity
- [x] 964: Repair artifact metadata truth (approval queue visible)
- [x] 965: Event semantics cleanup (idempotent creation events)
- [x] 966: Related files safety (tested — no abs paths, no traversal)
- [x] 967: CLI error handling (specific exceptions, no broad Exception)
- [x] 968: Runtime CLI tests for optional intent
- [x] 969: Proof/change alignment (proof_status invariant tests)
- [x] 970: Live review protocol — all findings with Done: R-XXXX markers
- [x] 971: Targeted tests — 57 pass, 0 fail
- [x] 972: Docs updated — repair-loop-v0.md
- [ ] 973: Review bundle check
- [ ] 974: Final handoff

## Pre-existing Issue
`test_project_brain.py::TestFileProvenanceChain::test_full_chain_order` fails on main.
