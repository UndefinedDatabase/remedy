# Plan — F107 Context compiler v2

Branch: feature/f107-context-compiler-v2, cut from main at 2e4142c3.
Next free finding ID: R-0293. R17 reviewed PASS at 54d05e37.

## Goal
The context compiler selects fenced-path files, their direct import neighbors,
and only SIGNATURES of distant dependencies, under a total context token budget
with tier demotion — and writes an omissions record naming everything it left
out and why. DONE when a fixture repo's task context shrinks measurably versus
whole-files with the fixture task still solvable by the fake provider, and the
omissions record explains every exclusion
(docs/roadmap/features/T2_F107.md).

## Current Step
R18 — the pre-closure repair round. Three findings registered (R-0290 the
self-drive Phase 0 branch blind spot, R-0291 two deferred Design bullets,
R-0292 the unparseable non-tier-1 file), R-0292 repaired in F107's own module
with three new tests, the fifth omission reason `unparseable` carried into the
guide and the feature file, and DECISIONS F107 D1 and D2 recorded. T001-T004
are complete and reviewed; the integration gate ran at R16 and is GREEN, with
its evidence committed under `.agent/gate_f107_r16/`.

## Next Steps
1. R19 — the feature file's `## Built State` section, which closure
   precondition 4 requires and which does not exist yet, plus the R18 gate.
2. R20 — closure per docs/roadmap/STATUS_closure_protocol.md: evidence job, a
   FRESH review zip, the reviewer-authored STATUS line, the README capability
   sync in the same commit, then the PR. The five pre-existing `[reviewer]`
   failures (R-0286) are carried as a documented risk, so the closure verdict is
   PASS_WITH_RISKS.
3. The closure PR is never merged in the session that creates it; it merges at
   the next feature's start via the AGENTS.md Open PR Gate.
