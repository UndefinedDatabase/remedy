# Handback — F009 R32 (ledger-clear)

Feature F009 · round R32 · branch `feature/f009-single-write-channel` · round base `5ad780198cc7bceaff3b4664a2d1500e45b24336`. This round records the R31 verdict, registers R-0646 and R-0647, and empties `.agent/candidates.md`. Next free id R-0648.

Fortschritt: ~99 % (T001 gebaut · T002 gebaut · T003 gebaut und verifiziert ·
             Integrations-Gate BESTANDEN; offen bleiben nur die zwei
             Closure-Runden: Evidenz und Zip, dann STATUS-Zeile und PR) —
             Schätzung

## Range

Review of `5ad78019`..HEAD.

## Commits

### fc470f84 docs(state): save the F009 R32 step block
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f009-r32.md | 250/0 | C0a — the R32 block saved byte-for-byte |

### 5c47adf5 docs(state): mirror the F009 R32 block into last_block
| Path | +/- | Reason |
|---|---|---|
| .agent/last_block.md | 160/152 | C0b — mirrored FROM the committed C0a blob |

### df1cc995 docs(state): point the F009 plan at the R32 ledger-clear round
| Path | +/- | Reason |
|---|---|---|
| .agent/plan.md | 6/8 | C1 — whole-file replacement by slice PLANF009R32 |

### 11ac72e1 docs(review): register the two carried reviewer-block defects
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | 4/0 | C2 — append of slice FINDINGS (R-0646, R-0647) |

### 7e5bf4b9 docs(review): record the R31 verdict as PASS
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | 2/0 | C3 — append of slice LEDGER32, based on C2 |

### 17303fb9 docs(state): empty the closure-candidate carrier
| Path | +/- | Reason |
|---|---|---|
| .agent/candidates.md | 5/40 | C4 — whole-file replacement by slice CANDIDATES32 |

### C5 docs(state): write the F009 R32 handback (this commit, self-reference)
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | — | C5 — this file; a handback cannot table its own SHA or cells (R-0149, R-0371); its numbers go to the round report per item 14 |

## Item status

| Item | Status | Reason |
|---|---|---|
| C0a | done | |
| C0b | done | |
| C1 | done | |
| C2 | done | |
| C3 | done | |
| C4 | done | |
| C5 | done | |

## External actions

`git push -u origin feature/f009-single-write-channel` after C5 — result in the round report. No PR created, none edited, no merge, no worktree added or removed, no other `gh` command run.

## Verification

