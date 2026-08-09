# Handoff — F105 R24 (worker → planner/reviewer)

R24 took T003 migration-order step 6, `_build_reviewer_prompt` — the LAST of the
six sites. The golden was captured from the PRE-migration function and committed
RED (C3) before the migration (C4), as ordered. Both mutually exclusive branches
stay a branch over which segments are REGISTERED; the two diff caps stay
distinct; no caller changed; no evidence wiring.
Branch: feature/f105-cache-optimal-prompt-ordering. Base 554d9521.
Deviations, declared: this file is 88 lines against the AGENTS.md cap of 60.
Cause per DECISION D15, all of it mandated: the seven-row changed-files table,
the A-I gate table with real exit codes and real output, the pair-proof table,
the item-status table and the three declared deviations. Nothing dropped, no
padding.

## Commits — changed files, one row per path
| Commit | Path | +/- | Reason |
|---|---|---|---|
| 6944716e `save the R24 block verbatim` | `.agent/authored/f105-r24-1.md` | +258/-0 | C1a — `cp`, block ALONE, 258 lines, under D5's 400 |
| b1f04abf `mirror the R24 block to last_block` | `.agent/last_block.md` | +226/-336 | C1b — `cp`, verbatim rewrite of ONE state file |
| 44bc257f `record the R23 gate in the live review` | `.agent/live_review.md` | +34/-0 | C2 — PAIR_A, APPEND-shaped |
| 6a0050fb `freeze the reviewer prompt renders before migration` | `tests/orchestration/test_reviewer_prompt_golden.py` | +279/-0 | C3 — TEST-ONLY, ordered RED (gate D) |
| bc7b59b4 `compose the reviewer prompt from registered segments` | `packages/orchestration/pingpong_loop.py` | +142/-60 | C4 — `compose_reviewer_prompt`; `_build_reviewer_prompt` delegates `.text` |
| (this commit) `land the reviewer prompt migration and close R24` | `.agent/plan.md` | +9/-17 | C5 — PAIR_B full replacement |
| (this commit) | `.agent/handoff.md` | rewrite | C5 — this file (R-0149: cannot table its own SHA) |

Insertions: 258, 226, 34, 279, 142, this one — each under 500.

## Item status
| Item | Status | Reason |
|---|---|---|
| C1a | done | |
| C1b | done | |
| C2 | done | |
| C3 | done | red recorded before C4; see gate D and deviation 1 |
| C4 | done | |
| C5 | done | |

## Verification (real exit codes, real output)
| Gate | Command | Exit | Real output |
|---|---|---|---|
| A | `sha256sum` on authored + last_block; `cmp` | 0 / 0 | both `eb6e071e399cd967…`, equal to the scratch original; `cmp` silent |
| B | `wc -l` authored | 0 | `258` |
| C | PAIR_A counts; `cmp` plan vs sliced PAIR_B; `wc -l` plan; marker counts | 0 | FROM 1 before / 1 after (APPEND, TO⊃FROM as prefix); 34 TO-only lines, 33 at exactly 1x — see deviation 2; `cmp` silent, both sha256 `73562a3bc94d8077…`; plan `39` lines, under 50; `PAIR_A_FROM` / `PAIR_B_PLAN` / `END_PAIR` = 0/0/0 in BOTH `.agent/plan.md` and `.agent/live_review.md` |
| D | golden vs PRE-migration code (ordered RED) | 2 (RED, as ordered) | `ImportError: cannot import name 'compose_reviewer_prompt' from 'packages.orchestration.pingpong_loop'`, `ERROR tests/orchestration/test_reviewer_prompt_golden.py`, `1 error in 0.22s`, 0 tests collected. Re-measured for test NAMES in a disposable worktree at 6a0050fb with the compose import deferred into `_composed` (nothing committed): exit 1, `16 failed in 0.26s` — ALL 16: `test_segments_reassemble_into_the_frozen_render[fallback_full/fallback_minimal/scoped_full/scoped_minimal]`, `test_the_reorder_is_real`, `test_manifest_ranks_are_non_decreasing[x4]`, `test_the_scoped_full_shape_registers_its_segments_in_rank_order`, `test_the_fallback_full_shape_registers_its_segments_in_rank_order`, `test_the_rank_inversions_are_fixed_in_the_manifest`, `test_build_reviewer_prompt_returns_the_composed_text[x4]`. Worktree removed and pruned |
| E | `pytest tests/orchestration/test_reviewer_prompt_golden.py -q` | 0 | `16 passed in 0.18s` |
| F | the four caller suites | 0 | `234 passed in 1.76s`; baseline taken BEFORE C4 was `234 passed in 1.73s` — EQUAL, so the migration added no test to them and removed none |
| G | `pytest tests/cli/test_golden_path.py -q` | 0 | `42 passed in 19.68s` |
| H | two mutations in `.remedy-wt/r24mut`, detached at bc7b59b4 | 1 / 1 (RED, as ordered) | M1 `reviewer_goal` TASK→SYSTEM: `4 failed, 12 passed in 0.18s` — `test_the_reorder_is_real`, `test_the_scoped_full_shape_registers_its_segments_in_rank_order`, `test_the_fallback_full_shape_registers_its_segments_in_rank_order`, `test_the_rank_inversions_are_fixed_in_the_manifest` (first assert: `assert 2 < 1`, manifest `['reviewer_system','reviewer_goal','reviewer_scope',…]`). M2 drop the bare `"\n"` from `reviewer_system`: `5 failed, 11 passed in 0.19s` — all four `test_segments_reassemble_into_the_frozen_render[…]` plus `test_the_reorder_is_real`. Both reverted, worktree removed and pruned |
| I | `git status --porcelain`; `git worktree list`; `git log --numstat b35d9d56..HEAD` | 0 / 0 / 0 | empty at handback; primary alone; `+` per commit above, each under 500 |

