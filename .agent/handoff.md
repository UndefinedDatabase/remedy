# Handoff — F105 R22 (worker → planner/reviewer)

R22 recorded the R21 gate, settled the schema tail as DECISION F105 D9 with a
test that PROVES the strict-prefix claim, and took migration-order step 5,
`pingpong_loop.py::_build_builder_prompt`, under a content-equality golden.
Branch: feature/f105-cache-optimal-prompt-ordering. Base 54049e6b.
Deviations, declared: this file is 80 lines against the AGENTS.md cap of 60.
Cause per DECISION D15, all of it mandated: the changed-files table over five
commits (nine path rows), the A-H gate table, gate H's own answer, the pair
proofs, the item-status table and three declared deviations. No section
dropped, no padding.

## Commits — changed files, one row per path
| Commit | Path | +/- | Reason |
|---|---|---|---|
| caf1440f `save the R22 block verbatim` | `.agent/authored/f105-r22-1.md` | +376/-0 | C1a — block ALONE, 376 lines, under D5's 400 |
| 9c121ddf `mirror the R22 block to last_block` | `.agent/last_block.md` | +306/-258 | C1b — `cp`, verbatim rewrite of ONE state file |
| 66f52226 `record the R21 gate` | `.agent/live_review.md` | +32/-0 | C2 — PAIR_A |
| 1e14e070 `pin the schema tail…` | `.agent/decisions.md` | +42/-0 | C3 — PAIR_B, DECISION F105 D9 |
| 1e14e070 | `tests/orchestration/test_prompt_segments.py` | +60/-1 | C3 — the D9 pin, one test class (+3 tests) |
| 769f025d `compose the builder prompt from segments` | `packages/orchestration/pingpong_loop.py` | +137/-28 | C4 — `compose_builder_prompt` + boundary rule |
| 769f025d | `tests/orchestration/test_builder_prompt_golden.py` | +255/-0 | C4 — the site-5 golden, 16 tests |
| (this commit) `update the plan and hand back R22` | `.agent/plan.md` | +14/-19 | C5 — PAIR_C full replacement |
| (this commit) | `.agent/handoff.md` | rewrite | C5 — this file (R-0149: cannot table its own SHA) |

Insertions: 376, 306, 32, 102, 392, this one — each under 500.

## Item status
| Item | Status | Reason |
|---|---|---|
| C1a | done | |
| C1b | done | |
| C2 | done | |
| C3 | done | |
| C4 | done | |
| C5 | done | |

## Verification (real exit codes, real output)
| Gate | Command | Exit | Real output |
|---|---|---|---|
| A | `sha256sum` pair; `cmp` | 0 / 0 | both `8f5fc0c8bf8bdb67…`; `cmp` silent |
| B | `wc -l` authored | 0 | `376` |
| C | 2 greps; marker grep; `wc -l` plan | 0/0/1/0 | `1`; `1`; `0`,`0`,`0` (exit 1 = no match, as intended); plan `45`, under 50 |
| D | golden; prompt_segments; pingpong trio; scope+task_input | 0/0/0/0 | `16 passed`; `25 passed` (baseline 22 + the 3 D9 pins); `336 passed` (before-count 336, UNCHANGED); `81 passed` (before-count 81, UNCHANGED) |
| E | `tests/cli/test_golden_path.py` | 0 | `42 passed in 21.05s` (baseline 42) |
| F | red-proof in `.remedy-wt/r22red`, detached at 769f025d | see dev. 1 | M1 (scope contract DOSSIER→STEERING): RED, `3 failed, 13 passed` — the two RANK tests plus the prefix measurement; the content-equality shapes stayed green, so the golden pins rank AND bytes separately. M2 (drop the leading-newline branch): stayed GREEN, `16 passed`, and `417 passed` across the pingpong/scope/task suites — declared, dev. 1. Both reverted; both worktrees removed and pruned |
| G | `git status --porcelain`; `git worktree list`; `git log --numstat` | 0/0/0 | empty at handback; primary alone; `+` per commit above, all <500 |
| H | assertion 4 | 0 | see below |

## Gate H — the shared prefix, measured
Assertion 4 measures **467 characters**. It does NOT end at the scope contract.
It runs past `builder_scope_contract` (ends at 401) and through the whole of
`builder_context` (ends at 441), then dies 24 characters into
`builder_staged_state`, on that segment's constant `## Current Staged State\n`
header. The block predicted the cutoff would come from `builder_task`'s round
number; that volatility is real (`builder_task`'s hash does differ) but it is
not the binding constraint, because the rank-3 staged state sorts AHEAD of the
rank-4 task. Splitting the round number out remains a CONTENT change and was
not attempted.

## Authored-text proofs
Transport: `.agent/authored/f105-r22-1.md` and `.agent/last_block.md` both
sha256 `8f5fc0c8…`, `cmp` exit 0, both 376 lines. Every pair SLICED by marker
with a python reader; marker count is 0 in all three targets.
| Pair | Target | Declared | Measured | FROM before/after | TO before/after | Stray |
|---|---|---|---|---|---|---|
| A | live_review | APPEND | APPEND | 1 / 1 | 0 / 1; 32 TO-only lines, min 1x | 32 added, 0 stray |
| B | decisions | APPEND | APPEND | 1 / 1 | 0 / 1; 34 TO-only lines, min 1x | 42 added, 0 stray |
| C | plan | full replacement | byte-equal | — | — | sha256 `45b21911…` on both |

## Deviations & assumptions
1. Gate F's M2 CANNOT go red, and did not. The `elif next segment starts with "\n"` branch is unreachable for this decomposition: every non-last segment's raw text already ends with `"\n"`, so the first branch always fires. Probed over all 64 optional-argument combinations — 352 boundaries, 352 trailing-branch, 0 leading-branch, 0 raise. With the branch deleted the golden and 417 wider tests stayed green. The branch and its raise are kept because the block specifies them and because a future segment edit is exactly what they exist to catch. M1 did go red, on rank tests, so gate F's rank half holds.
2. Gate H's answer contradicts the block's note about where the shared prefix ends (see above). Reported, not "fixed": changing it is a content change.
3. Shell layer: `cat`-heredoc redirection and `cd`-then-`git` are rejected here (carried from R15-R21). Slicing, gate running and the branch probe went through python helpers in gitignored `.remedy-wt/r22slices/`; every slice is marker-driven and no authored text was retyped.

## Next
The next round gates R22 over `54049e6b..HEAD` — a production file changed, so
a red-proof IS owed — then takes migration-order step 6,
`pingpong_loop.py::_build_reviewer_prompt`, last of the six.
Open findings: 4 (R-0221, R-0239, R-0246, R-0247).
