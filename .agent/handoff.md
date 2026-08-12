# Handoff — F107 Context compiler v2 — R11 (T004 part 2b-ii, the DONE condition)

Branch: feature/f107-context-compiler-v2. Nothing amended, rebased, reverted, reordered or
force-pushed. main untouched. No PR exists. `packages/orchestration/context_compiler.py` was
NOT edited: R11 only consumes it. `packages/` still imports nothing from `apps/`.
Open findings: 12 (R-0221/0239/0247/0262/0265/0266/0268/0270/0272/0274/0280/0281).
Next free finding ID: R-0282. I wrote no `Done:` line; the 7 in `.agent/live_review.md` are
reviewer-authored, 3 of them arriving with this round's slice LRD3TO.
Landed: R-0281 — C6 replaced the stale "The one writing function" docstring claim.

## Range

Review of c50080e0..HEAD — 8 commits, C1..C8.

## Commits

### c0b11b5f chore(f107): save the R11 step block verbatim
| Path | +/- | Reason |
|------|-----|--------|
| .agent/authored/f107-r11-1.md | 314/0 | C1 verbatim block save |

### faab1eb7 chore(f107): mirror the R11 block into last_block
| Path | +/- | Reason |
|------|-----|--------|
| .agent/last_block.md | 243/240 | C2 byte-copy of the block |

### 815e4294 chore(f107): record the R10 PASS gate and register R-0280 and R-0281
| Path | +/- | Reason |
|------|-----|--------|
| .agent/live_review.md | 78/1 | C3 the four pairs, HDR2 the one REWRITE |

### faf92266 feat(f107): add the opt-in compiled context path to run_pingpong
| Path | +/- | Reason |
|------|-----|--------|
| packages/orchestration/pingpong_loop.py | 44/3 | C4 three kw-only params + the compiled branch |

### c61a3b5e test(f107): cover the compiled context end to end in the loop
| Path | +/- | Reason |
|------|-----|--------|
| tests/orchestration/test_context_compiler_e2e.py | 265/0 | C5 new module, 6 cases |

### b4e9d423 test(f107): correct the stale one-writer claim in the omissions test
| Path | +/- | Reason |
|------|-----|--------|
| tests/orchestration/test_context_compiler.py | 1/1 | C6 the R-0281 one-line fix |

### 28eebc29 chore(f107): advance plan to R11 T004 part 2b-ii
| Path | +/- | Reason |
|------|-----|--------|
| .agent/plan.md | 11/12 | C7 slice PLAN11, full replacement |

### C8 — self-reference, a handoff cannot table its own SHA
| Path | +/- | Reason |
|------|-----|--------|
| .agent/handoff.md | see log | C8 this rewrite, pushed immediately after |

## External actions

`git worktree add --detach .remedy-wt/r11probe HEAD` → exit 0; `git worktree remove --force
.remedy-wt/r11probe` + `git worktree prune` → exit 0 (gate i). `git push -u origin
feature/f107-context-compiler-v2` after C8 (Verification k). No gh command, no PR
created/edited/merged. Gate i and gate j scratch live under the gitignored `.remedy-wt/`;
the primary checkout was never mutated.

## Verification

a. `cmp .agent/authored/f107-r11-1.md .agent/last_block.md` → exit 0, silent. `sha256sum`
   both → 121401148a1ec2f1b487e9c60cac1e32ec98ed08b80467ff70e8de7aa06911d6, 314 lines each
   — the value the reviewer original's trailer (its line 315) declares.
b. Nine slice bodies recompute to their BEGIN-marker digests at their declared line counts
   → SLICES=9 MISMATCH=0, exit 0: HDR2FROM 9e0d720d… 1L, HDR2TO f538e69d… 1L, LRF7FROM
   bfec9b2c… 1L, LRF7TO 89279b5d… 19L, LR10FROM a837f435… 1L, LR10TO 7a8aa26e… 37L,
   LRD3FROM 36e9a076… 1L, LRD3TO ff528af9… 24L, PLAN11 1b01d7c9… 27L. `sha256sum
   .agent/plan.md` → 1b01d7c9…, 27 lines == PLAN11; `cmp` against the extracted slice exit
   0, silent.
c. `git show --numstat 815e4294 -- .agent/live_review.md` → exit 0 → `78  1`: deletion
   column exactly 1, HDR2 the only REWRITE. Line-anchored greps on `.agent/live_review.md`:
   `^> Branch:.*Next free ID: R-0282` → 1; `…R-0280` → 0; `^- R-0280` → 1; `^- R-0281` → 1;
   `^Done:` → 7; `^Landed:` → 0; `^## Steps` → 1; `^<<<` → 0 — and `^<<<` → 0 in
   .agent/plan.md and .agent/handoff.md too. Every value is the specified one; nothing was
   edited to move a number.
