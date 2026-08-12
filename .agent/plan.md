# Plan — F107 Context compiler v2

Branch: feature/f107-context-compiler-v2, cut from main at 2e4142c3.
Next free finding ID: R-0295. R18 reviewed PASS at 6e1970c4.

## Goal
The context compiler selects fenced-path files, their direct import neighbors,
and only SIGNATURES of distant dependencies, under a total context token budget
with tier demotion — and writes an omissions record naming everything it left
out and why. DONE when a fixture repo's task context shrinks measurably versus
whole-files with the fixture task still solvable by the fake provider, and the
omissions record explains every exclusion
(docs/roadmap/features/T2_F107.md).

## Current Step
R19 — the last round before closure. The R18 gate is recorded, R-0291 and
R-0292 are resolved, R-0293 (the budget-demotion path shared the unparseable
blind spot) is registered and repaired with one test, R-0294 records the
reviewer-side pre-emission checklist miss, and the feature file now carries the
`## Built State` section closure precondition 4 requires. T001-T004 are
complete and reviewed; the integration gate ran at R16 and is GREEN, with its
evidence committed under `.agent/gate_f107_r16/`.

## Next Steps
1. R20 — closure per docs/roadmap/STATUS_closure_protocol.md: evidence job, a
   FRESH review zip, the reviewer-authored STATUS line, the README capability
   sync in the same commit, then the PR. The five pre-existing `[reviewer]`
   failures (R-0286) are carried as a documented risk, so the closure verdict is
   PASS_WITH_RISKS.
2. The closure PR is never merged in the session that creates it; it merges at
   the next feature's start via the AGENTS.md Open PR Gate.
