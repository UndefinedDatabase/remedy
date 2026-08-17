# Handback — F085 R47

Feature F085 (sandbox hardening) · Round R47 · Branch feature/f085-sandbox-hardening · Base SHA c8da1928

## Range

Review of c8da1928..HEAD

## Commits

### e0eee32f docs(f085): save the R47 step block — C0a
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f085-r47.md | +308/-0 | block saved byte-verbatim from the reviewer's .remedy-wt file |

### 313e8321 docs(f085): mirror the R47 block into last_block — C0b
| Path | +/- | Reason |
|---|---|---|
| .agent/last_block.md | +259/-143 | identical bytes mirrored |

### 3fe2667d docs(f085): advance the plan to R47 — C1
| Path | +/- | Reason |
|---|---|---|
| .agent/plan.md | +8/-9 | PLANF→PLANT rewrite; first substantive commit, per the rule C23T writes |

### 243f91fc docs(f085): record the R46 PASS and register R-0548 — C2
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +62/-0 | RECORD15 appended |

### 522d925a docs(f085): widen checklist item 16 and add item 23 — C3
| Path | +/- | Reason |
|---|---|---|
| docs/agents/planner_reviewer_prompt.md | +36/-0 | C16F→C16T and C23F→C23T, both APPEND-shaped |

### C4 — this commit, docs(f085): rewrite the handback for R47
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
| C3 | done | |
| C4 | done | this commit |

## External actions

`git push -u origin feature/f085-sandbox-hardening` after C4. No worktree added, no PR, no merge.

## Verification

G1 STATE, exit 0. `.agent/STOP` absent before C0a and again before C4 (`ls` → "No such file or directory" both times). `git status --porcelain` exit 0, empty output at round start and after each of C0a, C0b, C1, C2, C3. `git worktree list` one line throughout.

G2 TRANSPORT, exit 0. All FIVE copies byte-EQUAL disk-to-disk, no digest fallback — reviewer `.remedy-wt/f085-r47.md`, committed `.agent/authored/f085-r47.md`, committed `.agent/last_block.md` and both working copies: sha256 a1d2fe72fd6425b5bbf3a06d13e9eb25dbebabb80bfd8a10e49694251cb5530f, 22123 B, 308 lines, 14 marker lines — each of the four values measured separately on every copy.

G3 SHAPES, exit 0, measured separately per pair and per path. C1 / PLANF→PLANT / `.agent/plan.md`, REWRITE: PLANF 0x, PLANT 1x in the post-commit file, 0 marker LINES, numstat `8 9`. C2 / RECORD15 / `.agent/live_review.md`, PROSE APPEND: pre-commit blob a byte-exact prefix true, remainder exactly one blank line plus the slice true, slice an exact suffix true, 0 lines matching `^(BEGIN|END)-[A-Z0-9]+$`; slice 61 lines of which 2 empty against 62 added lines; 0 non-empty slice lines occur ≠1x among them; numstat `62 0`. C3 / both pairs / `docs/agents/planner_reviewer_prompt.md`, both APPEND: C16F 1x and C16T 1x, C23F 1x and C23T 1x; TO-only lines 18 and 18, all non-empty, each occurring exactly once among the 36 lines C3 adds to the path (18+18=36, 0 violations); 0 marker LINES; numstat `36 0`.

G4 SUITE, both in the PRIMARY checkout, both exit 0. Four state readers `-rf -q` → `159 passed in 19.90s`, against the reviewer's base of 159 at c8da1928. CANARY `tests/cli/test_golden_path.py -q` → `42 passed in 20.39s`, base 42.

G5 PLAN CONTRACT, exit 0, on `.agent/plan.md` after C1: 40 lines (cap 50); `## Goal` true, `## Next Steps` true, `\bF\d{3}\b` true.

G6 ARITHMETIC, exit 0. Line-start patterns `^- R-\d{4} `, `^Done: R-\d{4}`, `^Landed: R-\d{4}`. Base c8da1928: 162 / 27 / 0, 135 open, max registered R-0547, max resolved R-0532, 0 duplicate ids, 0 resolutions naming an unregistered id — reproduces the reviewer's stated base exactly. HEAD: 163 / 27 / 0, 136 open, max registered R-0548, max resolved R-0532, 0 duplicates, 0 orphan resolutions. Symmetric differences: registered exactly R-0548; done EMPTY; landed EMPTY. Next free id R-0549.

