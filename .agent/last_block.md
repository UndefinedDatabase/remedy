── STEP R3/~10 — F107 Context compiler v2 — close the T001 gate ──────────────
Goal:        Commit the unit tests that certify the import-neighbor graph
             layer written in R2, and record the R2 reviewer gate. No
             production code changes in this round.
Bundle:      C1 authored-block save; C2 last_block mirror; C3 R2 gate entry
             into live_review (authored append); C4 plan rewrite;
             C5 tests/orchestration/test_context_compiler.py (the T001 gate);
             C6 handoff rewrite; push; handback.
Change:      EXACTLY these paths and nothing else:
             .agent/authored/f107-r3-1.md (new), .agent/last_block.md,
             .agent/live_review.md (append pair LR2),
             .agent/plan.md (full replacement PLAN2),
             tests/orchestration/test_context_compiler.py (new),
             .agent/handoff.md (your handback rewrite).
Constraints: AGENTS.md in full. packages/orchestration/context_compiler.py is
             READ-ONLY this round — read it before writing tests, never edit
             it. Stdlib + pytest only; no new dependency. Import style is the
             repo's: `from packages.orchestration.context_compiler import ...`
             (pyproject pythonpath = ["."]). Fixture trees are built with
             pytest's tmp_path, never in the checkout. Never write a `Done:`
             line in live_review. Do NOT create a PR. Never touch main.
             Scratch only under .remedy-wt/, uncommitted. Apply authored
             slices byte for byte after sha256 verification; on mismatch STOP.

WHY THIS ROUND IS TESTS-ONLY: R2 was truncated by `.agent/STOP` after its
module commit, so context_compiler.py is on the branch with no committed test
evidence. The reviewer probed it on a throwaway tree and every contract case
held, but a reviewer probe is not evidence. This round's gate d is what
certifies that module.

TEST CONTRACT (C5) — tests/orchestration/test_context_compiler.py. Group into
readable test functions; the numbered cases are the obligations, not a
required function count. `pytestmark = pytest.mark.unit`. Build each fixture
tree under tmp_path and pass that tmp_path as `root`.

  Python — python_import_neighbors:
   1. `import pkg.mod` resolves to pkg/mod.py.
   2. `import pkg` where only pkg/__init__.py exists resolves to
      pkg/__init__.py.
   3. `from pkg import mod` where mod IS a module resolves to pkg/mod.py.
   4. `from pkg import VALUE` where VALUE is a symbol resolves to the package
      itself, pkg/__init__.py.
   5. `from . import mod` inside pkg/rel.py resolves to pkg/mod.py.
   6. `from .mod import VALUE` inside pkg/rel.py resolves to pkg/mod.py.
   7. `from ..a import z` inside pkg/rel.py resolves to a.py at the root.
   8. A relative import that climbs above the root (e.g. `from ... import x`
      in pkg/rel.py) lands in external, spelled with its leading dots.
   9. A two-file cycle (c1 imports c2, c2 imports c1): each file lists the
      other, and both calls return — assert the values, which is the
      termination proof.
  10. Unresolvable specifiers land in external with the source's own
      spelling: `import os` gives 'os', and `from typing import Iterable`
      gives 'typing.Iterable'. Pin both strings — this rendering is a
      deliberate contract choice, not an accident.
  11. A file with a SyntaxError gives parse_failed=True and two empty tuples.
  12. A path that does not exist gives parse_failed=True (unreadable source).
  13. A file that imports its own module name does not list itself in
      resolved.
  14. Duplicate imports of the same target appear once, and resolved comes
      back sorted (build a file importing two modules in reverse-alphabetical
      order and assert the sorted tuple).

  TS/JS — typescript_import_neighbors:
  15. `import {x} from './x'` resolves to the sibling x.ts.
  16. `import d from './dir'` resolves to dir/index.ts.
  17. `export {q} from './y'` resolves to y.tsx.
  18. `const c = require('./comp')` resolves to comp.jsx.
  19. A bare `import './side'` resolves to side.js.
  20. A non-relative specifier ('react') lands in external verbatim.
  21. Extension priority: when BOTH x.ts and x/index.ts exist, './x' resolves
      to x.ts. This is the case the mutation probe below must break.
  22. A relative specifier that climbs above the root ('../../escape') lands
      in external verbatim.
  23. A path that does not exist gives parse_failed=True.

  Graph — build_import_neighbor_graph:
  24. Over a mixed tree (.py + .ts + .md), keys are the deduplicated inputs in
      sorted order — pass a list with a duplicate and an unsorted order.
  25. Determinism: build twice over the same tree and assert the two dicts are
      equal.
  26. An unknown suffix (.md) gives ImportNeighbors((), (), parse_failed=True).

