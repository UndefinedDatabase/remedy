# Handback — F021 R16 (worker)

## Range
Review of 2d0532dad72e74ed0e8ecb2dd6292d12e6144673..HEAD — round base `2d0532da`, six commits C0a..C4.

## Commits

### 5c0b114f docs(state): save the F021 R16 step block
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f021-r16.md | +383/-0 | C0a, the block saved verbatim |

### 00535702 docs(state): mirror the F021 R16 block into last_block
| Path | +/- | Reason |
|---|---|---|
| .agent/last_block.md | +242/-297 | C0b, written FROM the committed C0a blob |

### 3c90509c docs(state): point the F021 plan at R16 and the now-card wiring
| Path | +/- | Reason |
|---|---|---|
| .agent/plan.md | +16/-18 | C1, PLANF021R16 + one terminator |

### 52d01adc docs(review): record the R15 verdict as PASS and register R-0651
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +6/-0 | C2, RECORD16 appended |

### e9b0dc0b feat(ui): show the newest stream action in the agent now-card
| Path | +/- | Reason |
|---|---|---|
| apps/ui/src/components/panels/AgentNowCard.tsx | +11/-4 | C3, ANCFILE whole-file write REPLACING a tracked file |
| apps/ui/src/components/panels/RightLivePanel.tsx | +1/-1 | C3, RLP3 pair |
| tests/ui_contracts/test_brain_stream_ring.py | +26/-0 | C3, CONTRACTPATHS3 pair then CONTRACTNOW append |

### C4 — this commit, whose SHA a handoff cannot name from inside itself (R-0494) — docs(state): hand back F021 R16
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | rewrite | C4, this file |

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
`git worktree add --detach .remedy-wt/redctl-r16 e9b0dc0b` — created for G13, a name no directory already used; `git worktree remove --force .remedy-wt/redctl-r16` + `git worktree prune` — removed, `git worktree list` now the primary checkout alone. `gh pr list --state open --json number,headRefName` — `[]`. `git push -u origin feature/f021-live-activity-feed` — run after C4. NO `gh pr create`, NO `gh pr merge`, no force-push, no history rewrite.

