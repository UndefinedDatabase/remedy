# Handoff — F107 Context compiler v2 — R10 (T004 part 2b-i, the size record + the docs)

Branch: feature/f107-context-compiler-v2. Nothing amended, rebased, reverted, reordered
or force-pushed. main untouched. No PR exists. The SELECTION behaviour is unchanged:
`compile_task_context`, the tiering, the budget demotion and `compare_context_size` were
not edited — C4 only ADDS a constant, an export and a writer.
Open findings: 13 (R-0221/0239/0247/0262/0265/0266/0268/0270/0272/0274/0277/0278/0279).
Next free finding ID: R-0280. I wrote no `Done:` and no `Landed:` line: of the four in
`.agent/live_review.md`, two arrived with this round's reviewer slice LRD2TO (R-0275,
R-0276) and two were already on disk from earlier rounds.

## Range

Review of f86bda87..HEAD — 8 commits, C1..C8.

## Commits

### 2841b6a9 chore(f107): save the R10 step block verbatim
| Path | +/- | Reason |
|------|-----|--------|
| .agent/authored/f107-r10-1.md | 311/0 | C1 verbatim block save |

### 30aaaa8e chore(f107): mirror the R10 block into last_block
| Path | +/- | Reason |
|------|-----|--------|
| .agent/last_block.md | 249/214 | C2 byte-copy of the block |

### 58742979 chore(f107): record the R9 PASS gate and register R-0277 through R-0279
| Path | +/- | Reason |
|------|-----|--------|
| .agent/live_review.md | 79/1 | C3 the four pairs targeting this file |

### 4ea02ff0 feat(f107): add the context size record export and writer
| Path | +/- | Reason |
|------|-----|--------|
| packages/orchestration/context_compiler.py | 60/5 | C4 constant + export + writer + docstrings |

### 96a6bd66 test(f107): cover the context size export and writer
| Path | +/- | Reason |
|------|-----|--------|
| tests/orchestration/test_context_compiler.py | 132/0 | C5 six appended cases + 4 import lines |

### f7d4551f docs(f107): document the job context view and index it
| Path | +/- | Reason |
|------|-----|--------|
| docs/guides/job-context-view-user-guide-v0.md | 184/0 | C6 new guide, written from the code |
| docs/README.md | 2/0 | C6 the IDXQ and IDXG rows |

### a6c56679 chore(f107): advance plan to R10 T004 part 2b-i
| Path | +/- | Reason |
|------|-----|--------|
| .agent/plan.md | 9/9 | C7 slice PLAN10, full replacement |

### C8 — self-reference, a handoff cannot table its own SHA
| Path | +/- | Reason |
|------|-----|--------|
| .agent/handoff.md | see log | C8 this rewrite, pushed immediately after |

## External actions

`git worktree add --detach .remedy-wt/r10probe HEAD` → exit 0, then
`git worktree remove --force` → exit 0 and `git worktree prune` (gate i).
`git push -u origin feature/f107-context-compiler-v2` after C8 (Verification k).
No gh command ran, no PR created/edited/merged. Gate i and gate j scratch live under the
gitignored `.remedy-wt/`; the primary checkout was never mutated.

## Verification

a. `cmp .agent/authored/f107-r10-1.md .agent/last_block.md` → exit 0, silent. `sha256sum`
   both → d0117326ae081a8dfdbed793b4f791d9e321fcf2e1f78437cfd4c59f2514ef60, 311 lines
   each — the value the reviewer original's trailer (its line 312) declares.
b. Thirteen slice bodies recompute to their BEGIN-marker digests at their declared line
   counts → SLICES=13 MISMATCH=0, exit 0: HDRFROM 969938db… 1L, HDRTO 9e0d720d… 1L,
   LRF6FROM 01fa41b1… 1L, LRF6TO 32d977f8… 29L, LR9FROM 4abc6ab4… 1L, LR9TO fc6bc0db…
   38L, LRD2FROM c87e031c… 1L, LRD2TO 7662036b… 14L, IDXQFROM 8b420a66… 1L, IDXQTO
   6876d1e0… 2L, IDXGFROM 4e4f9bb9… 1L, IDXGTO cca85dad… 2L, PLAN10 fd7a81e4… 28L.
   `sha256sum .agent/plan.md` → fd7a81e4…, 28 lines == PLAN10.
