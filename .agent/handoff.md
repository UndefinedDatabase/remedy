# Handback — F021 R17 (the feed's scroll discipline as a pure rule)

Feature F021, round R17. Branch `feature/f021-live-activity-feed`.
Round base `0328426b40c633c479fd77085a5991eb280a75c9`, the R16 handback commit.

Fortschritt: ~82 % (T002 — Feed und NowCard haengen am Stream, die Scroll-Regel
             liegt als reine Funktion vor; es fehlen ihre Verdrahtung, der
             Recency-Dot und T003) — Schaetzung

## Range

Review of 0328426b..HEAD, where HEAD is C4, the commit that writes this file.

## Item status

| Item | Status | Reason |
|------|--------|--------|
| C0a | done | block saved as authored text |
| C0b | done | mirrored from the committed C0a blob |
| C1 | done | plan rewritten to PLANF021R17 |
| C2 | done | R16 verdict recorded, R-0652 registered |
| C3 | done | pure rule, its vitest and its contract |
| C4 | done | this commit |

## Commits

### 8f676acb docs(state): save the F021 R17 step block as authored text
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f021-r17.md | +465/-0 | the block, byte for byte, NEW |

### 8223f301 docs(state): mirror the F021 R17 block into last_block
| Path | +/- | Reason |
|---|---|---|
| .agent/last_block.md | +378/-296 | written FROM the committed C0a blob |

### b45d0242 docs(state): point the F021 plan at R17 and the pure scroll rule
| Path | +/- | Reason |
|---|---|---|
| .agent/plan.md | +19/-13 | PLANF021R17 plus one terminating newline |

### bbf28b28 docs(review): record the R16 verdict as PASS and register R-0652
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +6/-0 | RECORD17 appended |

### cd1d56e2 feat(ui): decide feed scroll follow and unseen rows as a pure rule
| Path | +/- | Reason |
|---|---|---|
| apps/ui/src/api/feedScroll.ts | +50/-0 | FEEDSCROLL, NEW |
| apps/ui/src/api/feedScroll.test.ts | +64/-0 | FEEDSCROLLTEST, NEW |
| tests/ui_contracts/test_brain_stream_ring.py | +33/-0 | CONTRACTPATHS4 pair, then CONTRACTSCROLL append |

### C4, this commit, which cannot name its own SHA — docs(state): hand back F021 R17
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | rewrite | this handback |

## External actions

- `git worktree add --detach .remedy-wt/r17-red cd1d56e2` — created for G13; `git worktree remove --force .remedy-wt/r17-red` then `git worktree prune` — pruned, list is the primary checkout alone.
- `gh pr list --state open --json number,headRefName` — `[]`. Neither `gh pr create` nor `gh pr merge` was run; F021 is mid-feature.
- `git push -u origin feature/f021-live-activity-feed` after C4 — result in the round report.

## Verification — one line per gate, transcripts kept in the round report (R-0582)

