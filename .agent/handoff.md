# Handback — F085 R48

Feature F085 (sandbox hardening) · Round R48 · Branch feature/f085-sandbox-hardening · Base SHA d6b06997

## Range

Review of d6b06997..HEAD

## Commits

### 452ffd2b docs(f085): save the R48 step block — C0a
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f085-r48.md | +213/-0 | block saved byte-verbatim from the reviewer's .remedy-wt file |

### 5e81e727 docs(f085): mirror the R48 block into last_block — C0b
| Path | +/- | Reason |
|---|---|---|
| .agent/last_block.md | +140/-235 | identical bytes mirrored |

### 360897f7 docs(f085): advance the plan to R48 — C1
| Path | +/- | Reason |
|---|---|---|
| .agent/plan.md | +3/-4 | PLAN2F→PLAN2T rewrite inside `## Current Step` only; first substantive commit, per checklist item 23 |

### 3bc7977b docs(f085): record the R47 PASS and register R-0549 — C2
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +61/-0 | RECORD16 appended |

### C3 — this commit, docs(f085): rewrite the handback for R48
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | rewrite | a handback cannot table the commit that writes it (R-0149) |

## Item status

| Item | Status | Reason |
|---|---|---|
| C0a | done | |
| C0b | done | |
| C1 | done | |
| C2 | done | |
| C3 | done | this commit |

## External actions

`git push -u origin feature/f085-sandbox-hardening` after C3. No worktree added, no PR, no merge.

## Verification

G1 STATE, exit 0. `.agent/STOP` ABSENT before C0a and again before C3 (`test -e` false at both points). `git status --porcelain` exit 0 and EMPTY at round start and after each of C0a, C0b, C1, C2. `git worktree list` one line throughout.

G2 TRANSPORT, exit 0. FIVE copies byte-EQUAL disk-to-disk, no digest fallback — reviewer `.remedy-wt/f085-r48.md`, committed `.agent/authored/f085-r48.md`, committed `.agent/last_block.md` and BOTH working copies: sha256 da6fd5a6a1de5b03d5f78f39c312a04c6504fe39a51065a82088fde08751ca38, 15488 B, 213 lines, 6 marker lines — every one of the four values measured separately on every copy.

G3 SHAPES, exit 0, measured separately per pair and per path. C1 / PLAN2F→PLAN2T / `.agent/plan.md`, REWRITE: `TO contains FROM: false`; over the whole post-commit file PLAN2F occurs 0x and PLAN2T exactly 1x; 0 marker LINES; numstat `3 4`. C2 / RECORD16 / `.agent/live_review.md`, PROSE APPEND: pre-commit blob a byte-exact PREFIX true, remainder exactly one blank line plus the slice true, slice an exact suffix true, 0 lines matching `^(BEGIN|END)-[A-Z0-9]+$` in the file; slice 60 lines of which 2 empty against 61 lines added to that path; 0 non-empty slice lines occur ≠1x among the added lines; numstat `61 0`.

G4 SUITE, both in the PRIMARY checkout and in no worktree, both exit 0. Four state readers `-rf -q` → `159 passed in 20.49s`, against the reviewer's base of 159 at d6b06997. CANARY `python3 -m pytest tests/cli/test_golden_path.py -q` → `42 passed in 21.49s`, base 42.

G5 PLAN CONTRACT, exit 0, on `.agent/plan.md` after C1: 39 lines against the 50-line cap; `## Goal` true, `## Next Steps` true, `\bF\d{3}\b` true.

G6 ARITHMETIC, exit 0. Line-start patterns `^- R-\d{4} `, `^Done: R-\d{4}`, `^Landed: R-\d{4}`. Base d6b06997: 163 / 27 / 0, 136 open, max registered R-0548, max resolved R-0532, 0 duplicate ids, 0 resolutions naming an unregistered id — reproduces the reviewer's stated base exactly. HEAD: 164 / 27 / 0, 137 open, max registered R-0549, max resolved R-0532, 0 duplicates, 0 orphan resolutions. Symmetric differences: registered exactly R-0549; done EMPTY; landed EMPTY. Next free id R-0550.

