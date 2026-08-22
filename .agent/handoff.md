# Handback — F021 R21 (record-only; session close)

Feature F021 Live activity feed + now-card · round R21 · branch `feature/f021-live-activity-feed`
Round base: `a2740317709d5fa4c2d49e488627ef8aaecabdef` (the R20 handback commit).
Fortschritt: ~87 % (T002 — Feed, NowCard, Scroll- und Recency-Regel stehen als
             reine Funktionen; es fehlen nur noch ihre Verdrahtung und T003)
             — Schaetzung

## Range
Review of `a2740317`..`ff33eab4` (C0a–C2); C3 below is the commit that writes this file.

## Commits

### 52d005ea docs(state): save the F021 R21 step block
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f021-r21.md | +227/-0 | C0a — the R21 block, NEW |

### 58790535 docs(state): mirror the F021 R21 block into last_block
| Path | +/- | Reason |
|---|---|---|
| .agent/last_block.md | +143/-375 | C0b — written FROM the committed C0a blob |

### e317ed2c docs(state): point the F021 plan at R22, the wiring round
| Path | +/- | Reason |
|---|---|---|
| .agent/plan.md | +16/-16 | C1 — PLANF021R21 plus one terminating newline |

### ff33eab4 docs(review): record the R20 verdict, register R-0655 and correct the numeral
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +6/-0 | C2 — RECORD21 appended; `acb688a9` untouched |

### C3 docs(state): hand back F021 R21 — the handback commit, which cannot name its own SHA (R-0494)
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | rewrite | C3 — this file |

## Item status
| Item | Status | Reason |
|---|---|---|
| C0a | done | |
| C0b | done | |
| C1 | done | |
| C2 | done | |
| C3 | done | this commit |

## External actions
`git push -u origin feature/f021-live-activity-feed` runs immediately after C3; a handoff cannot table its own push, so the outcome is in the round report. No PR created, no PR merged, no worktree added or removed. `gh pr list --state open --json number,headRefName` → `[]`.

## Verification — one line per gate; transcripts kept in the round report (R-0582)
G1 PASS — `.agent/STOP` ABSENT before C0a and again before C3; branch `feature/f021-live-activity-feed`; `git status --porcelain` 0 lines after each of C0a, C0b, C1, C2. Owed reading: `a2740317` is single-parent and touches `.agent/handoff.md` alone at +57/-66, under the 500-insertion cap.
G2 PASS — sha256 `d7ed04859b43ec3a52e6993e96605b13c54fd86849865372a539d70e176c0599`, 22534 bytes, 227 lines, EQUAL across all four copies (bytes received, `.remedy-wt/f021-r21.md`, the C0a blob, the C0b blob); C0b was written FROM the committed C0a blob.
G3 PASS — the marker-line extractor read 2 slices over 48 CONTENT lines from the committed C0a blob; TOTAL 227 against D6's 490 and PROSE 179 against D5's 400, both equal to constraint 7.
G4 PASS — `cmp` of `.agent/plan.md` against PLANF021R21 plus one terminator exit 0; NEGATIVE CONTROL against the bare slice exit 1; last byte is a newline; `wc -l` reads EXACTLY 43, the ordered and measured value; `^## Goal$` 1 and `^## Next Steps$` 1.
G5 PASS — reader (a): the base blob is a byte-exact PREFIX, remainder exactly one newline + RECORD21 + one newline, sha256 `5b19434918b0663d6d58a3ae5044f99a6b4fdf013772f0a637d5218c263c3aac`, 7741 bytes, 6 lines; file 521496 B / 1130 L before, 529237 B / 1136 L after. reader (b): units 246 → 249 ELEMENTWISE over the whole list, RECORD21 exactly 3 units. NEGATIVE CONTROL at offset 5, inside the FIRST paragraph, `e` → `X` at equal length: BOTH readers REJECT it and BOTH accept the true file.
G6 PASS — round base → C2: `- R-` 217 → 218, all DISTINCT at both points; maximum `R-0654` → `R-0655`; `Done: R-` 0 and `Landed: ` 0 at both; `Gate: R` keys 19 → 20, both DISTINCT; `Gate: R21` 0 → 1.
G7 PASS — over the C2 file `EXACTLY 47` occurs exactly TWICE (line 1128, RECORD20's original; line 1132, the verbatim quotation inside R-0655) and `EXACTLY 43` exactly ONCE (line 1134, RECORD21's FIX line). `git diff a2740317..ff33eab4 -- .agent/live_review.md` has 0 deleted lines and 6 added — `acb688a9` was not edited.
G8 PASS — run SERIALLY from the repository root, cwd `/home/decodeux/Repos/remedy`, counting by passed plus skipped: the three state-reading suites exit 0 at 511; the golden-path canary exit 0 at 42; `tests/ui_contracts/` exit 0 at 461 passed + 4 skipped = 465, UNCHANGED. No docs gate is owed. Neither `npx tsc --noEmit` nor `npm run test:unit` was ordered, and neither was run.
G9 PASS — base..C2: 4 commits, every one single-parent; the path set EQUALS the four non-handoff `Change:` paths with both differences EMPTY; `git show --numstat` and `git diff --numstat` agree cell by cell with the tables above; insertions 227, 143, 16 and 6, each under the 500 cap; `git ls-files .remedy-wt` 0; `git worktree list` the primary checkout alone, no worktree created; `gh pr list --state open` `[]`, and neither `gh pr create` nor `gh pr merge` was run; the LINE-ANCHORED marker sweep reads 0 in `.agent/plan.md` and 0 in `.agent/live_review.md`; the reflog read BY OPERATION shows this round's four rows all `commit`, with `amend`, `rebase` and `cherry` each 0 in that field.

