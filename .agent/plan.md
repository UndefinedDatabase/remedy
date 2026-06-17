# Plan — Steps 2656-2675: Core Product Spine + Reliable Fast Test Lane v0

## Goal
Consolidation block. Document core operator flow, create fast test lane,
update docs to product language, add targeted consistency tests.
No new features, no new autonomy, no new provider execution.

## Steps
- [x] Step 2656: Mainline gate + stale review check
- [x] Step 2657: Core product spine audit
- [x] Step 2658: Command taxonomy audit
- [x] Step 2659: Canonical flow map document (core-product-spine-v0.md)
- [x] Step 2660: Fast test lane design (9 targeted suites)
- [x] Step 2661: scripts/remedy_test_fast.sh (420 tests, ~7s)
- [x] Step 2662: Test lanes manifest doc (test-lanes-v0.md)
- [x] Step 2663: scripts/remedy_test_full.sh wrapper
- [x] Step 2664: Full-suite hang risk — all subprocess tests use timeout+killpg
- [x] Step 2665: remedy doctor core --json (read-only, importlib-based)
- [x] Step 2666: Catalog + contract for doctor core
- [x] Step 2667: Update simple operator quickstart
- [x] Step 2668: Update controlled Claude operator docs (simple path primary)
- [x] Step 2669: Update mission report docs (product language)
- [x] Step 2670: Stale command scanner test (6 checks)
- [x] Step 2671: Product spine consistency tests (7 checks)
- [x] Step 2672: Fast lane self-test (7 checks)
- [x] Step 2673: Architecture guard scan — clean
- [x] Step 2674: Targeted (420 fast + 49 facade + 20 spine) + full (6863) tests
- [ ] Step 2675: Final handoff

## Hard rules
No auto-apply/approve/provider execution/shell=True/secret storage/raw leaks.
Consolidation only — docs, scripts, tests. No new features.
