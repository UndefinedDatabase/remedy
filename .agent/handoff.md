# Handback — F085 R45

Feature F085 (sandbox hardening) · Round R45 · Branch feature/f085-sandbox-hardening · Base SHA 981d08d0

## Range

Review of 981d08d0..HEAD

## Commits

### d6f42cd0 docs(f085): save the R45 block — C0a
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f085-r45.md | +477/-0 | block saved byte-verbatim from the reviewer's .remedy-wt file |

### 6977b3e8 docs(f085): mirror the R45 block into last_block — C0b
| Path | +/- | Reason |
|---|---|---|
| .agent/last_block.md | +410/-449 | identical bytes mirrored |

### 812626d3 docs(f085): record the R44 PASS, register eight findings, rule DECISION F085 D6 — C1
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +98/-0 | RECORD13 appended |
| .agent/decisions.md | +44/-0 | DEC6 appended |

### 778a74ba feat(f085): migrate the builder bridge test stage onto the stage-1 guard — C2
| Path | +/- | Reason |
|---|---|---|
| packages/orchestration/builder_bridge.py | +11/-5 | BBF1→BBT1, BBF2→BBT2, BBF3→BBT3 |
| tests/orchestration/test_builder_bridge.py | +59/-0 | TIMPF→TIMPT plus the TESTS append |

### 7cd2879d docs(f085): advance the plan to R46 — C3
| Path | +/- | Reason |
|---|---|---|
| .agent/plan.md | +7/-10 | PLANF1→PLANT1, PLANF2→PLANT2 |

### C4 — this commit, docs(f085): rewrite the handback for R45
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

G1 STATE, exit 0. `.agent/STOP` absent before C0a and again before C4. `git status --porcelain` exit 0 with empty output at round start and after each of C0a-C3. `git worktree list` one line throughout.

G2 TRANSPORT, exit 0. All five copies byte-EQUAL disk-to-disk, no digest fallback — reviewer `.remedy-wt/f085-r45.md`, committed `.agent/authored/f085-r45.md`, committed `.agent/last_block.md` and both working copies: sha256 448c531c3430eafe4efb0080363ff8c4e1908261f5d688bdbf248ce00c163cb0, 29951 B, 477 lines, 30 marker lines, each measured separately. Regions: lines 1-100 sha256 1ea3133c391af33f…, 7216 B; lines 101-end sha256 0651700f021fba95…, 22735 B; the two reassemble to the whole.

G3 APPEND SHAPE, exit 0, measured separately. RECORD13 → `.agent/live_review.md`: pre-commit blob is a byte-exact prefix true; remainder is exactly one blank line plus the slice true; slice is an exact suffix true; 0 marker LINES in the file; slice 97 lines of which 10 empty; C1 adds 98 lines to the path; 0 non-empty slice lines occur ≠1x among them; numstat `98 0`. DEC6 → `.agent/decisions.md`: prefix true, remainder true, suffix true, 0 marker LINES; slice 43 lines of which 5 empty; C1 adds 44 lines; 0 violations; numstat `44 0`.

G4 CODE, exit 0. `builder_bridge.py` reconstructs byte-identically from 981d08d0 under BBF1→BBT1, BBF2→BBT2, BBF3→BBT3: reconstructed sha256 5a95a367a15f9d34… = committed 5a95a367a15f9d34…. At HEAD BBF1 0x / BBT1 1x, BBF3 0x / BBT3 1x, BBT2 1x, 0 marker lines; numstat `11 5`. `test_builder_bridge.py` reconstructs byte-identically dffeaac42c130440… = dffeaac42c130440…; TIMPF 0x, TIMPT 1x. Ordered equality: the intermediate text (base with TIMPF→TIMPT already applied), 8226 B, IS a byte-exact prefix of the 10589 B post-commit file; TESTS is an exact suffix; the 59 lines C2 adds to that path are exactly TIMPT's 2 added lines followed by TESTS' 57, in order; 0 marker lines; numstat `59 0`.

G5 LINT, exit 0, primary checkout. `python3 -m ruff check packages/orchestration/builder_bridge.py tests/orchestration/test_builder_bridge.py` → `All checks passed!`

G6 SUITES, all three in the primary checkout, all exit 0. Five bridge files `-rf -q` → `82 passed, 1 skipped in 4.19s` (base 80 passed, 1 skipped; +2 = the two new tests). Four state-reading files `-rf -q` → `159 passed in 19.69s` (base 159). CANARY `tests/cli/test_golden_path.py -q` → `42 passed in 20.40s` (base 42).

G7 PLAN, exit 0. `.agent/plan.md` reconstructs byte-identically a4478c05ec9f2284… = a4478c05ec9f2284…; PLANF1 0x, PLANT1 1x, PLANF2 0x, PLANT2 1x; `## Goal` and `## Next Steps` both present; 0 marker lines; numstat `7 10`; 41 lines against the 50-line AGENTS.md cap.