G1 — `.agent/STOP` ABSENT before C0a and again before C5; `git rev-parse --abbrev-ref HEAD` prints `feature/f009-single-write-channel`; `git status --porcelain` printed 0 lines after each of C0a, C0b, C1, C2, C3 and C4; round base read at step 0 is `5ad780198cc7bceaff3b4664a2d1500e45b24336`.
G2 — TRANSPORT: `.agent/authored/f009-r32.md` at C0a, `.agent/last_block.md` at C0b and the block as received are all sha256 `3e56e730ad693a0a5dcffce43e006bb4d9bcc0159cabd5c3f78944b0670f3319` over 23131 bytes and 250 lines; C0b was written from the committed C0a blob, not from the scratch copy.
G3 — SLICES extracted from the committed C0a blob by their marker lines; the script printed an aggregate of 4 slices over 55 CONTENT lines: PLANF009R32 `71eb1a0a…` 2029 b / 38 l · FINDINGS `18e9e07a…` 3127 b / 3 l · LEDGER32 `01a19e02…` 4327 b / 1 l · CANDIDATES32 `357dedcd…` 736 b / 13 l. Re-measured from that same blob, constraint 9's two numbers reproduce: TOTAL 250 lines, PROSE = 250 − 55 = 195.
G4 — `cmp` EXIT 0 for `.agent/plan.md` at C1 vs PLANF009R32 (both `71eb1a0a…`) and for `.agent/candidates.md` at C4 vs CANDIDATES32 (both `357dedcd…`); each negative control (the crossed pair) EXITS 1, "differ: byte 3, line 1". Plan `wc -l` 38 against the 50-line cap; `^## Goal$` 1 and `^## Next Steps$` 1. Over `.agent/candidates.md`, line-anchored, base→C4: a leading `- ` 2→0, `^NON-EMPTY\.` 1→0, `^EMPTY\.` 0→1 — all six as ordered; the UNANCHORED `EMPTY.` reads 1 at BOTH points, so the substring form is the vacuous clause R-0646 registers, measured in the round that registers it.
G5 — FINDINGS at C2 on the ROUND BASE: (a) the base blob is a byte-exact PREFIX and the remainder is exactly one newline plus the slice, 3128 bytes; (b) N counted BY THE SCRIPT at 2 and the last 2 blank-line-separated units equal the slice's 2 paragraphs IN ORDER; 576883 b / 1138 l → 580011 b / 1142 l; an equal-length printable-byte flip in the FIRST appended paragraph, `R`→`Z` at offset 576886, is REJECTED by both readers while both ACCEPT the true file. LEDGER32 at C3 BASED ON C2: (a) prefix holds, remainder one newline plus the slice, 4328 bytes; (b) N counted at 1, tail matches in order; 580011 b / 1142 l → 584339 b / 1144 l; flip `G`→`Z` at offset 580012 REJECTED by both readers, true file ACCEPTED by both.
G6 — line-anchored at line START over `.agent/live_review.md`, reported at ALL THREE points. BASE: entries 211 over 211 DISTINCT · leading `Done: R-` 3 · leading `Landed: ` 0 · leading `Gate: R` keys 31 over 31 DISTINCT · `Gate: R32` 0. C2: 213 over 213 DISTINCT · 3 · 0 · 31 over 31 DISTINCT · 0. C3: 213 over 213 DISTINCT · 3 · 0 · 32 over 32 DISTINCT · 1. Every base reading the block ordered reproduces, and constraint 3's fixed values hold at C2 and C3.
G7 — the anchoring control ordered as a DIFFERENCE, reported at BOTH points. BASE: 211 leading `- R-` ids · 271 DISTINCT `R-\d{4}` strings anywhere · 60 of those never registered as a leading id · 31 leading `Gate: R` keys against 81 unanchored occurrences — all five of the reviewer's base numbers reproduce (see Deviations for the reading that yields 81). C3, MEASURED and predicted by nothing: 213 · 273 · 60 · 32 leading keys against 84 unanchored. The differences are 60 ids and 50 gate keys at the base, 60 and 52 at C3.
G8 — max REGISTERED id read line-anchored: R-0645 at the base, R-0647 at C3. Open by DECISION F009 D10's rule (leading `- R-` entries minus leading `Done: R-` lines): 211 − 3 = 208 at the base, 213 − 3 = 210 at C3. Both fixed values hold; the next round's id ceiling is R-0648.
G9 — RANGE base→C4 lists exactly the five declared paths other than `.agent/handoff.md`, set difference EMPTY in both directions, 0 paths beginning `packages/`, `apps/`, `docs/` or `tests/`. Every commit has ONE parent. `git show --numstat` (invoked with no `--` before the SHA) and `git diff --numstat` AGREE on every cell and every cell equals the `+/-` column of the tables above: 250/0, 160/152, 6/8, 4/0, 2/0, 5/40. Pre-handback insertions 250, 160, 6, 4, 2 and 5, each under the 500 cap. Leading `<<<SLICE ` and `<<<END ` read 0 LINES in `.agent/plan.md`, `.agent/live_review.md` and `.agent/candidates.md` (unanchored, `.agent/live_review.md` holds 24 and 24, which is LEDGER32 quoting both markers mid-line as the block says it does). `git ls-files .remedy-wt` reads 0. THIS ROUND's 6 reflog rows all classify as `commit` by the operation before the first `:`, so `amend`, `rebase` and `cherry` are each 0; no total is asserted over the whole reflog.
G10 — CANARY `python3 -m pytest tests/cli/test_golden_path.py -q -rf`, run in the PRIMARY checkout, serially, with no other pytest process alive: REAL exit code 0, and the count IT printed is "42 passed". No docs gate is owed — the change set holds no `docs/` path.
G11 — this file carries every mandated section of docs/agents/handback_template.md, an item-status row for each of C0a, C0b, C1, C2, C3, C4 and C5, the round base SHA, one line per gate, G6 at all three of its points and G7 at both of its points, and the block's four-line `Fortschritt:` verbatim. Its `wc -l` is reported in Deviations below.

## Authored-text proofs

Four reviewer-authored slices, all extracted programmatically from the COMMITTED C0a blob and applied by script, never retyped: PLANF009R32 → `.agent/plan.md` at C1, `cmp` EXIT 0; CANDIDATES32 → `.agent/candidates.md` at C4, `cmp` EXIT 0; FINDINGS → `.agent/live_review.md` at C2 and LEDGER32 → `.agent/live_review.md` at C3, each proved by the two independent readers of G5 with an equal-length negative control on its FIRST appended paragraph. The C0a blob itself is byte-equal to the block as received (G2).

## Deviations & assumptions

No departure from the block's ordered commit sequence: C0a, C0b, C1, C2, C3, C4, C5 were committed in that order, exactly once each, with no extra commit, no dropped commit and no reordering. No slice was altered.
ONE READING NEEDED A DISCRIMINATOR, declared rather than silently chosen. G7 orders "unanchored occurrences of `Gate: R`" and states the reviewer's base value as 81. A LITERAL substring scan for `Gate: R` reads 124 at the base and 131 at C3; the reviewer's 81 is the KEY-SHAPED scan, `Gate: R` followed by a digit, which reads 81 at the base and 84 at C3. Both readings are reported above; the key-shaped one is the population the anchored count of 31 is comparable to, and it reproduces the ordered value exactly. The 43 extra literal hits at the base are prose mentions such as a backticked `Gate: R` with no round number after it. Nothing was adjusted to make a number agree.
`git commit` printed 250/242 for C0b under its own rewrite detection while `--numstat` reads 160/152; the tables and G9 use the `--numstat` cells, which `git show` and `git diff` agree on, as checklist item 28 requires.
This file measures 94 lines by `wc -l` against the 100 that a per-commit table of more than five commits allows, so NO DECISION D15 overage is claimed and no section was dropped to fit.

## Next

Closure round one: run the evidence job and build a FRESH review zip, whose values the STATUS line will quote in closure round two. `.agent/candidates.md` is EMPTY as of C4, so the block condition this session inherited is cleared. Before authoring, re-read `.agent/STOP` from disk (Phase 1 rule 1) and only then the Open PR Gate (rule 2). No pull request exists for F009; it opens one at its own closure.
