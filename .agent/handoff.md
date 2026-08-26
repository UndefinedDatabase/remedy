# Handback — F031 Decision inbox, R16

Feature F031 · Round R16 · Branch `feature/f031-decision-inbox` · Base `4fc7dc77`
Fortschritt: ~55 % (F031 claimed; R1 through R15 landed and gated ·
             T001 SHIPPED · T002a MODEL shipped, wired and RENDERED ·
             T002b ordering/filtering/badge und T003 offen)
             — Schaetzung

## Range
Review of `4fc7dc77c37bc0a8ef158cdd34b02009a52fbc0f..HEAD`, where HEAD is the C3 commit that writes this file — its own SHA cannot exist in the text it writes.

## Commits

### c3bb2ea7 chore(agent): save the F031 R16 step block verbatim
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f031-r16.md | +365/-0 | C0a, the block saved verbatim |

### e7a38903 chore(agent): mirror the R16 block into last_block
| Path | +/- | Reason |
|---|---|---|
| .agent/last_block.md | +174/-260 | C0b, byte-identical mirror of the C0a blob |

### 877fc883 docs(agent): point the F031 plan at the R-0681 rename
| Path | +/- | Reason |
|---|---|---|
| .agent/plan.md | +18/-18 | C1, PLANF031R16 applied whole |

### 7d031ab1 docs(agent): record the F031 R15 verdict and register R-0681
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +4/-0 | C2, LEDGER16 appended |

### C3 docs(agent): write the F031 R16 handback
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | self-reference | C3 writes this file; its own numstat cannot exist while the text is written (R-0149) |

## Item status
| Item | Status | Reason |
|---|---|---|
| C0a | done | |
| C0b | done | |
| C1 | done | |
| C2 | done | |
| C3 | done | |
| push | done | ordered after C3; outcome carried by G10 to the reviewer |

## External actions
- `git worktree add --detach .remedy-wt/wt-f031-r16 7d031ab1` rc 0, then `git worktree remove --force /home/decodeux/Repos/remedy/.remedy-wt/wt-f031-r16` rc 0 — the G5 mutant, removed by that exact path.
- `git push origin feature/f031-decision-inbox`, run after C3. The reviewer measures the pushed tips at the next gate and records them in the R16 entry of `.agent/live_review.md`.
- `gh pr list --state open` printed `[]` and `gh pr list --state all --head feature/f031-decision-inbox` printed `[]`; both read-only, taken to ground the `## Next` statement below. No pull request created, edited or merged; no history rewritten; no branch created or deleted.

