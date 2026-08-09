# Handoff — F105 R18 second attempt (worker → planner/reviewer)

Deviations, declared: this file is 115 lines against the AGENTS.md cap of 60 and
above the >5-commit allowance of 100 as well. Cause per DECISION D15, all of it
mandated: SEVEN per-commit tables, the A-H gate table plus three mutation
red-proofs, SIX pair proofs, the item-status table over C0-C6. No section
dropped, no padding, no transcript longer than command + exit code + verdict.

## Range
Review of 70156f31..HEAD — 7 commits; one touches production code (`flight_plan.py`).

## Commits
### e6d5b73f chore(f105): save the R18 block verbatim
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f105-r18-2.md` | +400/-0 | C1a — block ALONE, 400 lines, exactly D5's cap |
### 80095222 chore(f105): mirror the R18 block to last_block
| Path | +/- | Reason |
|---|---|---|
| `.agent/last_block.md` | +296/-153 | C1b — verbatim rewrite of ONE state file |
### db9cd606 chore(f105): resolve R-0245 and register R-0247
| Path | +/- | Reason |
|---|---|---|
| `.agent/live_review.md` | +18/-1 | C2 — pairs A, B, C |
### 73e78abb chore(f105): record the R17 gate
| Path | +/- | Reason |
|---|---|---|
| `.agent/live_review.md` | +27/-0 | C3 — pair D, the owed R17 gate |
### 4c19cbd1 chore(f105): record DECISION F105 D6 and resolve R-0242
| Path | +/- | Reason |
|---|---|---|
| `.agent/decisions.md` | +32/-0 | C4 — pair E, DECISION F105 D6 |
| `.agent/live_review.md` | +6/-0 | C4 — pair F, R-0242 RESOLVED |
### e5287ab2 chore(f105): compose the flight plan prompt from registered segments
| Path | +/- | Reason |
|---|---|---|
| `packages/orchestration/flight_plan.py` | +72/-9 | C5.2 — five segments, composer, `project_facts` seam |
| `tests/orchestration/test_plan_prompt_golden.py` | +174/-0 | C5.1 — the golden, 5 tests, written FIRST |
### (this commit) chore(f105): update the plan and write the R18 handoff
| Path | +/- | Reason |
|---|---|---|
| `.agent/plan.md` | +13/-15 | C6 — PLAN_MD slice, 46 lines, under the <50 rule |
| `.agent/handoff.md` | rewrite | C6 — this file; cannot table its own commit (R-0149) |

Insertions: 400, 296, 18, 27, 38, 246, this one — each under 500.

## Item status
| Item | Status | Reason |
|---|---|---|
| C0 | done | pair copied to `.remedy-wt/`, tree restored to HEAD, NOT committed |
| C1a | done | |
| C1b | done | |
| C2 | done | |
| C3 | done | |
| C4 | done | |
| C5 | done | golden first, then the migration |
| C6 | done | |

## External actions
`git worktree add --detach .remedy-wt/r18-mut HEAD` (gate H), then
`git worktree remove --force` + `git worktree prune` — primary alone after.
`git push -u origin feature/f105-cache-optimal-prompt-ordering`. No PR (F105's
comes at closure), no gh.

## Verification
| Gate | Command | Exit | Real output (trimmed) |
|---|---|---|---|
| A | `cmp` block↔authored; authored↔last_block | 0 / 0 | no output; three sha256 `a89262c0…` |
| B | `wc -l` authored | 0 | `400` |
| C | `grep -c "^- R-0247 "`; `"^## DECISION F105 D6 "`; `sed -n 8p` | 0/0/0 | `1`; `1`; `…Next free ID: R-0248.` |
| D | pytest golden; pytest bundled_clarification + prompt_segments | 0 / 0 | `5 passed in 0.17s`; `60 passed in 0.23s` |
| E | pytest state contracts; `tests/docs/`; canary; `integrity check --json` | 0/0/0/0 | `4 passed, 47 deselected`; `294 passed`; `42 passed in 19.56s`; `passed:true, fail_count:0, check_count:5` |
| F | `git status --porcelain`; `worktree list`; `log --numstat` | 0/0/0 | empty; primary alone; per-commit `+` above |
| G | BASELINE at 70156f31, taken before any edit | 0 | `60 passed in 0.23s`; gate D returns the same 60 — the golden is a new FILE |
| H | 3 mutations in a disposable worktree, each reverted | — | in-worktree baseline `5 passed`; all three RED |

Gate H, the expected test named first: M1 `plan_intake` at rank CONVENTIONS →
`test_rules_now_compose_ahead_of_the_intake` RED (also `..._manifest_names_and_ranks`,
`..._build_plan_prompt_returns_the_composed_text`), 3 failed 2 passed. M2 trailing
newline dropped → `test_build_plan_prompt_returns_the_composed_text` RED (also the
segment-set and ordering tests), 3 failed 2 passed. M3 `plan_repo_facts` registration
deleted → `test_segment_texts_equal_the_pre_migration_parts` RED (also 3 more),
4 failed 1 passed. No mutation left the suite green.
Not ordered, run anyway: `ruff check` on both C5 files → `All checks passed!`, exit 0.

## Authored-text proofs
Transport: block, `.agent/authored/f105-r18-2.md` and `.agent/last_block.md` all
sha256 `a89262c0…`, both `cmp` exit 0, 400 lines. Every pair SLICED by marker; no
marker LINE entered a target (`grep -c '^===BEGIN\|^===END'` is 0 in all three).
| Pair | Target | Shape | FROM before/after | TO before/after |
|---|---|---|---|---|
| A | live_review | APPEND | 1 / 1 | 0 / 1; 6 TO-only lines fresh, 1x |
| B | live_review | APPEND | 1 / 1 | 0 / 1; 11 TO-only lines fresh, 1x |
| C | live_review | REWRITE | 1 / 0 | 0 / 1 |
| D | live_review | APPEND | 1 / 1 | 0 / 1; 27 TO-only lines fresh, 1x |
| E | decisions | APPEND | 1 / 1 | 0 / 1; 25 fresh 1x, `Reverse this decision by deleting this entry.` 3→4 |
| F | live_review | APPEND | 1 / 1 | 0 / 1; 6 TO-only lines fresh, 1x |

PLAN_MD: `.agent/plan.md` equals its slice byte for byte, 46 lines.
C5 prompt bytes: the five segments were sliced BY LINE INDEX out of `git show
70156f31:packages/orchestration/flight_plan.py` lines 39-72, and rejoining them in
template order reproduces the frozen template body byte for byte (asserted in
`.remedy-wt/r18_2_c5_gen.py`). No prompt byte was retyped and none was edited.

## Deviations & assumptions
1. Gates ran from scripts in gitignored `.remedy-wt/`; the shell layer rejects inline `$?` (R15-R17 dev. 1).
2. C1a lands BEFORE C1b, so D6's mechanism — `last_block.md` as the round's plan of record — does not yet cover C1a itself. The block orders it so; declared, not reordered.
3. `_build_plan_prompt` gained a short docstring naming the new `project_facts` seam. The block mandated WHY comments only above `_PLAN_RULES_SEGMENT` and `compose_flight_plan_prompt`; this is an addition, not a substitution, and no caller or existing test was touched.
4. Gate E's `integrity check` ran twice: BEFORE the C5 commit it read `passed:false, fail_count:1` on `relevant_untracked: tests/orchestration/test_plan_prompt_golden.py`; the commit cleared it. The green row above is the post-commit run.
5. Gate F is post-commit by construction — measured after the commit that writes this file (R-0149), before the push.
6. C0's preserved pair sits at `.remedy-wt/f105-r18-attempt1-handoff.md` and `-plan.md`, uncommitted by design.

## Next
Reviewer gates R18 over `70156f31..HEAD` (`LAST_REVIEWED_SHA` is 70156f31), then
migration-order step 4, `orchestrator_loop.py::build_orchestrator_system_prompt`.
