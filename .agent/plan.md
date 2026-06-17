# Plan — Steps 2696-2715: Fast Lane Runtime Split + Doctor Core Safety Closure v0.1

## Goal
Split subprocess-heavy tests out of fast lane into runtime lane.
Harden doctor core error redaction. No new features.

## Steps
- [x] Step 2696: Mainline gate — PR #89 merged, reviewer PASS
- [x] Step 2697: Baseline — fast lane 443 passed 6.79s, review bundle 11 passed 3.04s
- [x] Step 2698: Isolate review bundle — no local hang, but reviewer reported hang risk
- [x] Step 2699: Decision — move all 4 subprocess files to runtime lane
- [x] Step 2700: Create scripts/remedy_test_runtime.sh (4 subprocess-heavy files)
- [x] Step 2701: Update fast lane — pure in-process only (6 files)
- [x] Step 2702: Update lane self-tests (test_product_spine, test_test_categories)
- [x] Step 2703: Harden _safe_err — add /mnt/, /tmp/, /Users/, key=value secret redaction
- [x] Step 2704: Add negative tests for doctor core (path + secret redaction)
- [x] Step 2705: Update docs/test-lanes-v0.md with runtime lane
- [x] Step 2706: Targeted tests — 395 fast + 54 runtime + 12 categories + lint clean
- [x] Step 2707: Full suite — 6876 passed, 0 failures
- [x] Step 2708: Changed Line Map + commit + PR #90
- [x] Step 2709: Reviewer PASS @ 9c68161 — R-0155 INFO non-blocking

## Hard rules
Split only. No new features. No provider execution.
