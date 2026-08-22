# Handback — F021 R18 (the now-card badge goes back on the agent's own flag)

Feature F021, round R18. Branch `feature/f021-live-activity-feed`.
Round base `9dff7937b6b2d0a843713e89f0310fe08e7d0fdf`, the R17 handback commit.
Open findings after C2: 216, maximum R-0653, next free R-0654.

Fortschritt: ~84 % (T002 — Feed, NowCard und die reine Scroll-Regel stehen, das
             Badge sagt wieder die Wahrheit; es fehlen Recency-Dot, die
             Verdrahtung der Scroll-Regel und T003) — Schaetzung

## Range

Review of 9dff7937..HEAD, where HEAD is C4, the commit that writes this file.

## Item status

| Item | Status | Reason |
|------|--------|--------|
| C0a | done | block saved as authored text |
| C0b | done | mirrored from the committed C0a blob |
| C1 | done | plan rewritten to PLANF021R18 |
| C2 | done | R17 verdict recorded, R-0653 registered |
| C3 | done | badge repair plus its source contract |
| C4 | done | this commit |

## Commits

### 824387a8 docs(state): save the F021 R18 step block as authored text
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f021-r18.md | +357/-0 | the block, byte for byte, NEW |

### a451ac73 docs(state): mirror the F021 R18 block into last_block
| Path | +/- | Reason |
|---|---|---|
| .agent/last_block.md | +238/-346 | written FROM the committed C0a blob |

### 2d4cc31b docs(state): point the F021 plan at R18 and the badge repair
| Path | +/- | Reason |
|---|---|---|
| .agent/plan.md | +21/-21 | PLANF021R18 plus one terminating newline |

### 9b4b37e8 docs(review): record the R17 verdict as PASS and register R-0653
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +6/-0 | RECORD18 appended |

### 674d1420 fix(ui): key the now-card live badge to the agent, not the ring
| Path | +/- | Reason |
|---|---|---|
| apps/ui/src/components/panels/AgentNowCard.tsx | +7/-3 | ANCFILE2 whole-file write |
| tests/ui_contracts/test_brain_stream_ring.py | +25/-0 | CONTRACTBADGE append |

### C4, this commit, which cannot name its own SHA — docs(state): hand back F021 R18
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | rewrite | this handback |

## External actions

- `git worktree add --detach .remedy-wt/redproof-r18 674d1420` — created for G12; `git worktree remove --force .remedy-wt/redproof-r18` then `git worktree prune` — pruned, list is the primary checkout alone.
- `gh pr list --state open --json number,headRefName` — `[]`. Neither `gh pr create` nor `gh pr merge` was run; F021 is mid-feature.
- `git push -u origin feature/f021-live-activity-feed` after C4 — result in the round report.

## Verification — one line per gate, transcripts kept in the round report (R-0582)