G7 HYGIENE, exit 0, measured BEFORE C3. `git diff --name-only d6b06997..HEAD` returns exactly four paths — `.agent/authored/f085-r48.md`, `.agent/last_block.md`, `.agent/live_review.md`, `.agent/plan.md` — the declared change set minus `.agent/handoff.md`, and nothing else. Insertions: C0a 213, C0b 140, C1 3, C2 61; none exceeds 500, so the declared-oversize allowance spent at d4473f85 was not called on again. C3's own insertions go in the round report. Every commit has exactly one parent.

## Authored-text proofs

All three slices were extracted PROGRAMMATICALLY from the committed `.agent/authored/f085-r48.md` by BEGIN-/END- marker pair, read back through `git show HEAD:` — none retyped, none taken from the prompt, which carried none. PLAN2F sha256 c80f4c5519770adb13d8d892fce33f1676f91d5eadfc28cc927088595b5affb4 (351 B, 5 lines); PLAN2T e2f9ebdf64daf0238fb77505636d191ba5ce6198bd4b41ae1c9c1006df1637d9 (273 B, 4 lines); RECORD16 69bde8b259fa45b6a917bc54e0868e616bb160a31a76fe819714f73394f412fd (5289 B, 60 lines). Containment as constraint 3 orders: PLAN2T contains PLAN2F FALSE → REWRITE, the FROM 0x / TO 1x reading reported under G3; RECORD16 carries no FROM, so no containment reading is owed for it. 0 marker lines reached any target file. The disk-to-disk equality against the reviewer's own original is G2.

## Constraint 8 — the block's own size, re-measured from the committed file

TOTAL 213 lines; PROSE 144 — 213 minus the 69 lines strictly inside a marker pair, markers themselves counted as prose, the counting DECISION F085 D5 fixes; RECORD16 60 lines. All three AGREE with the block's stated PROSE 144 / TOTAL 213 / RECORD16 60; there is no mismatch to report. Inside the 490-line TOTAL budget DECISION F085 D6 as DEC6C corrects it rules, inside the 400-line prose cap and inside the 140-line RECORD cap.

## Deviations & assumptions

1. This handback exceeds the 60-line cap and the >5-commit ≤100 allowance does not apply (five commits). DECISION D15 stated cause, naming the mandated content behind it: the five-commit per-commit changed-files table, the item-status table over C0a-C3, the seven G1-G7 transcripts carrying their real numbers, the authored-text pair-and-digest proofs and the constraint 8 size reading. No section was dropped and no transcript was padded. Actual line count: 92.
2. No commit was added, dropped or reordered. The bundle ran C0a, C0b, C1, C2, C3 exactly as ordered, with C1 first among the substantive commits as constraint 4 requires, and no gate came out red.
3. `.agent/context.md` and `.agent/decisions.md` were NOT touched: this round changes no scope, assumption or constraint and rules no decision, and both paths are outside the block's change set.

Fortschritt: ~85 % (T001 gebaut · R13-R32 PASS · R33 FAIL, an R34 repariert · R34-R47 PASS ·
T002a KOMPLETT · T002b KOMPLETT, alle Sites der Klasse auf dem Seam · T002c-d, T003 offen) —
Schätzung, gegen die Klassentabelle aus Amendment F085 D1 gemessen.

## Next

ONE. The next round is R49, started by a FRESH session, and it opens T002c with the two DoD sites in `packages/orchestration/dod_runners.py`, whose policy differs from the `test` class because their children are the long-lived harness and take no wall timeout; T002d, T003, the integration gate and closure follow.

TWO. R48's own verdict is NOT on disk as a gate entry, because the round that records a verdict cannot record one on itself (docs/agents/planner_reviewer_prompt.md §4.13) — that absence is the terminator, not a missing gate, and R49 must not open a repair round to close it; R48's verdict, when the reviewer issues it, is recorded by R49's OWN record slice.

THREE. Open findings: 137, next free id R-0550.

FOUR. Phase 1 rule 1 first: re-read `.agent/STOP` from disk.
