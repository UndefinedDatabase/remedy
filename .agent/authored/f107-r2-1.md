── STEP R2/~10 — F107 Context compiler v2 — T001 import-neighbor graphs ──────
Goal:        Build the import-neighbor graph layer of the context compiler:
             Python via ast, TS/JS via a documented line-level scanner, with
             unit tests on fixture trees. Record the R1 gate first.
Bundle:      C1 authored-block save; C2 last_block mirror; C3 R1 gate entry
             into live_review (authored append); C4 plan rewrite;
             C5 packages/orchestration/context_compiler.py (T001 slice);
             C6 tests/orchestration/test_context_compiler.py;
             C7 handoff rewrite; push; handback.
Change:      EXACTLY these paths and nothing else:
             .agent/authored/f107-r2-1.md (new), .agent/last_block.md,
             .agent/live_review.md (append pair LRAPP),
             .agent/plan.md (full replacement PLAN),
             packages/orchestration/context_compiler.py (new),
             tests/orchestration/test_context_compiler.py (new),
             .agent/handoff.md (your handback rewrite).
Constraints: AGENTS.md in full. Read docs/roadmap/features/T2_F107.md before
             coding — its tier table is the feature contract (verbatim below).
             STDLIB ONLY: ast, re, pathlib, dataclasses, typing — a diff
             adding any TS parser or other dependency is rejected by the
             feature file's orchestrator brief. Do not touch prompt
             composition, the segment registry, or any existing module.
             Never write a `Done:` line in live_review. Do NOT create a PR.
             Never touch main. Scratch only under .remedy-wt/, uncommitted.
             Apply authored slices byte for byte after sha256 verification
             (extraction helper pattern from R1 is fine); on mismatch STOP.

TIER TABLE (the feature contract — T001 builds the graph that feeds it):
  (1) files matched by the task's files_hint and fence allow scope — full
      content; (2) direct import neighbors of tier 1 — full content up to a
      per-file size cap, else signatures; (3) transitive dependencies —
      signatures only; (4) everything else — omitted.

T001 CONTRACT (public names; Code Discoverability Conventions apply):
  Module packages/orchestration/context_compiler.py, module docstring naming
  the heuristic honestly: the TS/JS scanner is line-level regex, it does not
  parse; multi-line import statements, dynamic import() expressions and
  commented-out imports are documented limitations for v1.
  - @dataclass(frozen=True) ImportNeighbors:
      resolved: tuple[str, ...]   # repo-relative POSIX paths, sorted, deduped
      external: tuple[str, ...]   # unresolved specifiers/modules, sorted, deduped
      parse_failed: bool = False  # True when the source could not be parsed
  - python_import_neighbors(root: Path, rel_path: str) -> ImportNeighbors
      ast-based. Resolves: `import a.b` → a/b.py or a/b/__init__.py;
      `from pkg import name` → pkg/name.py or pkg/name/__init__.py when that
      file exists, else the pkg module itself (pkg/__init__.py or pkg.py);
      relative imports (from . import x / from ..p import y) resolved against
      the importing file's package. A specifier that resolves to no file
      under root goes to external. SyntaxError → parse_failed=True, empty
      tuples. The importing file itself never appears in its own resolved.
  - typescript_import_neighbors(root: Path, rel_path: str) -> ImportNeighbors
      line-level regex over: import ... from '<spec>' / "<spec>",
      bare import '<spec>', export ... from '<spec>', require('<spec>').
      Only relative specifiers (./ or ../) are resolved: exact path first,
      then +.ts/.tsx/.js/.jsx, then <spec>/index.(ts|tsx|js|jsx), first hit
      wins in that order. Non-relative specifiers go to external verbatim.
      Unreadable file → parse_failed=True.
  - build_import_neighbor_graph(root: Path, rel_paths: Iterable[str])
      -> dict[str, ImportNeighbors]
      dispatches on suffix (.py → python, .ts/.tsx/.js/.jsx → typescript,
      anything else → ImportNeighbors((), (), parse_failed=True)); pure
      per-file computation, so cyclic imports terminate by construction.
  Determinism: all outputs sorted tuples; same tree → same graph.

TESTS (C6, tests/orchestration/test_context_compiler.py, fixture trees via
tmp_path — the feature file names cycles, relative imports and index files):
  Python: absolute import of a module; from-import where the name IS a
  module vs where it is a symbol of the package; single- and double-dot
  relative imports; a two-file import cycle (each lists the other; the call
  terminates); stdlib/third-party specifier lands in external; a
  SyntaxError file reports parse_failed=True; the file never lists itself.
  TS/JS: './x' resolving to x.ts; './dir' resolving to dir/index.ts;
  export-from; require(); a .tsx/.jsx resolution; a non-relative specifier
  ('react') in external; extension priority (x.ts beats x/index.ts).
  Graph: build_import_neighbor_graph over a mixed fixture tree returns
  sorted, deterministic output (build twice, compare equal); unknown suffix
  → parse_failed.

PROCEDURE (in order, one commit per item):
0. Preconditions: branch feature/f107-context-compiler-v2, HEAD d2b962af,
   `git status --porcelain` empty (else STOP and hand back).
1. C1 — `cp .remedy-wt/f107-r2-1.block.md .agent/authored/f107-r2-1.md`,
   cmp silent; verify BOTH slices (LRAPP, PLAN) sha256 against their marker
   digests before applying anything.
   Commit: chore(f107): save the R2 step block verbatim
2. C2 — copy over .agent/last_block.md, cmp silent.
   Commit: chore(f107): mirror the R2 block into last_block
