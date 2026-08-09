# Handoff — F105 R16 (worker → planner/reviewer)

## Range

Review of ed5b2421..HEAD — 7 commits on `feature/f105-cache-optimal-prompt-ordering`.

## Commits

### eb41e0e7 chore(f105): save the R16 block verbatim
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f105-r16-1.md` | +399/-0 | C1a — the block ALONE, 399 lines, under D5's 400 |

### 65988c3b chore(f105): mirror the R16 block to last_block
| Path | +/- | Reason |
|---|---|---|
| `.agent/last_block.md` | +366/-194 | C1b — verbatim rewrite of ONE `.agent/**` state file (AGENTS.md exemption) |

### 6f295bf6 chore(f105): register R-0244 and amend R-0243
| Path | +/- | Reason |
|---|---|---|
| `.agent/live_review.md` | +24/-1 | C2 — pair A (append) + pair B (rewrite) |

### 618051d4 chore(f105): record the R15 gate
| Path | +/- | Reason |
|---|---|---|
| `.agent/live_review.md` | +35/-0 | C3 — pair C (append) |

### 7d661e10 chore(f105): record DECISION F105 D4 and D5
| Path | +/- | Reason |
|---|---|---|
| `.agent/decisions.md` | +55/-0 | C4 — pair D (append) |

### 934735e5 chore(f105): compose the mission prompt from registered segments
| Path | +/- | Reason |
|---|---|---|
| `packages/orchestration/mission_compiler.py` | +73/-12 | C5.2 — five sliced segment constants, `compose_mission_prompt`, D4's WHY comment |
| `tests/orchestration/test_mission_prompt_golden.py` | +182/-0 | C5.1 — the content-equality golden, 5 tests |

### (this commit) chore(f105): update the plan and write the R16 handoff
| Path | +/- | Reason |
|---|---|---|
| `.agent/plan.md` | +25/-32 | C6 — the PLAN_MD slice, 47 lines (R-0244 asked for ≤49) |
| `.agent/handoff.md` | rewrite | C6 — this file; a handoff cannot table its own commit (R-0149) |

## External actions

- `git worktree add --detach .remedy-wt/r16-mut HEAD` at 934735e5; `worktree remove --force` + `worktree prune` → primary alone.
- `git push -u origin feature/f105-cache-optimal-prompt-ordering`. No PR — F105's comes at closure.

## Verification

| Gate | Command | Exit | Real output (trimmed) |
|---|---|---|---|
| A | `cmp` block↔authored; authored↔last_block | 0 / 0 | no output; all three sha256 `744fe981…` |
| B | `wc -l .agent/authored/f105-r16-1.md` | 0 | `399` |
| C | `grep -c "^- R-0244 "`; `sed -n 8p` | 0 / 0 | `1`; `…Next free ID: R-0245.` |
| D | pytest `test_mission_prompt_golden.py -q` | 0 | `5 passed in 0.13s` |
| E | pytest `test_mission_compiler.py test_prompt_segments.py -q` | 0 | `135 passed` before AND after |
| F | pytest `test_test_runner.py -k …`; pytest `tests/docs/` | 0 / 0 | `4 passed, 47 deselected`; `294 passed` |
| G | pytest `tests/cli/test_golden_path.py`; `integrity check --json` | 0 / 0 | `42 passed in 19.49s`; `passed:true, fail_count:0, check_count:5` |
| H | `git status --porcelain`; `git worktree list`; `git log --numstat` | 0 / 0 / 0 | empty; primary alone; per-commit `+` above |

Mutation red-proofs, disposable worktree at 934735e5, suite = golden + mission_compiler + prompt_segments, baseline `140 passed`:
- M1 reorder two registrations (swap the `mission_rules`/`mission_goal` RANKS) → **3 RED**
  (`…ahead_of_the_goal`, `…names_and_ranks`, `…returns_the_composed_text`).
- M2 one word in the rules constant (`rejected`→`refused`) → **3 RED**
  (`…pre_migration_parts`, `…ahead_of_the_goal`, `…returns_the_composed_text`).
- M3 drop the schema directive's trailing newline → **3 RED**, the same three as M2.
- Control M0, swapping only the two `register()` STATEMENT positions → `140 passed`, 0 RED:
  a no-op by construction, the sort key being (rank, registration index).

## Authored-text proofs

All four pairs SLICED from `.agent/authored/f105-r16-1.md` by marker; no marker line entered a target.
| Pair | Target | Shape | FROM before/after | TO before/after |
|---|---|---|---|---|
| A | `live_review.md` | APPEND (TO starts with FROM) | 1 / 1 | 0 / 1; each of 23 TO-only lines x1 |
| B | `live_review.md` | REWRITE (disjoint) | 1 / 0 | 0 / 1 |
| C | `live_review.md` | APPEND | 1 / 1 | 0 / 1; each of 35 TO-only lines x1 |
| D | `decisions.md` | APPEND (3-line anchor) | 1 / 1 | 0 / 1; each of 44 TO-only lines x1 |

PLAN_MD slice: 47 lines, sha256 `8029c8ca…`, disk equals slice. Prompt bytes: the golden's
`_PRE_MIGRATION_MISSION_TEMPLATE` is `git show ed5b2421:…mission_compiler.py` lines 77-108, LHS name
aside, occurring x1; each of the five segment bodies occurs x1 in the migrated module. None retyped.

## Deviations & assumptions

1. Every gate ran from a script in gitignored `.remedy-wt/`: the shell layer rejects inline `$?`. Same commands, real exit codes (R15 dev. 2).
2. C6 rewrites `.agent/plan.md` LAST, so C1a-C5 were committed against the R15 plan — R-0242's own open condition, unchanged.
3. C5.1 test 5 "byte for byte": composition REORDERS, so byte identity is asserted as — the composed
   parts, put back in pre-migration order, join to exactly the frozen render, plus `endswith("\n")`
   and equal length. Literal equality of the two whole strings is impossible by design.
4. Mutation M1 is the RANK swap. A bare swap of the two `register()` statement positions changes
   nothing (the ranks differ), so it is reported as control M0, not passed off as a red proof.
5. `.pyc` caches are purged before each mutation run: M1 is byte-length neutral and a stale cache produced one false reading.

## Next

Planner/reviewer gates R16 over `ed5b2421..HEAD`, then migration-order step 3 (`flight_plan.py::_build_plan_prompt`), which needs a `repo_facts` seam first.
