# Handback — F031 R56 (the last two §3 checklist items this branch owed)

Branch: `feature/f031-decision-inbox`. NO PRODUCTION CODE CHANGED — nothing under
`apps/`, `packages/` or `tests/` moved. The ONLY `docs/` file touched is
`docs/agents/planner_reviewer_prompt.md`, which gained §3 items 34 and 35. NO
FINDING WAS RESOLVED AND NO ID WAS MINTED. Open findings AFTER this round: **257**.

## Range

Review of `58de811a..c49ba739` (C4, the handoff commit, follows it).

## Commits

### 3dd7e63e docs(agent): save the F031 R56 step block
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f031-r56.md | +293/-0 | C0a — the block saved byte for byte |

### 49ac3279 docs(agent): mirror the F031 R56 block into last_block
| Path | +/- | Reason |
|---|---|---|
| .agent/last_block.md | +162/-116 | C0b — mirror; same git blob as C0a |

### 0799371f docs(agent): advance the plan to the F031 R56 checklist round
| Path | +/- | Reason |
|---|---|---|
| .agent/plan.md | +20/-20 | C1 — PLANF031R56 |

### 527ab509 docs(agent): record the F031 R55 verdict
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +2/-0 | C2 — LEDGER56 appended (gate entry only, no id) |

### c49ba739 docs(agent): add the read-the-target and prose-versus-list checklist items
| Path | +/- | Reason |
|---|---|---|
| docs/agents/planner_reviewer_prompt.md | +64/-0 | C3 — S2NEW as item 34, S3NEW as item 35 |

### C4 docs(agent): write the F031 R56 handback
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | self | C4 — a handback cannot table its own commit (R-0149) |

## Item status

| Item | Status | Reason |
|---|---|---|
| C0a save the block | done | |
| C0b mirror into last_block | done | |
| C1 the plan | done | |
| C2 the R55 gate entry | done | |
| C3 the two checklist items | done | |
| C4 handback | done | this commit |
| push | pending | `git push origin feature/f031-decision-inbox`, run right after C4 |

## External actions

`git push origin feature/f031-decision-inbox` after C4. No PR, gh or worktree command.

## Verification

