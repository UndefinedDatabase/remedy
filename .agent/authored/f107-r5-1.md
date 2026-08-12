── STEP R5/~10 — F107 Context compiler v2 — T003 tiered selector ─────────────
Goal:        Add the SELECTOR layer: assign every candidate path a tier, render
             tier 1/2 full and tier 2/3 as signatures, enforce a total token
             budget by demotion (never by mid-file truncation), and record every
             demotion and omission with a reason. Record the R4 gate and resolve
             finding R-0271.
Bundle:      C1 authored-block save; C2 last_block mirror; C3 the two authored
             live_review pairs (FIX1 flips the R-0271 bullet to RESOLVED, LR4
             replaces the Landed line with the reviewer `Done:` text plus the R4
             gate entry); C4 plan rewrite; C5 the T003 code; C6 the tests;
             C7 handoff rewrite; push; handback.
Change:      EXACTLY these paths and nothing else:
             .agent/authored/f107-r5-1.md (new), .agent/last_block.md,
             .agent/live_review.md (authored pairs FIX1 and LR4 in C3 only),
             .agent/plan.md (full replacement PLAN4),
             packages/orchestration/context_compiler.py,
             tests/orchestration/test_context_compiler.py,
             .agent/handoff.md (your handback rewrite).
Constraints: AGENTS.md in full. T001 AND T002 ARE FROZEN: ImportNeighbors,
             python_import_neighbors, typescript_import_neighbors,
             build_import_neighbor_graph, FileSignatures, fits_inline_size_cap,
             python_file_signatures, typescript_file_signatures and
             extract_file_signatures keep their current behavior and their
             existing 29 tests keep passing UNCHANGED. You ADD to the module;
             you do not restructure it and you do not edit one existing test.
             Stdlib only, plus exactly ONE intra-repo import:
             `from packages.orchestration.token_economy import
             estimate_text_tokens` — reuse the repo's named token estimator
             rather than inventing a second spelling of the same concept
             (AGENTS.md Code Discoverability Conventions, "one spelling per
             concept"; that function is ceil(chars/4), estimates-only, and its
             module makes no provider, network or subprocess call). A diff
             adding a TS parser or any third-party dependency is rejected by
             the feature file's orchestrator brief. Do not touch prompt
             composition, the segment registry, or any other module. Never
             write a `Done:` line — C3's Done text is reviewer-authored and you
             apply it byte for byte; you author no resolution of your own. Do
             NOT create a PR. Never touch main. Scratch only under .remedy-wt/,
             uncommitted. Apply authored slices byte for byte after sha256
             verification; on mismatch STOP.

TIER TABLE (the feature contract, verbatim — the tiers ARE the contract):
(1) files matched by the task's files_hint and fence allow scope — full
content; (2) direct import neighbors of tier 1 — full content up to a per-file
size cap, else signatures; (3) transitive dependencies — signatures only;
(4) everything else — omitted.

