# Handback — F021 R25 (the discharge round: checklist item 32, the R24 verdict, the recovered R18 verdict)

Feature F021 Live activity feed + now-card · Round R25 · branch `feature/f021-live-activity-feed`.
Round base `1ae048937a12e247c410ed79e771adc25514f07b` (`1ae04893`). Open findings after C3: 222, maximum R-0659, next free R-0660. NO CODE CHANGES this round.
Fortschritt: ~89 % (T002 — Uhr injiziert und Ankunftsstempel auf dem Transport-
             Event; es fehlen Ring, NowCard und Feed-Scroll)
             — Schaetzung

## Range

Review of `1ae04893..34e14d02`, plus the C4 handoff commit that writes this file.

## Commits

### c5c9a183 docs(state): save the F021 R25 step block
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f021-r25.md | +303/-0 | C0a — the reviewer's block saved verbatim |

### c9bc5094 docs(state): mirror the F021 R25 step block into last_block
| Path | +/- | Reason |
|---|---|---|
| .agent/last_block.md | +195/-122 | C0b — written FROM the committed C0a blob |

### d8395de9 docs(state): point the F021 plan at R25, the discharge round
| Path | +/- | Reason |
|---|---|---|
| .agent/plan.md | +16/-14 | C1 — PLANF021R25 plus one terminating newline |

### 796bef72 docs(agents): promote the R-0656 rule into the section 3 checklist as item 32
| Path | +/- | Reason |
|---|---|---|
| docs/agents/planner_reviewer_prompt.md | +22/-0 | C2 — the ITEM32 pair, append-shaped |

### 34e14d02 docs(review): record the R24 verdict, register R-0659 and recover the lost R18 verdict
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +10/-0 | C3 — the RECORD25 append |

### C4 — the handback commit, which writes this file and therefore cannot name its own SHA or its own numstat (R-0149 pattern, R-0494 heading rule)
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | not tabled | C4 — this rewrite; its numbers do not exist when this text is written |

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

`gh pr list --state open --json number,headRefName` → `[]`, exit 0. `git push -u origin feature/f021-live-activity-feed` after C4. NEITHER `gh pr create` NOR `gh pr merge` was run. No worktree added or removed, no destructive check, no force-push, no history rewrite.

## Verification

One line per gate; the transcripts stay in the round report (R-0582). Every numeral below is one this worker measured.
- G1 PASS — `.agent/STOP` absent immediately before C0a and again before C4; branch `feature/f021-live-activity-feed`; `git status --porcelain` 0 lines after each of C0a, C0b, C1, C2 and C3; C4's own reading is left to the next session (§3 item 31). Owed reading from the last round: `1ae04893` is single-parent and touches `.agent/handoff.md` alone at 33 insertions, under the 500 cap.
- G2 PASS — transport: the reviewer's emitted `.remedy-wt/f021-r25.md`, the `.agent/authored/f021-r25.md` blob at C0a and the `.agent/last_block.md` blob at C0b are ALL byte-identical at sha256 `85ac405392030d0846796af87f0a39e8b43d1624561ff87ce1014ee77abe2613` over 34697 bytes and 303 lines. C0b was written from the committed C0a blob.
- G3 PASS — the marker-line extractor over the committed C0a blob printed 2 whole texts (PLANF021R25 49 lines, RECORD25 9 lines), 1 pair (ITEM32: FROM 2 lines, TO 24 lines) and 84 CONTENT lines. Re-measured from that same blob: TOTAL 303 against D6's 490, PROSE 219 against D5's 400 — both equal to constraint 9's numerals.
- G4 PASS — `cmp .agent/plan.md` against PLANF021R25 plus one terminating newline exit 0; NEGATIVE CONTROL against the bare slice exit 1. Last byte is a newline; `wc -l` 49, the MEASURED value the block ordered; `^## Goal$` 1, `^## Next Steps$` 1.
- G5 PASS — ITEM32 over `docs/agents/planner_reviewer_prompt.md`: FROM 1 at the round base and 1 at C2; TO 0 at the round base and 1 at C2. Ordered equality: 22 added lines, 22 TO-only lines, ELEMENTWISE equal in order, 0 deletions. Checklist items run 1..32 consecutively with no duplicate (31 items at the base); item 32 sits between item 31 and the "Why this is on disk and not a habit" paragraph; file 944 lines before, 966 after.
- G6 PASS — reader (a): the base blob is a byte-exact PREFIX of the C3 file and the remainder is exactly one newline plus RECORD25 plus one terminator, sha256 `6da288742762c35dba1c0619d714a18addfddf36d21245e94526999e0f21ab45` over 14930 bytes and 10 lines; file 551086 B / 1158 L before, 566016 B / 1168 L after. Reader (b), set-wise and ELEMENTWISE over the whole list: N 260 → 265, RECORD25 exactly 5 units. NEGATIVE CONTROL at byte offset 4 of the FIRST paragraph, `v` → `X` at equal length: BOTH readers REJECTED it and BOTH accepted the true file.
- G7 PASS — ledger sets, line-anchored, round base → C3: `- R-` 221 → 222, DISTINCT at both; maximum R-0658 → R-0659; `Done: R-` 0 → 0; `Landed: ` 0 → 0; `Gate: R` keys 23 → 24, DISTINCT at both; `Gate: R25` 0 → 1; `Gate: R19` 0 at BOTH; `- R-0656` exactly ONCE at BOTH. Base key sequence measured as R1-R18 and R20-R24, R19 absent, which is the gap R-0659 registers.
- G8 PASS — `git diff 1ae04893..34e14d02 -- .agent/live_review.md` has 0 deleted lines and 10 added. The `.agent/live_review.md` blob at `acb688a9` (521496 B / 1130 L) is a byte-exact PREFIX of the C3 file.
- G9 PASS — all four suites run SERIALLY from `/home/decodeux/Repos/remedy`, each exit 0, counted by passed plus skipped: state-readers `tests/ui_server/ tests/orchestration/test_test_runner.py tests/regression/test_resource_safety.py` 511 (511 passed); `tests/docs/` 295; canary `tests/cli/test_golden_path.py` 42; `tests/ui_contracts/` 473 (469 passed + 4 skipped), UNCHANGED. `npx tsc --noEmit` and `npm run test:unit` were NOT run and are not reported, as the block ordered.
- G10 PASS — base-to-C3: path set equals the five non-handoff `Change:` paths with BOTH differences EMPTY; all 5 commits single-parent; `git show --numstat` and `git diff --numstat` agree cell by cell with every cell of the `## Commits` tables above; insertions 303, 195, 16, 22, 10, each under 500; `git ls-files .remedy-wt` 0; `git worktree list` is the primary checkout alone; `gh pr list --state open` EMPTY. Marker sweep, line-anchored over the three files a slice or pair landed in: I counted 6 marker prefixes in this block (`<<<SLICE `, `<<<END `, `<<<PAIR `, `<<<FROM`, `<<<TO`, `<<<ENDPAIR`) and each reads 0 in each file, as does any line starting `<<<`. Reflog by OPERATION field over this round's 5 rows: every one `commit`; `amend`, `rebase` and `cherry` each 0.

