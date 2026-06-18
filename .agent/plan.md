# Plan — Steps 2876-2915: Approval Policy Package Truth + Runtime Lane Closure v0.2

## Goal
Fix high-impact package path bug: `_load_package()` searched `builder_adapter/packages`
instead of `main_builder_adapter/packages`. Add unmocked integration tests proving
real storage truth. Propagate specific denial codes. Guard artifact boundary.

## Steps
- [x] 2876: Mainline gate — main @ 0bc5a4f, PR #92 merged, clean tree
- [x] 2877: Baseline — compileall clean, fast 502, runtime 54, policy 76, mission 15
- [x] 2878: R-0164 — confirmed main_builder_adapter/packages path in source
- [x] 2879: R-0164 — fixed _load_package() from builder_adapter → main_builder_adapter
- [x] 2880: R-0164 — unmocked evaluate integration test (real storage, allowed)
- [x] 2881: R-0164 — missing-package integration test (real session, deleted pkg)
- [x] 2882: R-0165 — missing_package early return before policy matching
- [x] 2883: R-0165 — missing_task_type propagated from per-policy eval
- [x] 2884: R-0166 — TestPolicyEvaluationRealBuilderPackageStorage (3 tests)
- [x] 2885: R-0166 — TestPolicyGrantRealStorage::test_grant_real_storage
- [x] 2886: R-0166 — TestPolicyGrantRealStorage::test_grant_denied_missing_package
- [x] 2887: R-0167 — runtime lane green (54 pass, 6.34s, no hang)
- [x] 2888: R-0167 — no hang, no fix needed
- [x] 2889: R-0167 — no docs change needed (runtime lane stable)
- [x] 2890: R-0168 — full suite: 6997 passed, 1 failed pre-existing, 8 skipped
- [x] 2891: R-0169 — artifact boundary scan (0 live_review refs in policy code)
- [x] 2892: R-0169 — legacy refs documented as pre-existing
- [x] 2893: R-0169 — TestNoLiveReviewDependency guard test
- [x] 2894-2901: Regressions all green
- [x] 2902-2908: Test lanes + full suite green
- [ ] 2909-2911: Changed Line Map + protocol + final handoff

## Hard rules
Metadata only. No execution. No auto-apply/PR/merge.
