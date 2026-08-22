# Handback — F021 R27, the record-and-repair round

Branch `feature/f021-live-activity-feed`. ROUND BASE `457346b69f8beb23b868faa9315ef658aa932e27` (short `457346b6`).

Fortschritt: ~92 % (T002 — Uhr, Ankunftsstempel und Ring verdrahtet; es fehlen
             NowCard-Punkt und Feed-Scroll)
             — Schaetzung

## Range
Review of `457346b6`..HEAD, HEAD being C5 — the commit that carries this file.

## Commits

### 4c6aea98 docs(state): save the F021 R27 step block
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f021-r27.md` | +274/-0 | C0a — the block saved verbatim, byte for byte |

### 2b62c498 docs(state): mirror the F021 R27 step block into last_block
| Path | +/- | Reason |
|---|---|---|
| `.agent/last_block.md` | +169/-385 | C0b — written FROM the committed C0a blob |

### 15814e4c docs(state): point the F021 plan at R27, the record and repair round
| Path | +/- | Reason |
|---|---|---|
| `.agent/plan.md` | +23/-23 | C1 — PLANF021R27 plus one terminator; 48 lines |

### 86c1de16 docs(review): record the R26 verdict and register R-0660
| Path | +/- | Reason |
|---|---|---|
| `.agent/live_review.md` | +6/-0 | C2 — RECORD27 appended ALONE; registers R-0660, resolves nothing |

### 92ed0455 fix(ui): move the feedRow test shim below the last import
| Path | +/- | Reason |
|---|---|---|
| `apps/ui/src/api/feedRow.test.ts` | +1/-1 | C3 — SHIMMOVE alone; a pure reorder of nine lines |

### fd95980f docs(review): resolve R-0660, the shim now sits below the last import
| Path | +/- | Reason |
|---|---|---|
| `.agent/live_review.md` | +2/-0 | C4 — DONE660 appended ALONE; the first `Done:` line this ledger carries |

### C5 docs(state): hand back F021 R27 — SHA unnameable here, since this table sits inside the commit it describes (R-0494)
| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | rewrite | C5 — this file |

## External actions
- `gh pr list --state open --json number,headRefName` → exit 0, `[]`. NO `gh pr create` and NO `gh pr merge` was run this round.
- NO worktree was created, added or removed this round; `git worktree list` is the primary checkout ALONE.
- `npm run lint` was NOT run: constraint 8 forbids it, it is red tree-wide under R-0622 and it is no gate of this round.
- `git push -u origin feature/f021-live-activity-feed` → runs immediately AFTER C5; a commit cannot record the push that carries it. Its result is in the round report.

## Verification
G1 PASS — `.agent/STOP` ABSENT immediately before C0a and again before C5; branch `feature/f021-live-activity-feed`; `git status --porcelain` printed 0 lines after each of C0a, C0b, C1, C2, C3 and C4 (C5's own reading is ordered nowhere, §3 item 31). Owed reading from R26: `457346b6` is single-parent and touches `.agent/handoff.md` ALONE at +64/-48, under the 500-insertion cap.
G2 PASS — sha256 `ef9c3549c0fa1a040369f5d6b57eea48d430a10b456b0b447bb35701de8fc94a`, 26266 bytes, 274 lines, EQUAL over all four copies: the reviewer's `.remedy-wt/f021-r27.md`, the bytes I read, `.agent/authored/f021-r27.md` at C0a and `.agent/last_block.md` at C0b, the last written FROM the committed C0a blob.
G3 PASS — my marker-line extractor over the COMMITTED C0a blob printed 3 whole texts (PLANF021R27, RECORD27, DONE660), 1 pair (SHIMMOVE) and 72 CONTENT lines, with 0 stray `<<<` lines inside any slice body. Re-measured from that same blob: TOTAL 274 against DECISION F085 D6's 490, PROSE 202 against D5's 400 — both equal to constraint 9.
G4 PASS — `cmp .agent/plan.md <PLANF021R27 + one newline>` exit 0; NEGATIVE CONTROL `cmp` against the bare slice exit 1 (EOF after byte 2817, in line 48). Last byte is a newline; `wc -l` reads EXACTLY 48, equal to the reviewer's count, so <50 holds; `^## Goal$` 1 and `^## Next Steps$` 1.
G5 PASS — C2/RECORD27, reader (a): the `457346b6` blob is a byte-exact PREFIX of the C2 file, remainder EXACTLY one newline + slice + one terminator, sha256 `a7008d2cd7f36abbb1a7e01f12f4d7244657ff5609f1dc78f855aa6e925c2d4c`, 8100 B, 6 lines; file 572216 B / 1172 L → 580316 B / 1178 L. Reader (b): units 267 → 270, RECORD27 exactly 3 units, ELEMENTWISE equal over the WHOLE list. C4/DONE660, reader (a): the C2 blob is a byte-exact PREFIX of the C4 file, remainder sha256 `9d29c35494ae66d3136f0133174c17d1d91aed271ef8d239e1744088442ba0c5`, 764 B, 2 lines; file 580316 B / 1178 L → 581080 B / 1180 L. Reader (b): units 270 → 271, DONE660 exactly 1 unit, ELEMENTWISE equal. NEGATIVE CONTROL on the C4 file at offset 4 of the FIRST paragraph, byte `v` → `X` at equal length: reader (a) REJECTED it on the prefix clause and reader (b) REJECTED it at unit index 0, while BOTH ACCEPTED the true file. Neither the C2 diff (+6/-0) nor the C4 diff (+2/-0) deletes a line.
G6 PASS — base, then C2, then C4: `- R-` 222 → 223 → 223, ALL DISTINCT at all three points; MAXIMUM registered id R-0659 → R-0660 → R-0660, next free `R-0661`; `Landed: ` 0 → 0 → 0; `Gate: R` keys 25 → 26 → 26, DISTINCT at all three; `Gate: R27` 0 → 1 → 1. `Done: R-` reads 0 → 0 → 1, the FIRST `Done:` line this ledger has ever carried, and it names R-0660.
G7 PASS — `apps/ui/src/api/feedRow.test.ts`: SHIMMOVE's FROM 1 at the round base and 0 at C3, TO 0 at the round base and 1 at C3. THE MOVE CHANGES NOTHING BUT ORDER: the SORTED MULTISET of the file's lines is IDENTICAL at `457346b6` and at C3, the file is 79 newline-terminated lines at BOTH points and 3093 bytes at BOTH. At C3 the `^import ` lines are 1, 2 and 3 and `function feedRowOf` is line 8, so every import number is lower than the function's; at the base they were imports 1, 2 and 10 against the function at 7, which is the defect R-0660 records.
G8 PASS — PRIMARY checkout, from `apps/ui`, run SERIALLY and never two at once: `npx tsc --noEmit` exit 0 with EMPTY stdout and stderr; `npm run test:unit` exit 0 at 15 files and 212 tests, both UNCHANGED from the reviewer's base reading, as a behaviour-free move must be.
G9 PASS — PRIMARY checkout, working directory `/home/decodeux/Repos/remedy`, run SERIALLY, counted BY PASSED PLUS SKIPPED: `tests/ui_contracts/` exit 0 at 472 passed + 4 skipped = 476, UNCHANGED; `tests/ui_server/ tests/orchestration/test_test_runner.py tests/regression/test_resource_safety.py` exit 0 at 511 passed = 511; canary `tests/cli/test_golden_path.py` exit 0 at 42. No docs gate is owed: the `Change:` list holds no `docs/` path.
G10 PASS — `457346b6`..C4 `fd95980f`: path set EQUAL to the five non-handoff `Change:` paths, difference EMPTY BOTH ways; all six commits single-parent; `git show --numstat` and `git diff --numstat` agree cell by cell with every `## Commits` table above, the range's single aggregate cell `+8/-0` for `.agent/live_review.md` being exactly C2's +6/-0 plus C4's +2/-0; insertions 274, 169, 23, 6, 1 and 2 — each under the 500 cap; `git ls-files .remedy-wt` 0; `git worktree list` the primary checkout ALONE; `gh pr list --state open` EMPTY. Marker sweep, LINE-ANCHORED over all SIX prefixes this block uses (`<<<SLICE `, `<<<END `, `<<<PAIR `, `<<<FROM`, `<<<TO`, `<<<ENDPAIR`) plus any line starting `<<<`: 0 in each of the three files a slice or pair LANDED in; the two block mirrors read 10 each by construction. Reflog BY OPERATION FIELD (text before the first `:`), scoped to this round's six rows: every operation is `commit`, and `amend`, `rebase` and `cherry` each occur 0 times in that field.

