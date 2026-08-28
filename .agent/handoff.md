# Handback — F032 R14 (T003b: the card renders its receipts)

## Session

SESSION 3 of feature F032 · round R14 · rounds so far 14

Session 3 began at R10. Session 1 was R1 through R5; session 2 was R6 through
R9. Fourteen rounds across three sessions is inside the soft limit of 25 rounds
or 7 sessions, so no limit report is owed and none is emitted.

## Range

Review of `f28640ef`..`4b6a357a` (C5, the commit writing this file, is not in
that range and cannot table its own numstat).

## State

- Feature: F032, the evidence triple. Round R14, task T003b.
- Branch: `feature/f032-evidence-triple`. Base of the round: `f28640ef`,
  confirmed by `git rev-parse HEAD` before C0a and equal to the base constraint
  8 states.
- `.agent/STOP`: ABSENT at both readings constraint 7 orders — once before C0a,
  once before C5.
- No pull request created, none merged. Open PR Gate reports `[]`.
- Open findings: 250 (unmoved; this round registered none and resolved none).
  Maximum id `R-0713`, unmoved.
- The evidence triple is now VISIBLE: a card's receipts and its honest note ride
  above the answer strip, and each answer's expected outcome and downside ride
  under the answer they belong to. A ref's `target` is rendered nowhere.

## Commits

### 527d236d chore(agent): save the R14 step block
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/authored/f032-r14.md` | +306 / -0 | C0a, the byte-preserving copy of the block |

### 1e31d4fa chore(agent): mirror the R14 block into last_block
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/last_block.md` | +226 / -241 | C0b, the same bytes over the previous round's block |

### 83df7d73 docs(agent): point the plan at the R14 card round
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/plan.md` | +21 / -23 | C1, slice PLANF032R14 applied whole |

### d29f0cbe docs(agent): book the R13 verdict in the review record
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/live_review.md` | +2 / -0 | C2, slice LEDGER14 appended; the only commit touching the record |

### 07b52260 feat(ui): the decision card renders its receipts and each answer's stakes
| Path | +/- | Reason |
|------|-----|--------|
| `apps/ui/src/components/panels/DecisionInboxCard.tsx` | +64 / -0 | C3, S2/S3/S5: the receipts strip, the note, the per-answer outcome and downside, one new label constant |
| `apps/ui/src/components/panels/RightLivePanel.module.css` | +69 / -0 | C3, S4: the rules for all five new classes and their `:empty` collapses |

### 4b6a357a test(ui): pin the rendered evidence triple and the target that is not shown
| Path | +/- | Reason |
|------|-----|--------|
| `tests/ui_contracts/test_decision_answer_wiring.py` | +125 / -0 | C4, S6: `TestTheCardShowsTheEvidenceTriple`, 8 guards |