Extra (not ordered): `ruff check` on both changed source files — exit 0, `All checks passed!`.

## Authored-text proofs
Transport: `.remedy-wt/r24scratch/block.md`, `.agent/authored/f105-r24-1.md` and
`.agent/last_block.md` all sha256 `eb6e071e399cd967e226a4179a977ea9…`, `cmp`
exit 0, 258 lines each. Both pairs SLICED by marker with a python reader; zero
marker strings in either target.
| Pair | Target | Declared | Measured | FROM before/after | TO added | Stray |
|---|---|---|---|---|---|---|
| A | live_review | APPEND (TO⊃FROM prefix) | APPEND, prefix confirmed | 1 / 1 | 34 lines, 0 removed | 0 (diff added == TO-only, in order) |
| B | plan | full replacement | byte-equal | — | — | sha256 `73562a3b…` on slice and target |

## Deviations & assumptions
1. Gate D asked for "the failure count and the failing test names". With the
   module-level import the sibling golden uses, the pre-migration red is a
   COLLECTION error: pytest reports `1 error`, exit 2, and NO test names exist.
   The red is real and is the point of C3. To answer the question the gate
   actually asks, it was re-measured at test-name granularity in a disposable
   worktree with the compose import deferred — 16 failed, every test in the
   file, names in the gate table. That deferral was never committed.
2. Gate C's "each TO-ONLY line exactly 1x" is unsatisfiable as literally
   written for one line: `` `git worktree list` the primary alone at this
   verdict. `` already occurs once in the R22 gate paragraph on disk (count
   before 1, after 2). The other 33 are at exactly 1x. Re-measured against the
   real diff instead: 34 added, 0 removed, 0 stray, added lines equal to the
   TO-only lines in order — exactly one occurrence added. Reported, not fixed.
3. Shell layer: inline `$?`, `echo "…$?"` and `cd`-then-`git` are rejected in
   this environment (carried from R15-R23). Slicing, application, capture,
   gate running and both red-proofs went through python helpers in gitignored
   `.remedy-wt/r24worker/`; no authored text was retyped.
Observation, not acted on: `_drop_one_newline_per_segment_boundary` now serves
the reviewer too but its error text still says "builder prompt segment
boundary". Outside the block's `Change:` list, so untouched.

## Next
The next round gates R24 over `554d9521..HEAD`. With step 6 landed, ALL SIX
T003 migration sites are done. Open findings: 4 (R-0221, R-0239, R-0246,
R-0247) — unchanged; none was in this round's scope.
