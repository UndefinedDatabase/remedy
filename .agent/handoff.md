# Handoff — F021 Live activity feed · R13 · publish the bounded ring on the view

Round base a556f0c8bffec5b380d6b22b4af09575c24ed3ff · branch feature/f021-live-activity-feed · open findings 213, max R-0650, next free R-0651; this round mints and resolves none.

Fortschritt: ~55 % (T001 fertig · T002 fast fertig — Ring gebaut und jetzt auf
             der View veroeffentlicht, Identitaet by reference; es fehlen nur
             noch die Komponenten Feed und NowCard)
             — Schaetzung

## Range
Review of a556f0c8bffec5b380d6b22b4af09575c24ed3ff..HEAD.

## Commits
### 80e0a880 docs(state): save the F021 R13 publish-the-ring block as authored text
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f021-r13.md | 415/0 | C0a — the received block saved byte for byte |

### 0ad7eca0 docs(state): mirror the F021 R13 block into last_block
| Path | +/- | Reason |
|---|---|---|
| .agent/last_block.md | 267/342 | C0b — written FROM the committed C0a blob |

### 8c3a082a docs(state): point the F021 plan at R13 publishing the ring on the view
| Path | +/- | Reason |
|---|---|---|
| .agent/plan.md | 13/15 | C1 — PLANF021R13 plus one terminating newline |

### 665cded1 docs(review): record the R12 verdict in the F021 ledger
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | 2/0 | C2 — RECORD12 appended; no id minted, none resolved |

### 9cda5c86 feat(ui): publish the bounded ring on BrainStreamView by reference
| Path | +/- | Reason |
|---|---|---|
| apps/ui/src/api/brainStreamRunner.test.ts | 39/0 | C3 — TESTIMPORT2 pair, then TESTVIEW's 4 cases |
| apps/ui/src/api/brainStreamRunner.ts | 18/1 | C3 — RUNNER1-4: recent/recentDropped on the view, compared by reference, cachedView seeded from state |
| tests/ui_contracts/test_brain_stream_ring.py | 35/0 | C3 — CONTRACTVIEW's 4 source contracts |

### C4 docs(state): hand back F021 R13 — SHA UNNAMEABLE HERE because this is the commit that writes this file, the R-0149 self-reference exception
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | this file | C4 — the handback |

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
- `git worktree add .remedy-wt/g12-r13 9cda5c86` — created for G12 only; `git worktree remove --force` + `git worktree prune`; list is the primary checkout alone.
- `gh pr list --state open --json number,headRefName` — exit 0, `[]`. Neither `gh pr create` nor `gh pr merge` was run; F021 is mid-feature.
- `git push -u origin feature/f021-live-activity-feed` — after C4, per constraint 7.

