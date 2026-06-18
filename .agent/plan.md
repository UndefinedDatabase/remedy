# Plan — Steps 2836-2875: Approval Policy Closure + Truthful Mission Integration v0.1

## Goal
Harden approval policy: truthful evaluation, redaction, package-backed,
token-aware, honest reporting. No new features.

## Steps
- [x] 2836: Mainline gate — main synced, PR #91 merged, clean tree
- [x] 2837: Reproduce baseline — compileall, fast, runtime, targeted
- [x] 2838: R-0155 fix — mission-loop policy test paths
- [x] 2839-2840: R-0156 — runtime lane hang investigation (no repro, 11 pass in 3s)
- [x] 2841-2842: R-0157 — strengthen redaction + save/integrity rejection
- [x] 2843-2844: R-0158 — correct package loading + task type enforcement
- [x] 2845-2846: R-0158 — token estimate enforcement + honest docs
- [x] 2847: R-0160 — specific denial codes (23 total)
- [x] 2848: R-0159 — real-provider confirmation metadata
- [x] 2849: R-0161 — uses decrement after approval creation
- [x] 2850: R-0161 — grant binds package/policy id
- [x] 2851-2852: R-0162 — mission loop safety + tests
- [x] 2853-2855: R-0163 — morning report, review bundle, progress ledger
- [x] 2856-2857: CLI tests + data_dir isolation
- [x] 2858-2860: Docs, artifact boundary, architecture guard
- [x] 2861-2867: Targeted tests, lanes, full suite (6991 pass, 1 pre-existing)
- [ ] 2868-2870: Changed Line Map, protocol, final handoff

## Hard rules
Metadata only. No execution. No auto-apply/PR/merge.
