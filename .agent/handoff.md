# Handback — F021 R23 (the arrival stamp on the transport event)

Feature F021 Live activity feed + now-card · round R23 · branch `feature/f021-live-activity-feed`
Round base: `16186186e44ac4489a16e82b53e4d60f650ed578` (the R22 handback commit).
Fortschritt: ~89 % (T002 — die Uhr ist injiziert, der Frame traegt ab dieser
             Runde seinen Ankunftsstempel; es fehlen Ring, NowCard und Feed)
             — Schaetzung

## Range
Review of `16186186`..`3cd2eeeb` (C0a–C4); C5 below is the commit that writes this file.

## Item status
| Item | Status | Reason |
|---|---|---|
| C0a | done | |
| C0b | done | |
| C1 | done | |
| C2 | done | |
| C3 | done | |
| C4 | done | |
| C5 | done | this file; its own SHA is unquotable from inside itself |

## Commits

### 4dc0c06c docs(state): save the F021 R23 step block
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f021-r23.md | +357/-0 | C0a — the R23 block, NEW |

### d78eba54 docs(state): mirror the F021 R23 step block into last_block
| Path | +/- | Reason |
|---|---|---|
| .agent/last_block.md | +210/-270 | C0b — written FROM the committed C0a blob |

### fbb5a5ee docs(state): point the F021 plan at R23, the arrival stamp
| Path | +/- | Reason |
|---|---|---|
| .agent/plan.md | +17/-16 | C1 — PLANF021R23, whole-file write |

### a8215a65 docs(review): record the R22 verdict and register the two block-text findings
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +10/-0 | C2 — RECORD23 appended; R-0656 and R-0657 registered |

### ba396370 feat(ui): stamp each transport frame with its arrival instant
| Path | +/- | Reason |
|---|---|---|
| apps/ui/src/api/brainStreamDriver.ts | +9/-2 | DRIVEREVENTSTAMP — the frame member carries `receivedAtMs` |
| apps/ui/src/api/brainStreamHost.ts | +1/-1 | HOSTTELLSTAMP — the host stamps from `deps.now()` |
| apps/ui/src/api/brainStreamDriver.test.ts | +1/-1 | DRIVERTESTFRAME — literal feeds the new field |
| apps/ui/src/api/brainStreamRunner.test.ts | +1/-1 | RUNNERTESTFRAME — literal feeds the new field |
| apps/ui/src/api/brainStreamHost.test.ts | +3/-3 | HOSTTESTONEFRAME + HOSTTESTPOLLFRAMES |

### 3cd2eeeb test(ui-contracts): pin the arrival stamp on the transport event
| Path | +/- | Reason |
|---|---|---|
| tests/ui_contracts/test_brain_stream_ring.py | +35/-0 | C4 — CONTRACTSTAMP appended ALONE (constraint 8) |

### C5 — the handback commit, which cannot table its own SHA (R-0494)
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | rewrite | C5 — this file |

## External actions
`gh pr list --state open --json number,headRefName` → `[]`. `git push -u origin feature/f021-live-activity-feed` after C5. No `gh pr create`, no `gh pr merge`, no worktree add/remove, no force-push, no history rewrite.

