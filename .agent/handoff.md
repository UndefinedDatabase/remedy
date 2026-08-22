# Handback — F021 R24 (record R23, register R-0658, note the R-0656 recurrence)

Feature F021 Live activity feed + now-card · round R24 · branch `feature/f021-live-activity-feed`
Round base: `c76f90ac16d6c5236c0e097b960485aad000406c` (the R23 handback commit).
Fortschritt: ~89 % (T002 — Uhr injiziert und Ankunftsstempel auf dem Transport-
             Event; es fehlen Ring, NowCard und Feed-Scroll)
             — Schaetzung

## Range
Review of `c76f90ac`..`bdc242b4` (C0a–C2); C3 below is the commit that writes this file. RECORD-ONLY round: no code commit, no FROM/TO pair, nothing under `apps/` or `tests/` touched.

## Item status
| Item | Status | Reason |
|---|---|---|
| C0a | done | |
| C0b | done | |
| C1 | done | |
| C2 | done | |
| C3 | done | this file; its own SHA is unquotable from inside itself |

## Commits

### 09702f93 docs(state): save the F021 R24 step block
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f021-r24.md | +230/-0 | C0a — the R24 block, NEW |

### 675c12bb docs(state): mirror the F021 R24 step block into last_block
| Path | +/- | Reason |
|---|---|---|
| .agent/last_block.md | +152/-279 | C0b — written FROM the committed C0a blob |

### 946a888a docs(state): point the F021 plan at R25, the ring round
| Path | +/- | Reason |
|---|---|---|
| .agent/plan.md | +15/-15 | C1 — PLANF021R24, whole-file write |

### bdc242b4 docs(review): record the R23 verdict, register R-0658 and note the R-0656 recurrence
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +8/-0 | C2 — RECORD24 appended; R-0658 registered, R-0656 recurrence noted beside it |

### C3 — the handback commit, which cannot table its own SHA (R-0494)
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | rewrite | C3 — this file |

## External actions
`gh pr list --state open --json number,headRefName` → `[]`. `git push -u origin feature/f021-live-activity-feed` after C3. No `gh pr create`, no `gh pr merge`, no worktree add/remove, no force-push, no history rewrite.

