# Handoff — F021 R20 (self-drive)

## Range
Review of `45a437dc`..C4. ROUND BASE `45a437dc558e3f31f96e1058662b001b68d24083`, the R19 halt handback: single-parent, `.agent/handoff.md` alone, 69 insertions, under the 500 cap.

| Item | Status | Reason |
|---|---|---|
| C0a | done | |
| C0b | done | |
| C1 | done | |
| C2 | done | |
| C3 | done | |
| C4 | done | this commit |

Fortschritt: ~87 % (T002 — Feed, NowCard, Scroll-Regel und jetzt die
             Recency-Regel stehen als reine Funktionen; es fehlen nur noch ihre
             Verdrahtung und T003) — Schaetzung

## Commits

### 3df59508 docs(state): save the F021 R20 step block
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f021-r20.md | +459/-0 | C0a, the block saved byte-exact |

### a762bd51 docs(state): mirror the F021 R20 block into last_block
| Path | +/- | Reason |
|---|---|---|
| .agent/last_block.md | +98/-96 | C0b, written FROM the committed C0a blob |

### 476ad9e3 docs(state): point the F021 plan at R20 and the recency rule
| Path | +/- | Reason |
|---|---|---|
| .agent/plan.md | +21/-29 | C1, PLANF021R20 + one terminator, 43 lines |

### acb688a9 docs(review): record the R19 halt and register R-0654
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +6/-0 | C2, RECORD20 appended: R-0654 and `Gate: R20` |

### a71e5452 feat(ui): add the activity dot recency rule as a pure function
| Path | +/- | Reason |
|---|---|---|
| apps/ui/src/api/recency.ts | +44/-0 | C3, NEW: the pure recency rule |
| apps/ui/src/api/recency.test.ts | +58/-0 | C3, NEW: 11 vitest cases |
| tests/ui_contracts/test_brain_stream_ring.py | +32/-0 | C3, CONTRACTPATHS5 pair then CONTRACTRECENCY |

### C4, this handback commit — it cannot name its own SHA (R-0149/R-0494): docs(state): hand back F021 R20
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | rewrite | C4, this file |

## External actions
- `git worktree add --detach .remedy-wt/r20redctl a71e5452` — for G13; removed with `git worktree remove --force` then `git worktree prune`; `git worktree list` ends with the primary checkout alone.
- `gh pr list --state open --json number,headRefName` — `[]`. Neither `gh pr create` nor `gh pr merge` was run; F021 is mid-feature.
- `git push -u origin feature/f021-live-activity-feed` ordered after C4.