- G1 PASS — `.agent/STOP` ABSENT immediately before C0a and again before C4; branch `feature/f021-live-activity-feed`; `git status --porcelain` 0 lines after each of C0a, C0b, C1, C2, C3. Owed reading from R16: `0328426b` is single-parent (parent `e9b0dc0b`) and touches `.agent/handoff.md` alone at 36 insertions, under the 500 cap.
- G2 PASS — the received bytes, `.remedy-wt/f021-r17.md`, `.agent/authored/f021-r17.md` at C0a and `.agent/last_block.md` at C0b are ALL FOUR sha256 `7732815b36f47b159610793c81933df3973e7d22266ef6be0f5487229a4e75e3` over 33614 bytes and 465 lines; C0b was written FROM the committed C0a blob.
- G3 PASS — the marker-LINE extractor over the committed C0a blob printed 7 slices and 201 CONTENT lines; re-measured from that same blob, TOTAL 465 against D6's 490 and PROSE 264 against D5's 400, both equal to constraint 9.
- G4 PASS — `cmp .agent/plan.md` against PLANF021R17 plus one newline exit 0; NEGATIVE CONTROL against the bare slice exit 1; last byte is a newline; `^## Goal$` 1, `^## Next Steps$` 1, `wc -l` 48, at most 50.
- G5 PASS — reader (a): the base blob (501252 B, 1112 L, sha256 `bfcbd70a…b39f`) is a byte-exact PREFIX and the remainder is EXACTLY one newline plus RECORD17 plus one newline at 7534 B, 6 L, sha256 `14feb550812a3b6cd59b96cfa13341d9c8d72591053057c7ac3d9dc230f81dc3`; the file goes 501252→508786 B and 1112→1118 L. Reader (b), SET-WISE and ELEMENTWISE over the whole list: 237 units → 240, RECORD17 exactly 3. NEGATIVE CONTROL at offset 2 of the FIRST paragraph, printable byte `L`→`X` at equal length: BOTH readers REJECTED the mutant and ACCEPTED the true file.
- G6 PASS — round base then C2, line-anchored: `- R-` 214 → 215, all DISTINCT at both points; maximum R-0651 → R-0652; `Done: R-` 0 → 0; `Landed: ` 0 → 0; `Gate: R` keys 16 → 17, both DISTINCT; `Gate: R17` 0 → 1.
- G7 PASS — CONTRACTPATHS4 by WHOLE-STRING search over raw bytes: round base FROM 1, TO 0; C3 FROM 1, TO 1, the append-shaped reading the block predicted. The base FROM count was 1, so no occurrence was chosen.
- G8 PASS — the contract at the round base (10535 B, 236 L) WITH CONTRACTPATHS4 substituted in memory (10570 B) is a byte-exact PREFIX of the file at C3, which reads 11962 B and 269 L; the prefix side IS the substituted blob; the remainder is EXACTLY one newline plus CONTRACTSCROLL plus one newline at 1392 B, 32 L, sha256 `224ed5417f81cc6a80dca71a5f0d756f631bc40a8180abd20cf29e857cf989f4`, equal to the digest the block predicted. No per-line count was used.
- G9 PASS — blank lines immediately before CONTRACTSCROLL's `class ` line in the C3 file: 2, COUNTED and not delegated to ruff.
- G10 PASS — both paths are ABSENT from `git ls-tree 0328426b`, so this round CREATES them and replaces nothing. `feedScroll.ts` 2254 B, 50 L, sha256 `18ef679bdef07998b0179c5013056a67a0999671f377be2b215c50c34737e205`; `feedScroll.test.ts` 2043 B, 64 L, sha256 `816df6037f463746aaedda9a7417ecb6595f0d24dc2a505699d84871acabbcd6`; `cmp` against slice-plus-newline exit 0 and 0, NEGATIVE CONTROLS against the bare slices exit 1 and 1.
- G11 PASS — `npx tsc --noEmit` in `/home/decodeux/Repos/remedy/apps/ui`, the PRIMARY checkout: exit 0, output EMPTY.
- G12 PASS — `npm run test:unit` in `/home/decodeux/Repos/remedy/apps/ui`, the PRIMARY checkout: exit 0, 14 test files and 196 tests, the exact reading the block ordered for one added file and eleven added cases.
- G13 PASS — disposable worktree `.remedy-wt/r17-red` at C3, a name no directory already used: GREEN FIRST at 28 passed. The target `    return FEED_SCROLL_START;` occurs EXACTLY ONCE, whole-line 1 and indent-agnostic 1, the two counts agreeing. With `    return prev;` in its place: exactly 1 failed, 27 passed, the failure `TestTheFeedScrollRuleIsPureAndHeadless::test_the_unseen_count_clears_at_the_newest_edge`, assertion text "returning to the edge clears the unseen count rather than decrementing it". Tree pruned.
- G14 PASS — SERIALLY, never two at once, from `/home/decodeux/Repos/remedy`, the REPOSITORY ROOT, exit 0 each, counted by PASSED PLUS SKIPPED: `tests/ui_contracts/` 454 passed + 4 skipped = 458; `tests/ui_server/` with `tests/orchestration/test_test_runner.py` and `tests/regression/test_resource_safety.py` 511 passed + 0 skipped = 511; the canary `tests/cli/test_golden_path.py` 42 passed + 0 skipped = 42.
- G15 PASS — base-to-C3 path set equals the seven non-handoff `Change:` paths, the difference EMPTY BOTH WAYS; all five commits single-parent; `git show --numstat` and `git diff --numstat` agree cell by cell with the `## Commits` tables above; insertions 465, 378, 19, 6 and 147, every one under the 500 cap; `git ls-files .remedy-wt` 0 lines; `git worktree list` ends with the primary checkout alone; `gh pr list --state open` EMPTY. LINE-ANCHORED marker sweep, first characters `<<<SLICE ` or `<<<END `: 0 in every one of the five files a slice landed in, while `.agent/live_review.md` reads 2 under the containment reading, which is exactly why the anchored form is the gate. Reflog read BY OPERATION FIELD — the text before the first `:` — over this round's 5 rows: every operation is `commit`, and `amend`, `rebase` and `cherry` each occur 0 times in that field.

## Authored-text proofs

`.agent/authored/f021-r17.md` at C0a is byte-identical to the received block and to the reviewer's emitted `.remedy-wt/f021-r17.md` at sha256 `7732815b…e75e3` (G2). Every slice was extracted MECHANICALLY from the committed C0a blob by its marker LINES and applied byte for byte, never retyped: the disk-to-disk `cmp` results are under G4 (plan) and G10 (both modules), and the two append proofs are under G5 (ledger) and G8 (contract).

## Deviations & assumptions

None. The block's ordered commit sequence C0a, C0b, C1, C2, C3, C4 was followed exactly — no extra commit, none dropped, no reordering — and only paths on the `Change:` list were touched.
DECISION D15 overage: this file is 94 lines against the 60-line cap. The cause is mandated content: six per-commit changed-files tables plus one line for each of fifteen gates. AGENTS.md permits up to 100 lines when per-commit tables of more than five commits require it, which this round's six commits do. No section was dropped to meet the cap.

## Next

THIS SESSION ENDS with C4. The next session's FIRST action is docs/agents/self_drive_protocol.md Phase 1 rule 1 — the `.agent/STOP` check — BEFORE rule 2's Open PR Gate (R-0347). Rule 2 will find NO open pull request, so rule 5 applies and F021 continues on this branch. R17's own verdict is UNRECORDED and the next round's C2 owes it. R18 is the recency dot, which also OWES the R-0652 repair: the NowCard's live badge must fade back to idle under that same pure recency rule instead of latching on forever once any action has entered the ring.
