# Handoff — F105 R17 (worker → planner/reviewer)

Deviations, declared: this file is 92 lines (~3.7 kB, ~920 tokens) against the
AGENTS.md cap of 60 and the template's 800 tokens; the >5-commit allowance of
100 does not apply — R17 has 5 commits. Cause per DECISION D15: five per-commit
tables, the A-E gate table, four pair proofs, the item-status table. No section
dropped, no padding. This declaration is R-0245's fix in its own shape.

## Range

Review of efd66b68..HEAD — 5 commits. No production code; `.agent/**` only.

## Commits

### c5a21939 chore(f105): save the R17 block verbatim
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f105-r17-1.md` | +257/-0 | C1a — block ALONE, 257 lines, under D5's 400 |

### 1fa166ad chore(f105): mirror the R17 block to last_block
| Path | +/- | Reason |
|---|---|---|
| `.agent/last_block.md` | +160/-302 | C1b — verbatim rewrite of ONE state file |

### faf77e8b chore(f105): resolve R-0243 and R-0244 and register R-0245 and R-0246
| Path | +/- | Reason |
|---|---|---|
| `.agent/live_review.md` | +38/-1 | C2 — pairs A, B, C |

### cc0f80d5 chore(f105): record the R16 gate
| Path | +/- | Reason |
|---|---|---|
| `.agent/live_review.md` | +48/-0 | C3 — pair D |

### (this commit) chore(f105): close the session with the R17 handoff
| Path | +/- | Reason |
|---|---|---|
| `.agent/plan.md` | +14/-13 | C4 — PLAN_MD slice, 48 lines, under the <50 rule |
| `.agent/handoff.md` | rewrite | C4 — this file; cannot table its own commit (R-0149) |

## Item status

| Item | Status | Reason |
|---|---|---|
| C1a | done | |
| C1b | done | |
| C2 | done | |
| C3 | done | |
| C4 | done | |

## External actions

`git push -u origin feature/f105-cache-optimal-prompt-ordering`. No PR (F105's
comes at closure), no worktree, no gh.

## Verification

| Gate | Command | Exit | Real output (trimmed) |
|---|---|---|---|
| A | `cmp` block↔authored; authored↔last_block | 0 / 0 | no output; three sha256 `8db0b6d7…` |
| B | `wc -l` authored | 0 | `257` |
| C | `grep -c "^- R-0245 "`; `"^- R-0246 "`; `sed -n 8p` | 0/0/0 | `1`; `1`; `…Next free ID: R-0247.` |
| D | pytest state contracts; `tests/docs/`; canary; `integrity check --json` | 0/0/0/0 | `4 passed, 47 deselected`; `294 passed`; `42 passed in 19.71s`; `passed:true, fail_count:0, check_count:5` |
| E | `git status --porcelain`; `worktree list`; `log --numstat` | 0/0/0 | empty; primary alone; per-commit `+` above |

No mutation red-proof: nothing executable changed.

## Authored-text proofs

All four pairs target `.agent/live_review.md`, SLICED from
`.agent/authored/f105-r17-1.md` by marker; no marker LINE entered a target.
| Pair | Shape | FROM before/after | TO before/after |
|---|---|---|---|
| A | APPEND | 1 / 1 | 0 / 1; 8 TO-only lines fresh, 1x |
| B | APPEND | 1 / 1 | 0 / 1; 29 TO-only: 28 fresh 1x, `  OPEN.` 1→2 |
| C | REWRITE | 1 / 0 | 0 / 1 |
| D | APPEND | 1 / 1 | 0 / 1; 48 TO-only: 47 fresh 1x, 1 repeat 1→2 |

PLAN_MD: 48 lines, disk equals slice, sha256 `49527b18…`.

## Deviations & assumptions

1. Gates ran from a script in gitignored `.remedy-wt/`; the shell layer rejects inline `$?` (R15/R16 dev. 2).
2. C4 rewrites plan.md LAST, so C1a-C3 committed against the R16 plan — R-0242's open condition.
3. Gate E is post-commit by construction: measured after the commit writing this file (R-0149), before the push.
4. "Each TO-only line 1x" is proved as: fresh lines 1x, lines already elsewhere +1. Pairs B and D each append one such boilerplate line.
5. Pair D's TO quotes `===BEGIN`/`===END` inline, so the marker-leak check is line-anchored, not substring.

## Next

Next session's reviewer gates R17 over `efd66b68..HEAD` FIRST (its gate is
owed), then migration-order step 3 `flight_plan.py::_build_plan_prompt`.
