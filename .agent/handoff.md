# Handback — F021 R28, the NowCard activity dot

Round base `2b8830acbb74ec0b3ad56b7ccc4cf0840f94d9a4`, branch `feature/f021-live-activity-feed`.
Block `.agent/authored/f021-r28.md`, sha256 `3289c55b…3473e0`, 32905 B / 471 L.
Nothing registered and nothing resolved this round: R27 PASSED.

Fortschritt: ~95 % (T002 — Uhr, Ring und NowCard-Punkt verdrahtet; es fehlt nur
             noch der Feed-Scroll)
             — Schaetzung

| Item | Status | Reason |
|------|--------|--------|
| C0a  | done   | block saved verbatim to `.agent/authored/f021-r28.md` |
| C0b  | done   | mirrored FROM the committed C0a blob |
| C1   | done   | plan rewritten to PLANF021R28, 48 lines |
| C2   | done   | RECORD28 appended; only the `Gate:` series moved |
| C3   | done   | TOKENSLIVE and DOTCSS applied, both rewrites |
| C4   | done   | NOWCARDTSX whole-file write; badge untouched |
| C5   | done   | DOTCONTRACT appended, 6 cases, red-controlled |
| C6   | done   | this handback |

## Range
Review of `2b8830ac`..`HEAD`. G10, G11 and G12 ran at C5 `05beb725`, as G12 requires.

## Commits
### ae150fac docs(state): save the F021 R28 step block
| Path | +/- | Reason |
|------|-----|--------|
| .agent/authored/f021-r28.md | +471/-0 | the round's block, byte-identical |
### 190776e5 docs(state): mirror the R28 block into last_block
| Path | +/- | Reason |
|------|-----|--------|
| .agent/last_block.md | +400/-203 | written from the committed C0a blob |
### 3705462a docs(plan): point the F021 plan at R28, the activity dot
| Path | +/- | Reason |
|------|-----|--------|
| .agent/plan.md | +23/-23 | PLANF021R28 plus one terminating newline |
### 98dac323 docs(review): record the R27 verdict
| Path | +/- | Reason |
|------|-----|--------|
| .agent/live_review.md | +2/-0 | RECORD28, one unit, append-only |
### 9cf01f6d feat(ui): add the liveness tokens and the activity dot CSS
| Path | +/- | Reason |
|------|-----|--------|
| apps/ui/src/components/panels/RightLivePanel.module.css | +16/-0 | DOTCSS: 4 levels + keyframes |
| apps/ui/src/styles/tokens.css | +8/-0 | TOKENSLIVE, transcribed from the reference |
### 253aad56 feat(ui): drive the NowCard activity dot from the recency rule
| Path | +/- | Reason |
|------|-----|--------|
| apps/ui/src/components/panels/AgentNowCard.tsx | +30/-5 | NOWCARDTSX: own clock, `data-recency` |
### 05beb725 test(ui): pin the activity dot to the recency rule and its tokens
| Path | +/- | Reason |
|------|-----|--------|
| tests/ui_contracts/test_brain_stream_ring.py | +58/-0 | DOTCONTRACT, 6 cases |
### C6 — the handoff commit, which cannot name its own SHA (R-0494): docs(state): hand back F021 R28
| Path | +/- | Reason |
|------|-----|--------|
| .agent/handoff.md | owed by R29 | this file; C6 cannot state its own counts |

## External actions
- `git worktree add --detach .remedy-wt/r28-red 05beb725` exit 0, for G11 only; then `git worktree remove --force` + `git worktree prune` exit 0, leaving `git worktree list` as the primary checkout ALONE.
- `gh pr list --state open --json number,headRefName` → `[]`. Neither `gh pr create` nor `gh pr merge` was run; no PR created, edited or merged.
- `git push -u origin feature/f021-live-activity-feed` after C6.