IF A TEST FAILS BECAUSE THE MODULE DEVIATES from the contract quoted above:
do NOT edit context_compiler.py to make it pass, and do not weaken the
assertion to match the code. Leave that single case out of the commit, record
it in the handoff's item-status table as `skipped` with the exact fixture and
the observed vs contracted value, and continue with the rest. That is a
finding for the reviewer, not a repair for you.

PROCEDURE (in order, one commit per item):
0. Preconditions: branch feature/f107-context-compiler-v2, HEAD 5a9951d5,
   `git status --porcelain` empty (else STOP and hand back).
1. C1 — `cp .remedy-wt/f107-r3-1.block.md .agent/authored/f107-r3-1.md`,
   cmp silent; extract BOTH slices (LR2, PLAN2) with a helper under
   .remedy-wt/ and verify each body's sha256 against its marker digest before
   applying anything.
   Commit: chore(f107): save the R3 step block verbatim
2. C2 — copy the same file over .agent/last_block.md, cmp silent.
   Commit: chore(f107): mirror the R3 block into last_block
3. C3 — apply LR2 to .agent/live_review.md. APPEND shape: the slice's first
   line IS the file's current last non-empty line (the FROM); replace that one
   line with the whole slice body, leaving everything above untouched.
   Proof: the FROM line occurs exactly 1x in the file after the edit; every
   TO-only line occurs exactly 1x among the lines this commit's diff ADDS;
   report `git show --numstat HEAD -- .agent/live_review.md` (a pure append
   reads `<n> 0` — zero deletions is what proves the FROM line unedited).
   Commit: chore(f107): record the R2 gate in live_review
4. C4 — replace .agent/plan.md entirely with slice PLAN2 (cp+cmp).
   Commit: chore(f107): advance plan to R3 T001 gate
5. C5 — write tests/orchestration/test_context_compiler.py per the test
   contract above. Read context_compiler.py first. Self-review loop before
   commit. Commit: test(f107): cover the import-neighbor graph layer
6. MUTATION PROBE (after C5 is committed, before C6). Destructive checks run
   ONLY in a disposable worktree — never in the checkout:
     git worktree add .remedy-wt/f107_r3_mut HEAD
   In that worktree only, edit packages/orchestration/context_compiler.py so
   the index-file candidates are tried BEFORE the suffix candidates in
   `_ts_resolve_relative` (swap the two `candidates +=` lines). Then run
     python3 -m pytest tests/orchestration/test_context_compiler.py -q
   from inside the worktree and REPORT the real result: exit code and which
   tests failed. Expectation is that case 21 goes red; if NOTHING fails, say
   so plainly — that is a true report about a test that does not bite, not a
   failure of yours. Then:
     git worktree remove --force .remedy-wt/f107_r3_mut
     git worktree prune
   and confirm `git worktree list` shows the primary checkout alone.
7. C6 — rewrite .agent/handoff.md yourself: feature+round (F107 R3), branch,
   per-commit table C1–C6, changed-files table, the real gate results below
   (command + exit code + counted value), the mutation-probe result, open
   findings count 8 / next free ID R-0271, item-status table, next expected
   action: R4 = T002 signature extractors. Cap: 60 lines, or up to 100 if the
   per-commit table needs it (AGENTS.md handoff.md rule) — never drop a
   mandated section to fit.
   Commit: chore(f107): rewrite handoff for R3
   Then: git push (branch already tracks origin)

Done when (run each, record command + real exit code + counted value):
  a. sha256 of both extracted slice bodies == their marker digests; cmp of
     .agent/authored/f107-r3-1.md against .remedy-wt/f107-r3-1.block.md and
     against .agent/last_block.md both silent.
  b. LR2 proof from step 3 (FROM 1x; each TO-only line 1x among added lines;
     numstat reported). grep -c '^## Steps' .agent/live_review.md → 1.
  c. cmp .agent/plan.md against the verified PLAN2 bytes → silent;
     wc -l < .agent/plan.md → 29.
  d. python3 -m pytest tests/orchestration/test_context_compiler.py -q
     → exit 0 (report the passed count).
  e. python3 -m pytest tests/cli/test_golden_path.py -q → exit 0 (report the
     passed count).
  f. grep -c '^<<<' on .agent/live_review.md, .agent/plan.md and
     .agent/handoff.md → 0 each (grep exit 1 is the pass; the authored file
     and last_block are excluded by construction).
  g. git status --porcelain → empty; git worktree list → primary only;
     HEAD == origin/feature/f107-context-compiler-v2; insertions per commit
     (git log --numstat 5a9951d5..HEAD) each < 500.
  h. git diff --name-only 5a9951d5..HEAD → exactly the six paths the Change
     line names, nothing else.
  i. the mutation-probe result from step 6, reported as run.