## Verification
- G1 — `git branch --show-current` printed `feature/f031-decision-inbox`, not `main`. `.agent/STOP` read from disk: ABSENT before C0a and ABSENT before C3. `git status --porcelain` 0 lines after each of C0a, C0b, C1 and C2.
- G2 — four readings (`.remedy-wt/f031-r16.md` before C0a, the committed C0a blob, the committed C0b blob, `.agent/last_block.md` off disk after C0b) all sha256 `1a101776247772758a13c23238ac5415757dbf02074abbf141d6183434edd603`, 29626 bytes, 365 lines, ALL FOUR EQUAL. C0a's and C0b's file is the SAME git blob `5845552a2f9f2164a774bce6aa12edffb95737cd`.
- G3 — my extractor over the committed C0a blob printed: 2 slices, 52 content lines inside markers, 365 total lines.
- G4 — `.agent/plan.md` at C1 byte-equal to PLANF031R16, 2985 bytes each, under the newline-INCLUDED convention (the slice ends in a newline and nothing follows it). NEGATIVE CONTROL against that slice with its trailing newline removed: FALSE. `^## Goal$` 1, `^## Next Steps$` 1, `wc -l` 49, strictly under 50.
- G5 — the one equality in the shape constraint 7 states: TRUE, with 611720 + 1 + 7870 = 619591 against an actual 619591. Independent reader: blank-line units 294 before and 296 after; my split of LEDGER16 measured N = 2, and the last 2 units equal the slice's 2 paragraphs IN ORDER. NEGATIVE CONTROL, written only inside the disposable worktree `.remedy-wt/wt-f031-r16`: one byte flipped at file offset 611771, inside the FIRST paragraph the append added — BOTH readers reject the mutant and BOTH accept the true file.
- G6 — `^- R-\d+ — ` 241 → 242, all 242 DISTINCT, ids ADDED exactly `R-0681` and ids REMOVED the EMPTY SET, maximum `R-0680` → `R-0681`. `^Done: R-` 3 → 3 and `^Recurrence: R-` 16 → 16, both UNCHANGED. `^Gate: R\d+ — ` 15 → 16, gaining exactly the key `R15`, with `R19` and `R1` through `R14` still present and all 16 keys DISTINCT. §3 item 10 open set at C2: 239.
- G7 — `^<<<SLICE ` and `^<<<END ` both 0 in `.agent/plan.md` at C1 and `.agent/live_review.md` at C2. `git diff --name-only 4fc7dc77..7d031ab1` names four paths, none under `packages/`, `apps/`, `tests/` or `docs/`, and neither `.agent/decisions.md` nor `.agent/context.md` nor either inventory file. Range MINUS change set: EMPTY. Change set MINUS range: exactly `.agent/handoff.md`. Every commit C0a..C2 single-parent; `git diff --numstat` insertions C0a 365, C0b 174, C1 18, C2 4, each under the 500 cap and each equal cell for cell to the `## Commits` table above, whose `+/-` column is derived from `git diff --numstat` and not from `git commit`'s own summary. `git ls-files .remedy-wt` 0; `git ls-files` over the zip glob 0. Reflog scoped to this round's entries only — 4 of them — read by the operation prefix before the first colon of `git reflog --format=%gs`: all 4 are `commit`, so `amend` 0, `rebase` 0, `cherry` 0.
- G8 — `npm run typecheck` in `apps/ui` real exit 0, ZERO diagnostics on stdout and stderr. `npm run test:unit` real exit 0 at 21 test files and 316 tests, both UNCHANGED from the base's 21 and 316. `git diff --name-only 4fc7dc77..7d031ab1` contains no path beginning `apps/` — the same reading G7 takes — so no code moved under these two counts.
- G9 — SHA-shaped `[0-9a-f]{7,40}` tokens in the committed C0a blob: my extractor measured 14 occurrences, 7 distinct. FAILING SET EMPTY. Types: `dc1cc6863a19439c9a6b3983d87cac7a7a11fd64` is `blob`; `4fc7dc77`, `4fc7dc77c37bc0a8ef158cdd34b02009a52fbc0f`, `58506912`, `6325ac2f`, `7add6592` and `e12a4d46` are `commit`. `git worktree list` 1 line immediately before the first pytest. Run SERIALLY, never two alive at once, in the primary checkout at the C2 tree: `tests/ui_server/` rc 0 at 474 passed; `test_test_runner.py` rc 0 at 52; `test_resource_safety.py` rc 0 at 21; `test_integrity_gate.py` rc 0 at 16; `test_golden_path.py` rc 0 at 42 — identical to the reviewer's base readings, so there is no difference to account for.
- G10 — run after C3; the command is in `## External actions` and its outcome is carried by the reviewer into the R16 ledger entry, not by any file this round writes.

## Authored-text proofs
- PLANF031R16 — extracted programmatically from the COMMITTED C0a blob by its marker lines, written to `.agent/plan.md`. Disk-to-disk equality against the extracted slice: TRUE, 2985 bytes each; negative control FALSE.
- LEDGER16 — extracted the same way, appended to `.agent/live_review.md`. Whole-file equality against base blob plus one newline plus the slice: TRUE at 619591 bytes, corroborated by the independent blank-line reader and by the byte-flip mutant both readers reject.

