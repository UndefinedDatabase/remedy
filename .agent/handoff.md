# Handback — F021 R29 (STEP T002/BADGE), the NowCard badge ruling

Fortschritt: ~96 % (T002 — Punkt und Badge verdrahtet und geregelt; es fehlt nur
             noch der Feed-Scroll)
             — Schaetzung

## Range
Review of `baf079b1`..`HEAD`. ROUND BASE `baf079b10228885f08ba8550e4268359c4705eaf`. Eight commits, C0a..C6.

## Item status
| Item | Status | Reason |
|---|---|---|
| C0a | done | `02fb2407` |
| C0b | done | `e64de319` |
| C1 | done | `8af9d825` |
| C2 | done | `a8270b96` |
| C3 | done | `d938b34c` — constraint 4 applied literally; see Deviations |
| C4 | done | `d876d8ce` |
| C5 | done | `4bdc5b10` |
| C6 | done | this commit; a handback cannot name its own SHA (R-0494) |

## Commits
### 02fb2407 docs(agents): save the F021 R29 step block as authored text
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f021-r29.md | +414/-0 | C0a saves the block verbatim |
### e64de319 docs(state): mirror the F021 R29 block into last_block
| Path | +/- | Reason |
|---|---|---|
| .agent/last_block.md | +249/-306 | C0b mirrors it FROM the committed C0a blob |
### 8af9d825 docs(state): point the F021 plan at R29, the badge ruling round
| Path | +/- | Reason |
|---|---|---|
| .agent/plan.md | +16/-17 | C1, PLANF021R29 whole-file write |
### a8270b96 docs(review): record the R28 verdict and the R-0618 recurrence
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +4/-0 | C2, RECORD29 appended; no id minted |
### d938b34c docs(decisions): rule the NowCard badge as running AND recent
| Path | +/- | Reason |
|---|---|---|
| .agent/decisions.md | +11/-0 | C3, DECISION9 appended; D9 is the last heading |
### d876d8ce feat(ui): light the NowCard badge on running AND recent
| Path | +/- | Reason |
|---|---|---|
| apps/ui/src/components/panels/AgentNowCard.tsx | +11/-6 | C4, BADGEIMPORT + BADGELEVEL + BADGEJSX |
### C5 4bdc5b10 test(ui-contracts): pin the badge to the conjunction D9 rules
| Path | +/- | Reason |
|---|---|---|
| tests/ui_contracts/test_brain_stream_ring.py | +19/-12 | C5, PINBADGE + PINDOTDOC; a rewrite, so deletions are expected |
### C6, the handback commit, whose SHA and counts cannot be known to itself (R-0494): docs(state): hand back F021 R29
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | owed to R30 | C6 rewrites this file; its insertion count and line count are owed to the next round's ledger commit |

## External actions
- `git worktree add --detach .remedy-wt/r29red 4bdc5b10` — added for G11; `git worktree remove --force` + `git worktree prune` afterwards; `git worktree list` is the primary checkout ALONE.
- `gh pr list --state open --json number,headRefName` → `[]`. Neither `gh pr create` nor `gh pr merge` was run. No PR exists or was touched.
- `git push -u origin feature/f021-live-activity-feed` after C6.