## Verification
One line per gate; the transcripts stay in the round report (R-0582). All fourteen executed with real exit codes.
- G1 PASS — `.agent/STOP` absent before C0a and again before C4; branch `feature/f021-live-activity-feed`; `git status --porcelain` 0 lines after each of C0a, C0b, C1, C2, C3. Owed reading: a556f0c8 is single-parent, touches `.agent/handoff.md` alone, 73 insertions / 61 deletions, under the 500 cap.
- G2 PASS — sha256 `8cb5ccdcf3799f7b1b6c607957576a682a8b99721571f16e4b340510cf28bdc8`, 26571 bytes, 415 lines, EQUAL over the received bytes, `.remedy-wt/f021-r13.md`, C0a and C0b; C0b written from the committed C0a blob.
- G3 PASS — extractor over the committed C0a blob by marker LINES: 14 slices, 173 CONTENT lines. TOTAL 415 vs D6's 490; PROSE 415−173 = 242 vs D5's 400. Both equal constraint 8.
- G4 PASS — `cmp .agent/plan.md` against PLANF021R13+NL exit 0; negative control against the bare slice exit 1 (EOF after byte 2504). Last byte is a newline; `^## Goal$` 1; `^## Next Steps$` 1; `wc -l` 43 ≤ 50.
- G5 PASS — reader (a): base blob (477035 B, 1100 L, sha ac60d18b…) is a byte-exact PREFIX of C2 (481235 B, 1102 L); remainder 4200 B, 2 L, sha `f686d6a412e64e3552eee7c7baffb5f9cfcf9f57e1d1366c9063ecc8a0bfec2c` == NL+RECORD12+NL. Reader (b) set-wise: units 231 → 232, RECORD12 = 1 unit, ELEMENTWISE equal over the whole list. Negative control at offset 0 of the FIRST paragraph, `#`→`X` at equal length: both readers REJECT it and ACCEPT the true file.
- G6 PASS — base then C2: `- R-` 213 → 213, DISTINCT 213 → 213; maximum R-0650 → R-0650; `Done: R-` 0 → 0; `Landed: ` 0 → 0; `Gate: R` keys 12 → 13, both DISTINCT; `Gate: R13` 0 → 1. Every value as ordered.
- G7 PASS — whole-string over raw bytes. At the ROUND BASE every FROM is 1 (RUNNER1, RUNNER2, RUNNER3, RUNNER4, TESTIMPORT2). At C3, by shape: RUNNER1 APPEND-SHAPED FROM 1 TO 1; RUNNER2 FROM 0 TO 1; RUNNER3 FROM 0 TO 1; RUNNER4 FROM 0 TO 1; TESTIMPORT2 APPEND-SHAPED FROM 1 TO 1. Fifteen numbers, all as predicted.
- G8 PASS — prefix plus remainder, never a per-line count. `brainStreamRunner.test.ts`: the TESTIMPORT2-SUBSTITUTED base blob is the prefix, remainder 1332 B, 38 L, sha `49d4525a4b8c49e266f327cbca0ab0e24d7c4a0610dd35eaadcbc39ba52cfff5`. `test_brain_stream_ring.py`: the base blob is the prefix, remainder 1721 B, 35 L, sha `c8b8e03972de893a71731c206ef4170a0bbeb3f26779889e5799a1217f58a5f7`. Each == NL+slice+NL.
- G9 PASS — blank lines immediately before CONTRACTVIEW's `class ` line in the C3 file: 2. Counted, not delegated to ruff (R-0558). CONTRACTVIEW's leading blank was not trimmed.
- G10 PASS — `npx tsc --noEmit`, cwd `/home/decodeux/Repos/remedy/apps/ui`, exit 0, stdout and stderr both EMPTY.
- G11 PASS — `npx vitest run`, cwd `/home/decodeux/Repos/remedy/apps/ui`, PRIMARY checkout, exit 0: 12 files, 177 tests. Rise over the round base's 173 is exactly 4 — TESTVIEW's 4 cases.
- G12 PASS — worktree `.remedy-wt/g12-r13` at 9cda5c86, GREEN FIRST: exit 0, 13 passed. `    recent: state.recent,` occurs TWICE in `brainStreamRunner.ts`; I changed the FIRST, the one inside the `let cachedView` initializer, leaving `publish()`'s untouched. Re-run: exit 1, EXACTLY 1 failed / 12 passed, the failure `TestViewPublishesTheRing::test_cached_view_is_seeded_from_the_state`, assertion "a fresh [] here is a different array from the initial state's ring, so the first timer would announce a change nobody made". Worktree removed and pruned.
- G13 PASS — PRIMARY checkout, SERIALLY, cwd `/home/decodeux/Repos/remedy` (the repository root) for all three. `tests/ui_contracts/` exit 0, 439 passed + 4 skipped = 443. `tests/ui_server/ tests/orchestration/test_test_runner.py tests/regression/test_resource_safety.py` exit 0, 511. `tests/cli/test_golden_path.py` exit 0, 42 (canary). No docs gate owed.
- G14 PASS — base..C3: path set is the seven non-handoff `Change:` paths, BOTH differences EMPTY; all 5 commits single-parent; `git show --numstat` and `git diff --numstat` agree cell by cell with `## Commits` above; insertions 415, 267, 13, 2, 92 — every one under 500; `<<<SLICE `/`<<<END ` 0 LINES in all five files a slice landed in; `git ls-files .remedy-wt` 0; `git worktree list` the primary checkout alone; reflog for this round 6 rows, every ACTION `commit`, amend/rebase/cherry each 0; `gh pr list --state open` EMPTY.

## Authored-text proofs
- `.agent/authored/f021-r13.md` at C0a, `.agent/last_block.md` at C0b, the received bytes and the reviewer's emitted `.remedy-wt/f021-r13.md` are all sha256 `8cb5ccdc…` over 26571 bytes / 415 lines (G2).
- Every applied slice was extracted MECHANICALLY from the committed C0a blob by its marker lines and never retyped: PLANF021R13 by `cmp` exit 0 with a red control at exit 1 (G4); RECORD12 by two independent readers with a negative control (G5); the five pairs by whole-string byte counts (G7); TESTVIEW and CONTRACTVIEW by prefix-plus-remainder digests (G8).

## Deviations & assumptions
- No departure from the ordered commit sequence: C0a, C0b, C1, C2, C3, C4 were committed in exactly that order, six commits, none added, none dropped, none reordered.
- Constraint 5 (pairs before appends) is satisfied PER TARGET FILE, which is the only reading commit order 2 permits: RECORD12 is one of the three appends and lands at C2, ahead of C3's pairs, but no pair touches `.agent/live_review.md`, and inside `brainStreamRunner.test.ts` the TESTIMPORT2 pair was applied before the TESTVIEW append. Recorded as an assumption, not a silent choice.
- G14's reflog clause is measured by reflog ACTION, not by substring over whole rows. A substring count reads amend 84 / rebase 26 / cherry 60 across all 5612 rows, because this repository holds commits whose SUBJECT carries `amend0730`, `amend0816` and `amend0820` and because rows predating the round base belong to other features. By ACTION and scoped to this round: 6 rows, all `commit`, all three tokens 0.
- `npm run lint` in `apps/ui` is RED at base (R-0622); it is not a gate here and was not run. No formatter or linter that rewrites files was run.
- `.remedy-wt/` holds this round's scratch and is gitignored — `git ls-files .remedy-wt` is 0. That directory's presence in a review zip stays R-0403, routed to a paydown branch.
- DECISION D15 declared overage: this file is 91 lines against the 60-line cap, within the ≤100 the template allows when per-commit tables of more than five commits require it. Cause is mandated content only — six per-commit changed-files tables, the item-status table, fourteen one-line gate readings carrying the numerals G1-G14 order, and the four-line `Fortschritt:` block. No section was dropped and no prose padding was added.

## Next
R14 builds the feed and NowCard components over the published ring, reading it from the ONE `useBrainStream` call `RemedyShell` already makes — no second call and no new `EventSource`. `recentDropped` above zero is what the dropped-rows notice renders. Before authoring R14, re-read `.agent/STOP` from disk (Phase 1 rule 1) ahead of the Open PR Gate.
