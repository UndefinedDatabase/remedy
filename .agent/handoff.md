# F021 R36 handback — record R35, settle the tooltip, ship the disabled steering input

Fortschritt: ~100 % der Bauarbeit (jedes Teil von T001 bis T003 ist gebaut; es
             folgen nur noch Integrations-, Evidenz- und STATUS-Runde)
             — Schaetzung

## Range
Review of 78c72880ccfcdfbff0c39e9e65d7a8a4380ab558..HEAD — round base `78c72880`,
branch `feature/f021-live-activity-feed`. Open findings 223, by
`planner_reviewer_prompt.md` §3 item 10 — canonical `^- R-\d+ — ` 224 minus
`^Done: R-\d+ — ` 1 — measured at C2 `020ec7d1`. No id minted, none resolved.

## Item status
| Item | Status | Reason |
|---|---|---|
| C0a `6e7a8d0b` | done | |
| C0b `6cf2e62a` | done | |
| C1 `74296cab` | done | |
| C2 `020ec7d1` | done | |
| C3 `76299df3` | done | DECISION F021 D11, landed BEFORE the code citing it |
| C4 `c08e68c5` | done | CHATINPUT plus five pair halves, three files, one commit |
| C5 `c56b9727` | done | CHATCONSTPAIR plus CONTRACTSLICE36 |
| C6 (this file) | done | its own SHA is unnameable from inside it |

## Commits

### 6e7a8d0b chore(agent): save the F021 R36 step block
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f021-r36.md | +448/-0 | the block saved verbatim (C0a) |

### 6cf2e62a chore(agent): mirror the R36 block into last_block
| Path | +/- | Reason |
|---|---|---|
| .agent/last_block.md | +377/-328 | written FROM the committed C0a blob (C0b) |

### 74296cab docs(state): point the F021 plan at R36, the steering-input round
| Path | +/- | Reason |
|---|---|---|
| .agent/plan.md | +16/-20 | PLANF021R36 whole-file write (C1) |

### 020ec7d1 docs(review): record the R35 PASS and two reviewer defects in its own block
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +6/-0 | RECORD36 appended, ONE blank line at the join (C2) |

### 76299df3 docs(decisions): record F021 D11, which tooltip wording ships and why
| Path | +/- | Reason |
|---|---|---|
| .agent/decisions.md | +10/-0 | DECISIOND11 appended, ONE blank line at the join (C3) |

### c08e68c5 feat(ui): the steering input ships visible, disabled and honest
| Path | +/- | Reason |
|---|---|---|
| apps/ui/src/components/panels/ChatInput.tsx | +47/-0 | NEW, CHATINPUT plus one newline (C4) |
| apps/ui/src/components/panels/ActivityFeedCard.tsx | +9/-0 | CHATIMPORT, REASON, LIVEBRANCH, FALLBACKBRANCH pairs, in that order (C4) |
| apps/ui/src/components/panels/RightLivePanel.module.css | +13/-0 | CHATCSSPAIR, append-shaped (C4) |

### c56b9727 test(ui-contracts): pin the disabled steering input in both branches
| Path | +/- | Reason |
|---|---|---|
| tests/ui_contracts/test_brain_stream_ring.py | +47/-0 | CHATCONSTPAIR then CONTRACTSLICE36, TWO blank lines at the join (C5) |

### C6 docs(state): hand back F021 R36 — SHA unnameable: this is the commit that writes this file
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | owed to R37 | the handback itself (C6) |

## External actions
`git push -u origin feature/f021-live-activity-feed` after C6. `gh pr list --state
open --json number,headRefName,baseRefName,isDraft` exit 0, output `[]`; no `gh pr
create`, no `gh pr merge`. TWO worktrees, each added and removed:
`.remedy-wt/g6` at `c56b9727` for G6, and `.remedy-wt/base` at `78c72880` to
re-measure a base figure (Deviation 1).