- G1 PASS — `.agent/STOP` ABSENT immediately before C0a and again before C4; branch `feature/f021-live-activity-feed`; `git status --porcelain` 0 lines after each of C0a, C0b, C1, C2 and C3. Owed reading from R17: `9dff7937` is single-parent (parent `cd1d56e2`) and touches `.agent/handoff.md` alone at 63 insertions, under the 500-insertion cap.
- G2 PASS — the received bytes, `.remedy-wt/f021-r18.md`, `.agent/authored/f021-r18.md` at C0a and `.agent/last_block.md` at C0b are ALL FOUR sha256 `907d24aff162f3aa88e53145319d222a582e4f1e6db60d47252901fee225a85f` over 30318 bytes and 357 lines; C0b was written FROM the committed C0a blob.
- G3 PASS — the marker-LINE extractor over the committed C0a blob printed 4 slices and 114 CONTENT lines; re-measured from that same blob, TOTAL 357 against D6's 490 and PROSE 243 against D5's 400, both equal to constraint 8.
- G4 PASS — `cmp .agent/plan.md` against PLANF021R18 plus one newline exit 0; NEGATIVE CONTROL against the bare slice exit 1; last byte is a newline; `^## Goal$` 1, `^## Next Steps$` 1, `wc -l` 48, at most 50.
- G5 PASS — reader (a): the base blob (508786 B, 1118 L, sha256 `f9c5e93d…ba34`) is a byte-exact PREFIX and the remainder is EXACTLY one newline plus RECORD18 plus one newline at 7898 B, 6 L, sha256 `a22bd1349739924a8e42817ae890cfdb4f24b5e950bef23aedcb90eec71c5c83`; the file goes 508786→516684 B and 1118→1124 L. Reader (b), SET-WISE and ELEMENTWISE over the whole list: 240 units → 243, RECORD18 exactly 3. NEGATIVE CONTROL at offset 2 of the FIRST paragraph, printable byte `L`→`X` at equal length: BOTH readers REJECTED the mutant and ACCEPTED the true file.
- G6 PASS — round base then C2, line-anchored: `- R-` 215 → 216, all DISTINCT at both points; maximum R-0652 → R-0653; `Done: R-` 0 → 0; `Landed: ` 0 → 0; `Gate: R` keys 17 → 18, both DISTINCT; `Gate: R18` 0 → 1.
- G7 PASS — no pair was owed. The contract at the round base (11962 B, 269 L) is a byte-exact PREFIX of the file at C3, which reads 13034 B and 294 L; the remainder is EXACTLY one newline plus CONTRACTBADGE plus one newline at 1072 B, 25 L, sha256 `8ec6fe0866ae7fc87263f43289894e80dfa4f81e7b8dcedf389bd0e5f2ae23c8`, equal to the digest the block predicted. No per-line count was used.
- G8 PASS — blank lines immediately before CONTRACTBADGE's `class ` line in the C3 file: 2, COUNTED and not delegated to ruff.
- G9 PASS — `apps/ui/src/components/panels/AgentNowCard.tsx` at C3 is 1859 B, 37 L, sha256 `f1e4e3fd72aa18402660e1f96933deca007d78543509b65ac9e71943247febee`, equal to the block's prediction; `cmp` against ANCFILE2 plus one newline exit 0, NEGATIVE CONTROL against the bare slice exit 1. At the round base the same path is 1517 B and 33 L and `git ls-tree 9dff7937` DOES list it, so this REPLACES a tracked file. Over the C3 file `isActive` occurs 0 times and `newestActionRow` occurs 2.
- G10 PASS — `npx tsc --noEmit` in `/home/decodeux/Repos/remedy/apps/ui`, the PRIMARY checkout: exit 0, output EMPTY.
- G11 PASS — `npm run test:unit` in `/home/decodeux/Repos/remedy/apps/ui`, the PRIMARY checkout: exit 0, 14 test files and 196 tests, UNCHANGED from the round base as the block ordered.
- G12 PASS — disposable worktree `.remedy-wt/redproof-r18` at C3, a name no directory already used: GREEN FIRST at 31 passed. The target badge line occurs EXACTLY ONCE, whole-line 1 and indent-agnostic 1, the two counts agreeing. With the latching form `{(isRunning || liveAction !== null) && …}` in its place: exactly 1 failed, 30 passed, the failure `TestTheNowCardBadgeTracksTheAgent::test_the_badge_reads_the_running_flag`, assertion text "the live badge must track the agent, not the presence of a row". Tree pruned.
- G13 PASS — SERIALLY, never two at once, from `/home/decodeux/Repos/remedy`, the REPOSITORY ROOT, exit 0 each, counted by PASSED PLUS SKIPPED: `tests/ui_contracts/` 457 passed + 4 skipped = 461, the ordered rise of exactly 3 over the base's 458; `tests/ui_server/` with `tests/orchestration/test_test_runner.py` and `tests/regression/test_resource_safety.py` 511 passed + 0 skipped = 511; the canary `tests/cli/test_golden_path.py` 42 passed + 0 skipped = 42.
- G14 PASS — base-to-C3 path set equals the six non-handoff `Change:` paths, the difference EMPTY BOTH WAYS; all five commits single-parent; `git show --numstat` and `git diff --numstat` agree cell by cell with the `## Commits` tables above; insertions 357, 238, 21, 6 and 32, every one under the 500 cap; `git ls-files .remedy-wt` 0 lines; `git worktree list` ends with the primary checkout alone; `gh pr list --state open` EMPTY. LINE-ANCHORED marker sweep, first characters `<<<SLICE ` or `<<<END `: 0 in every one of the four files a slice landed in, while `.agent/live_review.md` reads 2 under the containment reading, which is exactly why the anchored form is the gate. Reflog read BY OPERATION FIELD — the text before the first `:` — over this round's 5 rows: every operation is `commit`, and `amend`, `rebase` and `cherry` each occur 0 times in that field.

## Authored-text proofs

`.agent/authored/f021-r18.md` at C0a is byte-identical to the received block and to the reviewer's emitted `.remedy-wt/f021-r18.md` at sha256 `907d24af…a85f` (G2). All four slices were extracted MECHANICALLY from the committed C0a blob by their marker LINES and applied byte for byte, never retyped: the disk-to-disk `cmp` results are under G4 (plan) and G9 (component), and the two append proofs are under G5 (ledger) and G7 (contract).

## Deviations & assumptions

None. The block's ordered commit sequence C0a, C0b, C1, C2, C3, C4 was followed exactly — no extra commit, none dropped, no reordering — and only paths on the `Change:` list were touched.
DECISION D15 overage: this file is 93 lines against the 60-line cap. The cause is mandated content: six per-commit changed-files tables plus one line for each of fourteen gates. AGENTS.md permits up to 100 lines when per-commit tables of more than five commits require it, which this round's six commits do. No section was dropped to meet the cap.

## Next

THIS SESSION ENDS with C4. The next session's FIRST action is docs/agents/self_drive_protocol.md Phase 1 rule 1 — the `.agent/STOP` check — BEFORE rule 2's Open PR Gate (R-0347). Rule 2 will find NO open pull request, so rule 5 applies and F021 continues on this branch. R18's own verdict is UNRECORDED and the next round's C2 owes it. R19 is the recency dot's PURE time rule — a function of the last action's arrival and a passed-in now — and its wiring, giving the badge and the dot one honest liveness source per T5_F021 line 63.
