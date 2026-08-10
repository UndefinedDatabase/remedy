# Handoff — F105 R38: record the R37 gate, resolve R-0261, register R-0262

Branch: feature/f105-cache-optimal-prompt-ordering. State-only round over
`c30b365e..HEAD`. Commits in order: ff537f4a (C1a), c5421db4 (C1b),
8f7105fe (C2), plus this C3 commit. Nothing under `packages/`, `apps/`,
`tests/` or `docs/` was touched this round. No mutation red-proof was ordered
and none was run: nothing executable changed (D8 item 5, DECISION F105 D10).

## Changed files
| Path | Commit | +/- | Reason |
|---|---|---|---|
| .agent/authored/f105-r38-1.md | ff537f4a | +230/-0 | the block, byte-identical to the scratch original |
| .agent/last_block.md | c5421db4 | +156/-265 | the same 230 lines |
| .agent/live_review.md | 8f7105fe | +62/-1 | PAIR_A ID bump, PAIR_B the R-0261 `Done:` plus R-0262, PAIR_C the R37 gate record |
| .agent/plan.md | C3 | +20/-13 | PAIR_P_PLAN verbatim, 49 lines |
| .agent/handoff.md | C3 | rewritten | this file |

## Items
| Item | Status | Reason |
|---|---|---|
| C1a | done | |
| C1b | done | |
| C2 | done | |
| C3 | done | |

## Verification (real exit codes, real output)
| Gate | Exit | Output |
|---|---|---|
| A transport | 0 / 0 / 0 | all three files `d746b069…`; both `cmp` runs silent |
| B size | 0 | `230 .agent/authored/f105-r38-1.md` — cap 400 (D5) |
| C pair shapes | 0 | declared == measured for all four — see proofs below |
| D reconciliation | 0 | C2 `ADDED 62 REMOVED 1`; STRAY ADDED 0, STRAY REMOVED 0 |
| E markers | 1 (grep no-match) | `^<<<` count `0` in live_review.md, plan.md and handoff.md |
| F state files | 0 / 0 | `tests/docs/` `294 passed in 0.30s`; dashboard `70 passed in 4.16s`; plan keeps `## Goal` 1x and `Steps` 1x; live_review keeps `## Steps` 1x |
| G no prod drift | 1 | RED as worded — see Deviations; green over the round's own range |
| H canary | 0 | golden path `42 passed in 19.55s` |
| I hygiene | 0 | `git status --porcelain` empty; `git worktree list` the primary alone; insertions 230, 156, 62, 70 — each under 500 |

## Authored-text proofs
Transport digest, all three files, 230 lines:
`d746b069f3954dada7f39dbc1b24a15fba7d5911f2cf671f66b828dc160ee46a`. PRIMARY
shape, not the digest fallback: the scratch original `.remedy-wt/f105-r38-1.block.md`
still exists and `cmp` against it is silent. Every pair was sliced out of the
COMMITTED authored file by a whole-line marker reader and never retyped.
DECLARED == MEASURED for all four. PAIR_A REWRITE: FROM 1x before, FROM 0x and
TO 1x after. PAIR_B and PAIR_C CONTAINS-FROM: FROM 1x before, FROM 1x and TO 1x
after. PAIR_P_PLAN a full replacement, `cmp` against the slice silent, 49 lines
against the cap of 50. No `Done:` and no `Landed:` line of the worker's own was
written; the block's authored text carries this round's only `Done:`.

## External actions
`git push` after C3. No PR — one is created at CLOSURE. No worktree created.

## Deviations, declared
Gate G is RED exactly as the block words it; the cause is its base SHA, not the
round. `git diff --name-only 25e6326a..HEAD` spans R37 too, so it lists eight
paths, two under `tests/` — `test_mission_compiler.py` and
`test_orchestrator_loop.py`, the comment-only edits of 82cbb3e5 that the
reviewer already gated PASS at R37. Over this round's own range,
`c30b365e..HEAD`, the list is `.agent/authored/f105-r38-1.md`,
`.agent/last_block.md`, `.agent/live_review.md` plus this commit's
`.agent/plan.md` and `.agent/handoff.md` — `.agent/` only, which is what the
gate meant to assert. Reported, not repaired: the block is authoritative and I
do not rewrite its gates. Base gate G on the previous LAST_REVIEWED_SHA next.
Length (DECISION D15): 75 lines, over 60. Cause, mandated content only: the
5-row changed-files table, the 4-row item-status table, the 11-row gate table,
the pair and transport proofs, and this declared deviation. No section dropped.

Open findings: 5 — R-0221, R-0239, R-0247, R-0256 and R-0262 are OPEN. R-0261
is now RESOLVED by reviewer-authored `Done:` text landed this round.

## Next
Gate R38 over `c30b365e..HEAD`, then run R39 per the plan's Next Steps — the
R-0256 fix: a keyword-only `composed=` on `plan_job_llm` and `run_intake` plus
the three `do_cmd.py` call sites, two tests, each red-proofed.