- G1 BRANCH/CLEAN/TRANSPORT — exit 0. Branch `feature/f031-decision-inbox`; `git status --porcelain` 0 lines after C0a, C0b, C1, C2, C3. `.agent/STOP` ABSENT before C0a and before C4. Block sha256 `e7ad33b5…0264a2bc`, 24076 bytes, 293 lines — EQUAL at C0a, at C0b and off disk at C3; C0a and C0b are the SAME git blob `af0b07059b4b`.
- G2 EXTRACTION AND CAPS — exit 0. 4 slices printed from the COMMITTED C0a blob (PLANF031R56, LEDGER56, S2NEW, S3NEW). CONTENT 113, TOTAL 293, PROSE 180. PROSE 180 ≤ 400, TOTAL 293 ≤ 490.
- G3 THE PLAN — exit 0. `.agent/plan.md` at C1 BYTE-EQUAL to PLANF031R56 (newline-included) TRUE; minus-trailing-newline control FALSE. `^## Goal$` 1, `^## Next Steps$` 1, `wc -l` 48 (< 50).
- G4 THE APPEND, TWICE — exit 0. Pre-commit blob 920032 — exactly the byte count the block predicted — + 1 + 3797 = 923830; committed blob 923830; reader 1 ACCEPT. Reader 2: N counted by my own script = 1, units 373 before → 374 after, the last 1 unit matches the slice's 1 paragraph IN ORDER. Negative control flipped one byte IN MEMORY inside the FIRST appended paragraph: BOTH readers REJECT. Tracked file never mutated; past blobs read with `git show`.
- G5 THE LEDGER SETS — exit 0. Before C2 → after C2: `^- R-\d+ — ` 265→265, `^Done: R-\d+ — ` 8→8, `^Landed: R-` 0→0, `^Gate: R\d+ — ` 19→19, `^Gate: F\d+ R\d+ — ` 36→37. ADDED ids EMPTY, REMOVED EMPTY; ADDED gate keys exactly `F031 R55`, REMOVED EMPTY. Ids DISTINCT, maximum `R-0704` unmoved. Open set 257 before, 257 after.
- G6 THE CHECKLIST EDIT — exit 0. At `58de811a`: anchor line 1, `  34. **` 0, `  35. **` 0, 993 lines. At C3: S2NEW 1x, S3NEW 1x, anchor 1x, `^  34\. \*\*` 1x, `^  35\. \*\*` 1x, `^  36\. \*\*` 0x, 1057 lines; S2NEW ends exactly where S3NEW begins, S3NEW ends exactly where the anchor begins; delta 64 = 36 + 28, the two slices' own line counts measured from the slices. `git diff --name-only 527ab509..c49ba739` = `docs/agents/planner_reviewer_prompt.md` and nothing else; numstat `64 0` — ZERO deleted lines.
- G7 NOTHING ELSE MOVED — exit 0. `58de811a..c49ba739` path set both residues EMPTY over the 5 expected paths. `--stat` restricted to `apps/`, `packages/`, `tests/`, `docs/roadmap/` each EMPTY. `^<<<SLICE `/`^<<<END ` = 0/0 in the plan at C1, live_review at C2 and the reviewer prompt at C3, against a CONTROL of 4/4 over the C0a blob. Insertions 293, 162, 20, 2, 64 — each single-parent and under 500. `git ls-files .remedy-wt` 0 lines; `git worktree list` 1 line.
- G8 DOCS READERS, CANARY, STATE READERS — all exit 0, run SERIALLY, every count EQUAL to the base reading: `tests/docs/` 295 passed; `tests/test_agent_tooling.py` 10 passed 1 skipped; `tests/orchestration/test_role_conventions.py` 35 passed; `tests/cli/test_golden_path.py` 42 passed (canary); `tests/ui_server/` 489 passed; `tests/orchestration/test_test_runner.py` 52 passed; `tests/regression/test_resource_safety.py` 21 passed; `tests/orchestration/test_integrity_gate.py` 16 passed. The three `docs/agents/` readers did not move.

## Authored-text proofs

All four slices were extracted from the COMMITTED C0a blob by their `<<<SLICE`
and `<<<END` marker lines and applied byte for byte; none was retyped from the
prompt and no marker line reached a target. PLANF031R56 → `.agent/plan.md`
byte-equal (G3). LEDGER56 → `.agent/live_review.md` byte-equal append (G4).
S2NEW and S3NEW → `docs/agents/planner_reviewer_prompt.md`, 1 occurrence each,
36 and 28 lines, zero deletions (G6). The block round-trips at one sha256 across
C0a, C0b and disk (G1). No slice looked wrong; none was corrected.

## Deviations & assumptions

None. The ordered sequence C0a, C0b, C1, C2, C3, C4 ran exactly as given, no
commit added, dropped or reordered; C0a and C0b landed while `.agent/plan.md`
still described R55. No worktree was created and nothing destructive ran;
`.agent/decisions.md` and `docs/roadmap/` were not touched. Two scratch files
under the gitignored `.remedy-wt/` carried the extracted slices between steps and
were deleted BY EXACT PATH before C4; `git ls-files .remedy-wt` reads 0. Cap
DERIVED, not quoted: the Bundle orders SIX commits, more than five, so the
100-line tier applies and this handback is within it. Honesty note: the push row
reads `pending`, not `done` — C4 is written before the push and cannot observe
it; the push runs immediately after this commit.

## Next

1. Re-read `.agent/STOP` from disk.
2. The Open PR Gate (`gh pr list --state open --json number,headRefName,baseRefName,isDraft`).
3. Review this round's handback.
4. The resolution sweep: re-measure the landed code halves of R-0695, R-0697, R-0698 and R-0699 on disk and resolve them.
5. Only then R57, the markup.