## Verification
One line per gate; full transcripts are in the round report, not this file (R-0582). Every exit code below is real.
- G1 PASS with one declared reading — `.agent/STOP` ABSENT immediately before C0a and again before C3; branch `feature/f021-live-activity-feed`; `git status --porcelain` 0 lines after each of C0b, C1 and C2 (the after-C0a reading is in Deviations). Owed reading: `c76f90ac` is single-parent (parent `3cd2eeeb`) and touches `.agent/handoff.md` alone at +55/-54, under the 500-insertion cap.
- G2 PASS — sha256 `346b25d8566baed4e44b42d1b08623012e51bec90c902972ebd152577c898d06`, 23071 bytes, 230 lines, EQUAL over all four copies (the reviewer's `.remedy-wt/` emission, the bytes I read, `.agent/authored/f021-r24.md` at C0a, `.agent/last_block.md` at C0b, the latter written FROM the committed C0a blob).
- G3 PASS — my extractor, run over the committed C0a blob `09702f93` by `<<<SLICE `/`<<<END ` marker LINES, printed 2 whole-text slices (PLANF021R24, RECORD24) and 54 CONTENT lines; no pair exists this round. Re-measured from that same blob: TOTAL 230 ≤ 490 (D6), PROSE 230−54 = 176 ≤ 400 (D5).
- G4 PASS — `cmp` `.agent/plan.md` against PLANF021R24 + one terminating newline exit 0; NEGATIVE CONTROL against the bare slice exit 1 (EOF after byte 2732, in line 47); last byte is a newline; `wc -l` reads EXACTLY 47, the MEASURED value the block ordered; `^## Goal$` 1, `^## Next Steps$` 1.
- G5 PASS — reader (a): the base blob is a byte-exact PREFIX and the remainder is EXACTLY one newline + RECORD24 + one newline, sha256 `ea9ca6bdae0b5f3fba246f316ac543519e4c44aacb43a93a251c5c341c711e63`, 8153 B / 8 L; the file 542933 B / 1150 L before and 551086 B / 1158 L after. Reader (b) SET-WISE, ELEMENTWISE over the whole list: 256 units → 260, RECORD24 exactly 4 units. NEGATIVE CONTROL at offset 4 of the C2 file's FIRST paragraph (`v` → `X`, equal length): BOTH readers REJECT it and BOTH accept the true file. The base blob was read with `git show` into `.remedy-wt/` scratch; no tracked file was overwritten to read an older revision.
- G6 PASS — round base → C2, line-anchored: `- R-` 220 → 221, DISTINCT at both; MAXIMUM R-0657 → R-0658; `Done: R-` 0 → 0; `Landed: ` 0 → 0; `Gate: R` keys 22 → 23, DISTINCT at both; `Gate: R24` 0 → 1. `- R-0656` occurs EXACTLY ONCE at BOTH points — the recurrence paragraph names that finding and did not mint it again.
- G7 PASS — `git diff c76f90ac..bdc242b4 -- .agent/live_review.md` has 0 deletion lines and 8 addition lines, numstat `8 0`: every changed line is an addition. The `.agent/live_review.md` blob at `a8215a65`, the commit that registered R-0656, is 542933 B / 1150 L and is a byte-exact PREFIX of the C2 file, so that entry survives exactly as written.
- G8 PASS — at C2, in the PRIMARY checkout, SERIALLY, cwd `/home/decodeux/Repos/remedy` for all three: `tests/ui_server/ tests/orchestration/test_test_runner.py tests/regression/test_resource_safety.py -q -rf` exit 0, 511 passed + 0 skipped = 511; `tests/cli/test_golden_path.py -q -rf` exit 0, 42 passed + 0 skipped = 42; `tests/ui_contracts/ -q -rf` exit 0, 469 passed + 4 skipped = 473, UNCHANGED. Neither `npx tsc --noEmit` nor `npm run test:unit` was run, as ordered.
- G9 PASS — round base → C2: 4 paths, both differences against the four non-handoff `Change:` paths EMPTY; 4 commits, every one single-parent; insertions 230, 152, 15 and 8, each under the 500 cap; `git show --numstat` per commit and `git diff --numstat` over the range agree cell by cell with the `## Commits` tables above, all 4 cells, nothing reconciled; `git ls-files .remedy-wt` 0; `git worktree list` ends with the primary checkout alone and NO worktree was created; `gh pr list --state open --json number,headRefName` → `[]`, and neither `gh pr create` nor `gh pr merge` was run. Marker sweep, line-anchored, over the two files a slice landed in (`.agent/plan.md`, `.agent/live_review.md`): 0 for each of the 2 marker prefixes this block uses, which G3's extractor counted for itself — `<<<SLICE ` and `<<<END ` — and 0 for any line starting `<<<`; `.agent/authored/f021-r24.md` and `.agent/last_block.md` read 2 and 2 BY CONSTRUCTION and are out of scope. Reflog read with `--format=%gs` and cut at the first `:`, scoped to this round's 4 rows: every OPERATION is `commit`, and `amend`, `rebase` and `cherry` each occur 0 times in that field.

## Authored-text proofs
Both whole-text slices were extracted MECHANICALLY from the committed C0a blob `09702f93` by their marker LINES, never hand-copied, and applied byte for byte; no FROM/TO pair exists this round. PLANF021R24: `cmp` exit 0 against slice + newline and exit 1 against the bare slice (G4). RECORD24: byte-exact remainder under two independent readers plus a same-length negative control both reject (G5), with 0 deleted lines in the C2 diff (G7).

## Deviations & assumptions
No departure from the ordered commit sequence: C0a, C0b, C1, C2, C3 exactly — no extra commit, none dropped, none reordered. No slice was retyped, rewrapped, reflowed or whitespace-adjusted, and no file outside the block's five `Change:` paths was written.
1. ONE GATE READING WAS NOT TAKEN AT THE ORDERED INSTANT. G1 orders `git status --porcelain` after each of C0a, C0b, C1 and C2. I printed 0 after C0b, C1 and C2, but did not run the command after C0a, and that state is no longer reachable, so I do not claim it. The nearest real evidence I did print is the C0b pre-commit self-review, whose `git status --porcelain` output was exactly one line, ` M .agent/last_block.md` — the edit I made after C0a — which leaves nothing else dirty at that point. Reported rather than reconstructed.
2. Every numeral this block predicted was met on independent measurement, so nothing had to be reported against it: constraint 7's 230 and 176, G4's 47, G6's 220 → 221 with maximum R-0657 → R-0658 and 22 → 23 `Gate: R` keys, and G8's 511, 42 and 473. No slice looked wrong and none was corrected.
Assumption: none beyond the block.
Size: this file is 74 lines, measured with `wc -l` on these final bytes. DECISION D15 declared overage against the 60-line cap: the mandated content causing it is the five per-commit changed-files tables, the item-status table, the one-line-per-gate verification block for nine gates, and the authored-text proofs — no prose padding, no transcripts, no restated procedure.

## Next
THIS SESSION IS OVER. The next session begins at docs/agents/self_drive_protocol.md Phase 1 rule 1 — the `.agent/STOP` check — BEFORE rule 2's Open PR Gate (R-0347). Rule 2 will find NO open pull request, so rule 5 applies and F021 continues on this branch. R24's OWN VERDICT IS UNRECORDED: the next round's C2 owes it. The next round is R25, THE RING ROUND — `FeedRow` gains `receivedAtMs`, `feedRowOf` takes it, and `receiveBrainFrame` threads it from the transport event R23 stamped. R25 is the FIRST round to touch the ring, whose append placement DECISION F021 D5 governs. The reviewer's standing obligation before R25 is to promote R-0656's rule into docs/agents/planner_reviewer_prompt.md §3, because a rule that lives only in a finding body is a rule the next block does not read.