Handback:    completion report (tables + raw gate results a–i + deviations)
             — .agent/handoff.md rewritten as C6.

<<<BEGIN SLICE LR2 sha256=8b35a83cd0c01e01d14f9242227d39b1b5c5202e154ae3ad1ed8d4cf9af54dc3 lines=38>>>
  discharged. `LAST_REVIEWED_SHA` advances 2e4142c3 -> d2b962af.

- Reviewer gate on R2 (2026-08-12): PASS, partial round — `.agent/STOP`
  truncated it after the module commit and the worker declared the truncation
  (guardrail G6, docs/agents/self_drive_protocol.md). Range d2b962af..5a9951d5
  is six commits touching six of the seven paths the R2 block named; the
  seventh, tests/orchestration/test_context_compiler.py, is the declared skip.
  Transport by the primary shape: `cmp` of the surviving reviewer original
  `.remedy-wt/f107-r2-1.block.md` against the committed
  `.agent/authored/f107-r2-1.md` is silent, and so is the authored copy
  against `.agent/last_block.md` — all three 182 lines. Both slice bodies
  recompute to their BEGIN-marker digests, the PLAN body is byte-equal to
  `.agent/plan.md`, and the LRAPP body is the verbatim tail of this file. That
  pair was APPEND-shaped and `git show --numstat 72d79079` reads `19 0`: zero
  deletions, which proves the FROM line was never edited. Every scoped gate
  was RE-RUN by the reviewer instead of read from the handback — the canary
  `python3 -m pytest tests/cli/test_golden_path.py -q` returns 42 passed,
  `grep -c` for the Steps heading is 1, `.agent/plan.md` is 28 lines,
  `git status --porcelain` is empty, `git worktree list` shows the primary
  checkout alone, and HEAD equals `origin/feature/f107-context-compiler-v2`.
  Insertions per commit 182, 155, 19, 10, 302, 49 — each under 500. Gate d
  could not run at all, because the round's own test module is the missing
  seventh path: `packages/orchestration/context_compiler.py` is REVIEWED AND
  PROBED BUT NOT GATED. The reviewer probe, on a throwaway fixture tree under
  `.remedy-wt/`, reproduced every case the T001 contract names — absolute
  import, from-module against from-symbol, single- and double-dot relative,
  two-file cycle terminating, stdlib to external, SyntaxError and missing file
  to parse_failed, no self-listing, './x' beating an x/index.ts sibling,
  './dir' to dir/index.ts, export-from, require(), .tsx and .jsx, 'react'
  external, an escaping specifier external, and a graph that is sorted,
  deduplicated, twice-equal and parse_failed on an unknown suffix — but a
  reviewer probe is not committed evidence and this file does not treat it as
  any. R3 commits that test module and R3's gate d is what certifies the
  module; until it is green, no verdict here claims T001 is test-covered.
  Recorded as an observation and not a finding: the R2 handoff is 62 lines
  where the R2 block asked for 60, which AGENTS.md permits outright for a
  per-commit table of more than five commits, and this one has six.
  `LAST_REVIEWED_SHA` advances d2b962af -> 5a9951d5.
<<<END SLICE LR2>>>

<<<BEGIN SLICE PLAN2 sha256=e90affa10f509626c53b04eb8fec5f6c9d816a32137f834c326249bece132d13 lines=29>>>
# Plan — F107 Context compiler v2

Branch: feature/f107-context-compiler-v2, cut from main at 2e4142c3.
Next free finding ID: R-0271. R2 reviewed PASS at 5a9951d5.

## Goal
The context compiler selects fenced-path files, their direct import
neighbors, and only SIGNATURES of distant dependencies, under a total
context token budget with tier demotion — and writes an omissions record
naming everything it left out and why. DONE when a fixture repo's task
context shrinks measurably versus whole-files with the fixture task still
solvable by the fake provider, and the omissions record explains every
exclusion (docs/roadmap/features/T2_F107.md).

## Current Step
R3 — close the T001 gate: unit tests for the import-neighbor graph layer in
tests/orchestration/test_context_compiler.py over tmp_path fixture trees
(cycles, relative imports, index files, extension priority, unknown suffix),
plus a mutation probe in a disposable worktree proving the extension-priority
case bites. packages/orchestration/context_compiler.py is read-only in this
round.

## Next Steps
1. T002 — signature extractors for both languages + size caps + goldens.
2. T003 — tiered selector + budget demotion + omissions writer +
   integration on a fixture repo.
3. T004 — segment integration + the `remedy job context` CLI view +
   an end-to-end fixture task with a size comparison in evidence.
4. Integration gate, then closure per STATUS_closure_protocol.md.
<<<END SLICE PLAN2>>>
