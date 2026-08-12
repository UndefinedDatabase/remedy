── STEP R7/~10 — F107 Context compiler v2 — repair round for R-0273 ──────────
Goal:        Make the compiled context's numbers describe the text that would
             actually be sent: carry the effective signature line cap ON the
             CompiledContext and render from it, so a context compiled at a
             custom `line_cap` can no longer be rendered at the module default.
             Record the R6 gate and register finding R-0273.
Bundle:      C1 authored-block save; C2 last_block mirror; C3 the two authored
             live_review pairs (LRF3 registers R-0273 in the Findings list, LR6
             appends the R6 gate entry); C4 plan rewrite; C5 the fix; C6 the
             tests; C7 handoff rewrite; push; handback.
Change:      EXACTLY these paths and nothing else:
             .agent/authored/f107-r7-1.md (new), .agent/last_block.md,
             .agent/live_review.md (authored pairs LRF3 and LR6 in C3 only),
             .agent/plan.md (full replacement PLAN6),
             packages/orchestration/context_compiler.py,
             tests/orchestration/test_context_compiler.py,
             .agent/handoff.md (your handback rewrite).
Constraints: AGENTS.md in full. This is a REPAIR round: it changes exactly one
             behavior and nothing else. Every one of the 52 existing tests
             keeps passing UNCHANGED — you do not edit a single existing test,
             and if the fix makes an existing test fail, STOP and hand back
             rather than editing that test. Every public name in the module
             keeps its current spelling: no rename, no removal, no new public
             function, no new constant. Do NOT touch prompt_segments.py,
             prompt composition, pingpong_loop, the CLI or any other module.
             Do NOT build the CLI view or the end-to-end fixture task — that
             is R8 and it is explicitly NOT this round. No new import of any
             kind. Never write a `Done:` line — `Done:` text is reviewer-
             authored only; a landed fix is `Landed: R-XXXX` and nothing else.
             Do NOT create a PR. Never touch main. Never force-push, never
             amend or rebase an existing commit. Scratch only under
             .remedy-wt/, uncommitted. Apply authored slices byte for byte
             after sha256 verification; on mismatch STOP.

THE DEFECT, measured (this is what you are fixing):
`compile_task_context(root, fenced, repo, line_cap=N)` estimates every
signatures-rendered file at the caller's N, and the budget demotes files using
those estimates. `render_compiled_context_text(root, compiled)` then re-renders
those same files at `DEFAULT_SIGNATURE_LINE_CAP`, because the CompiledContext
does not carry N and the function has no cap parameter. On a three-file fixture
at `line_cap=3` the reviewer measured `compiled.estimated_tokens` = 25 against a
rendered text estimating at 128 — 5.1x — with `compare_context_size` reporting
`saved_ratio=0.84`, a saving that does not exist.

DECISION D-F107-2, recorded here because it reverses an instruction the R6
block gave: R6 told the worker "do NOT add a field to CompiledContext", and
this round adds one. CHOSEN: carry `line_cap` on the CompiledContext, so the
rendering reads the cap the estimate was computed at and the two CANNOT drift.
ALTERNATIVE CONSIDERED AND REJECTED: add a `line_cap` parameter to
`render_compiled_context_text` — it leaves a caller free to pass a cap
different from the compiled one, which recreates the same divergence through a
new door and makes the invariant a convention instead of a guarantee. REVERSE
BY: deleting the field, restoring the module-default call in the renderer, and
deleting the two tests this round adds. The R6 instruction was right about not
changing those dataclasses casually and wrong to make it absolute; equality
semantics are preserved either way, because two contexts compiled from the same
inputs carry the same cap and so still compare equal.

