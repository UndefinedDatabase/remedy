── STEP R4/~10 — F107 Context compiler v2 — T002 signature extractors ────────
Goal:        Add the signature layer to the context compiler: Python via ast,
             TS/JS via the exported-line scanner, plus the per-file size cap
             that decides full content against signatures, with goldens per
             language. Record the R3 gate and clear finding R-0271.
Bundle:      C1 authored-block save; C2 last_block mirror; C3 the two authored
             live_review slices (LRF registers R-0271 under Findings, LR3
             appends the R3 gate); C4 plan rewrite; C5 the R-0271 lint fix;
             C6 the T002 code; C7 the tests and goldens; C8 handoff rewrite;
             push; handback.
Change:      EXACTLY these paths and nothing else:
             .agent/authored/f107-r4-1.md (new), .agent/last_block.md,
             .agent/live_review.md (authored pairs LRF and LR3 in C3, plus
             your own one-line Landed marker in C5),
             .agent/plan.md (full replacement PLAN3),
             packages/orchestration/context_compiler.py,
             tests/orchestration/test_context_compiler.py,
             .agent/handoff.md (your handback rewrite).
Constraints: AGENTS.md in full. The T001 layer is FROZEN: ImportNeighbors,
             python_import_neighbors, typescript_import_neighbors and
             build_import_neighbor_graph keep their current behavior and their
             existing 16 tests keep passing unchanged. You ADD to the module;
             you do not restructure it. STDLIB ONLY (ast, re, pathlib,
             dataclasses, collections.abc) — a diff adding a TS parser or any
             other dependency is rejected by the feature file's orchestrator
             brief. Do not touch prompt composition, the segment registry, or
             any other module. Never write a `Done:` line in live_review —
             only the `Landed:` line C5 specifies. Do NOT create a PR. Never
             touch main. Scratch only under .remedy-wt/, uncommitted. Apply
             authored slices byte for byte after sha256 verification; on
             mismatch STOP.

TIER TABLE (the feature contract — T002 builds the signature rendering the
tiers demote to): (1) files matched by the task's files_hint and fence allow
scope — full content; (2) direct import neighbors of tier 1 — full content up
to a per-file size cap, else signatures; (3) transitive dependencies —
signatures only; (4) everything else — omitted.