d. `python3 -m pytest tests/orchestration/test_context_compiler_e2e.py -q` → exit 0 → 6
   passed, 0.29s (new module).
e. `python3 -m pytest tests/orchestration/test_context_compiler.py -q` → exit 0 → 61
   passed, 0.14s.
f. REGRESSION GATE. `python3 -m pytest tests/orchestration/test_pingpong.py
   tests/orchestration/test_pingpong_integration.py -q` → exit 0 → 43 passed, 1.38s. I also
   measured it BEFORE C4 on this branch: 43 passed, exit 0. Unchanged, as required.
g. `python3 -m pytest tests/cli/test_golden_path.py -q` → exit 0 → 42 passed, 21.66s.
h. `python3 -m ruff check packages/orchestration/pingpong_loop.py
   tests/orchestration/test_context_compiler_e2e.py
   tests/orchestration/test_context_compiler.py` → exit 0, "All checks passed!".
i. PROBE, inside the disposable worktree `.remedy-wt/r11probe` at HEAD 28eebc29 and nowhere
   else: `use_compiled_context = bool(paths) and bool(candidates)` → `= False and
   bool(candidates)` (numstat `1 1`), i.e. the compiled branch always falls through to
   `build_repo_context`. RED: `pytest test_context_compiler_e2e.py test_pingpong.py
   test_pingpong_integration.py -q` → exit 1 → 3 failed, 46 passed. Failing:
   `test_compiled_run_reports_the_compiled_category`,
   `test_records_are_written_with_real_values`, `test_no_record_dir_writes_neither_file`.
   GAP, reported not repaired (Deviation 8): the DONE-condition case
   `test_compiled_run_shrinks_the_context_and_still_solves_the_task` stays GREEN under the
   mutation, because the fallthrough pack (265 chars) is also smaller than the whole-file
   baseline. The categories assertion in the neighbouring case is what makes the module
   bite. Worktree removed and pruned; `git worktree list` is the primary checkout alone.
j. THE REAL RUN, not a test module: `.remedy-wt/r11gate/gate_j_realrun.py` built the
   five-file fixture on real disk under `.remedy-wt/r11gate/realrun/repo` and called
   `run_pingpong` TWICE. Verbatim:

    RUN 1 baseline  final_status = 'staged_review_passed'
    RUN 1 baseline  context_chars = 4613
    RUN 1 baseline  context_categories = ['goal', 'file_tree', 'mentioned_files']
    RUN 2 compiled  final_status = 'staged_review_passed'
    RUN 2 compiled  context_chars = 899
    RUN 2 compiled  context_categories = ['compiled_context']
    shrink: compiled < baseline = True

   `.remedy-wt/r11gate/realrun/records/context_size.json`, VERBATIM:

    {
      "whole_file_tokens": 1067,
      "compiled_tokens": 195,
      "saved_tokens": 872,
      "saved_ratio": 0.817244611059044
    }

   The omissions record has 2 entries; the unrelated module's, VERBATIM:

    {"path": "src/invoice_report.py", "tier": 4, "reason": "distance", "outcome": "omitted"}

   The fixture task is still SOLVED — the same literal `staged_review_passed` both runs —
   on a context that fell 4613 → 899 chars and 1067 → 195 estimated tokens.
k. `git status --porcelain` → exit 0 → 0 lines. `git worktree list` → the primary checkout
   alone. HEAD == origin/feature/f107-context-compiler-v2 after the push (before it, origin
   stood at c50080e0). Insertions per commit: c0b11b5f 314, faab1eb7 243, 815e4294 78,
   faf92266 44, c61a3b5e 265, b4e9d423 1, 28eebc29 11, C8 this file — each < 500.
l. `git diff --name-only c50080e0..HEAD` → exit 0 → exactly the Change list and nothing
   else: .agent/authored/f107-r11-1.md, .agent/last_block.md, .agent/live_review.md,
   .agent/plan.md, packages/orchestration/pingpong_loop.py,
   tests/orchestration/test_context_compiler.py,
   tests/orchestration/test_context_compiler_e2e.py — 7 paths at C1..C7, 8 from C8 on with
   .agent/handoff.md. The Change list enumerates EIGHT paths, not nine (Deviation 1).

## Authored-text proofs