### C5 (this commit) docs(agent): hand back F032 R14
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/handoff.md` | not tabled | C5 writes this file, so it cannot read its own `git diff --numstat`; every other commit's `+/-` above is one `git diff --numstat` reading compared cell by cell against G8's |

## Item status

| Item | Status | Reason |
|------|--------|--------|
| C0a save this block | done | |
| C0b mirror into last_block | done | same bytes, same git blob |
| C1 the plan | done | |
| C2 the R13 verdict | done | |
| C3 the component and its styles | done | one commit, both files |
| C4 the contract guards | done | |
| C5 the handback | done | this file |
| S1 read the four existing guards first | done | all four re-measured at C3, see G6 |
| S2 receipts above the answer strip | deviated | one `span` per ref showing its `label`, the note in its own `p`, both unconditional — plus a `role="group"` and a label the item does not list; see deviation 2 |
| S3 outcome and downside under their answer | done | two `p` elements after the outcome paragraph, no operator, no `aria-live` |
| S4 the styles and the `:empty` collapses | deviated | a FOURTH `:empty` rule beyond the three named; see deviation 1 |
| S5 labels are module constants | done | the one label introduced is `DECISION_EVIDENCE_LABEL`, declared beside the file's existing constants |
| S6 the new guards | done | 8 tests in a class of their own; the region reader is REUSED, not re-written |
| S7 nothing else changes | done | `apps/ui/src/api/` untouched; send flow, in-flight set, jump chip, clarification form and outcome paragraph unchanged |

## External actions

- `git worktree add --detach .remedy-wt/f032-r14-mut 4b6a357a` — created for G7.
- `git worktree remove .remedy-wt/f032-r14-mut` then `git worktree prune` —
  removed; `git worktree list` is back to 1 line.
- `gh pr list --state open --json number,headRefName,baseRefName,isDraft` — `[]`.
  Nothing merged, nothing created.
- `git push -u origin feature/f032-evidence-triple` after C5 (see Next).

## Verification

- G1 HYGIENE, BASE, SENTINEL. `git rev-parse HEAD` before C0a →
  `f28640ef6f5056e7bc587148968f7b88bfbdb5a1`, which IS constraint 8's base.
  `git rev-parse --abbrev-ref HEAD` → `feature/f032-evidence-triple`.
  `git status --porcelain | wc -l` after each of C0a, C0b, C1, C2, C3, C4 → `0`,
  `0`, `0`, `0`, `0`, `0`. `.agent/STOP`: `ls -la .agent/STOP` before C0a → exit
  2, `ls: cannot access '.agent/STOP': No such file or directory`; the same
  command before C5 → the same exit 2 and the same line. ABSENT at both.
- G2 TRANSPORT. `sha256`, bytes and lines, all three
  `ab8e552d5733df15bb7fb17f4d2183ef077803649b81180459dbdc26521c23de`, `25057`,
  `306`: `.remedy-wt/f032-r14.md`, the committed `527d236d:.agent/authored/f032-r14.md`
  blob and the committed `1e31d4fa:.agent/last_block.md` blob. ALL THREE EQUAL:
  `True`. `git rev-parse` gives both committed paths blob
  `16367574f3dcd28d5bca0f6f87bb7732871e1d25` — the SAME blob. This proves the
  reviewer's scratch original, the saved copy and the mirror agree with one
  another on disk. It says NOTHING about the bytes of any prompt, and no claim
  about a prompt is made anywhere in this handback.
- G3 EXTRACTION AND CAPS, measured on the COMMITTED C0a blob: `PLANF032R14` 46
  content lines, `LEDGER14` 1 content line; regions `2`; CONTENT total `47`;
  TOTAL `306`; PROSE = 306 − 47 = `259`. PROSE under 400: `True`. TOTAL under
  490: `True`.
- G4 THE PLAN, at `83df7d73`. Byte-equal to slice `PLANF032R14` under constraint
  2: `True`. NEGATIVE CONTROL, the same comparison with the trailing newline
  removed: `False`. `wc -l` → `46`, under 50: `True`. `^## Goal$` → `1`.
  `^## Next Steps$` → `1`.
- G5 THE LEDGER APPEND, at `d29f0cbe`, read with `git show
  f28640ef:.agent/live_review.md` (the tracked file was never overwritten to get
  it). READER 1, byte identity against base + one newline + the slice + one
  newline: `True`; arithmetic, the three numbers summing to the result,
  `1091935 + 1 + 4513 = 1096449` (the third being the slice's 4512 bytes plus
  its one trailing newline); the base blob IS a byte PREFIX: `True`. Base measured at `f28640ef`:
  `1091935` bytes over `430` blank-line units, matching the reviewer's numbers.
  READER 2, structural: N = `1` paragraph in the slice, the LAST 1 blank-line
  unit matches it IN ORDER: `True`. NEGATIVE CONTROL, one byte flipped in memory
  inside the FIRST appended paragraph: reader 1 rejects `True`, reader 2 rejects
  `True`. Counts before → after C2: `^Gate: F\d+ R\d+ — ` 65 → 66; `^- R-\d+ — `
  274 → 274; `^Done: R-\d+ — ` 24 → 24; `^Landed: R-` 1 → 1; `^Gate: R\d+ — ` 19
  → 19. Open set 250 → 250. Maximum id `R-0713` → `R-0713`. Gate keys ADDED:
  `['Gate: F032 R13 — ']`. Ids ADDED to the resolved set: `[]`.