T002 CONTRACT (public names; Code Discoverability Conventions apply).
In this contract TQ means three double-quote characters in a row.

  Module constants:
    DEFAULT_INLINE_SIZE_CAP_BYTES = 16384
    DEFAULT_SIGNATURE_LINE_CAP = 200

  @dataclass(frozen=True) FileSignatures:
    lines: tuple[str, ...] = ()   # rendered signature lines, in source order
    truncated: bool = False       # True when the line cap cut the rendering
    parse_failed: bool = False    # source unreadable or unparseable

  fits_inline_size_cap(root, rel_path, cap_bytes=DEFAULT_INLINE_SIZE_CAP_BYTES)
      -> bool. True when the file exists and its size in BYTES is <= cap_bytes
      (equal to the cap fits). A path that is not a file is False — it cannot
      be inlined. This is the tier-2 demotion switch, nothing more.

  python_file_signatures(root, rel_path, line_cap=DEFAULT_SIGNATURE_LINE_CAP)
      -> FileSignatures. ast-based, source order, one rendered line per entry:
      * the module docstring's first non-empty line, wrapped in TQ on each
        side, when the module has a docstring;
      * every ClassDef, FunctionDef and AsyncFunctionDef at ANY nesting depth,
        rendered as a header line ending in a colon, indented four spaces per
        level of nesting below module level;
      * directly after each such header, that node's docstring first non-empty
        line wrapped in TQ on each side, indented four spaces deeper than its
        own header.
      Header rendering is RECONSTRUCTED from the ast, never copied from the
      source, so a signature spread over several source lines collapses to
      one: `class Name(Base1, Base2):`, or `class Name:` when there are no
      bases (no empty parentheses); `def name(<args>) -> <ret>:` and
      `async def name(<args>) -> <ret>:`, with ` -> <ret>` omitted when there
      is no return annotation. Render `<args>` with `ast.unparse` of the
      node's arguments node, and `<ret>` with `ast.unparse` of the annotation.
      Decorators, bodies, imports and assignments NEVER appear.
      Unreadable source or SyntaxError → parse_failed=True with empty lines.
      When the rendering exceeds line_cap lines, keep the FIRST line_cap of
      them and set truncated=True.

  typescript_file_signatures(root, rel_path, line_cap=DEFAULT_SIGNATURE_LINE_CAP)
      -> FileSignatures. Line-level regex, source order, one entry per source
      line whose FIRST non-space characters are the word `export` (so
      `export function`, `export default`, `export const|let|var`,
      `export class`, `export abstract class`, `export async function`,
      `export interface`, `export type`, `export {…} from …` and
      `export * from …` all match, while a non-exported declaration and a line
      where `export` appears mid-line do not).
      Rendering, deliberately minimal so it stays predictable: strip leading
      and trailing whitespace, then remove a TRAILING `{` together with any
      whitespace before it. Nothing else is rewritten — no cutting mid-line,
      no trailing semicolon removal. Unreadable file → parse_failed=True.
      Same line_cap and truncated semantics as the Python extractor.

  extract_file_signatures(root, rel_path, line_cap=DEFAULT_SIGNATURE_LINE_CAP)
      -> FileSignatures. Dispatches on suffix exactly like
      build_import_neighbor_graph does: .py → Python, .ts/.tsx/.js/.jsx →
      TS/JS, anything else → FileSignatures(parse_failed=True).

  Determinism: same file → same rendered tuple, always.
  Update the module docstring's Public API list with the new names, and say in
  it that the TS signature scanner shares the line-level heuristic limitations
  already documented there.

TEST CONTRACT (C7) — append to tests/orchestration/test_context_compiler.py,
leaving every existing test untouched. Goldens are module-level string
constants in that file, compared with exact tuple equality — the repo's
in-test golden convention (tests/orchestration/test_builder_prompt_golden.py).

  Python goldens and behavior:
   1. One golden fixture source exercising, in one file: a module docstring,
      a decorated top-level `def` with annotated args and a return annotation,
      an `async def`, a `class` with a base and a docstring, a method nested
      in that class, a signature written across THREE source lines, a
      module-level assignment and an import. Assert `lines` equals the golden
      tuple exactly. The golden therefore pins: decorators absent, assignment
      and import absent, the three-line signature collapsed to one, and the
      four-space indentation of the nested method and of docstring lines.
   2. A class with no bases renders `class Name:` — no empty parentheses.
   3. A def with no return annotation renders without ` -> `.
   4. A docstring whose first source line is blank contributes its first
      NON-EMPTY line.
   5. A file with no docstrings anywhere renders headers only.
   6. SyntaxError → parse_failed=True and empty lines; a missing path → the
      same.
   7. line_cap: a file rendering more than the cap returns exactly `line_cap`
      lines with truncated=True, and those are the FIRST ones; the same file
      under a generous cap returns truncated=False.

  TS/JS goldens and behavior:
   8. One golden fixture source exercising `export function` with a trailing
      `{`, `export default`, `export const`, `export class X extends Y {`,
      `export interface`, `export type`, `export async function`,
      `export * from './x';`, `export {a, b} from './y';`, an INDENTED
      `  export const nested = 1;`, a non-exported `function hidden() {`, and
      a line where the word `export` appears mid-line. Assert `lines` equals
      the golden tuple exactly — pinning that the trailing `{` is removed, the
      trailing semicolon is kept, indentation is stripped, and neither the
      non-exported line nor the mid-line `export` appears.
   9. A missing path → parse_failed=True.
  10. The TS extractor honors line_cap and truncated the same way.

  Size cap and dispatch:
  11. fits_inline_size_cap is True below the cap, True at EXACTLY the cap,
      False above it, and False for a path that does not exist. Size the
      fixtures in bytes and pass an explicit small cap_bytes.
  12. DEFAULT_INLINE_SIZE_CAP_BYTES and DEFAULT_SIGNATURE_LINE_CAP are the
      documented defaults (assert the values, so a silent change is a red
      test).
  13. extract_file_signatures dispatches .py to the Python extractor, .ts and
      .jsx to the TS one, and an unknown suffix (.md) to
      FileSignatures(parse_failed=True) — assert the dispatch by comparing
      against the direct call on the same fixture.