T003 CONTRACT (public names; Code Discoverability Conventions apply).

  Module constants:
    DEFAULT_CONTEXT_TOKEN_BUDGET = 24000
    TIER_FENCED = 1
    TIER_NEIGHBOR = 2
    TIER_DISTANT = 3
    TIER_OMITTED = 4
    OMISSION_REASON_BUDGET = "budget"
    OMISSION_REASON_DISTANCE = "distance"
    OMISSION_REASON_BINARY = "binary"
    OMISSION_REASON_SIZE = "size"

  @dataclass(frozen=True) SelectedFile:
    rel_path: str
    tier: int
    rendering: str          # "full" or "signatures"
    estimated_tokens: int

  @dataclass(frozen=True) OmissionRecord:
    rel_path: str
    tier: int               # the tier the file HELD when the decision was made
    reason: str             # one of the four OMISSION_REASON_* values
    outcome: str            # "omitted" or "signatures"

  @dataclass(frozen=True) CompiledContext:
    included: tuple[SelectedFile, ...]      # sorted by (tier, rel_path)
    omissions: tuple[OmissionRecord, ...]   # sorted by (tier, rel_path)
    estimated_tokens: int                   # sum over `included`
    budget_tokens: int
    over_budget: bool       # True when tier 1 alone still exceeds the budget

  compile_task_context(root, fenced_paths, repo_paths, *,
      token_budget=DEFAULT_CONTEXT_TOKEN_BUDGET,
      inline_cap_bytes=DEFAULT_INLINE_SIZE_CAP_BYTES,
      line_cap=DEFAULT_SIGNATURE_LINE_CAP) -> CompiledContext

  `fenced_paths` is the task's declared write scope (files_hint + fence allow
  scope, already resolved by the caller). `repo_paths` is the candidate
  listing the caller walked — this module stays PURE and never walks a tree
  itself. Both are iterables of repo-relative POSIX strings; both are
  deduplicated and order-insensitive on input.

  ASSIGNMENT, in this order:
   * tier 1 = every path in `fenced_paths`. Tier 1 is included in FULL and is
     NEVER demoted and NEVER omitted — not for size, not for budget. An
     unparseable or oversized tier-1 file is still included whole ("better
     safe", the feature file's Edge cases). A tier-1 path that does not exist
     under root is dropped silently — it is not a candidate at all.
   * tier 2 = `build_import_neighbor_graph(root, tier-1 paths)` → every
     `files` entry, minus anything already tier 1. Full content when
     `fits_inline_size_cap(root, path, inline_cap_bytes)`, else rendered as
     signatures with an OmissionRecord(tier 2, reason "size",
     outcome "signatures").
   * tier 3 = the same graph call over the TIER-2 paths → every `files` entry,
     minus tiers 1 and 2. Signatures only, always. No record: signatures are
     tier 3's normal rendering, not a demotion.
   * tier 4 = every remaining path in `repo_paths`, omitted with
     OmissionRecord(tier 4, reason "distance", outcome "omitted").
   * BINARY: any tier-1, tier-2 or tier-3 path whose bytes are not valid UTF-8
     is omitted entirely with OmissionRecord(its tier, reason "binary",
     outcome "omitted") — this is the ONE case that removes a tier-1 file,
     because a binary blob cannot be inlined at all.

  BUDGET, applied after assignment, in exactly these three phases, each
  repeating while the total still exceeds `token_budget`:
   A. demote the tier-2 file with the LARGEST estimated_tokens from full to
      signatures → OmissionRecord(2, "budget", "signatures");
   B. omit the tier-3 file with the LARGEST estimated_tokens →
      OmissionRecord(3, "budget", "omitted");
   C. omit the tier-2 file with the LARGEST estimated_tokens →
      OmissionRecord(2, "budget", "omitted").
  Ties in estimated_tokens break by rel_path ASCENDING, so the choice is
  deterministic. A file is never truncated mid-content — only demoted or
  dropped whole. When all three phases are exhausted and tier 1 alone still
  exceeds the budget, stop and set over_budget=True: report the overflow
  honestly rather than cutting the declared write scope.

  ESTIMATES: `estimated_tokens` is `estimate_text_tokens(rendered_text)`,
  where rendered_text is the file's full text for "full" and
  "\n".join(signature lines) for "signatures".

  export_omitted_context_json(compiled) -> list[dict]. PURE. One dict per
  OmissionRecord in `omissions` order, with exactly the keys "path", "tier",
  "reason", "outcome". No absolute paths ever appear — `rel_path` is already
  repo-relative.

  write_omitted_context_json(compiled, target_path) -> Path. The ONLY function
  in this module that touches disk for writing: it creates the parent
  directory, writes `export_omitted_context_json(compiled)` as JSON with
  `indent=2` and a trailing newline, and returns the path it wrote.

  Determinism: same inputs → same CompiledContext, always.
  Update the module docstring: add the new names to the Public API list, and
  amend the "never writes evidence" sentence — it is now accurate only of
  everything EXCEPT write_omitted_context_json, which writes exactly where the
  caller points it.

DECISION D-F107-1, recorded here because it amends the feature file: the
feature file's Design names the omissions entry as {path, tier, reason}. That
shape cannot distinguish a file DEMOTED to signatures from one OMITTED
entirely, and T004's debugging view ("why didn't the model see X") needs the
difference. Chosen: add the fourth key "outcome". Alternative considered and
rejected: two separate lists, which duplicates the reason vocabulary. Reverse
by deleting the key and the tests that assert it.

TEST CONTRACT (C6) — append to tests/orchestration/test_context_compiler.py,
leaving every existing test untouched. Build fixture trees with the existing
`_write_tree` helper and pass `tmp_path` as root, as every test there does.

   1. Tier assignment on one fixture tree: `app.py` (fenced) imports `lib.py`,
      `lib.py` imports `deep.py`, and `unrelated.py` is imported by nobody.
      Assert the included tiers exactly: app.py tier 1 "full", lib.py tier 2
      "full", deep.py tier 3 "signatures"; and that unrelated.py is NOT in
      `included` but IS in `omissions` with tier 4, reason "distance",
      outcome "omitted".
   2. A tier-2 file over `inline_cap_bytes` is included with rendering
      "signatures" and carries an OmissionRecord(2, "size", "signatures") —
      pass a small explicit cap so the fixture stays readable.
   3. Budget squeeze demotes TIER 2 FIRST, LARGEST FIRST. The fixture MUST
      carry TWO tier-2 files of clearly different sizes (say lib_big.py and
      lib_small.py, both imported by the fenced file) so that WHICH one is
      demoted is observable. With a budget that forces exactly one demotion,
      assert that lib_big.py flipped to "signatures" with reason "budget",
      that lib_small.py is STILL "full", and that the tier-3 file is still
      present. Without the second tier-2 file this test cannot see the
      ordering rule at all, which is why the sizes are part of the contract.
   4. A tighter budget then omits the tier-3 file (phase B) while tier 2
      remains present as signatures; a tighter one still omits tier 2
      (phase C). Assert the phase order by asserting WHICH files survive.
   5. Tier 1 is never demoted or omitted by budget: with `token_budget=1`, the
      fenced file is still `included` with rendering "full", and
      `over_budget` is True.
   6. A binary tier-2 file (write bytes that are not valid UTF-8) is omitted
      with reason "binary", outcome "omitted", and does not appear in
      `included`.
   7. A fenced path that does not exist under root appears in neither
      `included` nor `omissions`.
   8. Determinism: two calls with the SAME inputs in a DIFFERENT input order
      return equal CompiledContext values.
   9. `estimated_tokens` equals the sum of the included files'
      `estimated_tokens`, and each one equals
      `estimate_text_tokens` of that file's rendered text — assert against a
      direct call, never against a hand-copied number.
  10. `export_omitted_context_json` returns dicts with exactly the four keys
      {"path", "tier", "reason", "outcome"} (assert `set(entry) == {...}`) in
      the same order as `compiled.omissions`.
  11. `write_omitted_context_json` writes a file that `json.loads` reads back
      equal to `export_omitted_context_json(compiled)`, creating a missing
      parent directory, and returns that path.
  12. `DEFAULT_CONTEXT_TOKEN_BUDGET == 24000` and the four
      OMISSION_REASON_* constants equal "budget", "distance", "binary" and
      "size" — a silent change is a red test.
  13. Completeness, the feature's own Acceptance wording: every path in
      `repo_paths` appears EXACTLY ONCE across `included` plus `omissions`
      for a tree where all paths exist and none is a duplicate. Assert it by
      comparing sorted path lists, so a path that silently vanishes is red.

IF THE CODE AND THIS CONTRACT DISAGREE while you are writing the tests, the
contract wins and you change the code you wrote in C5 — it is yours this
round. What you must NOT do is weaken an assertion to match a rendering you
find convenient, or change any T001/T002 behavior to make a new test pass.

PROCEDURE (in order, one commit per item):
0. Preconditions: branch feature/f107-context-compiler-v2, HEAD 2c75bddf,
   `git status --porcelain` empty (else STOP and hand back).
1. C1 — copy .remedy-wt/f107-r5-1.block.md to .agent/authored/f107-r5-1.md and
   prove byte identity (`cmp` if your permission layer allows it, otherwise
   `sha256sum` of both — say which you used). Extract ALL THREE slice bodies
   (FIX1TO, LR4TO, PLAN4) and verify each body's sha256 against its BEGIN
   marker digest BEFORE applying anything. On any mismatch STOP.
   Commit: chore(f107): save the R5 step block verbatim
2. C2 — copy the same file over .agent/last_block.md, prove byte identity.
   Commit: chore(f107): mirror the R5 block into last_block
3. C3 — apply BOTH live_review pairs in this ONE commit. Both are REWRITES:
   the TO does NOT contain the FROM, so the proof shape is "FROM 0x, TO 1x".
     * FIX1 — replace the single line held in slice FIX1FROM with the body of
       slice FIX1TO. This flips the R-0271 bullet from OPEN to RESOLVED.
     * LR4 — replace the single line held in slice LR4FROM with the body of
       slice LR4TO: the reviewer-authored `Done:` resolution followed by the
       R4 gate entry.
   Apply FIX1 first, then LR4. Proof after the commit: each FROM string occurs
   0x in the file; every line of both TO bodies occurs exactly 1x among the
   lines this commit's diff ADDS; report `git show --numstat HEAD --
   .agent/live_review.md` as `<added> <deleted>` (deleted is 2 — one line per
   rewritten anchor). Also: `grep -c '^## Steps' .agent/live_review.md` → 1,
   and `grep -c '^Done: R-0271' .agent/live_review.md` → 1.
   Commit: chore(f107): record the R4 gate and resolve R-0271
4. C4 — replace .agent/plan.md entirely with slice PLAN4; prove byte identity.
   Commit: chore(f107): advance plan to R5 T003
5. C5 — extend packages/orchestration/context_compiler.py with the T003
   contract above. Read the whole file first; self-review loop before commit.
   Commit: feat(f107): tiered context selector with budget demotion
6. C6 — extend tests/orchestration/test_context_compiler.py per the test
   contract above. Commit: test(f107): tier assignment budget demotion and
   omissions
7. MUTATION PROBE (after C6 is committed, before C7). Destructive checks run
   ONLY in a disposable worktree — never in the checkout:
     git worktree add .remedy-wt/f107_r5_mut HEAD
   In that worktree only, make budget phase A pick the SMALLEST tier-2 file
   instead of the largest. Then run, from inside the worktree,
     python3 -m pytest tests/orchestration/test_context_compiler.py -q
   and REPORT the real result: exit code and which tests failed. If NOTHING
   fails, say so plainly — a true report about a test that does not bite is
   worth more than a colour. Then:
     git worktree remove --force .remedy-wt/f107_r5_mut
     git worktree prune
   and confirm `git worktree list` shows the primary checkout alone.
8. C7 — rewrite .agent/handoff.md yourself: feature+round (F107 R5), branch,
   per-commit table C1–C7, changed-files table, the real gate results below
   (command + exit code + counted value), the mutation-probe result, open
   findings count and next free ID (R-0271 is RESOLVED by C3, so: 8 open,
   next free R-0272), item-status table, next expected action: R6 = T004
   segment integration and the `remedy job context` CLI view.
   Cap: 60 lines, or up to 100 if the per-commit table needs it (AGENTS.md
   handoff.md rule) — never drop a mandated section to fit; if you exceed 60,
   carry the stated-cause line naming the actual count and the mandated
   content that caused it.
   Commit: chore(f107): rewrite handoff for R5
   Then: git push (branch already tracks origin)

Done when (run each, record command + real exit code + counted value):
  a. all three slice bodies' sha256 == their marker digests; the R5 block,
     .agent/authored/f107-r5-1.md and .agent/last_block.md are byte-identical
     (name the tool you used).
  b. the C3 proof from step 3: both FROM strings 0x, every TO line 1x among
     the added lines, numstat reported, '^## Steps' → 1, '^Done: R-0271' → 1.
  c. .agent/plan.md byte-identical to the verified PLAN4 bytes;
     wc -l < .agent/plan.md → 28 (PLAN4 is 28 lines).
  d. python3 -m pytest tests/orchestration/test_context_compiler.py -q
     → exit 0 (report the passed count; it includes the 29 frozen tests).
  e. python3 -m pytest tests/cli/test_golden_path.py -q → exit 0 (report the
     passed count).
  f. grep -c '^<<<' on .agent/live_review.md, .agent/plan.md and
     .agent/handoff.md → 0 each (grep exit 1 is the pass).
  g. git status --porcelain → empty; git worktree list → primary only;
     HEAD == origin/feature/f107-context-compiler-v2; insertions per commit
     (git log --numstat 2c75bddf..HEAD) each < 500.
  h. git diff --name-only 2c75bddf..HEAD → exactly the seven paths the Change
     line names, nothing else.
  i. python3 -m ruff check packages/orchestration/context_compiler.py
     tests/orchestration/test_context_compiler.py → exit 0, zero errors
     (report the real output).
  j. the mutation-probe result from step 7, reported as run.
Handback:    completion report (tables + raw gate results a–j + deviations)
             — .agent/handoff.md rewritten as C7.

<<<BEGIN SLICE FIX1FROM sha256=06f8ce67627c5bb95ceff870b5292e2fa0bc7c24a95ab12e5db2190bb7078ab8 lines=1>>>
  carry. OPEN.
<<<END SLICE FIX1FROM>>>

<<<BEGIN SLICE FIX1TO sha256=547f5a527a519022b2d58ab2594d6608c5d1bc6d24b827afc16a5c64a097a06d lines=2>>>
  carry. RESOLVED at the R4 gate (2026-08-12) — the `Done:` text closing it is
  the last entry of this file.
<<<END SLICE FIX1TO>>>

<<<BEGIN SLICE LR4FROM sha256=3541d8ff965f5809997d59862f7ace48550d292d79b37742f27610050eb7246f lines=1>>>
Landed: R-0271 — Iterable now imports from collections.abc (this commit).
<<<END SLICE LR4FROM>>>

<<<BEGIN SLICE LR4TO sha256=b07a255e54acd9226b412710bef122fba8db574b7dbaa100f1c42ff4ee8ba243 lines=53>>>
- Reviewer gate on R4 (2026-08-12): PASS. Range ef64cf72..2c75bddf = eight
  commits touching exactly the seven paths the R4 block named. Transport by the
  PRIMARY shape, the reviewer original having survived the session boundary:
  `sha256sum` of `.remedy-wt/f107-r4-1.block.md`, of the committed
  `.agent/authored/f107-r4-1.md` and of `.agent/last_block.md` returns
  7cf9a5f065db… for all three. This session's permission layer denies `cmp`,
  so byte identity was proven by digest instead — strictly stronger than the
  ordered check, never weaker. All three slice bodies recompute to their
  BEGIN-marker digests at their declared lengths (LRF fac600cb… 7 lines, LR3
  1dc20c0b… 33 lines, PLAN3 4b98f108… 29 lines), and `sha256sum
  .agent/plan.md` returns that same PLAN3 digest: the plan on disk IS the
  authored slice, not a retype of it. The C3 pair was ANCHOR-PRESERVING and
  `git show --numstat 657b98fb -- .agent/live_review.md` reads `38  0` — zero
  deletions; both FROM lines occur exactly 1x in the file and 0x among the 38
  added lines, and every TO-only line of both slices occurs exactly 1x among
  those added lines, with no strays. Every scoped gate was RE-RUN by the
  reviewer rather than read from the handback: `python3 -m pytest
  tests/orchestration/test_context_compiler.py -q` returns 29 passed (the 16
  frozen T001 tests plus 13 new), the canary `python3 -m pytest
  tests/cli/test_golden_path.py -q` returns 42 passed, `python3 -m ruff check`
  over the module and its test file returns "All checks passed!" — which is
  what closes R-0271 — `.agent/plan.md` is 29 lines, the Steps heading count
  is 1, `grep -c '^<<<'` is 0 across all three state files, `git status
  --porcelain` is empty, HEAD equals `origin/feature/f107-context-compiler-v2`
  and `git worktree list` shows the primary checkout alone. Insertions per
  commit 326, 280, 38, 2, 11, 242, 271, 80 — each under 500. The 13 test
  functions carry all 13 numbered obligations of the R4 contract as exact
  tuple equalities rather than truthiness checks, and the goldens are
  mechanically captured rather than hand-written — `limit: int=10` is
  `ast.unparse` spacing, which no human would type on purpose. The reviewer
  ran THREE mutation probes in a disposable worktree at 2c75bddf, two of them
  deliberately different from the worker's: turning the size cap's `<=` into
  `<` reddens exactly `test_fits_inline_size_cap_is_inclusive_at_the_cap_and`
  `_false_when_absent` with `AssertionError: assert False is True`, and
  deleting the nested-declaration recursion line reddens exactly the Python
  whole-file golden and
  `test_python_file_without_any_docstring_renders_headers_only`. The worker's
  own probe reproduces verbatim — `1 failed, 28 passed`, failing
  `test_typescript_signature_golden_renders_exported_lines_only` on
  `'export function renderWidget(id: string): void {' !=` the same line
  without its brace — so the handback's probe evidence is confirmed TRUE
  rather than taken on trust. That worktree was removed and pruned before this
  verdict and `git worktree list` shows the primary alone. The 96-line handoff
  is a declared stated-cause overage carrying its mandated tables, which
  AGENTS.md DECISION D15 permits; both declared deviations are accurate and
  neither weakens a proof. No new findings this round.
  `LAST_REVIEWED_SHA` advances ef64cf72 -> 2c75bddf.

Done: R-0271 — RESOLVED. `packages/orchestration/context_compiler.py` now reads
`from collections.abc import Iterable` (commit b52b1c3c, numstat `1 1`), and the
reviewer's own re-run of `python3 -m ruff check` over that module and its test
file returns exit 0 with "All checks passed!" — zero errors, where the same
command reported UP035 before the fix. Open findings 9 -> 8.
<<<END SLICE LR4TO>>>

<<<BEGIN SLICE PLAN4 sha256=320c489005c5aafce40a1c0e2aca14ab1e30d464b7c199fc4eb6a93cfb202722 lines=28>>>
# Plan — F107 Context compiler v2

Branch: feature/f107-context-compiler-v2, cut from main at 2e4142c3.
Next free finding ID: R-0272. R4 reviewed PASS at 2c75bddf.

## Goal
The context compiler selects fenced-path files, their direct import
neighbors, and only SIGNATURES of distant dependencies, under a total
context token budget with tier demotion — and writes an omissions record
naming everything it left out and why. DONE when a fixture repo's task
context shrinks measurably versus whole-files with the fixture task still
solvable by the fake provider, and the omissions record explains every
exclusion (docs/roadmap/features/T2_F107.md).

## Current Step
R5 — T003 tiered selector: assign tiers 1-4 from the fenced paths outward,
render tier 1/2 full and tier 2/3 as signatures, enforce a total token budget
by demoting tier 2 first and never truncating mid-file, and record every
demotion and omission with a reason and an outcome, all added to
packages/orchestration/context_compiler.py with fixture-tree tests in
tests/orchestration/test_context_compiler.py. T001 and T002 are frozen. The
round also resolves finding R-0271.

## Next Steps
1. T004 — segment integration + the `remedy job context` CLI view +
   an end-to-end fixture task with a size comparison in evidence.
2. Integration gate per docs/agents/integration_gate.md.
3. Closure per docs/roadmap/STATUS_closure_protocol.md.
<<<END SLICE PLAN4>>>
