# Plan — F107 Context compiler v2 — CLOSED

Branch: feature/f107-context-compiler-v2, cut from main at 2e4142c3.
Next free finding ID: R-0298. Last reviewed SHA 9aacd70d (R22 PASS).

## Goal
The context compiler selects fenced-path files, their direct import neighbors,
and only SIGNATURES of distant dependencies, under a total context token budget
with tier demotion — and writes an omissions record naming everything it left
out and why. DONE, and closed at PASS_WITH_RISKS: the fixture task's context
shrinks measurably against whole-files, the fake provider still solves it, and
the omissions record explains every exclusion
(docs/roadmap/features/T2_F107.md).

## Current Step
R23 — closure. The R20, R21 and R22 gates and the closure verdict are recorded,
`docs/roadmap/STATUS.md` carries the `[x]` line with the README capability sync
in the same commit, and the PR is open. 22 findings remain open, none above
Medium, each named as an accepted risk in the closure verdict.

## Next Steps
1. The PR is NOT merged by this session. It merges at the next feature's start
   via the AGENTS.md Open PR Gate — that gap is the operator's manual-review
   window, and the operator may merge manually at any time instead.
2. The next session claims the next feature under Rule A5: F111 Diff-only
   repair, the first `[ ]` line of docs/roadmap/STATUS.md.
3. Owed follow-ups, all registered: R-0295 the packager prune, R-0296 the flake
   routed to F252, R-0290 and R-0297 the two self-drive protocol gaps.