## Verification
One line per gate; transcripts stay in the round report (R-0582).
- G1 `.agent/STOP` ABSENT before C0a and again before C4; branch `feature/f021-live-activity-feed`; `git status --porcelain` 0 lines after each of C0a, C0b, C1, C2, C3.
- G2 TRANSPORT sha256 `3de736c0f4a30fb168d1e70160d180eede89dfe45c1fe55c7549146f1f51b6e3`, 30944 bytes, 459 lines, EQUAL over all four copies: received bytes, `.remedy-wt/f021-r20.md`, `.agent/authored/f021-r20.md` at C0a, `.agent/last_block.md` at C0b.
- G3 SLICES: the marker-LINE extractor over the committed C0a blob printed 7 slices and 183 CONTENT lines; TOTAL 459 ≤ 490 (D6) and PROSE 276 ≤ 400 (D5), both equal to constraint 9.
- G4 `cmp` plan.md vs PLANF021R20+newline exit 0; negative control vs the bare slice exit 1; last byte is a newline; `wc -l` EXACTLY 43; `^## Goal$` 1; `^## Next Steps$` 1. The extractor measured the slice at 43 lines.
- G5 reader (a) base is a byte-exact PREFIX, remainder exactly one newline + RECORD20 + one terminator; reader (b) units 243 → 246 elementwise, RECORD20 3 units; base sha256 `9060f703…56d6`, 516684 B / 1124 L before, 521496 B / 1130 L after; negative control at byte offset 2, `L`→`Z` in the FIRST paragraph `# Live Review …`, REJECTED by both readers, true file ACCEPTED by both.
- G6 base→C2: `- R-` 216→217 both DISTINCT; MAX R-0653→R-0654; `Done: R-` 0/0; `Landed: ` 0/0; `Gate: R` keys 18→19 both DISTINCT; `Gate: R20` 0→1; `Gate: R19` 0 at BOTH.
- G7 whole-string over raw bytes: base FROM 1, TO 0; C3 FROM 1, TO 1 — the append-shaped reading the gate predicts.
- G8 base contract 13034 B / 294 L; substituted in memory 13067 B is a byte-exact PREFIX of C3's 14374 B / 326 L; remainder 1307 B / 31 L, sha256 `e1212600fdfe595b3c02e3bacb1d3fa777ec9523ad158fd11e55ce9417ee5a88`.
- G9 blank lines immediately before `class TestTheRecencyRuleIsPureAndHeadless:` = 2.
- G10 recency.ts `cmp` 0 / control 1, 2012 B, 44 L, sha256 `14f990bd…2d49`; recency.test.ts `cmp` 0 / control 1, 1643 B, 58 L, sha256 `d7a227d3…3913`; BOTH ABSENT from `git ls-tree` at the round base, so C3 CREATES both and replaces nothing.
- G11 `npx tsc --noEmit`, cwd `/home/decodeux/Repos/remedy/apps/ui` — exit 0, empty output.
- G12 `npm run test:unit`, cwd `apps/ui` — exit 0, 15 files, 207 tests; recency.test.ts contributes 11.
- G13 worktree `.remedy-wt/r20redctl` at C3: GREEN first, 35 passed; target `    return "none";` unique, whole-line 1 and indent-agnostic 1 AGREEING; after `"none"`→`"idle"` exit 1 with 1 failed / 34 passed, the one failure `TestTheRecencyRuleIsPureAndHeadless::test_the_pre_stream_state_is_not_idle`, assertion text "nothing-has-acted-yet is a distinct level from acted-then-went-quiet". Tree pruned.
- G14 SERIAL, cwd = repository ROOT: `tests/ui_contracts/` exit 0, 461 passed + 4 skipped = 465; `tests/ui_server/ tests/orchestration/test_test_runner.py tests/regression/test_resource_safety.py` exit 0, 511; `tests/cli/test_golden_path.py` exit 0, 42.
- G15 base..C3: path set EQUALS the seven non-handoff `Change:` paths, difference EMPTY both ways; all five commits single-parent; `git show --numstat` and `git diff --numstat` agree cell by cell with `## Commits` above; largest per-commit insertions 459 < 500; `git ls-files .remedy-wt` 0; `git worktree list` the primary checkout alone; `gh pr list` `[]`; marker clause LINE-ANCHORED 0 in every file a slice landed in; reflog BY OPERATION over this round's 5 rows all `commit`, with `amend`, `rebase` and `cherry` 0 each.

## Authored-text proofs
`.agent/authored/f021-r20.md` at C0a is byte-equal to the received block and to the reviewer's `.remedy-wt/f021-r20.md` at sha256 `3de736c0…b6e3` (G2). Per slice: `.agent/plan.md`, `recency.ts` and `recency.test.ts` each `cmp` exit 0 against their mechanically extracted slice plus one terminator, each with a bare-slice negative control at exit 1 (G4, G10).

## Deviations & assumptions
- NO departure from the ordered commit sequence: C0a, C0b, C1, C2, C3, C4 exactly — no extra commit, none dropped, none reordered.
- DECISION D15 overage: this file is 87 lines against the 60-line cap. Mandated cause: six per-commit tables (>5 commits, the case the template's own ≤100 allowance covers), the fifteen mandated one-line gate results, and the item-status table. No section was dropped.
- OBSERVED, NOT FIXED (constraint 1): RECORD20's FIX paragraph, now committed at `acb688a9`, reads "this block's G4 says the slice is 47 lines, so the file is 47, and orders `wc -l` to read EXACTLY 47". G4 as written orders 43, and the extractor measured PLANF021R20 at 43. The slice was applied BYTE FOR BYTE as constraint 1 requires, so a stale numeral now sits in the ledger record; the reviewer owns whether to correct it.
- G15's marker clause was read as "every file a SLICE LANDED IN" — the five targets, all 0 line-anchored. `.agent/authored/f021-r20.md` and `.agent/last_block.md` read 14 line-anchored BY CONSTRUCTION: they ARE the block, not files a slice landed in.
- `npm run lint` was NOT run (constraint 8: red at base, R-0622, not a gate here).

## Next
THIS SESSION ENDS with C4. The next session's FIRST action is docs/agents/self_drive_protocol.md Phase 1 rule 1 — the `.agent/STOP` check — BEFORE rule 2's Open PR Gate (R-0347). Rule 2 will find NO open pull request, so rule 5 applies and F021 continues on this branch. R20's own verdict is UNRECORDED and the next round's C2 owes it. R21 wires BOTH pure rules: `recency.ts` becomes the ONE liveness source for the NowCard's badge AND its dot, and `feedScroll.ts` drives the feed's scroll container.