## Verification — one line per gate, transcripts in the round report (R-0582)
G1 `.agent/STOP` ABSENT before C0a and again before C6; branch `feature/f021-live-activity-feed`; `git status --porcelain` 0 lines after each of C0a, C0b, C1, C2, C3, C4, C5.
G2 sha256 `3fff7dabfd6d9d060b649f81d899817a5364d0813bfc9839de655e90f615f908`, 32143 bytes, 448 lines — EQUAL over the bytes I read, `.remedy-wt/f021-r36.md`, `.agent/authored/f021-r36.md` at C0a and `.agent/last_block.md` at C0b. My extractor printed 5 whole texts, 6 pairs, 193 CONTENT lines, 28 marker lines; TOTAL 448 against 490, PROSE 255 against 400 — both re-measured from that blob, both matching constraint 13.
G3 `cmp` plan.md vs PLANF021R36+newline exit 0; NEGATIVE CONTROL vs the bare slice exit 1; last byte `0a`; `^## Goal$` 1, `^## Next Steps$` 1; `wc -l` 43, under 50.
G4 LIVEBRANCHPAIR and FALLBACKBRANCHPAIR each FROM 1x at base, 0x at C4. CHATIMPORTPAIR, REASONPAIR, CHATCSSPAIR append-shaped, 1x at base and 1x at C4; CHATCONSTPAIR 1x at base and 1x at C5. My script printed all six shapes; the four append-shaped ones are the four whose TO opens with its own FROM. REPLAY: base blob plus that file's own transformation reproduces the committed blob BYTE FOR BYTE for all three files. `git cat-file -e 78c72880:…/ChatInput.tsx` exit 128, `Not a valid object name`; `cmp` committed vs CHATINPUT+newline exit 0, vs the bare slice exit 1. `<ChatInput disabled` in the CARD 0 then 2; `.chatInput` in the CSS 0 then 4.
G5 canonical `^- R-\d+ — ` 224→224, ALL DISTINCT at both, max R-0661 at both; loose `^- R-` 225→225, gap 1 at both; `^Done: R-` 1→1; `^Gate: R` 34→35, DISTINCT at both; `^Gate: R36` 0→1; `^Recurrence: ` 11→13; `^Recurrence: R-0439 — ` 0→1; `^Recurrence: R-0402 — ` 1→2; `^- R-0439 — ` and `^- R-0402 — ` 1→1 each. RECORD36 paragraphs opening `- R-` = 0 of 3. `.agent/decisions.md` `^## DECISION ` 117→118, `F021 D11` 0→1, `F021 D10` 1→1. BOTH base blobs byte-exact PREFIXES; remainders EXACTLY one newline + slice + one newline, 5158 and 2069 bytes, measured equal to predicted.
G6 RED-PROOF in `.remedy-wt/g6` at C5, the FALLBACK branch's `<ChatInput …/>` line deleted whole-line, the live branch's copy left: `1 failed, 66 passed`, the sole failure `tests/ui_contracts/test_brain_stream_ring.py::TestTheSteeringInputIsHonestlyDisabled::test_the_card_renders_it`, the node id the gate names. Worktree removed; `git status --porcelain` 0 lines; `git worktree list` the primary checkout ALONE.
G7 SERIAL, PRIMARY checkout: `tests/ui_contracts/` exit 0, 495 passed 4 skipped = 499, against 490+4 = 494 at the base, difference +5, exactly CONTRACTSLICE36's five tests. `npm run test:unit` in `apps/ui` exit 0, 16 files and 218 tests — UNCHANGED from the base, as ordered. `npx tsc --noEmit` in `apps/ui` exit 0, EMPTY stdout and stderr; per constraint 11 this was its FIRST honest execution, run BEFORE committing C4 and again after C5, exit 0 both times. FOUR state readers exit 0, 528 passed. Canary `tests/cli/test_golden_path.py` exit 0, 42 passed. `python3 -m ruff check tests/ui_contracts/test_brain_stream_ring.py` exit 0. `npm run lint` neither run nor reported (constraint 9).
G8 `git diff --name-only 78c72880..HEAD` at C5: I COUNT NINE paths, equal to the NINE non-handoff `Change:` paths with BOTH set differences EMPTY. At C6 I COUNT TEN, those nine plus `.agent/handoff.md`, both differences EMPTY again. 8 commits at C6, 7 at C5, every one single-parent; `git show --numstat` and `git diff --numstat` agree cell by cell on all seven measurable commits; insertions 448, 377, 16, 6, 10, 69, 47 and C6's own, each under 500. Marker sweep LINE-ANCHORED 0 for each of `<<<SLICE `, `<<<END `, `<<<FROM `, `<<<TO ` over all six named files. UNANCHORED `<<<` 0 over each of the three `apps/` files and the contract file. Reflog BY OPERATION: all seven of this round's rows are `commit`, `amend`/`rebase`/`cherry` 0 each in that field. `gh pr list --state open` printed `[]`.

