# Handoff — F105 R37: record the R36 gate, resolve R-0259/R-0260, fix R-0261

Branch: feature/f105-cache-optimal-prompt-ordering. Review of 25e6326a..HEAD.
Commits in order: 3cb60a80 (C1a), 4431344b (C1b), 02d14f35 (C2), 82cbb3e5 (C3),
plus this C4 commit. No production code: the two test edits change COMMENT and
DOCSTRING text only, so NO mutation red-proof was ordered or run (D8 item 5,
DECISION F105 D10) — the block explicitly ordered none.

## Changed files
| Path | Commit | +/- | Reason |
|---|---|---|---|
| .agent/authored/f105-r37-1.md | 3cb60a80 | +339/-0 | the block, byte-identical to the original |
| .agent/last_block.md | 4431344b | +281/-205 | the same 339 lines |
| .agent/live_review.md | 02d14f35 | +101/-3 | PAIR_V/W/X/Y/Z — ID bump, both `Done:` texts, R-0261, the R36 gate record |
| tests/orchestration/test_mission_compiler.py | 82cbb3e5 | +5/-2 | PAIR_F2, comment text only |
| tests/orchestration/test_orchestrator_loop.py | 82cbb3e5 | +4/-2 | PAIR_G2, docstring text only |
| .agent/plan.md | C4 | +8/-7 | PAIR_P_PLAN verbatim, 42 lines |
| .agent/handoff.md | C4 | rewritten | this file |

## Items
| Item | Status | Reason |
|---|---|---|
| C1a | done | |
| C1b | done | |
| C2 | deviated | five pairs applied byte for byte; the `Landed: R-0261` marker was NOT written — see Deviations |
| C3 | done | |
| C4 | done | |

## Verification (real exit codes, real output)
| Gate | Exit | Output |
|---|---|---|
| A transport | 0 / 0 / 0 | all three files `0fc0c2c7…`; `cmp` scratch-vs-authored and authored-vs-last_block both silent |
| B size | 0 | `339 .agent/authored/f105-r37-1.md` — cap 400 (D5) |
| C pair shapes | 0 | declared == measured for all 8 — see proofs below |
| D reconciliation | 0 | C2 is `101 3`; STRAY ADDED 0, STRAY REMOVED 0 |
| E markers | 1 (grep no-match) | `^<<<` count `0` in all five written targets |
| F state files | 0 / 0 | `tests/docs/` `294 passed in 0.30s`; dashboard `70 passed in 4.27s`; plan keeps `## Goal` 1x and `Steps` 1x, live_review keeps `## Steps` 1x |
| G scoped | 0 | compiler + loop `317 passed in 1.66s` |
| H number gone | 1 (grep no-match) | `test_mission_compiler.py:0`, `test_orchestrator_loop.py:0` |
| I comments only | 0 | 13 changed lines in C3, `NOT a comment line and NOT docstring prose: 0`; AST with docstrings blanked IDENTICAL before/after in BOTH files |
| J canary | 0 | golden path `42 passed in 20.86s` |
| K hygiene | 0 | `git status --porcelain` empty; `git worktree list` the primary alone; insertions 339, 281, 101, 9, 62 — each under 500 |

## Authored-text proofs
Transport digest, all three files, 339 lines:
`0fc0c2c71e800ac650febcf24dec1cc1a5733fc3998537ea8865b0ef9f99ef5a`. PRIMARY
shape, not the digest fallback: the scratch original still exists and `cmp`
against it is silent. Every pair was sliced from the COMMITTED authored file by
a whole-line marker reader and never retyped. DECLARED == MEASURED for all
eight: PAIR_V, PAIR_W, PAIR_X, PAIR_F2, PAIR_G2 REWRITE at FROM 1x before and
FROM 0x / TO 1x after; PAIR_Y and PAIR_Z CONTAINS-FROM at FROM 1x before and
FROM 1x / TO 1x after; PAIR_P_PLAN a full replacement proved by `cmp` silent
against the slice, 42 lines against the cap of 50. PAIR_Y's TO carried its blank
line verbatim; nothing was added to any slice.

## External actions
`git push` after C4. No PR — one is created at CLOSURE. No worktree created.

## Deviations, declared
Content: ONE deviation, declared not repaired. The round brief asked for a
`Landed: R-0261 — <one line>` marker in `.agent/live_review.md` for the fix C3
lands. The step block orders no such line — C2 names exactly PAIR_V/W/X/Y/Z, and
its own gate D mandates ZERO stray added lines against those five TOs. Writing
the marker would have made gate D red; the block is authoritative for what to
change and improvising authored text is forbidden, so the marker was omitted and
is reported here instead. R-0261 therefore reads OPEN on disk with no landing
marker, which under-claims rather than over-claims: `.agent/plan.md` (reviewer
text) already records that the fix lands this round and awaits the `Done:`.
Either accept 82cbb3e5 as the landing record or order the line next block.
Length (DECISION D15): 80 lines, over 60. Cause, mandated content only: the
7-row changed-files table, the 5-row item-status table, the 11-row gate table
and the pair proofs. No section was dropped.

Open findings: 5 — R-0221, R-0239, R-0247 and R-0256 fully open; R-0261 is
registered and OPEN, its fix landed at 82cbb3e5, awaiting the reviewer's
`Done:`. R-0259 and R-0260 are now RESOLVED by reviewer-authored `Done:` text.

## Next
Gate R37 over `25e6326a..HEAD`. Then the R-0256 round — compose once, not twice,
a signature change on `plan_job_llm` and `run_intake`, its own round (R38).