G7 STRUCTURE, exit 0, on `docs/agents/planner_reviewer_prompt.md` after C3. Region walked from the checklist's introductory bullet (line 173) to `  Why this is on disk` (line 544). Numeral list as the walk produced it: 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23 — ascending, no duplicate, no gap. 0 lines match `^  24\. ` anywhere in the file. Item 23 stands at the END of the list, so no surviving entry was renumbered.

G8 HYGIENE, exit 0, measured BEFORE C4. `git diff --name-only c8da1928..HEAD` returns exactly five paths — `.agent/authored/f085-r47.md`, `.agent/last_block.md`, `.agent/live_review.md`, `.agent/plan.md`, `docs/agents/planner_reviewer_prompt.md` — the declared change set minus `.agent/handoff.md`, and nothing else. Insertions: C0a 308, C0b 259, C1 8, C2 62, C3 36; none exceeds 500, so the allowance spent at d4473f85 was not called on again. C4's own insertions go in the round report. Every commit has exactly one parent.

## Authored-text proofs

All five slices were extracted PROGRAMMATICALLY from the committed `.agent/authored/f085-r47.md` by BEGIN-/END- marker pair, read back through `git show HEAD:` — none retyped, none taken from the prompt, which carried none. PLANF sha256 5937c07070887623b58838a6396d9687c13015da3b3e29e380225031fac0acc5 (890 B, 14 lines); PLANT 730c6b2700a295794d792b5eaf34e068d82c2537e4cbc6e38f1200e17cccfdaa (801 B, 13 lines); RECORD15 a2f714830b29258056067e1c128a58c23ca94e74baa64eae87710703e946278b (5402 B, 61 lines); C16F 1906879ad126020c…, C16T 259e137eb4096733…, C23F db67c66d98688977…, C23T 327a60407c47298d…. Containment readings as constraint 3 orders: PLANT contains PLANF FALSE (REWRITE, FROM-zero reading reported under G3); C16T contains C16F TRUE and C23T contains C23F TRUE (APPEND, §4.9 per-line obligation discharged under G3). RECORD15 carries no FROM. 0 marker lines reached any target. The disk-to-disk equality against the reviewer's original is G2.

## Constraint 9 — the block's own size, re-measured from the committed file

TOTAL 308 lines; PROSE 180 — 308 minus the 128 lines strictly inside a marker pair, markers counted as prose, the counting DECISION F085 D5 fixes; RECORD15 61 lines. All three AGREE with the reviewer's stated PROSE 180 / TOTAL 308 / RECORD15 61; there is no mismatch to report. Inside the 490-line total D6-as-corrected-by-DEC6C rules, the 400-line prose cap and the 140-line RECORD cap.

## Deviations & assumptions

1. This handback exceeds the 60-line cap. It is inside the ≤100 allowance the template grants when per-commit tables of >5 commits require it (six here), and the cause is named as AGENTS.md DECISION D15 asks either way: the six-commit per-commit changed-files table, the item-status table over C0a-C4, the eight G1-G8 transcripts carrying their real numbers, the authored-text pair-and-digest proofs and the constraint 9 size reading. No section was dropped and no transcript was padded. Actual line count: 94.
2. No commit was added, dropped or reordered. The bundle ran C0a, C0b, C1, C2, C3, C4 exactly as ordered, C1 first among the substantive commits as constraint 4 requires, and no gate came out red.
3. `.agent/context.md` and `.agent/decisions.md` were NOT touched: this round changes no scope, assumption or constraint and rules no decision, and both paths are outside the block's change set.

Fortschritt: ~85 % (T001 gebaut · R13-R32 PASS · R33 FAIL, an R34 repariert · R34-R46 PASS ·
T002a KOMPLETT · T002b KOMPLETT, alle Sites der Klasse auf dem Seam · T002c-d, T003 offen) —
Schätzung, gegen die Klassentabelle aus Amendment F085 D1 gemessen.

## Next

R48, started by a FRESH session. R48 opens T002c with the two DoD sites in `packages/orchestration/dod_runners.py`, whose policy differs from the `test` class because their children are the long-lived harness and take no wall timeout. T002d, T003, the integration gate and closure follow. R47's own verdict is NOT on disk as a gate entry, because the round that records a verdict cannot record one on itself (docs/agents/planner_reviewer_prompt.md §4.13) — that absence is the terminator, not a missing gate, and R48 must not open a repair round to close it.
