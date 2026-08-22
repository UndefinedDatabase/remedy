# Handoff — F021 R19, HALTED at C1 because gate G4 is RED

## Range
Review of `65931e3d`..`c239b75c`. Round base `65931e3d`, the R18 handback.

Fortschritt: ~87 % (T002 — Feed, NowCard, Scroll-Regel und jetzt die
             Recency-Regel stehen als reine Funktionen; es fehlen nur noch ihre
             Verdrahtung und T003) — Schaetzung
(quoted verbatim as the block orders; it describes the round as PLANNED. The
Recency-Regel did NOT land — see Deviations.)

## Item status
| Item | Status | Reason |
|---|---|---|
| C0a | done | `.agent/authored/f021-r19.md` at `9d6b087a` |
| C0b | done | `.agent/last_block.md` at `cd139caa` |
| C1 | done | `.agent/plan.md` at `c239b75c`; its own gate G4 then measured RED |
| C2 | skipped | round halted at the G4 red before the ledger append |
| C3 | skipped | round halted; no `recency.ts`, no vitest, no contract edit |
| C4 | done | this file, the halt report |

## Commits
### 9d6b087a docs(state): save the F021 R19 step block
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f021-r19.md | 457/0 | C0a, the block saved verbatim |

### cd139caa docs(state): mirror the F021 R19 block into last_block
| Path | +/- | Reason |
|---|---|---|
| .agent/last_block.md | 318/218 | C0b, written from the committed C0a blob |

### c239b75c docs(state): point the F021 plan at R19 and the recency rule
| Path | +/- | Reason |
|---|---|---|
| .agent/plan.md | 19/16 | C1, PLANF021R19 plus one terminator |

### C4 — the handoff commit, which cannot table its own SHA (R-0149)
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | rewrite | this halt report |

## External actions
`git push -u origin feature/f021-live-activity-feed` after C4. No worktree added
or removed. No `gh pr create`, no `gh pr merge`; `gh pr list --state open` EMPTY.

## Verification
- G1 GREEN — `.agent/STOP` ABSENT before C0a and before C4; branch
  `feature/f021-live-activity-feed`; `git status --porcelain` 0 lines after C0a,
  C0b and C1; base `65931e3d` single-parent, `.agent/handoff.md` alone, 41
  insertions, under the 500 cap.
- G2 GREEN — sha256 `f515556e6419bacd6f93a3dcd2c5c7797504f4d48267736e6b7fbed224e86983`,
  31368 bytes, 457 lines, EQUAL over the received bytes, `.remedy-wt/f021-r19.md`,
  `.agent/authored/f021-r19.md` at C0a and `.agent/last_block.md` at C0b.
- G3 GREEN — marker-LINE extractor over the committed C0a blob: 7 slice regions
  (5 named, the pair as FROM and TO), 14 marker lines, 187 CONTENT lines; TOTAL
  457 ≤ 490 and PROSE 457−187 = 270 ≤ 400, both equal to constraint 9.
- G4 **RED** — cmp(plan@C1, PLANF021R19+NL) exit 0; negative control vs the bare
  slice exit 1; last byte newline; `^## Goal$` 1; `^## Next Steps$` 1; but
  `wc -l` = **51** against the ordered "at most 50". G4's two clauses cannot both
  hold: PLANF021R19 is 51 lines of text, so the file its cmp clause demands is
  necessarily 51 lines. AGENTS.md's plan.md rule is "<50 lines", so the SLICE is
  the wrong side, and constraint 1 forbids fixing a slice.
- G5-G15 NOT RUN — the round halted at the G4 red before C2 and C3, per
  constraint 1 and self_drive_protocol.md guardrail G8. No number is reported for
  them because none was measured.

## Authored-text proofs
`.agent/plan.md` at `c239b75c` equals PLANF021R19 — extracted mechanically by
marker line from the committed C0a blob, never hand-copied — plus one terminator:
`cmp` exit 0, negative control exit 1. No other authored text was applied.

## Deviations & assumptions
DEVIATION, declared: the ordered sequence C0a, C0b, C1, C2, C3, C4 was truncated
to C0a, C0b, C1, C4. C2 (the RECORD19 ledger append) and C3 (`recency.ts`, its
vitest, the contract pair and append) were NOT made. Reason: G4 went RED at C1
and no honest action makes it green — trimming a line would break G4's own cmp
clause and violate constraint 1. Consequence: `.agent/plan.md` "Current Step"
describes recency work this round did not do; THIS file, not the plan, is the
authority on what landed. Nothing else deviates. Open set UNCHANGED at 216 open,
maximum R-0653, next free R-0654 — nothing registered, nothing resolved.
DECISION D15: this handoff is 96 lines against the 60-line cap. Cause: the
mandated per-commit tables, the item-status table, and the red gate G4 carrying
its own measurement and the reason it cannot be met.

## Next
THIS SESSION ENDS with C4 and the push. The next session's FIRST action is
docs/agents/self_drive_protocol.md Phase 1 rule 1, the `.agent/STOP` check,
BEFORE rule 2's Open PR Gate (R-0347); rule 2 finds NO open pull request, so
rule 5 applies and F021 continues on this branch. R19's own verdict is
UNRECORDED. Before anything else the reviewer must re-derive G4 — either
PLANF021R19 loses a line and the cmp clause is re-stated against the shorter
slice, or the ≤50 clause is withdrawn against AGENTS.md — and then re-order C2
and C3, which are unapplied: the RECORD19 ledger entry, `recency.ts` with its
vitest and its source contract. R20 still wires BOTH pure rules, recency for the
badge and the dot and scroll for the feed.