## Verification
G1 exit 0 — `.agent/STOP` ABSENT before C0a and again before C4; branch `feature/f021-live-activity-feed`; `git status --porcelain` 0 lines after each of C0a, C0b, C1, C2, C3. Owed reading from R15: `2d0532da` is single-parent (parent `0e1fe68f`) and touches `.agent/handoff.md` alone at +43, under the 500-insertion cap.
G2 exit 0 — sha256 `20b0e961a63693b03ef3913d6947803545f5e9b4b75d19dcff3a9e68a91258a5`, 31506 bytes, 383 lines, EQUAL across the received bytes, `.remedy-wt/f021-r16.md`, the C0a blob and the C0b file; C0b written from `git show 5c0b114f:.agent/authored/f021-r16.md`.
G3 exit 0 — extractor over the COMMITTED C0a blob by marker LINES printed 8 slices and 109 CONTENT lines; TOTAL 383 (cap 490) and PROSE 383-109 = 274 (cap 400), both equal to constraint 9.
G4 exit 0 / control exit 1 — `cmp .agent/plan.md` vs PLANF021R16+NL exit 0, vs the bare slice exit 1 (EOF after byte 2455); last byte is a newline; `^## Goal$` 1; `^## Next Steps$` 1; `wc -l` 42, at most 50.
G5 exit 0 — reader (a): base blob is a byte-exact PREFIX, remainder = NL+RECORD16+NL at 8272 bytes, 6 lines, sha256 `51e76c6dfce675845102190ca27cce38c1560f4086cb60ec5f8f8cb6cb048e4d`; file 492980 B / 1106 L before, 501252 B / 1112 L after. Reader (b) SET-WISE: units 234 -> 237 ELEMENTWISE equal, RECORD16 exactly 3 units (= the reviewer's THREE: finding, FIX, gate entry). NEGATIVE CONTROL at offset 2 of the FIRST paragraph, `L` -> `X`, equal length: reader (a) rejected ("base is not a prefix"), reader (b) rejected ("unit 0 differs"), both ACCEPTED the true file.
G6 exit 0 — base -> C2, all line-anchored: `- R-` 213 -> 214, DISTINCT at both; maximum `R-0650` -> `R-0651`; `Done: R-` 0 -> 0; `Landed: ` 0 -> 0; `Gate: R` keys 15 -> 16, DISTINCT at both; `Gate: R16` 0 -> 1. ONE id minted, none resolved.
G7 exit 0 — whole-string search over raw bytes, all eight numbers: CONTRACTPATHS3 (append-shaped) FROM 1 / TO 0 at the round base, FROM 1 / TO 1 at C3; RLP3 (replacing) FROM 1 / TO 0 at the round base, FROM 0 / TO 1 at C3. Both base FROM counts were 1, so no occurrence had to be chosen.
G8 exit 0 — the CONTRACTPATHS3-SUBSTITUTED base blob (9431 bytes, from 9367 B / 210 L at base) is a byte-exact PREFIX of the C3 file (10535 B / 236 L); remainder is EXACTLY NL+CONTRACTNOW+NL at 1104 bytes, 25 lines, sha256 `eff284d5939063acf1ce9f0d974160e2e5fc29806927e67aaa5232ff5cd5ea62` — identical to the reviewer's measurement. No per-line count used.
G9 exit 0 — blank lines immediately before CONTRACTNOW's `class ` line in the C3 file: 2. COUNTED, not delegated to ruff.
G10 exit 0 / control exit 1 — `apps/ui/src/components/panels/AgentNowCard.tsx` cmp vs ANCFILE+NL exit 0, vs the bare slice exit 1; 1517 bytes, 33 lines, sha256 `0418f0805c142ca82beea3dfc249299fc6f5f061303faea09e313f13a4a238f0` — the reviewer's digest exactly. At the round base the same path is 1009 bytes / 26 lines and `git ls-tree 2d0532da` DOES list it (blob `5e876b0b`), so this REPLACED a tracked file.
G11 exit 0 — `npx tsc --noEmit`, working directory `/home/decodeux/Repos/remedy/apps/ui` (PRIMARY checkout), stdout and stderr both EMPTY. Not red, so nothing was widened.
G12 exit 0 — `npm run test:unit` from `/home/decodeux/Repos/remedy/apps/ui` (PRIMARY checkout), the script defined as `vitest run` at apps/ui/package.json line 11: 13 test files, 185 tests, all passed. UNCHANGED from the round base, as the block predicted; this round adds no vitest case. No deviation was needed — the substituted form R-0651 documents is the form the block ordered.
G13 exit 0 then exit 1 — disposable worktree `.remedy-wt/redctl-r16` at `e9b0dc0b`: GREEN FIRST, exit 0, 24 passed. Target `      <AgentNowCard dashboard={dashboard} recent={recent} />` occurs EXACTLY ONCE, whole-line 1 and indent-agnostic 1, the two AGREEING. Unwired to `      <AgentNowCard dashboard={dashboard} />`: exit 1, 1 failed and 23 passed, the failure `tests/ui_contracts/test_brain_stream_ring.py::TestTheNowCardShowsTheNewestAction::test_the_panel_hands_the_ring_to_the_now_card` with `AssertionError: the NowCard is wired to nothing and shows the fallback forever`. Tree removed and pruned.
G14 exit 0 / 0 / 0 — SERIALLY from `/home/decodeux/Repos/remedy` (REPOSITORY ROOT), counting by passed plus skipped: `tests/ui_contracts/` 450 passed + 4 skipped = 454, the ordered rise of 3 over the base's 451; `tests/ui_server/ tests/orchestration/test_test_runner.py tests/regression/test_resource_safety.py` 511; `tests/cli/test_golden_path.py` 42 (canary). No docs gate owed.
G15 exit 0 — base..C3 path set EQUALS the seven non-handoff `Change:` paths, both differences EMPTY; five commits, EVERY one single-parent; `git show --numstat` and `git diff --numstat` agree cell by cell with `## Commits` above, no disagreement; insertions 383, 242, 16, 6, 38, all under 500; `git ls-files .remedy-wt` 0; `git worktree list` the primary checkout alone; `gh pr list --state open` `[]`, and neither `gh pr create` nor `gh pr merge` was run. Markers counted LINE-ANCHORED (first characters `<<<SLICE ` / `<<<END `): 0 in each of the five files a slice landed in — plan.md, live_review.md, AgentNowCard.tsx, RightLivePanel.tsx, test_brain_stream_ring.py; live_review.md reads 2 under the containment reading, which is why the clause is anchored. Reflog read by OPERATION field only (text before the first `:`) over this round's 6 rows: every one `commit`, and `amend`, `rebase`, `cherry` each 0 in that field.

## Authored-text proofs
All eight slices were extracted MECHANICALLY from the committed C0a blob by their marker LINES and applied byte for byte; none was retyped, rewrapped, reflowed or reindented. Disk-to-disk: `.agent/plan.md` cmp 0 against PLANF021R16+NL with the bare-slice control at 1 (G4); `AgentNowCard.tsx` cmp 0 against ANCFILE+NL with the bare-slice control at 1 (G10); the two appends are proved by prefix + remainder digest instead of cmp, `51e76c6d…8e4d` for RECORD16 (G5) and `eff284d5…ea62` for CONTRACTNOW (G8); the two pairs by the eight whole-string counts (G7). Constraint 5 honoured: `test_brain_stream_ring.py` took CONTRACTPATHS3 FIRST and CONTRACTNOW SECOND.

## Deviations & assumptions
NONE. The ordered commit sequence C0a, C0b, C1, C2, C3, C4 was followed exactly, with no extra, dropped or reordered commit, and no gate clause was edited around. Exactly ONE finding id was minted and none resolved: 214 open, maximum R-0651, next free R-0652. Only the paths in `Change:` were touched. `npm run lint` was neither run nor repaired (constraint 8).
D15 — this file is 82 lines against the 60-line cap. Cause is MANDATED content only: six per-commit changed-file tables (>5 commits, so AGENTS.md permits up to 100), the item-status table, fifteen one-line gate results, and the authored-text proofs. No section was dropped and no transcript was inlined (R-0582).

## Next
THIS SESSION ENDS with C4. The next session's FIRST action is docs/agents/self_drive_protocol.md Phase 1 rule 1 — the `.agent/STOP` check — BEFORE rule 2's Open PR Gate (R-0347). Rule 2 will find NO open pull request (`gh pr list --state open` reads `[]`), so rule 5 applies and F021 continues on `feature/f021-live-activity-feed`. R16's OWN verdict is UNRECORDED and the next round's C2 owes it. R17 is the scroll discipline that never yanks a reader who has scrolled up.

Fortschritt: ~80 % (T002 fast fertig — Feed und NowCard haengen jetzt beide am
             Stream; es fehlen Scroll-Disziplin, der Recency-Dot und T003)
             — Schaetzung