FIX CONTRACT (C5) — three edits in
packages/orchestration/context_compiler.py, and nothing else in that file
beyond the docstrings the edits make stale:

  1. `CompiledContext` gains a FIFTH field, declared LAST so no positional
     construction anywhere changes meaning:
         line_cap: int
     Document it in the class docstring as: the signature line cap this
     context was compiled at, carried so a rendering cannot drift from the
     estimate the budget was enforced against.
  2. `compile_task_context` passes `line_cap=line_cap` at its SINGLE
     `CompiledContext(...)` construction site. It is the only one in the
     repository — `grep -rn "CompiledContext(" packages/ tests/ apps/` returns
     that one line — so no other call site needs touching. Run that grep
     yourself and report what it returns.
  3. `render_compiled_context_text` renders signature bodies at
     `compiled.line_cap` instead of `DEFAULT_SIGNATURE_LINE_CAP`. Replace the
     sentence in its docstring that currently discloses the default-cap
     behavior ("Signature bodies are re-rendered at the module default line
     cap, so a context compiled with a custom ``line_cap`` renders its
     signature blocks at that default.") with the new invariant: signature
     bodies are rendered at the cap the context was compiled at, so the
     rendered text and ``estimated_tokens`` describe the same bytes. Do not
     leave the old sentence standing next to the new behavior — a docstring
     that describes a fixed defect is worse than no docstring.

TEST CONTRACT (C6) — append to tests/orchestration/test_context_compiler.py,
leaving every existing test untouched. Reuse the existing helpers and
`tmp_path` as root. Assert against COMPUTED values; a hand-copied number is a
finding.

   1. `CompiledContext.line_cap` is the cap the context was compiled at:
      compiling without the argument gives `DEFAULT_SIGNATURE_LINE_CAP`, and
      compiling with an explicit small cap gives exactly that value.
   2. THE REGRESSION TEST, and the one that must go red without the fix. Build
      a fixture whose TIER-3 file has clearly MORE declarations than the cap
      you pass — at least six top-level functions against a cap of 2 — so the
      capped rendering is unmistakably shorter than the uncapped one. Compile
      it at that small cap, render it, and assert BOTH halves of the
      invariant:
        (a) for EVERY included file whose `rendering` is "signatures", the
            body that appears in the rendered text equals
            `"\n".join(extract_file_signatures(root, path, <the small cap>)
            .lines)` — the capped rendering, not the default one; and
        (b) `estimate_text_tokens` of that body equals that file's
            `SelectedFile.estimated_tokens` — the estimate and the rendering
            describe the same bytes.
      Assert at least one such file exists, so a fixture that accidentally
      produced no signatures file cannot make this test vacuously pass.
   3. Determinism survives the new field: two contexts compiled from the same
      tree at the same custom cap are equal, and their rendered texts are
      equal.

PROCEDURE (in order, one commit per item):
0. Preconditions: branch feature/f107-context-compiler-v2, HEAD 861eb371,
   `git status --porcelain` empty, `git worktree list` primary only (else STOP
   and hand back without changing anything).
1. C1 — copy .remedy-wt/f107-r7-1.block.md to .agent/authored/f107-r7-1.md and
   prove byte identity (`cmp` if your permission layer allows it, otherwise
   `sha256sum` of both — say which you used). Extract ALL FIVE slice bodies and
   verify each body's sha256 against its BEGIN marker digest BEFORE applying
   anything. On any mismatch STOP.
   Commit: chore(f107): save the R7 step block verbatim
2. C2 — copy the same file over .agent/last_block.md, prove byte identity.
   Commit: chore(f107): mirror the R7 block into last_block
3. C3 — apply BOTH live_review pairs in this ONE commit. BOTH ARE APPEND-
   SHAPED: each TO literally CONTAINS its FROM, so the proof is NOT "FROM 0x".
     * LRF3 — replace the single line held in slice LRF3FROM with the body of
       slice LRF3TO. This registers finding R-0273 at the end of the Findings
       list.
     * LR6 — replace the single line held in slice LR6FROM with the body of
       slice LR6TO. This appends the R6 gate entry to the Steps section.
   Apply LRF3 first, then LR6. Proof after the commit, scoped to the ADDED
   lines because the TO bodies legitimately repeat sentences the file already
   carries (planner_reviewer_prompt.md §4.9): each FROM string occurs exactly
   1x in the file; each TO-ONLY line occurs exactly 1x among the lines this
   commit's diff ADDS; and `git show --numstat HEAD -- .agent/live_review.md`
   reports 0 DELETIONS, which is what proves neither anchor line was edited.
   Also report `grep -c '^## Steps' .agent/live_review.md` → 1 and
   `grep -c '^- R-0273' .agent/live_review.md` → 1.
   Commit: chore(f107): record the R6 gate and register R-0273
4. C4 — replace .agent/plan.md entirely with slice PLAN6; prove byte identity.
   Commit: chore(f107): advance plan to R7 repair
5. C5 — apply the three edits of the FIX CONTRACT. Read the whole file first;
   self-review loop before commit. Report the `grep -rn "CompiledContext("`
   output as part of the handback.
   Commit: fix(f107): render signatures at the compiled line cap
6. C6 — append the three tests of the TEST CONTRACT.
   Commit: test(f107): the rendering matches the cap it was compiled at
7. RED-PROOF, then MUTATION PROBE. Both run ONLY in a disposable worktree —
   never in the checkout:
     git worktree add .remedy-wt/f107_r7_mut HEAD
   In that worktree only, and in this order, reporting each real result:
     (i) RED-PROOF of the regression test: revert ONLY edit 3 — put
         `DEFAULT_SIGNATURE_LINE_CAP` back in `render_compiled_context_text`,
         leaving the field and the constructor edit in place. Run
           python3 -m pytest tests/orchestration/test_context_compiler.py -q
         and report the exit code and which tests failed. Test 2 above is
         expected to go RED; if it does NOT, say so plainly — that would mean
         the regression test does not actually bite, which is a finding I need
         rather than a failure of yours.
     (ii) restore the worktree file (`git checkout -- <path>`), then MUTATE
         differently: make `compile_task_context` store
         `line_cap=DEFAULT_SIGNATURE_LINE_CAP` instead of the caller's value.
         Run the same command and report the real result.
   Then:
     git worktree remove --force .remedy-wt/f107_r7_mut
     git worktree prune
   and confirm `git worktree list` shows the primary checkout alone.
8. C7 — rewrite .agent/handoff.md yourself: feature+round (F107 R7), branch,
   per-commit table C1–C7, changed-files table, the real gate results a–i
   below (command + real exit code + counted value), BOTH step-7 results, open
   findings count and next free ID (R-0273 is REGISTERED by C3 and LANDED by
   C5 but only reviewer text resolves it, so it stays OPEN: 10 open, next free
   R-0274), item-status table, next expected action: R8 = T004 part 2, the
   `remedy job context` CLI view and the end-to-end fixture task.
   Record the R-0273 fix in this file as `Landed: R-0273 — <one line: what
   changed, which commit>` in .agent/live_review.md ONLY IF you are certain —
   re-read planner_reviewer_prompt.md §4.4 first; the safe reading is that C3
   already registered it and C5 landed it, so a single `Landed:` line is
   correct and a `Done:` line is forbidden. That line is part of commit C5.
   Cap: 60 lines, or up to 100 if the per-commit table needs it (AGENTS.md
   handoff.md rule) — never drop a mandated section to fit; if you exceed 60,
   carry the stated-cause line naming the actual count and the mandated
   content that caused it.
   Commit: chore(f107): rewrite handoff for R7
   Then: git push (branch already tracks origin; plain push, never force)

Done when (run each, record command + real exit code + counted value):
  a. all five slice bodies' sha256 == their marker digests; the R7 block,
     .agent/authored/f107-r7-1.md and .agent/last_block.md byte-identical
     (name the tool you used).
  b. the C3 append proof from step 3: each FROM 1x in the file, each TO-only
     line 1x among the added lines, numstat deletions 0, '^## Steps' → 1,
     '^- R-0273' → 1.
  c. .agent/plan.md byte-identical to the verified PLAN6 bytes;
     wc -l < .agent/plan.md → 28 (PLAN6 is 28 lines).
  d. python3 -m pytest tests/orchestration/test_context_compiler.py -q
     → exit 0 (report the passed count; it includes the 52 frozen tests, so
     55 is the expected number and any other number needs explaining).
  e. python3 -m pytest tests/cli/test_golden_path.py -q → exit 0 (report the
     passed count).
  f. grep -c '^<<<' on .agent/live_review.md, .agent/plan.md and
     .agent/handoff.md → 0 each (grep exit 1 is the pass).
  g. git status --porcelain → empty; git worktree list → primary only;
     HEAD == origin/feature/f107-context-compiler-v2; insertions per commit
     (git log --numstat 861eb371..HEAD) each < 500.
  h. git diff --name-only 861eb371..HEAD → exactly the seven paths the Change
     line names, nothing else. Also: python3 -m ruff check
     packages/orchestration/context_compiler.py
     tests/orchestration/test_context_compiler.py → exit 0, zero errors
     (report the real output).
  i. both step-7 results, reported as run, with the failing test names.
Handback:    completion report (tables + raw gate results a–i + deviations)
             — .agent/handoff.md rewritten as C7.

<<<BEGIN SLICE LRF3FROM sha256=4ad9497dbf1e5bc5c62c9c7769bcb3d21948fc5607848e2b79d24381ba1e668d lines=1>>>
  fields that exist. OPEN.
<<<END SLICE LRF3FROM>>>

<<<BEGIN SLICE LRF3TO sha256=e3fdd1067cb91dbb3389947a34c3c3348ce583ca765f8e3b6864256d45e3257b lines=20>>>
  fields that exist. OPEN.
- R-0273 (Medium, F107 R6): a CompiledContext compiled with a NON-DEFAULT
  `line_cap` is RENDERED at the module default, so the budget's numbers stop
  describing the text that would actually be sent.
  `render_compiled_context_text` calls `_signature_render_text(root, path,
  DEFAULT_SIGNATURE_LINE_CAP)` unconditionally, while `compile_task_context`
  estimated every signatures file at the CALLER's `line_cap`
  (`packages/orchestration/context_compiler.py`). Measured by the reviewer on
  a three-file fixture at `line_cap=3`: `compiled.estimated_tokens` reads 25
  while the rendered text estimates at 128 — 5.1x — and `compare_context_size`
  reports `saved_ratio=0.84`, a saving that does not exist. Both the budget
  enforcement and the size comparison therefore rest on a figure that does not
  describe the segment. The cause is the R6 step block, which fixed the
  rendering signature at `(root, compiled)` with no cap; the worker followed
  that contract and DISCLOSED the consequence in its handback instead of
  widening scope, which is exactly the right worker behavior and is why this
  is a finding against the contract, not against the round. No caller passes a
  custom cap today, so nothing on disk is wrong yet — but T004 part 2 is the
  first caller and must not inherit it. Fixed in R7 per DECISION D-F107-2.
  OPEN.
<<<END SLICE LRF3TO>>>

<<<BEGIN SLICE LR6FROM sha256=d85c84acc5beeaa533d3df50dc20c38b77268ba4f657f4f0dfe81c6d72efad73 lines=1>>>
  `LAST_REVIEWED_SHA` advances 2c75bddf -> 54bc56c2.
<<<END SLICE LR6FROM>>>

<<<BEGIN SLICE LR6TO sha256=dac43442e587f6d5ac371efbbdef0115a328f3796f315f66e5f50f5990d4b82c lines=50>>>
  `LAST_REVIEWED_SHA` advances 2c75bddf -> 54bc56c2.
- Reviewer gate on R6 (2026-08-12): PASS, with one new finding. Range
  54bc56c2..861eb371 = seven commits touching exactly the seven paths the R6
  block named. Transport by the PRIMARY shape: `cmp` of
  `.remedy-wt/f107-r6-1.block.md` against `.agent/authored/f107-r6-1.md`, and
  of that copy against `.agent/last_block.md`, is silent, and all three sha256
  to c263869d4444… at 364 lines each. All five slice bodies recompute to their
  BEGIN-marker digests at their declared lengths (LRF2FROM 2bb66673… 1 line,
  LRF2TO 830262c1… 10, LR5FROM b96097af… 1, LR5TO 98b340c5… 51, PLAN5
  27f9c8ef… 28), and `sha256sum .agent/plan.md` returns that same PLAN5
  digest. Both C3 pairs were APPEND-shaped and were proven as such rather than
  as rewrites: `git show --numstat 2afec22b -- .agent/live_review.md` reads
  `59  0` — ZERO deletions, which is what proves neither anchor line was
  edited — each FROM still occurs exactly 1x in the file, each of the 9 LRF2TO
  and 50 LR5TO TO-only lines occurs exactly 1x among the 59 added lines, and 0
  added lines belong to neither body. Every scoped gate was RE-RUN by the
  reviewer rather than read from the handback: `python3 -m pytest
  tests/orchestration/test_context_compiler.py -q` returns 52 passed (the 42
  frozen tests plus 10 new), `tests/orchestration/test_prompt_segments.py`
  returns 25 passed — that module's suite was gated because this round imports
  from it for the first time — the canary `tests/cli/test_golden_path.py`
  returns 42 passed, `python3 -m ruff check` over the module and its test file
  returns "All checks passed!", `.agent/plan.md` is 28 lines, the Steps
  heading count is 1, `grep -c '^- R-0272'` is 1, the stray-marker count is 0
  across the three state files, `git status --porcelain` is empty, HEAD equals
  `origin/feature/f107-context-compiler-v2` and `git worktree list` shows the
  primary checkout alone. Insertions per commit 364, 285, 59, 10, 162, 190, 75
  — each under 500. The reviewer ran FOUR mutation probes in a disposable
  worktree at 861eb371, three of them deliberately different from the
  worker's: collapsing the block separator from a blank line to a single
  newline and dropping the tier number from the header line each redden
  exactly `test_render_compiled_context_text_builds_one_block_per_included`
  `_file`, and making the zero-baseline ratio guard return a fabricated 1.0
  reddens exactly `test_compare_context_size_reports_no_ratio_for_a_zero`
  `_baseline`. The worker's own probe reproduces verbatim — moving the
  registered rank from JOB_CONTEXT to TASK gives `2 failed, 50 passed`,
  reddening the segment-rank test and the manifest-row test — so the
  handback's probe evidence is confirmed TRUE rather than taken on trust. That
  worktree was removed and pruned before this verdict. All three declared
  deviations are accurate: the 100-line handoff sits exactly at the AGENTS.md
  D15 ceiling with its stated cause, the greedy `rstrip` is the reading that
  actually delivers the stated invariant, and the two docstring header updates
  are inside files the change set already names. What the round did NOT do is
  the finding: the worker's third disclosure — that a custom `line_cap` is
  rendered at the module default — is real, is larger than the note implied,
  and was MEASURED by the reviewer rather than accepted as written. It is
  registered above as R-0273 and R7 fixes it. Recorded as an observation and
  not a finding: `context_compiler.py` still has no caller outside its own
  test module, so F107 remains a library that is not yet wired to anything a
  user can run. `LAST_REVIEWED_SHA` advances 54bc56c2 -> 861eb371.
<<<END SLICE LR6TO>>>

<<<BEGIN SLICE PLAN6 sha256=047fcc7a691f958976fedb0c35b8de3b3a47bad0c879c451bc642c7975f3d161 lines=28>>>
# Plan — F107 Context compiler v2

Branch: feature/f107-context-compiler-v2, cut from main at 2e4142c3.
Next free finding ID: R-0274. R6 reviewed PASS at 861eb371.

## Goal
The context compiler selects fenced-path files, their direct import
neighbors, and only SIGNATURES of distant dependencies, under a total
context token budget with tier demotion — and writes an omissions record
naming everything it left out and why. DONE when a fixture repo's task
context shrinks measurably versus whole-files with the fixture task still
solvable by the fake provider, and the omissions record explains every
exclusion (docs/roadmap/features/T2_F107.md).

## Current Step
R7 — repair round for finding R-0273 (DECISION D-F107-2): carry the effective
signature line cap on CompiledContext and render from it, so a context
compiled at a custom `line_cap` can no longer be rendered at the module
default and the budget's figures always describe the text that would actually
be sent. Change set is packages/orchestration/context_compiler.py and
tests/orchestration/test_context_compiler.py. T001-T003 behavior is otherwise
frozen and the T004 part 1 segment layer keeps its public names.

## Next Steps
1. R8 — T004 part 2: the `remedy job context` CLI view, an end-to-end fixture
   task solved by the fake provider, and the size comparison in evidence.
2. Integration gate per docs/agents/integration_gate.md.
3. Closure per docs/roadmap/STATUS_closure_protocol.md.
<<<END SLICE PLAN6>>>