## Verification
- G1 PASS — `.agent/STOP` ABSENT before C0a and again before C6; branch `feature/f021-live-activity-feed`; `git status --porcelain` 0 lines after each of C0a, C0b, C1, C2, C3, C4, C5.
- G2 PASS — sha256 `723b3bd9dc70e692938d908f9464cb67b09a6eb4bc8b604a1c32fcd490fa1ada`, 36795 bytes, 414 lines, equal over the bytes read, `.remedy-wt/f021-r29.md`, `.agent/authored/f021-r29.md` at C0a and `.agent/last_block.md` at C0b, the last written FROM the committed C0a blob.
- G3 PASS — my extractor over the committed C0a blob printed 3 whole texts (PLANF021R29, RECORD29, DECISION9), 5 pairs, 137 CONTENT lines, 26 lines starting with the marker character, every one a marker; re-measured TOTAL 414 ≤ 490 and PROSE 414−137 = 277 ≤ 400.
- G4 PASS — `cmp .agent/plan.md <slice+NL>` exit 0; negative control `cmp` against the bare slice exit 1; last byte is a newline; `wc -l` EXACTLY 47; `^## Goal$` 1; `^## Next Steps$` 1.
- G5 C2 PASS / C3 SPLIT — C2: prefix true, remainder sha256 `acef2823…07833d` 8671 B / 4 L, file 585795 B/1182 L → 594466 B/1186 L, units 272 → 274 elementwise with RECORD29 at 2 units under BOTH splits. C3: reader (a) PASS, remainder sha256 `446030a6…fa14f3` 2830 B / 11 L, file 500137 B/7009 L → 502967 B/7020 L; reader (b) units 1235 → 1240, DECISION9 5 units, elementwise TRUE under a blank-line-RUN split and FALSE under a strict two-newline split at index 1235 (see Deviations). Negative control on the C3 file at offset 4, `c`→`X` (`# Decisions`→`# DeXisions`): REJECTED by reader (a) and by both reader-(b) variants, while the true file is accepted by reader (a) and by the run split. Neither diff deletes a line: 4/0 and 11/0.
- G6 RED on ONE clause, and it is the R-0618 defect again — line-anchored `- R-` reads 223 at the round base and 224 at C2, and "all DISTINCT at both" is false at C2, because RECORD29's own first line IS `- R-0618 RECURRED, …`; the duplicated id is R-0618 and nothing else. Every semantic clause holds: DISTINCT ids 223 at BOTH, maximum `R-0660` at BOTH, `Done: R-` 1 at BOTH, `Landed: ` 0 at BOTH, `Gate: R` keys 27 → 28 DISTINCT at both, `Gate: R29` 0 → 1, `- R-0661` 0 at C2. No id was minted and none resolved.
- G7 PASS — `^## DECISION F021 D9 ` 0 at the round base and 1 at C3; `^## DECISION F021 D` 5 → 6 (D1, D2, D3, D4, D5, D9); D9 is the LAST such heading in the file.
- G8 PASS — BADGEIMPORT, BADGELEVEL, BADGEJSX each FROM 1 at base / 0 at C4 and TO 0 at base / 1 at C4. Comment-stripped card at C4 via the suite's own `strip_ts_comments`: `newestActionRow` 2, `recent ?? []` 1, `liveAction ? liveAction.line : detail` 1, `recencyLevel(` 1, `data-recency={level}` 1, `setInterval` 1, `isRunning && isLiveByRecency(` 1, `isActive` 0. Raw card: `Builder is working` 0, `@mui` 0. `RightLivePanel.tsx` is ABSENT from this round's path set.
- G9 PASS — PINBADGE and PINDOTDOC each FROM 1 at base / 0 at C5 and TO 0 at base / 1 at C5; file 486 → 493 lines; C5's diff DELETES 12 lines, non-zero as a pin rewrite must be.
- G10 PASS, run SERIALLY in the PRIMARY checkout — from `apps/ui`: `npx tsc --noEmit` exit 0 with EMPTY output; `npm run test:unit` exit 0, 15 files and 212 tests, unchanged. From the repository root `/home/decodeux/Repos/remedy`: `tests/ui_contracts/` exit 0, 478 passed + 4 skipped = 482, UNCHANGED from the base's 482; the three state-reading suites exit 0, 511 passed; the golden-path canary exit 0, 42 passed.
- G11 PASS — in the disposable worktree at C5 the target `isRunning && isLiveByRecency(level)` counted 1 whole-line-containing AND 1 indent-agnostic (raw substring also 1), both agreeing; replaced with `isLiveByRecency(level)` — DECISION F021 D9's rejected option (a); `python3 -m pytest tests/ui_contracts/test_brain_stream_ring.py -q -rf` exit 1, 1 failed / 51 passed, the failure being `TestTheNowCardBadgeTracksTheAgent::test_the_badge_needs_running_and_recent_together`. Worktree removed and pruned; `git worktree list` is the primary checkout ALONE.
- G12 PASS — base-to-C5 path set EQUAL to the seven non-handoff `Change:` paths, both differences EMPTY; all seven commits single-parent; `git show --numstat` and `git diff --numstat` agree cell by cell with the tables above; insertions 414, 249, 16, 4, 11, 11, 19, each under the 500 cap; `git ls-files .remedy-wt` 0; `gh pr list --state open` EMPTY. Marker sweep, line-anchored over all six prefixes and over any line starting with the marker character, reads 0 in each of `.agent/plan.md`, `.agent/live_review.md`, `.agent/decisions.md`, `AgentNowCard.tsx` and `test_brain_stream_ring.py`; the two block mirrors read 26 each by construction. Reflog BY OPERATION: 7 rows this round, every operation `commit`, with `amend`, `rebase` and `cherry` each 0 in that field.