## Authored-text proofs
All eleven texts — five slices and six pairs — were extracted BY MARKER LINE from
the COMMITTED C0a blob `6e7a8d0b:.agent/authored/f021-r36.md`, never retyped.
`plan.md` and `ChatInput.tsx`: `cmp` exit 0 against slice + one newline, exit 1
against the bare slice. `live_review.md`, `decisions.md` and
`test_brain_stream_ring.py`: each base blob a byte-exact PREFIX, remainders
EXACTLY one, one and two newlines plus the slice plus one terminator. Each pair's
FROM was asserted present EXACTLY once in the ONE file the `Change:` list names
for it, immediately before its replacement, by a script that refuses any other
count. REPLAY PROOF: re-applying each file's own pairs to its BASE blob in
constraint 10's order reproduces all three committed blobs BYTE FOR BYTE.

## Deviations & assumptions
None repaired; constraint 1 forbids editing reviewer text, so each is declared.
1. A SECOND worktree beyond constraint 9's "ONE worktree … for G6's red-proof
   alone": `.remedy-wt/base` at `78c72880`, used ONLY to re-measure the base
   figure G7 states rather than accept it. It printed 62 passed for
   `test_brain_stream_ring.py`, against 67 at C5, confirming +5 independently of
   the suite reading. Added and removed sequentially, never concurrently with
   another pytest; the tree is clean and `git worktree list` names the primary
   checkout alone.
2. G6's mutation target needed BOTH readings R-0629 orders. The gate quotes
   `      <ChatInput disabled reason={STEERING_DISABLED_REASON} />` at SIX
   spaces, which is a SUBSTRING of the live branch's EIGHT-space copy, so a
   naive substring count reads 2 and my first applier refused. Measured
   whole-line the 6-space form is UNIQUE (1 occurrence, line 180), and
   indent-agnostic there are 2 — the two branches. I deleted by whole-line
   index and confirmed the line below is the fallback's `    </section>` and
   that the live copy survived. The gate's prose identifies it unambiguously;
   only a substring count would have.
3. The `tsc` gate, which constraint 11 could not dry-run, is GREEN: exit 0 with
   empty stdout and stderr, at C4 and again at C5. No repair was needed.
4. Constraint 12's settled wording shipped verbatim and unmerged. I re-read both
   sources: `ux_spec.md` line 112 carries the sentence, and `T5_F021.md` line 65
   carries the paraphrase line-wrapped, so D11 quotes both faithfully.
5. No departure from the ordered commit sequence: exactly C0a, C0b, C1, C2, C3,
   C4, C5, C6 — none extra, dropped or reordered. No finding id minted or
   resolved.
6. DECISION D15, size: 137 lines, over the ≤100 tier this round's eight commit
   tables earn. Mandated cause: eight commit tables, eight gate lines, the
   item-status table, the authored-text section and six deviations, two of which
   must evidence a measurement the gate's own wording could not settle. No
   section was dropped and no transcript is restated here.

## Next
R36's OWN VERDICT IS UNRECORDED and the next round's ledger commit owes it, with
the three readings C6 cannot state about itself: C6's SHA, its insertion count
and its `wc -l`. Every item of T001, T002 and T003 is now built, so the next
action is the INTEGRATION-GATE round — the whole suite at the branch tip and the
feature file's Goal & Done read clause by clause against what is on disk — then
the evidence round and the STATUS-commit round. The next session's first action
is Phase 1 rule 1, re-reading `.agent/STOP` from disk, before rule 2.