- G6 TYPECHECK AND THE FOUR TEXT READINGS. From `apps/ui`: `npx tsc --noEmit`
  produced NO output; re-run as `npx tsc --noEmit && echo "TSC EXIT 0 WITH NO
  OUTPUT ABOVE"` it printed only that marker, so exit 0 with no output — the
  same reading the reviewer took at the base, and nothing in it is this round's.
  (The `&&` marker is used because this session's bash guard refuses `$?`.) Over
  `DecisionInboxCard.tsx` at C3, comments stripped by the module's own
  `strip_ts_comments`: count of `hidden` → `0`; the LAST `aria-live="polite"` is
  opened by a `<p` tag → `True`; the exact text
  `jsx_between_answer_button_and_live_paragraph` returns →
  `'\n                        ) : (\n                          <code className={styles.decisionAnswerText}>{answer.value}</code>\n                        )}\n                        {}\n                        '`
  with `?` → 0, `&&` → 0, `||` → 0; `setSendingKeys(` → `2`;
  `clarification.defaultAnswer` → `1`; `.target` → `1`, and the line carrying it
  is `const typed = event.target.value;`, the clarification input's DOM event
  target. No ref's target reached the markup.
- G7 THE GUARDS, GREEN THEN RED. At C4:
  `python3 -m pytest tests/ui_contracts/test_decision_answer_wiring.py -q` → exit
  0 (`&&`-chained marker `PYTEST EXIT 0` printed), `49 passed in 0.29s`.
  `python3 -m pytest tests/ui_contracts/ -q` → exit 0, `574 passed, 4 skipped in
  5.41s`; the reviewer measured `566 passed, 4 skipped` at the base, so passed
  GREW by 8 (the 8 new guards) and skipped did not move. In the disposable
  worktree `git worktree add --detach .remedy-wt/f032-r14-mut 4b6a357a`, one
  test file per run:
  - CONTROL before any mutation → exit 0, `49 passed in 0.30s`, `^FAILED` 0.
  - (a) render of `answer.downside` deleted. FILE
    `apps/ui/src/components/panels/DecisionInboxCard.tsx`; exact byte string
    occurrences in that file before applying: `1`. → exit 1, `3 failed, 46
    passed in 0.30s`, `^FAILED` 3:
    `test_each_answer_shows_its_own_expected_outcome_and_downside`,
    `test_every_receipt_class_the_card_names_has_a_rule_of_its_own`,
    `test_the_answer_stakes_sit_after_the_live_region_and_add_no_operator`.
  - (b) a ref's `target` rendered beside its label. FILE
    `apps/ui/src/components/panels/DecisionInboxCard.tsx`; occurrences before
    applying: `1`. → exit 1, `1 failed, 48 passed in 0.29s`, `^FAILED` 1:
    `test_no_refs_target_ever_reaches_the_markup`.
  - (c) the `:empty` collapse rule replaced by `display: none`. FILE
    `apps/ui/src/components/panels/RightLivePanel.module.css`; occurrences
    before applying: `1`. → exit 1, `2 failed, 47 passed in 0.29s`, `^FAILED` 2:
    `test_every_new_empty_state_is_collapsed_out_of_flow`,
    `test_the_new_collapse_rules_never_remove_the_node`.
  - CONTROL after all three restorations → exit 0, `49 passed in 0.28s`,
    `^FAILED` 0, and the worktree's `git status --porcelain` 0 lines (it was 0
    after each individual restoration too). Worktree removed and pruned.
- G8 STRUCTURE, CANARY, PR GATE. `python3 -m pytest tests/cli/test_golden_path.py
  -q` → exit 0, `42 passed in 20.69s`. `git diff --name-only f28640ef..4b6a357a`
  → exactly the 7 paths the Change set lists other than `.agent/handoff.md`;
  both residues EMPTY (`[]` and `[]`). `git diff --stat f28640ef..4b6a357a --
  packages/` EMPTY, the same for `-- docs/` EMPTY, `git diff --name-only
  f28640ef..4b6a357a -- apps/ui/src/api/` EMPTY. Insertions per commit, each
  single-parent and each under 500: `527d236d` +306, `1e31d4fa` +226,
  `83df7d73` +21, `d29f0cbe` +2, `07b52260` +133, `4b6a357a` +125 — these are
  the same `git diff --numstat` reading as the `## Commits` column above,
  compared cell by cell, and they agree. `^<<<SLICE ` and `^<<<END ` counts:
  `.agent/plan.md` 0/0, `.agent/live_review.md` 0/0, `DecisionInboxCard.tsx`
  0/0, `RightLivePanel.module.css` 0/0,
  `tests/ui_contracts/test_decision_answer_wiring.py` 0/0, against a CONTROL
  over the committed C0a blob of 2/2. `git ls-files .remedy-wt` 0 lines, `git
  worktree list` 1 line, `git branch --list "tmp/*"` 0 lines. `gh pr list
  --state open --json number,headRefName,baseRefName,isDraft` → `[]`.