## Verification
One line per gate; full transcripts are in the round report, not this file (R-0582). Every exit code below is real.
- G1 PASS — `.agent/STOP` absent before C0a and before C5; branch `feature/f021-live-activity-feed`; `git status --porcelain` 0 lines after each of C0a, C0b, C1, C2, C3, C4. Owed reading: `16186186` is single-parent and touches `.agent/handoff.md` alone at +51/-32, under the 500 cap.
- G2 PASS — sha256 `f3b960d05beb4a87807e72037dd0514aeb6605567493951c100d2450b9329b40`, 28934 bytes, 357 lines, equal over all four copies (reviewer's `.remedy-wt/` emission, the bytes read, C0a, C0b).
- G3 PASS — my extractor read, over the committed C0a blob: 6 pairs, 3 whole-text slices, 127 CONTENT lines. Re-measured caps: TOTAL 357 ≤ 490 (D6), PROSE 357−127 = 230 ≤ 400 (D5).
- G4 PASS — six REWRITES, table `Pair | FROM@base | FROM@C3 | TO@C3`: DRIVEREVENTSTAMP 1/0/1 · HOSTTELLSTAMP 1/0/1 · DRIVERTESTFRAME 1/0/1 · RUNNERTESTFRAME 1/0/1 · HOSTTESTONEFRAME 1/0/1 · HOSTTESTPOLLFRAMES 1/0/1.
- G5 PASS with one declared reading — C3 blob is a byte-exact PREFIX of the C4 file (True); remainder is EXACTLY one newline + CONTRACTSTAMP + one newline (True), sha256 `db6d3ede8cfb42c507cb54af98db8f863e4da3708b7db9f96f89c5e95a6e34b0`, 1531 bytes / 35 lines; file 16125 B / 363 L before, 17656 B / 398 L after; 0 deleted lines; EXACTLY 2 blank lines precede the new top-level class, counted from the blob, not from a linter. Ordered equality: see Deviations.
- G6 PASS — `cmp` C1 blob vs PLANF021R23+newline exit 0; NEGATIVE CONTROL vs the bare slice exit 1; last byte is a newline; `wc -l` 47, the MEASURED value the block ordered; `^## Goal$` 1, `^## Next Steps$` 1.
- G7 PASS — reader (a): base blob a byte-exact prefix, remainder one newline + RECORD23 + one newline, sha256 `5ea2081037cb47b125d539495ae835305f26620cb4bfec649c2c5c784edeaf9e`, 8533 B / 10 L; file 534400 B / 1140 L → 542933 B / 1150 L. Reader (b) ELEMENTWISE over the whole list: 251 → 256 units, RECORD23 exactly 5 units. NEGATIVE CONTROL at offset 4 of the C2 file's FIRST paragraph (`v`→`X`, equal length): BOTH readers REJECT it, BOTH accept the true file. Base blob read via `git show` into `.remedy-wt/` scratch; no tracked file was overwritten.
- G8 PASS — base → C2: `- R-` 218 → 220, DISTINCT at both; maximum R-0655 → R-0657; `Done: R-` 0 → 0; `Landed: ` 0 → 0; `Gate: R` keys 21 → 22, DISTINCT at both; `Gate: R23` 0 → 1.
- G9 PASS — serially, at C4, in the primary checkout: `npx tsc --noEmit` in `apps/ui` exit 0, output EMPTY (0 bytes); `npm run test:unit` in `apps/ui` exit 0, 15 files / 209 tests, UNCHANGED from base; `python3 -m pytest tests/ui_contracts/ -q -rf` from the repo root exit 0, 469 passed + 4 skipped = 473; the three state-reading suites from the repo root exit 0, 511 passed = 511; `tests/cli/test_golden_path.py` from the repo root exit 0, 42 passed = 42. Every total equals the block's.
- G10 PASS — base→C4: 10 paths, both differences against the ten non-handoff `Change:` paths EMPTY; 6 commits, every one single-parent; insertions 357, 210, 17, 10, 15, 35, each under 500; `git show --numstat` and `git diff --numstat` agree cell by cell with the `## Commits` tables above, all 10 cells; `git ls-files .remedy-wt` 0; `git worktree list` the primary checkout alone; `gh pr list --state open` EMPTY, and neither `gh pr create` nor `gh pr merge` was run. Marker sweep, line-anchored over the eight files a slice landed in: 0 for each of `<<<SLICE `, `<<<END `, `<<<PAIR `, `<<<FROM`, `<<<TO`, `<<<ENDPAIR`, and 0 for any line starting `<<<`. Reflog BY OPERATION over this round's 6 rows: every operation `commit`; `amend`, `rebase`, `cherry` each 0 in that field.

## Authored-text proofs
All three whole-text slices and all twelve pair halves were extracted MECHANICALLY by marker line from the committed C0a blob `4dc0c06c`, never hand-copied. PLANF021R23: `cmp` exit 0 against slice+newline, exit 1 against the bare slice (G6). RECORD23: byte-exact remainder under two independent readers plus a same-length negative control (G7). CONTRACTSTAMP: byte-exact remainder, 0 deletions (G5). Six pairs: FROM 1 at base, FROM 0 and TO 1 at C3 (G4).

## Deviations & assumptions
No departure from the ordered commit sequence: C0a, C0b, C1, C2, C3, C4, C5 exactly, no extra commit, none dropped, none reordered. No slice was retyped, rewrapped or adjusted. Two observations about the BLOCK's own text, reported rather than reconciled (constraint 1):
1. G5's ordered-equality clause reads "the lines C4's diff ADDS to that file are exactly the slice's lines IN ORDER". Measured strictly, that is FALSE: the diff adds 35 lines and CONTRACTSTAMP has 34. The extra line is the separator newline that constraint 5's own append convention mandates ("one newline, then the slice, then one terminator"), so `added[0]` is the empty separator line and `added[1:]` equals the slice's 34 lines ELEMENTWISE IN ORDER — measured True. The two clauses of the block cannot both be literally satisfied by any conforming append; I applied the convention and report both readings. This is the R-0657 family (a clause read against the property it must establish), one degree milder.
2. G10 says "each of the four marker prefixes", but G3 names SIX marker tokens (`<<<SLICE `, `<<<END `, `<<<PAIR `, `<<<FROM`, `<<<TO`, `<<<ENDPAIR`). Rather than guess the intended partition of four, I swept all six line-anchored plus any line starting `<<<`; every one reads 0 in all eight files. This is the R-0656 family (a hand-counted numeral about the block's own parts).
Assumption: none beyond the block.
Size: this file is 91 lines, measured with `wc -l` on these final bytes. DECISION D15 declared overage against the 60-line cap (the 7-commit tables put it in AGENTS.md's ≤100 band anyway): the mandated content causing it is the seven per-commit changed-files tables, the item-status table, the one-line-per-gate verification block for ten gates, and the authored-text proofs — no prose padding and no transcripts.

## Next
Reviewer verdict on R23. Then R24 puts the stamp on the RING's row: `feedRow.ts` gains `receivedAtMs` on `FeedRow` and `feedRowOf` takes it, and `brainStream.ts`'s `receiveBrainFrame` threads it from the event this round created. R24 is the first round to touch the ring, whose append placement DECISION F021 D5 governs. Next session: Phase 1 rule 1 (`.agent/STOP`) before rule 2 (Open PR Gate).