## Authored-text proofs
- PLANF021R29, RECORD29, DECISION9 and the five pairs were extracted MECHANICALLY by marker line from the COMMITTED `.agent/authored/f021-r29.md` blob at `02fb2407` and applied byte for byte; nothing was retyped, rewrapped or reindented.
- Whole-file write proved by `cmp` at exit 0 with a red negative control (G4); the two appends proved by remainder digest and by an independent unit reader (G5); the five pairs proved by FROM/TO occurrence counts before and after (G8, G9), each FROM re-checked for exactly 1 occurrence at the moment IT was applied, in the listed order.

## Deviations & assumptions
- COMMIT SEQUENCE: none. C0a, C0b, C1, C2, C3, C4, C5, C6 exactly as ordered — no extra commit, none dropped, none reordered, none merged or split.
- THE BLOCK CONTRADICTS ITSELF AT C3, and no application can satisfy both halves of G5. Constraint 4 says the prose-record append is "TWO newlines, then the slice, then one terminator", parallel to the ledger's "ONE newline", which R28 established means one ADDED newline. I applied constraint 4 literally: two added newlines. Reader (a) then passes exactly as written. But the boundary now carries TWO blank lines (`…changes.\n\n\n## DECISION F021 D9`), so reader (b)'s "split on the blank line" rejects under a strict two-newline split — the first appended unit reads `\n## DECISION…`. Constraint 4's own gloss ("the blank line that separates entries in that file", singular), the file's convention (114 of 115 entries use ONE blank line) and the immediately preceding append `9c7fdfc2` all point at ONE added newline, under which BOTH readers would pass and reader (a)'s literal text would not. I did NOT repair it: constraint 8 forbids editing landed text, an amend would rewrite history and a corrective commit would put a deletion into an append-only file. Reported, not papered over.
- G6's `- R-` clause is FALSIFIED BY THE BLOCK'S OWN SLICE, which is R-0618's FOURTH instance and lands inside the round that records the third — the exact thing constraint 9 was written to prevent. The gate orders 223 "at BOTH points, all DISTINCT"; RECORD29 opens with a line-anchored `- R-0618 …` bullet, so C2 necessarily reads 224 with a duplicate. The registered SET is unchanged and no id was minted, so nothing on disk is wrong; the arithmetic is. The reviewer's fix clause needs the same anchor discipline it just added for declared names: a `- R-` count must exclude, or be scoped to, the recurrence bullets the block's own record slice writes.
- ASSUMPTION: reader (b)'s "split each on the blank line into units" was implemented as splitting on a RUN of blank lines (paragraph units); the strict two-newline variant is reported alongside it everywhere, and both agree on C2 and on the negative control.
- `npm run lint` was NOT run (constraint 11, R-0622). No formatter or in-place rewriter was run. No PR was created or merged.

## Next
THIS SESSION IS OVER. The NEXT session begins at docs/agents/self_drive_protocol.md Phase 1 rule 1 — the `.agent/STOP` check — BEFORE rule 2's Open PR Gate (R-0347). R29's own verdict is UNRECORDED: the next round's ledger commit owes it, together with C6's own insertion count and `wc -l`, which C6 cannot state about itself. It also owes a ruling on the two gate defects above. R30 wires `feedScroll.ts` into the feed's scroll container with the new-rows pill component_spec.md line 86 binds — the last rule this feature has built headless and left unread.

Deviations, declared (DECISION D15): this handback measures 89 lines by `wc -l`. That is OVER the 60-line baseline and WITHIN the 100-line tier AGENTS.md grants a handback whose per-commit tables cover more than five commits, which these EIGHT do. Mandated cause: eight per-commit changed-files tables, the eight-row item-status table, twelve one-line gate results and the two block contradictions this round must record. No section was dropped and no transcript was inlined (R-0582).