## Authored-text proofs
`.agent/authored/f021-r21.md` at C0a and `.agent/last_block.md` at C0b are byte-identical to the received block at the G2 digest. PLANF021R21 → `.agent/plan.md` by `cmp` exit 0 with the bare-slice control at exit 1 (G4). RECORD21 → `.agent/live_review.md` under two independent readers with a rejected mutant (G5). Both slices were extracted MECHANICALLY from the committed C0a blob by their `<<<SLICE `/`<<<END ` marker lines; neither was hand-copied.

## Deviations & assumptions
No departure from the ordered commit sequence: C0a, C0b, C1, C2, C3 exactly — no extra commit, none dropped, no reordering. No slice was altered; no path outside `Change:` was written; nothing under `apps/` or `tests/` was touched. Environment note, not a block deviation: this session's bash guard refuses `git diff --name-only <A> <B>` in the two-positional-ref form, so G9's path-set reading used the equivalent `<A>..<B>` range form; every other gate command ran as written.
DECISION D15 — this handback is 71 lines against the 60-line cap. Cause, mandated content only: five per-commit changed-files tables, the item-status table, and one line for each of nine gates whose readings ARE the evidence. No section was dropped and no transcript was inlined.

## Next
THIS SESSION IS OVER. The NEXT session begins at docs/agents/self_drive_protocol.md Phase 1 rule 1 — the `.agent/STOP` check — BEFORE rule 2's Open PR Gate (R-0347). Rule 2 will find NO open pull request, so rule 5 applies and F021 continues on this branch. R21's own verdict is UNRECORDED and the next round's C2 owes it. The next round is R22, THE WIRING ROUND: `recency.ts` becomes the ONE liveness source for the NowCard's badge AND its new dot, and `feedScroll.ts` drives the feed's scroll container and the new-rows pill that component_spec.md line 86 binds. R22 is the largest component change of this feature and the first round to need CSS; `docs/ui/design_reference/assets_spec.md` is the asset authority for any new dot or pill styling.
Open findings: 218 open, maximum R-0655, next free R-0656 — one registered this round (R-0655), none resolved.
