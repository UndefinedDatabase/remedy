# Handoff — F021 R12, the bounded event ring in the state layer

Feature F021 · round R12 · branch `feature/f021-live-activity-feed` · ROUND BASE
`a8bb037d9f539dfcae771d0020239cf6b75154a5`. Open findings 213, maximum R-0650,
next free R-0651: this round minted none and resolved none, per constraint 3.
Deviations, declared (DECISION D15): this file measures 109 lines by `wc -l`,
against the 60-line cap and the 100-line >5-commit allowance. Cause is mandated
content only — six per-commit changed-files tables, the item-status table
AGENTS.md requires, and one line for each of the block's fourteen gates.

Fortschritt: ~45 % (T001 fertig · T002 laeuft — die Projektion Frame→Zeile ist
             gebaut, dieser Block haengt den beschraenkten Ring dahinter; die
             Veroeffentlichung auf der View und die Komponenten folgen)
             — Schaetzung

## Range

Review of a8bb037d9f539dfcae771d0020239cf6b75154a5..HEAD

## Commits

### d2b91200 docs(state): save the F021 R12 ring block as authored text
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f021-r12.md | 490/0 | C0a — the block, byte-identical to the emitted copy |

### dd194642 docs(state): mirror the F021 R12 ring block into last_block
| Path | +/- | Reason |
|---|---|---|
| .agent/last_block.md | 459/219 | C0b — written FROM the committed C0a blob |

### 24c1dc09 docs(state): point the F021 plan at the R12 ring round
| Path | +/- | Reason |
|---|---|---|
| .agent/plan.md | 28/31 | C1 — PLANF021R12 plus one terminating newline |

### 8daad3b7 docs(review): record the R11 verdict as PASS on every gate
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | 2/0 | C2 — RECORD11 appended; nothing registered |

### 1dae12ca feat(ui): bound the brain stream feed ring behind the replay guard
| Path | +/- | Reason |
|---|---|---|
| apps/ui/src/api/brainStream.test.ts | 43/2 | C3 — TESTIMPORT, then TESTRING's 5 cases |
| apps/ui/src/api/brainStream.ts | 33/2 | C3 — 5 pairs; ring inside receiveBrainFrame |
| tests/ui_contracts/test_brain_stream_ring.py | 93/0 | C3 — new source contract, 9 tests |

### C4 docs(state): hand back F021 R12 with the bounded ring built — the handoff commit, which cannot table or name its own SHA (R-0494)
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | this file | C4 — the round's completion report |

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

- `git worktree add --detach .remedy-wt/wt-f021-r12-base a8bb037d` then `git worktree remove` + `prune` — exit 0, 0, 0. Read-only; measured G11's base count.
- `git worktree add --detach .remedy-wt/wt-f021-r12-red 1dae12ca` then `git worktree remove --force` + `prune` — exit 0, 0, 0. G12's mutation lived only here.
- `gh pr list --state open --json number,headRefName` → `[]`. Neither `gh pr create` nor `gh pr merge` was run.
- `git push -u origin feature/f021-live-activity-feed` runs AFTER C4, so its exit code cannot exist in the file C4 writes (R-0371); it is reported in the round report and readable from the remote ref.

## Verification