## Verification
One line per gate; transcripts stay in the round report (R-0582).
- G1 PASS — `.agent/STOP` ABSENT before C0a and again before C6; branch `feature/f021-live-activity-feed`; `git status --porcelain` 0 lines after each of C0a, C0b, C1, C2, C3, C4 and C5.
- G2 PASS — sha256 `3289c55b7eb3bb1e3fd8cf9a41aac032f3da502d5db341541fffd5be783473e0`, 32905 B / 471 L, EQUAL across five copies: `.remedy-wt/f021-r28.md`, the bytes I read, C0a's committed blob, C0b's committed blob and both files on disk. C0b was written FROM the C0a blob.
- G3 PASS — my extractor read from the committed C0a blob 4 whole texts (PLANF021R28, RECORD28, NOWCARDTSX, DOTCONTRACT), 2 pairs (TOKENSLIVE, DOTCSS) and 203 CONTENT lines; 16 lines start `<<<`, all markers (4×2 + 2×4). TOTAL 471 ≤ 490 (D6); PROSE 471−203 = 268 ≤ 400 (D5).
- G4 PASS — `cmp .agent/plan.md` vs PLANF021R28+NL exit 0; vs the bare slice exit 1; `wc -l` exactly 48; last byte is `\n`; `^## Goal$` 1; `^## Next Steps$` 1.
- G5 PASS — (a) base blob a byte-exact PREFIX, remainder exactly NL+RECORD28+NL, sha256 `4225a477…c2af87`, 4715 B / 2 L, file 581080 B / 1180 L → 585795 B / 1182 L. (b) units 271 → 272, RECORD28 exactly 1 unit, equal ELEMENTWISE over the whole list. Negative control — offset 2 of the FIRST paragraph, `L`→`X`, equal length — REJECTED by (a) on its prefix clause and by (b) at unit index 0; both ACCEPT the true file. The diff deletes 0 lines.
- G6 PASS — base → C2: `- R-` 223 → 223, all DISTINCT at both; MAX R-0660 at both; `Done: R-` 1 → 1; `Landed: ` 0 → 0; `Gate: R` keys 26 → 27, DISTINCT at both; `Gate: R28` 0 → 1. Exactly one series moved.
- G7 PASS EXCEPT ONE PREDICTED NUMERAL, declared below — TOKENSLIVE and DOTCSS each: FROM 1 at base → 0 at C3, TO 0 → 1, in their own targets; `TO contains FROM` measured `false` for both. `--remedy-dur-pulse` 0 → 1, `--remedy-live` 0 → **2** where G7 predicts 1. Both values BYTE EQUAL to `docs/ui/design_reference/tokens.css` read at C3: `#34c27e`, `1600ms`.
- G8 PASS — `cmp` card vs NOWCARDTSX+NL exit 0, vs the bare slice exit 1. Comment-stripped card (via the suite's own `strip_ts_comments`): `newestActionRow` 2, `recent ?? []` 1, `liveAction ? liveAction.line : detail` 1, `{isRunning && <span` 1, `isActive` 0, `recencyLevel` 2, `isLiveByRecency` 0. Raw card: `Builder is working` 0, `@mui` 0, `Agent` 4. `RightLivePanel.tsx`: the `<AgentNowCard dashboard={dashboard} recent={recent} />` line exactly 1; that file is untouched and absent from the round's path set.
- G9 PASS — C4 blob a byte-exact PREFIX of the C5 file; remainder exactly two newlines + DOTCONTRACT + one newline, sha256 `a6ba8be5…1f5a31`, 2695 B / 58 L; file 428 → 486 lines; the diff deletes 0 lines and its 58 ADDED lines equal the remainder's 58 lines ELEMENTWISE, in order.
- G10 PASS — serially, never two at once. From `apps/ui`: `npx tsc --noEmit` exit 0, output EMPTY; `npm run test:unit` exit 0, 15 files / 212 tests, unchanged as a round adding no vitest case must be. From the repository root `/home/decodeux/Repos/remedy`: `tests/ui_contracts/` exit 0, 478 passed + 4 skipped = 482 = base 476 + DOTCONTRACT's 6 (counted by `--collect-only` on its class) — the two AGREE; the three state-reader suites exit 0, 511; the golden-path canary exit 0, 42.
- G11 PASS — disposable worktree only: `data-recency={level}` counted 1 whole-line-containing AND 1 indent-agnostic, both agreeing; deleting that attribute text made `pytest tests/ui_contracts/test_brain_stream_ring.py` exit 1 — FAILED `…::TestTheActivityDotReadsTheRecencyRule::test_the_level_reaches_the_dom_as_data`, 1 failed / 51 passed. Not vacuous. Worktree removed and pruned; `git worktree list` is the primary checkout ALONE.
- G12 PASS — base..C5: path set EQUALS the eight non-handoff `Change:` paths, difference EMPTY both ways; 7 commits, every one single-parent; `git show --numstat` and `git diff --numstat` agree cell by cell with the tables above; insertions 471, 400, 23, 2, 24, 30, 58 — each under the 500 cap; marker sweep line-anchored 0 for all six prefixes and for any `<<<` line, in each of the six files a slice or pair landed in; `git ls-files .remedy-wt` 0; `gh pr list --state open` `[]`; reflog BY OPERATION — all 7 of this round's rows `commit`, with `amend`, `rebase` and `cherry` 0 each.

## Authored-text proofs
Every applied byte was extracted MECHANICALLY from the committed C0a blob by marker line, never retyped. PLANF021R28 and NOWCARDTSX: `cmp` exit 0 against slice+NL, bare-slice control exit 1 (G4, G8). RECORD28 and DOTCONTRACT: remainder digests under G5 and G9. TOKENSLIVE and DOTCSS: FROM→0 / TO→1 in their own targets (G7).

## Deviations & assumptions
- No departure from the ordered commit sequence: C0a, C0b, C1, C2, C3, C4, C5, C6 ran in that order; none added, dropped, merged, split or reordered.
- BLOCK SELF-CONTRADICTION, NOT REPAIRED (constraint 1). G7 orders that `--remedy-live` occur "exactly 1 time" in `apps/ui/src/styles/tokens.css` at C3; it occurs 2 times, because the TOKENSLIVE TO half's OWN comment names the token in prose ("…8px, --remedy-live,") beside the declaration it adds. The DECLARATION reading (`^\s*--remedy-live:`) is exactly 1 — the reading DOTCONTRACT itself asserts via `"--remedy-live:" in tokens`. The slice was applied byte for byte and nothing was edited to reach the predicted numeral: the gate's prose disagrees with the block's own slice, not with the tree. Reviewer to rule.
- No assumption_log entry is owed: both tokens are TRANSCRIBED from the binding reference per constraint 9, and I verified both values against that file rather than against the block's prose.
- `npm run lint` was NOT run (constraint 10; RED tree-wide under R-0622).
- Deviations, declared — this handoff is 91 lines by `wc -l`: over the 60-line baseline and WITHIN the 100-line tier AGENTS.md grants when per-commit tables cover more than five commits, which this round's eight tables do (DECISION D15). The cause is mandated content alone — eight commit tables, twelve gate readings and the item-status table. No section was dropped and no transcript inlined.

## Next
THIS SESSION IS OVER. The NEXT session begins at `docs/agents/self_drive_protocol.md` Phase 1 rule 1 — the `.agent/STOP` check — BEFORE rule 2's Open PR Gate (R-0347). R28's own verdict is UNRECORDED: the next round's ledger commit owes it, together with C6's insertion count and this file's line count, which C6 cannot state about itself. R29 then rules the badge's liveness source with a DECISION in `.agent/decisions.md` — the question constraint 8 deliberately left open, and the reason the badge still reads `isRunning` here.
