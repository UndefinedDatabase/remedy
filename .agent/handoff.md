# Handback — F009 R31 (session close)

Fortschritt: ~99 % (T001 gebaut · T002 gebaut · T003 gebaut und verifiziert ·
             Integrations-Gate BESTANDEN; offen bleiben nur die zwei
             Closure-Runden: Evidenz und Zip, dann STATUS-Zeile und PR) —
             Schätzung

## Range
Review of 002e0e83d57bad21fd88a24880a5a0e9e2552e70..HEAD; that SHA is the round base.

## Commits
### a4d92d41 docs(state): save the F009 R31 step block as authored text
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f009-r31.md | +242/-0 | C0a, transport copy of the block |

### 192f3dc2 docs(state): mirror the F009 R31 block into last_block
| Path | +/- | Reason |
|---|---|---|
| .agent/last_block.md | +179/-240 | C0b, from the committed C0a blob |

### b4149410 docs(state): point the F009 plan at the session close
| Path | +/- | Reason |
|---|---|---|
| .agent/plan.md | +12/-12 | C1, PLANF009R31 in full |

### 6cae6a53 docs(review): record the R30 verdict as PASS
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +2/-0 | C2, LEDGER31 appended at the round base |

### 896f0312 and C4, grouped (a handoff cannot table the commit that writes it)
| Path | +/- | Reason |
|---|---|---|
| .agent/candidates.md | +46/-10 | C3 896f0312, CANDIDATES in full; NON-EMPTY |
| .agent/handoff.md | round report | C4, this commit; item 14 keeps its numstat there |

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
`git push -u origin feature/f009-single-write-channel` after C4. No PR created —
F009 opens one at its own closure. No other `gh` call, no worktree add/remove.

## Verification
One line per gate; the raw transcripts are in the round report (R-0582).
- G1 PASS. `.agent/STOP` ABSENT before C0a and again before C4; branch
  `feature/f009-single-write-channel`; `git status --porcelain` 0 lines after each
  of C0a, C0b, C1, C2, C3.
- G2 PASS. Emitted bytes, C0a blob and C0b file all sha256 `55e0ca46…` over 20989
  bytes and 242 lines; C0b came from the committed C0a blob.
- G3 PASS. 3 slices extracted from the C0a blob by marker line, 89 CONTENT lines
  summed; TOTAL 242 and PROSE 153, both agreeing with constraint 7.
- G4 PASS. `cmp` exit 0 for plan-at-C1 vs PLANF009R31 and candidates-at-C3 vs
  CANDIDATES, both negative controls exit 1; plan 40 lines against the 50 cap,
  `^## Goal$` 1 and `^## Next Steps$` 1.
- G5 PASS. Both readers ACCEPT the true file and both REJECT an equal-length
  printable-byte flip in the FIRST appended paragraph; N counted at 1; 571277 to
  576883 bytes and 1136 to 1138 lines.
- G6 PASS. Base: entries 211 all DISTINCT, `Done:` 3, `Landed: ` 0, `Gate: R` keys
  30 over 30 DISTINCT, `Gate: R31` 0, max REGISTERED id R-0645, open 208 by
  DECISION F009 D10. At C2: entries UNCHANGED at 211 all DISTINCT, max R-0645,
  open 208, `Gate: R31` 1 — nothing was minted.
- G7 PASS. base→C3 lists exactly the 5 declared paths, set difference EMPTY both
  ways, 0 under `packages/`, `apps/`, `docs/`, `tests/`; every commit ONE parent;
  `git show --numstat` and `git diff --numstat` agree on every cell and each equals
  the tables above; insertions 242, 179, 12, 2, 46, each under 500; leading marker
  LINES 0 in all three slice targets; `git ls-files .remedy-wt` 0; this round's 5
  reflog rows all `commit`, amend/rebase/cherry each 0, no total over the reflog.
- G8 PASS. `python3 -m pytest tests/cli/test_golden_path.py -q -rf`, primary
  checkout, serial, no other pytest alive: exit 0, 42 passed.
- G9 PASS. This file; its `wc -l` against the 100-line cap is in the round report.

## Authored-text proofs
`.agent/authored/f009-r31.md` at a4d92d41, `.agent/last_block.md` at 192f3dc2 and
the reviewer's emitted bytes still on disk at `.remedy-wt/f009-r31.md` are all
sha256 55e0ca46a24cda5cc3b26488547b9991e852495a6988ed55904be33f5ac33d1e over 20989
bytes and 242 lines. Every slice came out of the COMMITTED C0a blob by its marker
lines and was applied by script; none was hand-transcribed.

## Deviations & assumptions
None. The sequence C0a, C0b, C1, C2, C3, C4 was followed exactly — no commit extra,
dropped or reordered. No id minted, nothing resolved (constraint 3); next id R-0646.

## Next
1. The next session's FIRST action is Phase 1 rule 1 — re-read `.agent/STOP` from
   disk — BEFORE rule 2. Phase 0 is one-shot; that re-read is not.
2. `.agent/candidates.md` is NON-EMPTY: two entries, both reviewer-block defects
   surfaced at R30. They are a BLOCK CONDITION which the FIRST reviewed round of
   the next session must register (next free id R-0646) or resolve inline as a
   planner_reviewer_prompt.md §4.7 DECISION, emptying the file that same round.
3. The R31 verdict is UNWRITTEN by construction: the SESSION ended, not the branch
   (R-0583). The next reviewer writes it from this handback and the range above.