One line per gate; the transcripts stay in the round report (R-0582).
- G1 `.agent/STOP` absent before C0a and again before C4; branch `feature/f021-live-activity-feed`; `git status --porcelain` 0 lines after each of C0a, C0b, C1, C2, C3.
- G2 sha256 `af4a8a005381c749aa3fe625a32f3fd27a95b31a3c9880470b15981d0f1030fd`, 29018 bytes, 490 lines — equal over the received bytes, `.remedy-wt/f021-r12.md`, the C0a blob and the C0b blob.
- G3 extractor over the committed C0a blob: 16 slices, 254 CONTENT lines, 32 marker lines; TOTAL 490 against D6's 490, PROSE 236 against D5's 400 — both equal to constraint 8.
- G4 `cmp` exit 0 against PLANF021R12+newline, exit 1 against the bare slice (EOF after byte 2630, line 45); last byte is `\n`; `^## Goal$` 1, `^## Next Steps$` 1, `wc -l` 45 ≤ 50.
- G5 reader (a) prefix true, remainder sha256 `62373553bbc74bfe4ba9e3571ff508156f22149b3bca9326bab5318f353ae381`, 3484 bytes / 2 lines, file 473551→477035 bytes and 1098→1100 lines; reader (b) elementwise 230→231 units with RECORD11 = 1 unit; control at byte offset 2 of the FIRST paragraph (`L`→`Q`, equal length) REJECTED by both readers, true file ACCEPTED by both.
- G6 base then C2: `- R-` 213/213 both all DISTINCT, maximum R-0650 at both, `Done: R-` 0/0, `Landed: ` 0/0, `Gate: R` keys 11→12 both DISTINCT, `Gate: R12` 0→1 — every value as predicted.
- G7 eighteen numbers, whole-string over raw bytes. Base FROM 1 for all six. C3: SRC1 FROM 1 TO 1, SRC2A FROM 1 TO 1 (both append-shaped, as ordered), SRC2B 0/1, SRC3A 0/1, SRC3B 0/1, TESTIMPORT 0/1.
- G8 prefix side is the round-base test blob WITH TESTIMPORT substituted in memory; byte-exact prefix true; remainder is exactly `\n`+TESTRING+`\n`, sha256 `0f531cedd9be34f7b89460bb5eafc209265e569f871ec01a6d79c864bb32aa1b`, 1598 bytes / 40 lines; file 4641→6239 bytes, 113→153 lines.
- G9 `git ls-tree <base> -- tests/ui_contracts/test_brain_stream_ring.py` printed NOTHING at exit 0; `cmp` exit 0 against RINGCONTRACT+newline, exit 1 against the bare slice (EOF after byte 3871, line 93).
- G10 `npx tsc --noEmit` in `/home/decodeux/Repos/remedy/apps/ui` — exit 0, stdout and stderr both EMPTY.
- G11 `npx vitest run` in `/home/decodeux/Repos/remedy/apps/ui`, primary checkout — exit 0, 12 files, 173 tests, against a MEASURED 12 files / 168 tests at the round base: rise exactly 5, TESTRING's 5 cases.
- G12 disposable worktree `.remedy-wt/wt-f021-r12-red` at 1dae12ca: green first, exit 0, 9 passed. After reordering the three lines to appended, guard, isGap: exit 1, 1 failed and 8 passed, the failure being `TestAppendSitsBehindTheReplayGuard::test_the_replay_guard_returns_before_the_append` with `AssertionError: an append ahead of the guard duplicates a row on reconnect replay` / `assert 199 < 148`. Tree removed and pruned.
- G13 serially from `/home/decodeux/Repos/remedy`: `tests/ui_contracts/` exit 0, 435 passed + 4 skipped = 439; `tests/ui_server/ tests/orchestration/test_test_runner.py tests/regression/test_resource_safety.py` exit 0, 511 passed; canary `tests/cli/test_golden_path.py` exit 0, 42 passed.
- G14 base..C3 path set EQUAL to the seven non-handoff `Change:` paths, both differences EMPTY; all five commits single-parent; `git show --numstat` and `git diff --numstat` agree cell by cell with the tables above; insertions 490, 459, 28, 2, 169 all under 500; marker lines 0 in every file a slice LANDED in (32 in the two files that carry the block itself, by construction); `git ls-files .remedy-wt` 0; `git worktree list` the primary checkout alone; reflog amend 0, rebase 0, cherry 0; `gh pr list` EMPTY.

## Authored-text proofs

- PLANF021R12 → `.agent/plan.md`: `cmp` exit 0 with a negative control at exit 1 (G4).
- RINGCONTRACT → `tests/ui_contracts/test_brain_stream_ring.py`: `cmp` exit 0 with a negative control at exit 1 (G9).
- RECORD11 → `.agent/live_review.md` and TESTRING → `brainStream.test.ts`: proven as prefix plus remainder digests, not by `cmp` (G5, G8).
- The six FROM/TO pairs: whole-string counts at base and at C3 (G7). Every slice was extracted mechanically from the committed C0a blob; none was retyped.

## Deviations & assumptions

- Commit sequence: C0a, C0b, C1, C2, C3, C4 exactly as ordered — no extra commit, none dropped, no reordering.
- ONE action the block did not order: a SECOND disposable worktree at the round base, with `node_modules` symlinked in from the primary checkout, run read-only to MEASURE G11's base count of 168 rather than accept the figure recorded in the ledger. It was removed and pruned; `git worktree list` ends with the primary checkout alone.
- No slice looked wrong; nothing was reflowed, rewrapped or reindented. No formatter or linter ran. `brainStreamRunner.ts` was not touched. No PR was created or merged.

## Next

R13 publishes `recent` on `BrainStreamView` in `brainStreamRunner.ts`. `publish()`
compares the ring BY REFERENCE — sound only because `receiveBrainFrame` returns
the identical state object when it drops a replay — and `cachedView` must be
seeded FROM the initial state, not from a fresh `[]`, or the very first publish
fires on nothing.
