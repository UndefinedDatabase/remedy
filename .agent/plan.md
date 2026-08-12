# Plan — F107 Context compiler v2

Branch: feature/f107-context-compiler-v2, cut from main at 2e4142c3.
Next free finding ID: R-0290. R16 reviewed PASS at 5c808a59.

## Goal
The context compiler selects fenced-path files, their direct import
neighbors, and only SIGNATURES of distant dependencies, under a total
context token budget with tier demotion — and writes an omissions record
naming everything it left out and why. DONE when a fixture repo's task
context shrinks measurably versus whole-files with the fixture task still
solvable by the fake provider, and the omissions record explains every
exclusion (docs/roadmap/features/T2_F107.md).

## Current Step
R17 — land the tail R16 never reached: the reviewer's R16 PASS gate and the
F107 integration-gate verdict, finding R-0289, this plan and the handoff, and
push the branch. T001-T004 are complete and reviewed. The integration gate ran
at R16 and is GREEN — branch and base fail the same five R-0286 ids, zero
branch-only, zero base-only — with its evidence committed under
`.agent/gate_f107_r16/`. No production, test, docs or roadmap file moves here.

## Next Steps
1. Closure per docs/roadmap/STATUS_closure_protocol.md: evidence job, a FRESH
   review zip, the reviewer-authored STATUS line, then the PR. The five
   pre-existing `[reviewer]` failures (R-0286) are carried as a documented
   risk, so the closure verdict is PASS_WITH_RISKS.
2. The closure PR is never merged in the session that creates it; it merges at
   the next feature's start via the AGENTS.md Open PR Gate.
