# Plan — Steps 2916-2995: Development Artifact Boundary + Product Truth Sources v0

## Goal
Separate development-time coordination artifacts (.agent/live_review.md) from
Remedy product/runtime truth. Audit, classify, guard, and document the boundary.

## Steps
- [x] 2916: PR #93 gate — merged @ f0b6cea, main synced
- [x] 2917: Baseline — compileall clean, fast 508, runtime 54
- [x] 2918: Audit — full source scan of live_review.md refs (30+ hits classified)
- [x] 2919: Boundary doc — docs/development-artifact-boundary-v0.md
- [x] 2920: Product truth source map — in same doc
- [x] 2921: Module boundary decision — no new module needed (documented)
- [x] 2922: Operator surfaces identified — worker/mission/approval are product
- [x] 2923: progress_cmd.py audit — development progress display
- [x] 2924: feature_cmd.py audit — development feature display
- [x] 2925: orchestrator_brain.py — development context only
- [x] 2926: overnight_executor.py — development self-dev gate
- [x] 2927: repair_loop_v2.py — development repair loop only
- [x] 2928: self_dogfood*.py — development self-dogfood paths
- [x] 2929: review_bundle.py — development evidence inclusion
- [x] 2930: integrity_gate.py — development process health
- [x] 2931: Whitelist boundary test — TestWhitelistBoundary
- [x] 2932: Product path guard — TestProductModulesNoLiveReview (4 modules)
- [x] 2933: Doctor core guard — TestDoctorCoreNoDevTruth
- [x] 2934: Mission report guard — TestMissionReportNoDevTruth
- [x] 2935: Approval CLI guard — TestApprovalCLINoDevTruth
- [x] 2936-2939: Docs updated (test-lanes-v0.md, boundary doc)
- [x] 2940-2948: Guards cover all product paths
- [x] 2949: Fast lane updated (boundary tests added, 516 pass)
- [x] 2950: No runtime lane change needed
- [x] 2951: Architecture guard — no shell=True, no provider SDK
- [x] 2952-2958: Targeted tests all pass
- [x] 2959: Fast lane: 516 pass
- [x] 2960: Runtime lane: 54 pass
- [x] 2961: Lint: ruff + mypy clean
- [x] 2962: Full suite: 7005 passed, 1 pre-existing, 8 skipped
- [x] 2963-2968: Final handoff

## Hard rules
No execution. No auto-apply/PR/merge. No provider SDK. No shell=True.