IF THE CODE AND THIS CONTRACT DISAGREE while you are writing the tests, the
contract wins and you change the code you wrote in C6 — it is yours this
round. What you must NOT do is weaken an assertion to match a rendering you
find convenient, or change any T001 behavior to make a new test pass.

PROCEDURE (in order, one commit per item):
0. Preconditions: branch feature/f107-context-compiler-v2, HEAD ef64cf72,
   `git status --porcelain` empty (else STOP and hand back).
1. C1 — `cp .remedy-wt/f107-r4-1.block.md .agent/authored/f107-r4-1.md`,
   cmp silent; extract ALL THREE slices (LRF, LR3, PLAN3) with a helper under
   .remedy-wt/ and verify each body's sha256 against its marker digest before
   applying anything.
   Commit: chore(f107): save the R4 step block verbatim
2. C2 — copy the same file over .agent/last_block.md, cmp silent.
   Commit: chore(f107): mirror the R4 block into last_block
3. C3 — apply BOTH live_review slices in this one commit. Each is an
   anchor-preserving insertion: the slice's FIRST line already exists in the
   file (the FROM) and the slice's TO contains it verbatim, so you replace
   that one line with the whole slice body and touch nothing else.
     * LRF — its FROM is the LAST line of the `## Findings` list, so R-0271
       is registered as a finding among the findings, not in the gate log.
     * LR3 — its FROM is the file's current LAST non-empty line, so the R3
       gate entry lands at the end of the gate log.
   Apply LRF first, then LR3; each FROM occurs exactly once in the file both
   before and after the edit. Proof: after the commit, each of the two FROM
   lines occurs exactly 1x in the file, every TO-only line of both slices
   occurs exactly 1x among the lines this commit's diff ADDS, and
   `git show --numstat HEAD -- .agent/live_review.md` reads `<n> 0` — zero
   deletions is what proves both anchors unedited. Report n.
   Commit: chore(f107): record the R3 gate and register R-0271
4. C4 — replace .agent/plan.md entirely with slice PLAN3 (cp+cmp).
   Commit: chore(f107): advance plan to R4 T002
5. C5 — fix finding R-0271: in packages/orchestration/context_compiler.py
   replace the `Iterable` import from `typing` with an import from
   `collections.abc` (ruff UP035), leaving every other line alone. Keep the
   import block sorted the way ruff's isort rules want it. Then append to
   .agent/live_review.md, as the file's new last line, exactly one line of
   your own authorship in this form — no other text, no `Done:`:
     Landed: R-0271 — Iterable now imports from collections.abc (this commit).
   Commit: fix(f107): import Iterable from collections abc
6. C6 — extend packages/orchestration/context_compiler.py with the T002
   contract above. Read the whole file first; self-review loop before commit.
   Commit: feat(f107): signature extractors and the inline size cap
7. C7 — extend tests/orchestration/test_context_compiler.py per the test
   contract above. Commit: test(f107): golden signature rendering per language