## Authored-text proofs

Every applied byte was extracted MECHANICALLY from the committed C0a blob by marker LINES, never copied by eye. PLANF021R25 sha256 `548cae252db642666c39d2a76f2c0641a78a128156be3669b3451b363a2d0f0c` (2855 B); RECORD25 sha256 `c4fca2deff8a0f55653808a7bf451009b6bbbead42113b10083922c4dd8876bf` (14928 B); ITEM32 FROM sha256 `f290ae45159246694b9b6573345c23942b66e5b9d48c108b07ccfbbfa0dcbb4b` (117 B), TO sha256 `0cb8575957e6fa8a947d7345c208e3b9638a3b94f3f06149a50e5fc90d802180` (1820 B). `.agent/plan.md` proved by `cmp` at exit 0 with a red control at exit 1 (G4); the ledger append proved by two independent readers with a same-length mutant both rejected (G6); the pair proved by ordered equality against the TO-only lines (G5).

## Deviations & assumptions

NONE. The ordered commit sequence C0a, C0b, C1, C2, C3, C4 was executed exactly, in order, with no extra, dropped or reordered commit. No slice or pair half was retyped, rewrapped, reflowed, reindented or whitespace-adjusted. Nothing in the block was found wrong: every numeral it predicted — TOTAL 303, PROSE 219, plan 49 lines, `- R-` 221 → 222, maximum R-0658 → R-0659, `Gate: R` keys 23 → 24, `Gate: R19` 0 at both, suite totals 511 / 295 / 42 / 473 — matched the value this worker measured independently.
DECISION D15, stated-cause overage: this file is 85 lines against the 60-line cap and within the 100 AGENTS.md permits for per-commit tables of more than five commits. Cause is mandated content only — six per-commit changed-files tables, the item-status table, the ten one-line gate results with their measured numerals, and the authored-text proofs. No section was dropped to meet the cap.

## Next

THIS SESSION IS OVER. The NEXT session begins at docs/agents/self_drive_protocol.md Phase 1 rule 1 — the `.agent/STOP` check — BEFORE rule 2's Open PR Gate (R-0347). Rule 2 will find NO open pull request, so rule 5 applies and F021 continues on this branch. R25's own verdict is UNRECORDED and the next round's ledger commit owes it. The next round is R26, THE RING ROUND, moved there by DECISION F021 D7: `FeedRow` gains `receivedAtMs`, `feedRowOf` takes it, and `receiveBrainFrame` threads it from the transport event R23 stamped. R26 is the first round to touch the ring, whose append placement DECISION F021 D5 governs. The reviewer's promotion debt is now DISCHARGED: R-0656's rule is §3 checklist item 32 as of C2, so a later block reads it from the checklist rather than from a finding body.