c. `git show --numstat 58742979 -- .agent/live_review.md` → exit 0 → `79  1`: deletion
   column exactly 1, HDR being the only REWRITE. `git show --numstat 58742979 --
   docs/README.md` → exit 0, EMPTY: the index rows are in C6, not C3 (Deviation 1); at
   C6, `git show --numstat f7d4551f -- docs/README.md` → `2  0`, deletion column 0 as
   the gate specifies. Line-anchored greps on `.agent/live_review.md`:
   `^> Branch:.*Next free ID: R-0280` → 1; `…R-0277` → 0; `^- R-0277` → 1; `^- R-0278`
   → 1; `^- R-0279` → 1; `^Done:` → 4; `^Landed:` → 0; `^## Steps` → 1; `^<<<` → 0 —
   and `^<<<` → 0 in .agent/plan.md, .agent/handoff.md and docs/README.md too. Every
   sub-check met its specified value; nothing was edited to move a number.
d. `python3 -m pytest tests/orchestration/test_context_compiler.py -q` → exit 0 → 61
   passed, 0.17s (55 before this round; C5 adds 6).
e. `python3 -m pytest tests/cli/test_job_context_cmd.py -q` → exit 0 → 9 passed, 2.56s.
f. `python3 -m pytest tests/cli/test_golden_path.py -q` → exit 0 → 42 passed, 19.70s.
g. `python3 -m pytest tests/docs/ -q` → exit 0 → 294 passed, 0.25s.
h. `python3 -m ruff check packages/orchestration/context_compiler.py
   tests/orchestration/test_context_compiler.py` → exit 0, "All checks passed!".
i. PROBE, inside the disposable worktree `.remedy-wt/r10probe` at HEAD a6c56679 and
   nowhere else: `target.write_text(payload + "\n")` → `target.write_text(payload)`
   (numstat `1 1`). RED, which is the wanted answer:
   `python3 -m pytest tests/orchestration/test_context_compiler.py -q` → exit 1 →
   1 failed, 60 passed —
   `test_write_context_size_comparison_json_creates_its_parent_and_round_trips` on
   `assert written_text.endswith("\n")`. Worktree removed and pruned; `git worktree
   list` is the primary checkout alone and `git status --porcelain` 0 lines after it.
j. THE REAL RUN, not a test: `.remedy-wt/r10gate/gate_j_realrun.py` over the real
   5-file git checkout `.remedy-wt/r9gate/demo_repo`, candidates from its own
   `git ls-files -z` (README.md, src/clock_source.py, src/invoice_report.py,
   src/payment_gateway.py, src/retry_policy.py), fenced `src/payment_gateway.py`.
   `compare_context_size` → ContextSizeComparison(whole_file_tokens=215,
   compiled_tokens=164, saved_tokens=51, saved_ratio=0.2372093023255814);
   `write_context_size_comparison_json` created the missing parent and returned
   `.remedy-wt/r10gate/realrun/context_size.json`. That file, VERBATIM:

    {
      "whole_file_tokens": 215,
      "compiled_tokens": 164,
      "saved_tokens": 51,
      "saved_ratio": 0.2372093023255814
    }

   whole_file_tokens = 215, compiled_tokens = 164. The 164 is the same number
   `remedy job context … --task T001` prints for that repo, so the record and the
   shipped view agree on the same selection.
k. `git status --porcelain` → exit 0 → 0 lines. `git worktree list` → the primary
   checkout alone. HEAD == origin/feature/f107-context-compiler-v2 after the push
   (before it, origin stood at f86bda87). Insertions per commit: 2841b6a9 311,
   30aaaa8e 249, 58742979 79, 4ea02ff0 60, 96a6bd66 132, f7d4551f 186, a6c56679 9,
   C8 this file — each < 500.
l. `git diff --name-only f86bda87..HEAD` → exit 0 → the Change list and nothing else:
   .agent/authored/f107-r10-1.md, .agent/last_block.md, .agent/live_review.md,
   .agent/plan.md, docs/README.md, docs/guides/job-context-view-user-guide-v0.md,
   packages/orchestration/context_compiler.py,
   tests/orchestration/test_context_compiler.py. Measured at C1..C7 that is 8 paths;
   .agent/handoff.md is the ninth and arrives with C8, so the count is 9 only from C8 on.

## Authored-text proofs