8. MUTATION PROBE (after C7 is committed, before C8). Destructive checks run
   ONLY in a disposable worktree — never in the checkout:
     git worktree add .remedy-wt/f107_r4_mut HEAD
   In that worktree only, make the TS renderer STOP removing the trailing `{`
   (leave the stripped line as it is). Then run
     python3 -m pytest tests/orchestration/test_context_compiler.py -q
   from inside the worktree and REPORT the real result: exit code and which
   tests failed. If NOTHING fails, say so plainly — a true report about a
   golden that does not bite is worth more than a colour. Then:
     git worktree remove --force .remedy-wt/f107_r4_mut
     git worktree prune
   and confirm `git worktree list` shows the primary checkout alone.
9. C8 — rewrite .agent/handoff.md yourself: feature+round (F107 R4), branch,
   per-commit table C1–C8, changed-files table, the real gate results below
   (command + exit code + counted value), the mutation-probe result, open
   findings count and next free ID (R-0271 is registered by C3 and landed by
   C5, but only the reviewer's `Done:` text resolves it, so it stays OPEN:
   9 open, next free R-0272), item-status table, next expected action:
   R5 = T003 tiered selector with budget demotion and the omissions writer.
   Cap: 60 lines, or up to 100 if the per-commit table needs it (AGENTS.md
   handoff.md rule) — never drop a mandated section to fit; if you exceed 60,
   carry the stated-cause line naming the actual count and the mandated
   content that caused it.
   Commit: chore(f107): rewrite handoff for R4
   Then: git push (branch already tracks origin)

Done when (run each, record command + real exit code + counted value):
  a. sha256 of all three extracted slice bodies == their marker digests; cmp
     of .agent/authored/f107-r4-1.md against .remedy-wt/f107-r4-1.block.md and
     against .agent/last_block.md both silent.
  b. the C3 proof from step 3 (both FROM lines 1x; every TO-only line 1x among
     added lines; numstat reported). grep -c '^## Steps' .agent/live_review.md
     → 1.
  c. cmp .agent/plan.md against the verified PLAN3 bytes → silent;
     wc -l < .agent/plan.md → 29.
  d. python3 -m pytest tests/orchestration/test_context_compiler.py -q
     → exit 0 (report the passed count, which includes the 16 T001 tests).
  e. python3 -m pytest tests/cli/test_golden_path.py -q → exit 0 (report the
     passed count).
  f. grep -c '^<<<' on .agent/live_review.md, .agent/plan.md and
     .agent/handoff.md → 0 each (grep exit 1 is the pass).
  g. git status --porcelain → empty; git worktree list → primary only;
     HEAD == origin/feature/f107-context-compiler-v2; insertions per commit
     (git log --numstat ef64cf72..HEAD) each < 500.
  h. git diff --name-only ef64cf72..HEAD → exactly the seven paths the Change
     line names, nothing else.
  i. python3 -m ruff check packages/orchestration/context_compiler.py
     tests/orchestration/test_context_compiler.py → exit 0, zero errors
     (this is what closes R-0271; report the real output).
  j. the mutation-probe result from step 8, reported as run.
Handback:    completion report (tables + raw gate results a–j + deviations)
             — .agent/handoff.md rewritten as C8.

<<<BEGIN SLICE LRF sha256=fac600cb0c03ce265017a2eeda5336fe617bbb2acecf99764bc87c37b98ab5c2 lines=7>>>
  together — it is neither F107's code nor F107's scope. OPEN.
- R-0271 (Low, F107 R3): `packages/orchestration/context_compiler.py` imports
  `Iterable` from `typing`, which ruff reports as UP035. The repo's ruff
  baseline already carries 24 other errors, so no gate turns red and nothing
  is blocked — but this one is F107's own new code, it is one line, and the
  module is open for editing in R4 anyway, so it is cheaper to clear than to
  carry. OPEN.
<<<END SLICE LRF>>>

<<<BEGIN SLICE LR3 sha256=1dc20c0b9bc0fed30d125f077c3dc004a097a278b9240dadeb8eb6b179f272da lines=33>>>
  `LAST_REVIEWED_SHA` advances d2b962af -> 5a9951d5.