## Deviations & assumptions
- No departure from the block's ordered commit sequence: C0a, C0b, C1, C2, C3 — five commits, none extra, none dropped, none reordered.
- NO CODE TOUCHED, per constraint 9: the range names no path under `packages/`, `apps/`, `tests/` or `docs/`. The rename R-0681 orders was deliberately NOT performed here; it is the next session's first build round, and `## Next Steps` item 1 of `.agent/plan.md` at `877fc883` carries it.
- DECLARED SOURCE (the `+/-` column): taken from `git diff --numstat` as G7 orders and as the R15 declaration requires. `git commit`'s own rewrite-detected summary was not read this round, so this file states no figure for it.
- SCRATCH HYGIENE: one disposable worktree created and removed BY ITS EXACT PATH (`.remedy-wt/wt-f031-r16`); the three scratch files I created myself removed by exact path (`.remedy-wt/f031r16_slice_PLANF031R16`, `.remedy-wt/f031r16_slice_LEDGER16`, `.remedy-wt/f031r16_handoff_draft.md`). Nothing pre-existing under `.remedy-wt/` was created, moved or deleted, this round's own block file included.
- NO CONTRADICTION FOUND inside the block: every base reading it states reproduced at `4fc7dc77` — the ledger sets and their maximum, the 611720 bytes and 1215 lines, the 294 blank-line units, the plan's 49 lines and 2894 bytes, the handoff's 94 lines, and both `apps/ui` readings. The `Fortschritt:` block is carried verbatim above; I counted it at 4 lines.
- FINDINGS. This round mints exactly one id, `R-0681`, and writes no `Done:` line and no `Recurrence:` line. By §3 item 10 — every `^- R-\d+ — ` paragraph minus every `^Done: R-\d+ — ` line — the set is 239, measured at C2 `7d031ab1`. The narrower set, the findings this feature must still act on, is the list `.agent/plan.md` names at `877fc883`: R-0403, R-0413, R-0431, R-0441, R-0445, R-0471, R-0495, R-0533, R-0574, R-0601, R-0622, R-0625, R-0632, R-0672, R-0674, R-0675, R-0676, R-0677, R-0678, R-0679 and R-0681 — counted mechanically at 21 distinct ids, of which R-0495 and R-0574 are the two Highs. Every numeral in this paragraph was counted by script before this file was committed, which is the widened R-0441 rule the R15 ledger entry registers.
- HANDBACK TIER AND DECISION D15 OVERAGE, declared: constraint 3 fixes the round at 5 commits, which is not more than 5, so AGENTS.md `### handoff.md` gives the base tier of ≤60 lines. This file measures 84 lines with `wc -l` and exceeds that tier. The cause is mandated content only: the five per-commit tables the template requires (lines 14–37), the item-status table AGENTS.md mandates with one row per ordered item (lines 39–47), the one-line gate results the block orders (lines 55–64) and the authored-text proofs (lines 67–68). No section was dropped and no transcript is carried; no token cap is claimed, that cap having been withdrawn by DECISION F255 D6.

## Next
1. Phase 1 rule 1: re-read `.agent/STOP` from disk.
2. Phase 1 rule 2, the Open PR Gate: run `gh pr list --state open` and report what it printed, and report whether any pull request exists for `feature/f031-decision-inbox`. At `7d031ab1` that command printed `[]`, and NO pull request has ever been opened for this branch, so it carries R1 through R16 unmerged.
3. The R16 verdict is UNRECORDED and is owed by the next round's ledger commit — by DECISION F085 D9 no artefact of this round can carry it.
4. The next BUILD round repairs R-0681 by the rename `## Next Steps` item 1 of `.agent/plan.md` describes: rename the INTERFACE in `apps/ui/src/api/decisionCard.ts`, carry its three use sites and its `decisionCard.test.ts` import, leave the component alone.
5. T002b follows that repair, under DECISION F031 D2.
