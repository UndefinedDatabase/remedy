── STEP R6/~10 — F107 Context compiler v2 — T004 part 1, the segment layer ───
Goal:        Make the compiled context ENTER A PROMPT the way this repo says
             prompts are built: render a CompiledContext into segment text,
             register it into a PromptSegmentRegistry at rank JOB_CONTEXT, name
             the omissions filename once, and add the whole-file size
             comparison the feature's Acceptance requires. Record the R5 gate
             and register finding R-0272.
Bundle:      C1 authored-block save; C2 last_block mirror; C3 the two authored
             live_review pairs (LRF2 registers R-0272 in the Findings list, LR5
             appends the R5 gate entry); C4 plan rewrite; C5 the T004-P1 code;
             C6 the tests; C7 handoff rewrite; push; handback.
Change:      EXACTLY these paths and nothing else:
             .agent/authored/f107-r6-1.md (new), .agent/last_block.md,
             .agent/live_review.md (authored pairs LRF2 and LR5 in C3 only),
             .agent/plan.md (full replacement PLAN5),
             packages/orchestration/context_compiler.py,
             tests/orchestration/test_context_compiler.py,
             .agent/handoff.md (your handback rewrite).
Constraints: AGENTS.md in full. T001, T002 AND T003 ARE FROZEN: every existing
             name in the module keeps its current behavior and all 42 existing
             tests keep passing UNCHANGED. You APPEND to the module; you do not
             restructure it and you do not edit one existing test. Do NOT add a
             field to SelectedFile, OmissionRecord or CompiledContext — their
             equality is what the T003 determinism test rests on. Stdlib only,
             plus the ONE intra-repo import the module already has
             (estimate_text_tokens) and exactly ONE new one:
             `from packages.orchestration.prompt_segments import (
             PromptSegment, PromptSegmentRegistry, SegmentStabilityRank)`.
             That direction is safe — prompt_segments imports nothing from this
             module — and it is the whole point of the round: the registry owns
             composition, this feature owns SELECTION, and the compiled context
             enters as a ranked segment (feature file, "How it fits"). Do NOT
             touch prompt_segments.py, prompt composition, pingpong_loop, the
             CLI, or any other module — wiring a real builder prompt is NOT
             this round. A diff adding a TS parser or any third-party
             dependency is rejected by the feature file's orchestrator brief.
             Never write a `Done:` line — `Done:` text is reviewer-authored
             only; if you must record a landed fix, write `Landed: R-XXXX` and
             nothing else. Do NOT create a PR. Never touch main. Never force-
             push. Scratch only under .remedy-wt/, uncommitted. Apply authored
             slices byte for byte after sha256 verification; on mismatch STOP.

TIER TABLE (the feature contract, verbatim — the tiers ARE the contract):
(1) files matched by the task's files_hint and fence allow scope — full
content; (2) direct import neighbors of tier 1 — full content up to a per-file
size cap, else signatures; (3) transitive dependencies — signatures only;
(4) everything else — omitted.