The reviewer original `.remedy-wt/f107-r10-1.block.md` survives on disk: 312 lines,
20764 bytes, line 312 the trailer `BLOCK_SHA256 (bytes above this line) = d0117326…`.
Its first 20660 bytes (the block body, 311 lines) `cmp` exit 0 and silent against BOTH
`.agent/authored/f107-r10-1.md` and `.agent/last_block.md`, and all three sha256 to
d0117326ae081a8dfdbed793b4f791d9e321fcf2e1f78437cfd4c59f2514ef60. The six applied pairs
are proven by the thirteen digest recomputations in b, by the C3 numstat `79 1` and the
C6 numstat `2 0` in c, and by the pre-apply shape check: each FROM occurred exactly 1x
in its target before replacement, HDR's TO disjoint from its FROM (the one REWRITE) and
the other five TOs each literally containing their FROM (APPENDS).

## Deviations & assumptions

1. docs/README.md is in C6, not C3. The block says both: PROCEDURE step 3 puts all six
   pairs in C3 and gate c measures `docs/README.md` at C3, while the Bundle line ("C6
   the user guide + the two index rows") and the Change list ("docs/README.md (C6, the
   IDXQ and IDXG pairs ONLY)") put them in C6. I took C6, because
   `tests/docs/test_docs_consistency.py::TestPrimaryDocLinksResolve` asserts every
   relative link in docs/README.md resolves: an index row landing in C3 points at a
   guide that does not exist until C6, so C3, C4 and C5 would each be a RED tree. Both
   readings are reported in Verification c.
2. C4 corrected a THIRD stale absolute claim the block does not name: the module
   docstring (context_compiler.py:49-51) said "nothing writes evidence EXCEPT
   `write_omitted_context_json`", which C4 makes false exactly like the two function
   docstrings the block does name. Same reason, same fix.
3. C4 added `from typing import Any` — the block's ordered signature
   `-> dict[str, Any]` needs it and the module had no typing import.
4. C5 is "append only" plus 4 lines inside the existing import block (CONTEXT_SIZE_
   FILENAME, ContextSizeComparison, export_…, write_…): the appended cases cannot
   reference the new names otherwise. No existing test line was changed.
5. NOT fixed, flagged instead: `tests/orchestration/test_context_compiler.py:801`
   still calls `write_omitted_context_json` "The one writing function" in a test
   docstring — the same stale absolute claim class as Deviation 2, but editing it is
   not an append, so the block's C5 constraint forbids it. A one-line fix for R11.
6. Every block-cited line number was checked and all were correct: OMITTED_CONTEXT_
   FILENAME at 931, write_omitted_context_json at 904 with the "ONLY writing function"
   sentence at 907, the dataclass docstring at 997, compare_context_size at 1012, the
   Public API list at 70-93, and the omissions-filename test at 963. No citation error
   this round.
7. Line count: this file is 197 lines, over the 60 of the block and over the AGENTS.md
   100-line ceiling, declared under DECISION D15. Cause is mandated content, counted
   mechanically: the Commits section's eight per-commit changed-files tables = 43
   lines, the Verification section's twelve gates a-l with their real values including
   gate j's verbatim JSON = 66 lines, the item-status table = 13 lines. 122 of the 197
   are those three blocks. No section was dropped to fit; no transcript was padded.

## Item status

| Item | Status   | Reason                                                          |
|------|----------|-----------------------------------------------------------------|
| C1   | done     | cmp exit 0, sha256 d0117326… == BLOCK_SHA256, 311 lines           |
| C2   | done     | cmp exit 0 silent against the authored copy and the original      |
| C3   | done     | numstat `79 1`, deletion column exactly 1 (HDR, the one REWRITE)  |
| C4   | done     | 60 insertions; constant + export + writer, selection untouched    |
| C5   | done     | 61 passed (55 → 61); the probe in gate i is RED, so C5 bites      |
| C6   | deviated | the two index rows land here, not in C3 — Deviation 1             |
| C7   | done     | plan.md sha256 == PLAN10 digest fd7a81e4…, 28 lines               |
| C8   | done     | this rewrite; pushed immediately after, gate k re-measured        |

## Next

Reviewer gate on R10, range f86bda87..HEAD. Then R11 = T004 part 2b-ii: the fixture task
solved by the fake provider with the compiled context as its JOB_CONTEXT segment, writing
both records into the task's evidence directory.