G8 ARITHMETIC, exit 0. Line-start patterns `^- R-\d{4}`, `^Done: R-\d{4}`, `^Landed: R-\d{4}`. Base 981d08d0: 153 / 27 / 0, 126 open, max registered R-0538, max resolved R-0532, 0 duplicate ids, 0 resolutions naming an unregistered id. HEAD: 161 / 27 / 0, 134 open, max registered R-0546, 0 duplicates, 0 orphan resolutions. Symmetric differences: registered exactly R-0539 R-0540 R-0541 R-0542 R-0543 R-0544 R-0545 R-0546; done EMPTY; landed EMPTY. Next free id R-0547.

G9 HYGIENE, exit 0, measured before C4. `git diff --name-only 981d08d0..HEAD` returns exactly seven paths — `.agent/authored/f085-r45.md`, `.agent/decisions.md`, `.agent/last_block.md`, `.agent/live_review.md`, `.agent/plan.md`, `packages/orchestration/builder_bridge.py`, `tests/orchestration/test_builder_bridge.py` — the declared change set minus `.agent/handoff.md`, and nothing else. Insertions: C0a 477, C0b 410, C1 142, C2 70, C3 7; none exceeds 500, so the spent d4473f85 allowance was not touched. C4's own insertions go in the round report. Every commit has exactly one parent.

## Authored-text proofs

All 15 slices were extracted PROGRAMMATICALLY from the committed `.agent/authored/f085-r45.md` by BEGIN-/END- marker pair; none retyped, none taken from the prompt. Each FROM matched exactly 1x in its target at 981d08d0 (BBF1, BBF2, BBF3, TIMPF, PLANF1, PLANF2). Constraint 2's pair shapes reproduce as its own containment test's output: `TO contains FROM: true` for BBF2→BBT2 alone, `false` for BBF1→BBT1, BBF3→BBT3, TIMPF→TIMPT, PLANF1→PLANT1 and PLANF2→PLANT2. 0 marker lines reached any target file.

## Constraint 9 — the block's own size, re-measured from the committed file

TOTAL 477 lines, PROSE 219 (477 minus 258 slice lines, the counting DECISION F085 D5 fixes; R44's 516 / 277 / 239 reproduces the same rule). Both agree with the reviewer's stated PROSE 219 / TOTAL 477 — no disagreement.

## Constraint 7 — staleness sweep, measured

Each of the seven edited paths was written by exactly ONE commit of this round, so no sentence this round put on disk can have been falsified by a later commit of the same round. Every quote of another text names its commit (007f18df, f3e9687a, da47ee40, 91ad51ae, d4473f85, 9cc4772c), and each re-measures at HEAD: `git show --name-only 7c4a2583` returns exactly `.agent/plan.md`; the `## DECISION F085 D<n> —` heading count is 0 / 0 in live_review.md and 2 / 3 in decisions.md at 0e2cdacd / 4c7bcb3a; `500-line cap` occurs 2x in f085-r41.md at 9cc4772c; `def test_` in test_ci_run.py goes 10 at f3e9687a to 14 at 981d08d0; f085-r44.md is d8bf11c9…, 30615 B, 516 lines and contains neither `239` nor `516`; R-0545's 4206 B intermediate IS a byte-exact prefix of the 6317 B post-commit test_ci_run.py while its 4089 B pre-commit blob is not; `main..981d08d0` is 268 commits with exactly one over 500, d4473f85 at 516, next 454 then four at 400. All reproduce.

## Deviations & assumptions

1. This handback exceeds the 60-line cap under AGENTS.md DECISION D15. Cause, named: the six-commit per-commit changed-files table, the item-status table over C0a-C4, and the nine G1-G9 transcripts carrying their real numbers. No section was dropped. Actual line count: 103.
2. FINDING AGAINST THE BLOCK, applied byte-verbatim and NOT repaired (constraints 1 and 6): the DEC6 slice contradicts itself on the budget it rules. Its heading reads "budgeted at 480 lines TOTAL"; its CHOSEN paragraph, 18 lines below, reads "budgeted at 490 lines TOTAL", which is also what the block's Goal line and constraint 9 say. Harmless this round — the block measures 477, inside either number — but the ruled figure is now ambiguous on disk.
3. Observation only, no action: DEC6 quotes DECISION F085 D5's CHOSEN wording without naming D5's commit, inside the same commit that appends to `.agent/decisions.md` — the R-0520 shape. Not falsified, because C1 is a pure append and leaves D5 byte-identical.
4. No commit was added, dropped or reordered. The bundle ran C0a, C0b, C1, C2, C3, C4 exactly as ordered, with C1 before C2 per constraint 8.

Fortschritt: ~85 % (T001 gebaut · R13-R32 PASS · R33 FAIL, an R34 repariert · R34-R44 PASS ·
T002a KOMPLETT · T002b KOMPLETT, alle Sites der Klasse auf dem Seam · T002c-d, T003 offen) —
Schätzung, gegen die Klassentabelle aus Amendment F085 D1 gemessen.

## Next

R46. It makes the checklist item 16 widening this round cut for size, and opens T002c — the two DoD sites in `packages/orchestration/dod_runners.py`, whose policy differs because their children are the long-lived harness and take no wall timeout. T002d, T003, the integration gate and closure follow. R46's first reviewed act is recording R45's gate entry. Open findings: 134, next free id R-0547. Phase 1 rule 1 first: re-read `.agent/STOP` from disk.