T004-P1 CONTRACT (public names; Code Discoverability Conventions apply).

  Module constants:
    COMPILED_CONTEXT_SEGMENT_NAME = "compiled_context"
    OMITTED_CONTEXT_FILENAME = "omitted_context.json"
  The filename constant exists so the writer, the future CLI view and every
  test spell the omissions file ONE way (AGENTS.md, "one spelling per
  concept"). It is a bare filename, never a path: where the file sits is the
  caller's decision, and write_omitted_context_json already takes a full path.

  render_compiled_context_text(root, compiled) -> str
    The segment body. One block per file in `compiled.included`, in that order
    — which is already sorted by (tier, rel_path), so the rendering inherits
    T003's determinism instead of inventing its own — joined by "\n\n".
    Each block is exactly:
        "# <rel_path> — tier <tier> (<rendering>)\n<body>"
    where <body> is the file's full decoded text when `rendering` is "full",
    and the signature lines joined by "\n" when it is "signatures". Strip a
    trailing newline from <body> so the "\n\n" join is the only separator
    between blocks and the text is stable regardless of whether a fixture file
    ends in a newline. PURE READ: it opens the included files and nothing else,
    never walks a tree and never writes. An OMITTED file contributes NOTHING —
    not its content, not its path: the omissions record is where those live,
    which is exactly the separation the debugging view depends on.
    An empty `included` renders to "".

  register_compiled_context_segment(registry, root, compiled) -> PromptSegment
    Calls registry.register(COMPILED_CONTEXT_SEGMENT_NAME,
    SegmentStabilityRank.JOB_CONTEXT, render_compiled_context_text(root,
    compiled)) and returns what the registry returns. It adds NO discipline of
    its own: a second call against the same registry must raise the registry's
    own PromptSegmentError, and that is asserted rather than prevented here.
    JOB_CONTEXT is the rank because the compiled context IS the job/task
    context of the prompt; the choice is pinned by a test so a silent change
    to a different rank is red.

  @dataclass(frozen=True) ContextSizeComparison:
    whole_file_tokens: int      # what whole-file context would have cost
    compiled_tokens: int        # what the compiled context costs
    saved_tokens: int           # whole_file_tokens - compiled_tokens
    saved_ratio: float          # saved_tokens / whole_file_tokens, or 0.0

  compare_context_size(root, repo_paths, compiled) -> ContextSizeComparison
    The measurement the feature's Done condition rests on ("a fixture repo's
    task context shrinks measurably versus whole-files"). `whole_file_tokens`
    is the sum of estimate_text_tokens over the full text of every path in
    `repo_paths` that exists under root AND decodes as UTF-8 — a missing or
    binary path contributes 0 and never raises, because the baseline is "what
    whole files would have cost", and a file that could not be inlined either
    way costs nothing either way. `compiled_tokens` is
    `compiled.estimated_tokens`, read, never recomputed. `saved_tokens` is the
    difference and MAY BE NEGATIVE — report it honestly, never clamp it to
    zero. `saved_ratio` is saved_tokens / whole_file_tokens, and EXACTLY 0.0
    when whole_file_tokens is 0: a zero baseline has no ratio, and inventing
    one would be a fabricated number. PURE: reads files, writes nothing.

  Update the module docstring: add the two constants, the dataclass and the
  three functions to the Public API list, and extend the scope-boundary text
  to say what this layer deliberately does NOT do — it does not migrate any
  builder prompt and does not write the segment manifest into evidence; those
  are R7 and later, and a reader searching here should find that sentence
  rather than conclude the wiring was forgotten.

TEST CONTRACT (C6) — append to tests/orchestration/test_context_compiler.py,
leaving every existing test untouched. Reuse the existing `_selector_tree`,
`_SELECTOR_REPO_PATHS` and `_write_tree` helpers; pass `tmp_path` as root.
Assert against COMPUTED values — a hand-copied number is a finding.

   1. `render_compiled_context_text` on the `_selector_tree` fixture equals an
      expected string you BUILD in the test from the fixture's own file texts
      and from `extract_file_signatures(...).lines` — never a pasted literal.
      Assert the four blocks appear in `compiled.included` order and that each
      header line reads exactly "# <path> — tier <n> (<rendering>)".
   2. The omitted file contributes nothing: neither "unrelated.py" nor its
      content "UNRELATED = 1" occurs in the rendered text, while the tier-1
      file's content does.
   3. `register_compiled_context_segment` returns a PromptSegment with
      `name == COMPILED_CONTEXT_SEGMENT_NAME`,
      `rank == SegmentStabilityRank.JOB_CONTEXT` and `text ==
      render_compiled_context_text(...)`; and `registry.registered_segments()`
      equals the one-tuple of that segment.
   4. `compose_prompt_segments(registry.registered_segments())` yields a
      manifest of exactly one entry whose `name` is the constant, whose `rank`
      is `int(SegmentStabilityRank.JOB_CONTEXT)`, and whose `sha256` equals
      `hashlib.sha256(text.encode("utf-8")).hexdigest()` computed in the test.
      Also assert the composed `text` equals the segment text.
   5. Registering twice against the SAME registry raises `PromptSegmentError`
      (`pytest.raises`) — the registry's duplicate discipline is inherited,
      not bypassed.
   6. Determinism: compile the same tree twice and render both; the two
      strings are equal.
   7. `OMITTED_CONTEXT_FILENAME == "omitted_context.json"`, and
      `write_omitted_context_json(compiled, tmp_path / "task_runs" / "t1" /
      OMITTED_CONTEXT_FILENAME)` returns that path and writes JSON that
      `json.loads` reads back equal to `export_omitted_context_json(compiled)`.
   8. `compare_context_size` on the fixture: `whole_file_tokens` equals a sum
      you compute in the test over the five fixture files' texts,
      `compiled_tokens == compiled.estimated_tokens`, `saved_tokens` is the
      difference, and `saved_ratio == saved_tokens / whole_file_tokens`.
      Assert `saved_tokens > 0` as well — the feature's Done condition is that
      the context actually shrank, and a test that never checks the sign would
      pass on a compiler that saved nothing.
   9. `compare_context_size(root, (), compiled)` gives `whole_file_tokens == 0`
      and `saved_ratio == 0.0` and does not raise — the zero-baseline guard.
  10. `compare_context_size` tolerates junk in `repo_paths`: a path with no
      file under root and a file whose bytes are not valid UTF-8 each
      contribute 0 to `whole_file_tokens` instead of raising. Build the binary
      file with `write_bytes` as the existing binary test does.

IF THE CODE AND THIS CONTRACT DISAGREE while you are writing the tests, the
contract wins and you change the code you wrote in C5 — it is yours this
round. What you must NOT do is weaken an assertion to match a rendering you
find convenient, or change any T001/T002/T003 behavior to make a new test
pass. If the contract is genuinely impossible, STOP and hand back saying so.

PROCEDURE (in order, one commit per item):
0. Preconditions: branch feature/f107-context-compiler-v2, HEAD 54bc56c2,
   `git status --porcelain` empty, `git worktree list` primary only (else STOP
   and hand back without changing anything).
1. C1 — copy .remedy-wt/f107-r6-1.block.md to .agent/authored/f107-r6-1.md and
   prove byte identity (`cmp` if your permission layer allows it, otherwise
   `sha256sum` of both — say which you used). Extract ALL FIVE slice bodies and
   verify each body's sha256 against its BEGIN marker digest BEFORE applying
   anything. On any mismatch STOP.
   Commit: chore(f107): save the R6 step block verbatim
2. C2 — copy the same file over .agent/last_block.md, prove byte identity.
   Commit: chore(f107): mirror the R6 block into last_block
3. C3 — apply BOTH live_review pairs in this ONE commit. BOTH ARE APPEND-
   SHAPED: each TO literally CONTAINS its FROM, so the proof is NOT "FROM 0x".
     * LRF2 — replace the single line held in slice LRF2FROM with the body of
       slice LRF2TO. This registers finding R-0272 at the end of the Findings
       list.
     * LR5 — replace the single line held in slice LR5FROM with the body of
       slice LR5TO. This appends the R5 gate entry to the Steps section,
       keeping the gate entries contiguous.
   Apply LRF2 first, then LR5. Proof after the commit, scoped to the ADDED
   lines because the TO bodies legitimately repeat sentences the file already
   carries (planner_reviewer_prompt.md §4.9): each FROM string occurs exactly
   1x in the file; each TO-ONLY line (a TO line that is not the FROM line)
   occurs exactly 1x among the lines this commit's diff ADDS; and
   `git show --numstat HEAD -- .agent/live_review.md` reports 0 DELETIONS,
   which is what proves neither anchor line was edited. Also report
   `grep -c '^## Steps' .agent/live_review.md` → 1 and
   `grep -c '^- R-0272' .agent/live_review.md` → 1.
   Commit: chore(f107): record the R5 gate and register R-0272
4. C4 — replace .agent/plan.md entirely with slice PLAN5; prove byte identity.
   Commit: chore(f107): advance plan to R6 T004 part 1
5. C5 — extend packages/orchestration/context_compiler.py per the T004-P1
   contract above. Read the whole file first; self-review loop before commit.
   Commit: feat(f107): compiled context as a ranked prompt segment
6. C6 — extend tests/orchestration/test_context_compiler.py per the test
   contract above.
   Commit: test(f107): segment rendering registration and size comparison
7. MUTATION PROBE (after C6 is committed, before C7). Destructive checks run
   ONLY in a disposable worktree — never in the checkout:
     git worktree add .remedy-wt/f107_r6_mut HEAD
   In that worktree only, change the rank passed by
   `register_compiled_context_segment` from `SegmentStabilityRank.JOB_CONTEXT`
   to `SegmentStabilityRank.TASK`. Then run, from inside the worktree,
     python3 -m pytest tests/orchestration/test_context_compiler.py -q
   and REPORT the real result: exit code, which tests failed, and the actual
   assertion text of one failure. If NOTHING fails, say so plainly — a true
   report about a test that does not bite is worth more than a colour, and it
   is a finding I need rather than a failure of yours. Then:
     git worktree remove --force .remedy-wt/f107_r6_mut
     git worktree prune
   and confirm `git worktree list` shows the primary checkout alone.
8. C7 — rewrite .agent/handoff.md yourself: feature+round (F107 R6), branch,
   per-commit table C1–C7, changed-files table, the real gate results a–j
   below (command + real exit code + counted value), the mutation-probe
   result, open findings count and next free ID (R-0272 is REGISTERED by C3
   and stays OPEN, so: 9 open, next free R-0273), item-status table, next
   expected action: R7 = T004 part 2, the `remedy job context` CLI view and
   the end-to-end fixture task.
   Cap: 60 lines, or up to 100 if the per-commit table needs it (AGENTS.md
   handoff.md rule) — never drop a mandated section to fit; if you exceed 60,
   carry the stated-cause line naming the actual count and the mandated
   content that caused it.
   Commit: chore(f107): rewrite handoff for R6
   Then: git push (branch already tracks origin; plain push, never force)

Done when (run each, record command + real exit code + counted value):
  a. all five slice bodies' sha256 == their marker digests; the R6 block,
     .agent/authored/f107-r6-1.md and .agent/last_block.md byte-identical
     (name the tool you used).
  b. the C3 append proof from step 3: each FROM 1x in the file, each TO-only
     line 1x among the added lines, numstat deletions 0, '^## Steps' → 1,
     '^- R-0272' → 1.
  c. .agent/plan.md byte-identical to the verified PLAN5 bytes;
     wc -l < .agent/plan.md → 28 (PLAN5 is 28 lines).
  d. python3 -m pytest tests/orchestration/test_context_compiler.py -q
     → exit 0 (report the passed count; it includes the 42 frozen tests).
  e. python3 -m pytest tests/orchestration/test_prompt_segments.py -q → exit 0
     (report the passed count) — this round imports prompt_segments for the
     first time, so its own suite is part of the round gate.
  f. python3 -m pytest tests/cli/test_golden_path.py -q → exit 0 (report the
     passed count).
  g. grep -c '^<<<' on .agent/live_review.md, .agent/plan.md and
     .agent/handoff.md → 0 each (grep exit 1 is the pass).
  h. git status --porcelain → empty; git worktree list → primary only;
     HEAD == origin/feature/f107-context-compiler-v2; insertions per commit
     (git log --numstat 54bc56c2..HEAD) each < 500.
  i. git diff --name-only 54bc56c2..HEAD → exactly the seven paths the Change
     line names, nothing else. Also: python3 -m ruff check
     packages/orchestration/context_compiler.py
     tests/orchestration/test_context_compiler.py → exit 0, zero errors
     (report the real output).
  j. the mutation-probe result from step 7, reported as run.
Handback:    completion report (tables + raw gate results a–j + deviations)
             — .agent/handoff.md rewritten as C7.

<<<BEGIN SLICE LRF2FROM sha256=2bb66673d69bd45b672dee4b85eefc4743737c9b31cdb14e51bd7ca4ddd1b768 lines=1>>>
  the last entry of this file.
<<<END SLICE LRF2FROM>>>

<<<BEGIN SLICE LRF2TO sha256=830262c11e23e62b4e1a4dbfd407290da27211662036516de7d2f2645beaa69e lines=10>>>
  the last entry of this file.
- R-0272 (Low, F107 R5): the R5 step block specified tier 2 as
  `build_import_neighbor_graph(...)` yielding "every `files` entry", but
  `ImportNeighbors` has no `files` field — its neighbor tuple is named
  `resolved` (the T001 dataclass in
  `packages/orchestration/context_compiler.py`). The worker implemented
  `resolved`, which is correct, so nothing on disk is wrong and no work is
  outstanding. Registered as the record of the citation-accuracy lesson, the
  same class as R-0239 and R-0247: a reviewer-authored contract must name
  fields that exist. OPEN.
<<<END SLICE LRF2TO>>>

<<<BEGIN SLICE LR5FROM sha256=b96097af0f6672a781d0b4eaa864a157cd96c4d238fbcdf5bf30fed50df10789 lines=1>>>
  `LAST_REVIEWED_SHA` advances ef64cf72 -> 2c75bddf.
<<<END SLICE LR5FROM>>>

<<<BEGIN SLICE LR5TO sha256=98b340c5bfba9bb70fd9081ecc4b1cc6982c951f6e8bd89e392737d355d35612 lines=51>>>
  `LAST_REVIEWED_SHA` advances ef64cf72 -> 2c75bddf.
- Reviewer gate on R5 (2026-08-12): PASS. Range 2c75bddf..54bc56c2 = seven
  commits touching exactly the seven paths the R5 block named. The round spanned
  TWO worker sessions: a prior worker committed C1-C6 and ended before PROCEDURE
  step 7, and this session's worker ran the mutation probe, re-verified the disk
  state and committed C7 alone. The single-writer rule held throughout — the
  reviewer wrote nothing, and no existing commit was amended, rebased, reverted
  or reordered. Transport by the PRIMARY shape: `cmp` of
  `.remedy-wt/f107-r5-1.block.md` against `.agent/authored/f107-r5-1.md`, and of
  that copy against `.agent/last_block.md`, is silent, and all three sha256 to
  220d64ec8aa4… at 393 lines each. All five slice bodies recompute to their
  BEGIN-marker digests at their declared lengths (FIX1FROM 06f8ce67… 1 line,
  FIX1TO 547f5a52… 2, LR4FROM 3541d8ff… 1, LR4TO b07a255e… 53, PLAN4 320c4890…
  28), and `cmp .agent/plan.md` against the extracted PLAN4 body is silent: the
  plan on disk IS the authored slice, not a retype of it. Both C3 pairs were
  REWRITES and `git show --numstat 4860115e -- .agent/live_review.md` reads
  `55  2` — both FROM strings now occur 0x, each of the 2 FIX1TO and 53 LR4TO
  lines occurs exactly 1x among the 55 added lines, and 0 added lines belong to
  neither body. Every scoped gate was RE-RUN by the reviewer rather than read
  from the handback: `python3 -m pytest
  tests/orchestration/test_context_compiler.py -q` returns 42 passed (the 29
  frozen T001+T002 tests plus 13 new T003 tests), the canary `python3 -m pytest
  tests/cli/test_golden_path.py -q` returns 42 passed, `python3 -m ruff check`
  over the module and its test file returns "All checks passed!",
  `.agent/plan.md` is 28 lines, the Steps heading count is 1, the stray-marker
  count is 0 across the three state files, `git status --porcelain` is empty,
  HEAD equals `origin/feature/f107-context-compiler-v2`, and `git worktree list`
  shows the primary checkout alone. Insertions per commit 393, 322, 55, 11, 351,
  284, 76 — each under 500. The 13 new test functions carry all 13 numbered
  obligations of the R5 contract as exact equality assertions on real values,
  and every token figure is asserted against a direct `estimate_text_tokens`
  call rather than against a hand-copied number. The reviewer ran THREE mutation
  probes in a disposable worktree at 54bc56c2, two of them deliberately
  different from the worker's: pointing budget phase B at TIER_NEIGHBOR instead
  of TIER_DISTANT reddens exactly
  `test_budget_omits_tier_three_before_it_omits_tier_two` and
  `test_tier_one_is_never_cut_by_the_budget_and_the_overflow_is_reported`, while
  suppressing the tier-4 distance records reddens exactly the tier-assignment
  test, the export-keys test and the completeness test. The worker's own probe
  reproduces verbatim — `1 failed, 41 passed`, failing
  `test_budget_demotes_the_largest_tier_two_file_first` on `At index 1 diff:`
  the big neighbor rendering `full` where the test requires `signatures` — so
  the handback's probe evidence is confirmed TRUE rather than taken on trust.
  That worktree was removed and pruned before this verdict. The 95-line handoff
  is a declared stated-cause overage carrying its mandated tables, which
  AGENTS.md DECISION D15 permits. One new finding, R-0272, is registered above.
  Recorded as an observation and NOT as a finding: `context_compiler.py` still
  has no caller outside its own test module, because T003 is a library layer by
  design and T004 is the round that wires it — a green gate here is not yet a
  working feature, and no verdict in this file claims otherwise.
  `LAST_REVIEWED_SHA` advances 2c75bddf -> 54bc56c2.
<<<END SLICE LR5TO>>>

<<<BEGIN SLICE PLAN5 sha256=27f9c8efd656f92a65417d6ffb6c9b384ee3c24fa60c548a106419376f26e768 lines=28>>>
# Plan — F107 Context compiler v2

Branch: feature/f107-context-compiler-v2, cut from main at 2e4142c3.
Next free finding ID: R-0273. R5 reviewed PASS at 54bc56c2.

## Goal
The context compiler selects fenced-path files, their direct import
neighbors, and only SIGNATURES of distant dependencies, under a total
context token budget with tier demotion — and writes an omissions record
naming everything it left out and why. DONE when a fixture repo's task
context shrinks measurably versus whole-files with the fixture task still
solvable by the fake provider, and the omissions record explains every
exclusion (docs/roadmap/features/T2_F107.md).

## Current Step
R6 — T004 part 1, the SEGMENT layer: render a CompiledContext into segment
text, register that text into a PromptSegmentRegistry at rank JOB_CONTEXT so
the compiled context enters a prompt as a ranked segment instead of ad hoc
concatenation, name the omissions filename once, and add the whole-file size
comparison the feature's Acceptance requires — all appended to
packages/orchestration/context_compiler.py, with tests in
tests/orchestration/test_context_compiler.py. T001-T003 are frozen.

## Next Steps
1. R7 — T004 part 2: the `remedy job context` CLI view, an end-to-end fixture
   task solved by the fake provider, and the size comparison in evidence.
2. Integration gate per docs/agents/integration_gate.md.
3. Closure per docs/roadmap/STATUS_closure_protocol.md.
<<<END SLICE PLAN5>>>