- Reviewer gate on R3 (2026-08-12): PASS. Range 5a9951d5..ef64cf72 = six
  commits touching exactly the six paths the R3 block named. Transport by the
  primary shape: `cmp` of the reviewer original `.remedy-wt/f107-r3-1.block.md`
  against the committed `.agent/authored/f107-r3-1.md` silent, and the authored
  copy against `.agent/last_block.md` silent, all 232 lines; both slice bodies
  recompute to their BEGIN-marker digests, PLAN2 is byte-equal to
  `.agent/plan.md` and LR2 is the verbatim tail of this file. The LR2 pair was
  APPEND-shaped and `git show --numstat 0dbdaa83` reads `37 0` — zero
  deletions. No worker-authored `Done:` line exists in this file. Gates were
  RE-RUN by the reviewer rather than read from the handback: the T001 gate
  `python3 -m pytest tests/orchestration/test_context_compiler.py -q` returns
  16 passed, the canary returns 42 passed, `.agent/plan.md` is 29 lines, the
  Steps heading count is 1, `git status --porcelain` is empty and
  `git worktree list` shows the primary checkout alone. Insertions per commit
  232, 189, 37, 7, 274, 63 — each under 500. The 16 test functions carry all
  26 numbered obligations of the R3 contract, each as an equality assertion on
  real values rather than a truthiness check, and the deliberate external
  renderings ('os', 'typing.Iterable', '...x', '../../escape', 'react') are
  pinned verbatim. The reviewer ran TWO independent mutation probes in a
  disposable worktree at ef64cf72, one of them deliberately different from the
  worker's: removing the self-discard line reddens exactly
  `test_python_file_importing_its_own_module_name_does_not_list_itself`, and
  swapping the TS candidate order reproduces the worker's reported failure
  `AssertionError: assert ('x/index.ts',) == ('x.ts',)` in
  `test_typescript_suffix_candidate_beats_index_file_candidate` — so the
  handback's probe evidence is confirmed true and the goldens bite. That
  worktree was removed and pruned before this verdict. The 75-line handoff is
  a declared stated-cause overage carrying its mandated tables, which
  AGENTS.md permits for a per-commit table of more than five commits. T001 is
  now test-covered on the branch and the R2 ungated-module caveat is
  discharged. `LAST_REVIEWED_SHA` advances 5a9951d5 -> ef64cf72.
<<<END SLICE LR3>>>

<<<BEGIN SLICE PLAN3 sha256=4b98f1085f506a5f5d26710b978ae5498a682b1c31300c32f1706331dfb86149 lines=29>>>
# Plan — F107 Context compiler v2

Branch: feature/f107-context-compiler-v2, cut from main at 2e4142c3.
Next free finding ID: R-0272. R3 reviewed PASS at ef64cf72.

## Goal
The context compiler selects fenced-path files, their direct import
neighbors, and only SIGNATURES of distant dependencies, under a total
context token budget with tier demotion — and writes an omissions record
naming everything it left out and why. DONE when a fixture repo's task
context shrinks measurably versus whole-files with the fixture task still
solvable by the fake provider, and the omissions record explains every
exclusion (docs/roadmap/features/T2_F107.md).

## Current Step
R4 — T002 signature extractors: Python headers and docstring first lines via
ast, TS/JS exported-line rendering, the per-file inline size cap that decides
full content against signatures, and a suffix dispatcher, all added to
packages/orchestration/context_compiler.py with per-language goldens in
tests/orchestration/test_context_compiler.py. The T001 layer is frozen. The
round also clears finding R-0271 (ruff UP035 in the same module).

## Next Steps
1. T003 — tiered selector + budget demotion + omissions writer +
   integration on a fixture repo.
2. T004 — segment integration + the `remedy job context` CLI view +
   an end-to-end fixture task with a size comparison in evidence.
3. Integration gate per docs/agents/integration_gate.md.
4. Closure per docs/roadmap/STATUS_closure_protocol.md.
<<<END SLICE PLAN3>>>