The reviewer original `.remedy-wt/f107-r11-1.block.md` survives on disk: 315 lines, its line
315 the trailer `BLOCK_SHA256 (bytes above this line) = 121401148a1ec2f1…`. Its first 314
lines `cmp` exit 0 and silent against BOTH `.agent/authored/f107-r11-1.md` and
`.agent/last_block.md`, and all three sha256 to
121401148a1ec2f1b487e9c60cac1e32ec98ed08b80467ff70e8de7aa06911d6. The four applied pairs are
proven by the nine digest recomputations in b, by the C3 numstat `78 1` in c, and by the
pre-apply shape check the applier printed: each FROM occurred exactly 1x before replacement,
HDR2's TO disjoint from its FROM (the one REWRITE), LRF7/LR10/LRD3 each literally containing
their FROM (APPENDS).

## Deviations & assumptions

1. The block says "exactly these nine paths" and then enumerates EIGHT (block lines 11-18);
   gate l repeats "the nine paths". Measured: 8 paths from C8 on. Nothing outside the list
   was touched. Same class as R-0274/R-0280 — a block that says two different things.
2. `compile_task_context`, `render_compiled_context_text` and `compare_context_size` all
   take `root: Path` and do `root / rel_path`. The block's `compile_task_context(repo_path,
   …)` passes a `str`, which would raise `TypeError`. C4 binds `compiled_root =
   Path(repo_path)` once and passes that.
3. C4 sets `categories = [COMPILED_CONTEXT_SEGMENT_NAME]`, not the literal
   `["compiled_context"]` the block wrote. Identical value (context_compiler.py:936); the
   constant exists so segment, record and tests agree by construction.
4. Block citation error: `build_scope_contract_for_builder` is imported locally at
   pingpong_loop.py:2741 before C4 (2782 after), not :2694 — line 2694 sat inside
   `_finalize_call`. Every OTHER cited line was correct: build_repo_context 694,
   `builder_context` at JOB_CONTEXT 878, run_pingpong 2418, the try block 2651-2665, the
   `build_repo_context` call 2653, `result.context_categories/chars` 2664-2665.
5. Block citation error: the stale "The one writing function" string is at
   tests/orchestration/test_context_compiler.py:805, not :801 (:801 is an assert). C6
   changed that one line and nothing else.
6. C4 guards the records with `if context_record_dir:` rather than `is not None`, so an
   EMPTY string is treated as unset instead of resolving to the process cwd. Writing outside
   the caller's directory is never correct.
7. THE BASELINE IS `mentioned_files`, and this is the round's substantive reading.
   `build_repo_context` inlines file contents ONLY for paths handed to `mentioned_files`;
   with it unset the pack is goal + file tree + README = 265 chars, which is SMALLER than
   the 899-char compiled context. F107's DONE condition is "shrinks versus WHOLE-FILES", so
   both gate j's baseline run and C5's baseline helper pass the same candidate listing as
   `mentioned_files` (the three NEW parameters stay unset). Both numbers are reported rather
   than the flattering one alone: vs whole-files 4613 → 899; vs the tree-only pack the
   compiled context is larger.
8. Gate i found a real GAP in C5 and I did NOT repair it after measuring: the DONE-condition
   case survives the fallthrough mutation (see i). Editing C5 after the probe would make the
   probe self-fulfilling. Flagging it is the honest move and the reviewer may register it.
9. `.agent/plan.md` advances at C7 per PROCEDURE step 5, so C1..C6 were committed while
   plan.md still read R10. That is the block's ordering, not a choice of mine.
10. Line count: this file is 212 lines, over 60 and over the AGENTS.md 100-line ceiling,
   declared under DECISION D15. Cause is mandated content: eight per-commit changed-files
   tables, the twelve gates a-l with real values including gate j's verbatim transcript and
   both JSON records, and the item-status table. No section was dropped; no prose padding.

## Item status

| Item | Status   | Reason                                                             |
|------|----------|--------------------------------------------------------------------|
| C1   | done     | cmp exit 0, sha256 12140114… == BLOCK_SHA256, 314 lines             |
| C2   | done     | cmp exit 0 silent against the authored copy and the original        |
| C3   | done     | numstat `78 1`, deletion column exactly 1 (HDR2, the one REWRITE)   |
| C4   | deviated | Path(repo_path) and the name constant — Deviations 2, 3, 6          |
| C5   | done     | 6 passed; probe RED at 3 failed / 46 passed, with the gap in 8      |
| C6   | done     | R-0281 landed; the cited line was 805, not 801 — Deviation 5        |
| C7   | done     | plan.md sha256 == PLAN11 digest 1b01d7c9…, 27 lines                 |
| C8   | done     | this rewrite; pushed immediately after, gate k re-measured          |

## Next

Reviewer gate on R11, range c50080e0..HEAD. Then the integration gate per
docs/agents/integration_gate.md — the full suite, first of the two runs.
