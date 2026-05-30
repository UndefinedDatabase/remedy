# Plan — Steps 91-100

## Goal
Directional semantic brain UX (ELK layout), live autorun, autocoder foundation.

## Current Step
Complete. All steps 91-100 implemented and tested.

## Steps
- [x] Step 91: ELK directional layout — replace ring with elk-layered, RIGHT direction
- [x] Step 92: True semantic zoom v2 — 7 zoom levels, default 1 node, max counts per level
- [x] Step 93: Screen-space labels + minimal detail v2 — fixed-size labels, compact card
- [x] Step 94: Explainable edges — user-facing edge kinds, tooltips, styling
- [x] Step 95: Live growth — live-state/events-since API, polling, animated node entry
- [x] Step 96: remedy do v1 — high-level autorun command, dry-run, autonomy gates
- [x] Step 97: Source context injection — dynamic file selector, budget-aware, builder injection
- [x] Step 98: Structured code patch intent — file_ops/unified_diff builder output
- [x] Step 99: Source patch apply — safe diff apply, snapshot/revert, denylist
- [x] Step 100: Autocode satisfaction smoke — end-to-end fixture test

## Test Results
- 2994 tests pass (full suite)
- 48 new tests in test_steps_91_100.py
- 32 updated tests in test_steps_83_90.py (v2 schema compatibility)

## Risks (mitigated)
- elkjs bundle size: using rank-based layout computed server-side, elkjs in deps for future client-side use
- Live polling vs SSE: implemented polling with hash-based change detection
- LLM availability for smoke: fixture builder provides deterministic path