## Authored-text proofs
PLANF021R27 — `cmp` against the slice extracted from the committed C0a blob plus one terminator: exit 0; negative control against the bare slice: exit 1 (G4). RECORD27 and DONE660 — prefix-plus-remainder equality under two independent readers, with a same-length mutant of the C4 file rejected by both (G5). Both SHIMMOVE halves were extracted MECHANICALLY from the committed C0a blob by their marker lines and applied by exact byte replacement, refusing unless FROM occurred exactly once; not one half was retyped, rewrapped, reflowed or reindented, and the applied file's sorted line multiset is unchanged (G7).

## Deviations & assumptions
None. The ordered sequence C0a, C0b, C1, C2, C3, C4, C5 was executed exactly: no extra commit, none dropped, none reordered; C2, C3 and C4 were kept as three separate commits per constraint 2, so the finding persists on disk before the fix.
Observations, no action taken: (a) constraint 5's stated property holds — SHIMMOVE's containment test printed `TO contains FROM: false` here too, and its FROM and TO hold the SAME nine lines, so no second difference was found. (b) Every numeral this block predicted was reproduced by my own measurement; none differed. (c) `.agent/decisions.md` and `.agent/context.md` were not touched — no path outside the `Change:` list was.
DECISION D15 overage, declared: this file measures 87 lines by `wc -l`. That is over the 60-line baseline cap and WITHIN the ≤100 tier the template grants a handback whose per-commit tables cover more than 5 commits; this round has 7. Cause is mandated content only — seven per-commit changed-files tables for C0a through C5, ten one-line gate results, the item-status table, the external-actions list and the authored-text proofs. No section was dropped and no transcript was inlined (R-0582).

## Item status
| Item | Status | Reason |
|---|---|---|
| C0a | done | `4c6aea98` |
| C0b | done | `2b62c498` |
| C1 | done | `15814e4c` |
| C2 | done | `86c1de16`, the ledger's only change in that commit |
| C3 | done | `92ed0455`, the pair alone |
| C4 | done | `fd95980f`, the ledger's only change in that commit |
| C5 | done | this commit |

## Next
THIS SESSION IS OVER. The NEXT session begins at docs/agents/self_drive_protocol.md Phase 1 rule 1 — the `.agent/STOP` check — BEFORE rule 2's Open PR Gate (R-0347); that gate will find NO open pull request, so rule 5 applies and F021 continues on this branch. R27's own verdict is UNRECORDED and the next round's ledger commit owes it. R28 builds the NowCard's recency dot from `recency.ts` with the CSS `docs/ui/design_reference/assets_spec.md` governs — the first round able to subtract two instants on ONE clock.