3. C3 — apply LRAPP to .agent/live_review.md. APPEND shape: the slice's
   first line IS the file's current last non-empty line (the FROM); replace
   that line with the whole slice, leaving everything above untouched.
   Proof: the FROM line occurs exactly 1x in the file after the edit; every
   one of the 19 TO-only lines occurs exactly 1x among the lines this
   commit's diff ADDS (`git show --numstat HEAD -- .agent/live_review.md`
   reports the totals; report them).
   Commit: chore(f107): record the R1 gate in live_review
4. C4 — replace .agent/plan.md entirely with slice PLAN (cp+cmp).
   Commit: chore(f107): advance plan to R2 T001
5. C5 — write packages/orchestration/context_compiler.py per the T001
   contract above. Self-review loop before commit.
   Commit: feat(f107): import-neighbor graphs for python and ts
6. C6 — write tests/orchestration/test_context_compiler.py per the test
   list above. Commit: test(f107): cover the import-neighbor graph layer
7. C7 — rewrite .agent/handoff.md yourself (≤60 lines): feature+round
   (F107 R2), branch, per-commit table C1–C7, changed-files table, the real
   gate results below (command + exit code + counted value), open findings
   count 8 / next free ID R-0271, item-status table, next expected action:
   R3 = T002 signature extractors.
   Commit: chore(f107): rewrite handoff for R2
   Then: git push (branch already tracks origin)

Done when (run each, record command + real exit code + counted value):
  a. sha256 of both extracted slices == marker digests; cmp authored vs
     last_block silent.
  b. LRAPP proof from step 3 (FROM 1x; 19 TO-only lines 1x among added;
     numstat reported). grep -c '^## Steps' .agent/live_review.md → 1.
  c. cmp .agent/plan.md vs the verified PLAN bytes → silent;
     wc -l < .agent/plan.md → 28.
  d. python3 -m pytest tests/orchestration/test_context_compiler.py -q
     → exit 0 (report the passed count).
  e. python3 -m pytest tests/cli/test_golden_path.py -q → exit 0.
  f. grep -c '^<<<' on live_review.md, plan.md, handoff.md → 0 each
     (grep exit 1 is the pass; authored file and last_block excluded).
  g. git status --porcelain → empty; HEAD == origin; insertions per commit
     (git log --numstat d2b962af..HEAD) each < 500.
  h. git diff --name-only d2b962af..HEAD → exactly the seven paths the
     Change line names, nothing else.
Handback:    completion report (tables + raw gate results a–h + deviations)
             — .agent/handoff.md rewritten as C7.

<<<BEGIN SLICE LRAPP sha256=4bdd5a51873414bdc0cdff77fceecf099b97672b007f7f0b8723cc5935d0e52f lines=20>>>
docs/roadmap/STATUS_closure_protocol.md.

- Reviewer gate on R1 (2026-08-12): PASS. Range 2e4142c3..d2b962af = eight
  commits touching exactly the eight paths the R1 block named — no production
  code, no test module, no docs beyond the one STATUS.md line. Transport by
  the primary shape: `cmp` of every applied state file against the reviewer's
  surviving `.remedy-wt/` originals silent; the block original, the committed
  `.agent/authored/f107-r1-1.md` and `.agent/last_block.md` byte-identical at
  274 lines. The claim commit's numstat for STATUS.md reads `1 1`, the TO line
  counts 1x and the FROM 0x after the edit. Every scoped gate was RE-RUN by
  the reviewer instead of read from the handback: `python3 -m pytest
  tests/docs/ -q` returns 294 passed, the canary
  `python3 -m pytest tests/cli/test_golden_path.py -q` returns 42 passed,
  `grep -c '^## Steps'` is 1 and `grep -c '^<<<'` is 0 across the five state
  files, `.agent/plan.md` is 29 lines, `git status --porcelain` is empty,
  `git worktree list` shows the primary checkout alone, and HEAD equals
  `origin/feature/f107-context-compiler-v2`. Insertions per commit 274, 265,
  1, 62, 2, 22, 30, 53 — each under 500. R-0270 is registered and
  `.agent/candidates.md` is empty, so the feature-claim block condition is
  discharged. `LAST_REVIEWED_SHA` advances 2e4142c3 -> d2b962af.
<<<END SLICE LRAPP>>>

<<<BEGIN SLICE PLAN sha256=00a665116442f223f7977d4d30d42c2b972f1202e7af3c582b5c8247e2cb5fb8 lines=28>>>
# Plan — F107 Context compiler v2

Branch: feature/f107-context-compiler-v2, cut from main at 2e4142c3.
Next free finding ID: R-0271. R1 reviewed PASS at d2b962af.

## Goal
The context compiler selects fenced-path files, their direct import
neighbors, and only SIGNATURES of distant dependencies, under a total
context token budget with tier demotion — and writes an omissions record
naming everything it left out and why. DONE when a fixture repo's task
context shrinks measurably versus whole-files with the fixture task still
solvable by the fake provider, and the omissions record explains every
exclusion (docs/roadmap/features/T2_F107.md).

## Current Step
R2 — T001 import-neighbor graphs: Python via ast, TS/JS via the
documented line-level scanner, in
packages/orchestration/context_compiler.py, with unit tests on fixture
trees (cycles, relative imports, index files) in
tests/orchestration/test_context_compiler.py.

## Next Steps
1. T002 — signature extractors for both languages + size caps + goldens.
2. T003 — tiered selector + budget demotion + omissions writer +
   integration on a fixture repo.
3. T004 — segment integration + the `remedy job context` CLI view +
   an end-to-end fixture task with a size comparison in evidence.
4. Integration gate, then closure per STATUS_closure_protocol.md.
<<<END SLICE PLAN>>>
