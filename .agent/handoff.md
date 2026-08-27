# Handback — F031 R55 (the §3 checklist item R-0703 calls for, and the plan repair)

Branch: `feature/f031-decision-inbox`.
NO PRODUCTION CODE CHANGED — nothing under `apps/`, `packages/` or `tests/` moved.
The ONLY `docs/` file touched is `docs/agents/planner_reviewer_prompt.md`, the
reviewer prompt. `R-0704` is now ON DISK and OPEN. Open findings AFTER this
round: **257**.

## Range

Review of `84551691..b76aca50` (C4, the handoff commit, follows it).

## Commits

### f52c6446 docs(agent): save the F031 R55 block
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f031-r55.md | +247/-0 | C0a — the block saved byte for byte |

### f8132d3d docs(agent): mirror the F031 R55 block into last_block
| Path | +/- | Reason |
|---|---|---|
| .agent/last_block.md | +152/-88 | C0b — mirror; same git blob as C0a |

### 770b1a99 docs(agent): advance the plan to the F031 R55 checklist round
| Path | +/- | Reason |
|---|---|---|
| .agent/plan.md | +20/-14 | C1 — PLANF031R55; repairs the R-0704 defect |

### f8758096 docs(agent): record the F031 R54 verdict and register R-0704
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +4/-0 | C2 — LEDGER55 appended (gate entry + R-0704) |

### b76aca50 docs(agent): add the worktree colour item to the pre-emission checklist
| Path | +/- | Reason |
|---|---|---|
| docs/agents/planner_reviewer_prompt.md | +27/-0 | C3 — S1NEW inserted as item 33 |

### C4 docs(agent): write the F031 R55 handback
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | self | C4 — a handback cannot table its own commit (R-0149) |

## Item status

| Item | Status | Reason |
|---|---|---|
| C0a save the block | done | |
| C0b mirror into last_block | done | |
| C1 the plan | done | |
| C2 the R54 gate entry and R-0704 | done | |
| C3 the checklist item | done | |
| C4 handback | done | this commit |
| push | pending | `git push origin feature/f031-decision-inbox`, run right after C4 |

## External actions

`git push origin feature/f031-decision-inbox` after C4. No PR, gh or worktree command.

## Verification

- G1 BRANCH/CLEAN/TRANSPORT — exit 0. Branch `feature/f031-decision-inbox`; `git status --porcelain` 0 lines after C0a, C0b, C1, C2, C3. `.agent/STOP` ABSENT before C0a and before C4. Block sha256 `bff31a47…d0c4c41b`, 22145 bytes, 247 lines — EQUAL at C0a, at C0b and off disk at C3; C0a and C0b are the SAME git blob `6e018b05b1d0`.
- G2 EXTRACTION AND CAPS — exit 0. 3 slices printed from the COMMITTED C0a blob (PLANF031R55, LEDGER55, S1NEW). CONTENT 78, TOTAL 247, PROSE 169. PROSE 169 ≤ 400, TOTAL 247 ≤ 490.
- G3 THE PLAN — exit 0. `.agent/plan.md` at C1 BYTE-EQUAL to PLANF031R55 (newline-included) TRUE; minus-trailing-newline control FALSE. `^## Goal$` 1, `^## Next Steps$` 1, `wc -l` 48 (< 50).
- G4 THE APPEND, TWICE — exit 0. Pre-commit blob 914510 + 1 + 5521 = 920032; committed blob 920032; reader 1 ACCEPT. Reader 2: N counted by my script = 2, units 371 before → 373 after, last 2 units match the slice's 2 paragraphs IN ORDER. Negative control flipped one byte IN MEMORY inside the FIRST appended paragraph (the gate entry): BOTH readers REJECT. Tracked file never mutated; past blobs read with `git show`.
- G5 THE LEDGER SETS — exit 0. Before C2 → after C2: `^- R-\d+ — ` 264→265, `^Done: R-\d+ — ` 8→8, `^Landed: R-` 0→0, `^Gate: R\d+ — ` 19→19, `^Gate: F\d+ R\d+ — ` 35→36. ADDED ids {R-0704}, REMOVED {}; ADDED gate keys {F031 R54}, REMOVED {}. Ids DISTINCT, maximum `R-0704`. Open set 256 before, 257 after.
- G6 THE CHECKLIST EDIT — exit 0. At `84551691`: anchor line 1, `  33. **` 0, 966 lines. At C3: S1NEW 1x, anchor 1x, `^  33\. \*\*` 1x, `^  34\. \*\*` 0x, 993 lines; delta 27 = S1NEW's own 27 lines measured from the slice. `git diff --name-only f8758096..b76aca50` = `docs/agents/planner_reviewer_prompt.md` and nothing else; numstat `27 0` — ZERO deleted lines.
- G7 NOTHING ELSE MOVED — exit 0. `84551691..b76aca50` path set both residues EMPTY over the 5 expected paths. `--stat` restricted to `apps/`, `packages/`, `tests/`, `docs/roadmap/` each EMPTY. `^<<<SLICE `/`^<<<END ` = 0/0 in the plan at C1, live_review at C2 and the reviewer prompt at C3, against a CONTROL of 3/3 over the C0a blob. Insertions 247, 152, 20, 4, 27 — each single-parent and under 500. `git ls-files .remedy-wt` 0 lines; `git worktree list` 1 line.
- G8 DOCS READERS, CANARY, STATE READERS — all exit 0, run SERIALLY, every count EQUAL to the base reading: `tests/docs/` 295 passed; `tests/test_agent_tooling.py` 10 passed 1 skipped; `tests/orchestration/test_role_conventions.py` 35 passed; `tests/cli/test_golden_path.py` 42 passed (canary); `tests/ui_server/` 489 passed; `tests/orchestration/test_test_runner.py` 52 passed; `tests/regression/test_resource_safety.py` 21 passed; `tests/orchestration/test_integrity_gate.py` 16 passed. The three `docs/agents/` readers did not move.

## Authored-text proofs

All three slices were extracted from the COMMITTED C0a blob by their marker
lines and applied byte for byte; none was retyped. PLANF031R55 → `.agent/plan.md`
byte-equal (G3). LEDGER55 → `.agent/live_review.md` byte-equal append (G4).
S1NEW → `docs/agents/planner_reviewer_prompt.md`, 1 occurrence, 27 lines, zero
deletions (G6). The block itself round-trips at one sha256 across C0a, C0b and
disk (G1).

## Deviations & assumptions

None. The ordered commit sequence C0a, C0b, C1, C2, C3, C4 ran exactly as given,
no commit added, dropped or reordered. No slice was corrected. No finding was
resolved and no id was minted by me. `.agent/decisions.md` and `docs/roadmap/`
were not touched. Handback cap DERIVED, not quoted: the Bundle orders SIX
commits, more than five, so per-commit tables put this handback under the
100-line cap; it is within it. One honesty note: the push row of the item-status
table reads `pending`, not `done` — C4 is written before the push and cannot
observe it; the push itself is executed immediately after this commit.

## Next

1. Re-read `.agent/STOP` from disk.
2. The Open PR Gate (`gh pr list --state open --json number,headRefName,baseRefName,isDraft`).
3. Review this round's handback.
4. The remaining §3 checklist round: the R-0694 through R-0699 item, landed
   together with the counter-measure R-0704 names, after re-reading all seven
   findings from `.agent/live_review.md`.
5. Only then R56, the markup.