## Authored-text proofs

Two reviewer-authored texts were applied, and neither was retyped: both were
extracted programmatically from the COMMITTED C0a blob and written under
constraint 2's convention.

- `PLANF032R14` → `.agent/plan.md` at `83df7d73`: byte-equal `True`, negative
  control (trailing newline removed) `False`. See G4.
- `LEDGER14` → `.agent/live_review.md` at `d29f0cbe`: byte identity `True`,
  base a byte prefix `True`, structural reader `True`, both readers rejecting a
  flipped byte. See G5.
- The block itself: `.remedy-wt/f032-r14.md`, `.agent/authored/f032-r14.md` and
  `.agent/last_block.md` are one sha256 and one git blob. See G2.

## The design reference

This is the first F032 round `docs/ui/design_reference/ux_spec.md` binds, and
three of its rules governed real choices:

- §17 (copy rules) decided the whole shape of S2. The default UI never shows raw
  UUIDs or present/missing signals, so a chip carries the ref's already-scrubbed
  `label` and nothing else, a ref's `target` appears in no text and no attribute
  a browser shows, and the note is the model's prose rather than the raw
  `evidence_status`. The new guard `test_no_refs_target_ever_reaches_the_markup`
  is that rule made mechanical.
- §14 (states) decided the downside's styling: it is NOT told by colour alone —
  it carries a left rule as well as the warn tint, so an operator who cannot
  separate the two hues still reads two differently marked lines.
- §4/§5 by way of this card's own established scale: the receipt chips reuse the
  `.decisionChip` scale rather than inventing a second chip shape inside one
  card, and every value resolves to a `--remedy-*` property
  `apps/ui/src/styles/tokens.css` already defines (R-0661).

NO VISUAL DEVIATION WAS TAKEN. Nothing in this round departs from the canonical
reference, so the assumption_log gains no visual entry.

## Deviations & assumptions

1. S4 names three empty states to collapse — the receipt note, the expected
   outcome and the downside. A FOURTH `:empty` rule was added, for
   `.decisionEvidence`, the receipt strip itself. Reason: `.decisionRow` is a
   column flex box with an 8px `gap`, so an empty strip still claims a gap and
   would show as a stray blank band on every card carrying no receipts. It uses
   the SAME out-of-flow mechanism S4 mandates (`position: absolute`), never
   `display: none` or `visibility: hidden`, and the new guards read all four
   selectors as one set.
2. S2 does not ask for a label on the receipts strip; S5 rules how one must be
   written if introduced. One WAS introduced: `DECISION_EVIDENCE_LABEL = "What
   this decision is based on"`, a module-level constant beside the file's
   existing ones, carried on a `role="group"` rather than a bare `div` because
   an `aria-label` on a `generic` role is computed and dropped (finding R-0682,
   the same reason the filter row above carries one). Without it the chips reach
   a screen-reader user as bare words with no context. It names no status, no
   schema key and no field name.
3. G7's restoration step: this session's sandbox refuses `git checkout -- <path>`
   inside the worktree, so each mutated file was restored by writing back the
   bytes of `git -C <worktree> show HEAD:<path>` — a byte-for-byte restore of the
   committed blob, verified by the worktree's `git status --porcelain` reporting
   0 lines after EACH restoration and after the final control run.
4. Mutation (a) reddened THREE tests rather than one. That is not a deviation
   from the block, which orders the count to be reported rather than predicted;
   it is reported above. Deleting the downside paragraph removes the class the
   stylesheet guard looks for and makes the source-order guard's `index` lookup
   raise, so three of the eight guards see it.
5. `npx tsc --noEmit`, the pytest runs and the mutation runs were chained with
   `&& echo …` markers to surface their exit codes, because this session's bash
   guard refuses `$?`. The commands themselves are exactly the ones the block
   ordered.
6. Constraint 10 is noted and nothing was corrected by a commit of its own: no
   numeral in the R13 handback was found false this round.

## Next

1. Phase 1 rule 1 of `docs/agents/self_drive_protocol.md`: re-read `.agent/STOP`
   FROM DISK before anything else.
2. The Open PR Gate: `gh pr list --state open --json
   number,headRefName,baseRefName,isDraft`.
3. T003c: the receipt chips become deep links into the evidence panel — the
   slice that finally uses the `target` this round deliberately does not render.
