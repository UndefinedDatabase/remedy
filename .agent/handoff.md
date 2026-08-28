# Handback — F032 Approval with the evidence triple, round R15

## Session

SESSION 4 of feature F032 · round R15 · rounds so far 15
(R1–R5 session 1, R6–R9 session 2, R10–R14 session 3, R15 opens session 4.)

STEP T003c — the receipt chip becomes the evidence entry point. T003 is closed
by ruling its deep link: the evidence panel belongs to F023, which is unclaimed,
so F032 ships the ENTRY POINT F023 wires. Recorded as DECISION F032 D8 and as
amendment A7 in `docs/roadmap/features/T5_F032.md`.

## Range

Review of `a4a24663eb3d99bdc9507d1877ba9e623462d598`..`8569e717` (C0a–C5;
C6 writes this file and cannot table itself).

Branch: `feature/f032-evidence-triple`. Base: `a4a24663`, the R14 handback.

## Commits

### 7aeba650 docs(agent): save the F032 R15 block as authored
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f032-r15.md` | +488/-0 | C0a — the block saved verbatim |

### 8891317d docs(agent): mirror the R15 block into last_block
| Path | +/- | Reason |
|---|---|---|
| `.agent/last_block.md` | +464/-282 | C0b — same bytes, extracted from the committed C0a blob |

### 3d15fd16 docs(agent): point the plan at the R15 entry-point round
| Path | +/- | Reason |
|---|---|---|
| `.agent/plan.md` | +21/-22 | C1 — slice PLANF032R15 applied whole |

### 4af8405e docs(agent): book the R14 verdict in the review record
| Path | +/- | Reason |
|---|---|---|
| `.agent/live_review.md` | +2/-0 | C2 — slice LEDGER15 appended (the R14 PASS) |

### 112d9922 docs(agent): rule the receipt chip an entry point F023 wires
| Path | +/- | Reason |
|---|---|---|
| `.agent/decisions.md` | +66/-0 | C3 — slice DECISION8 appended |
| `docs/roadmap/features/T5_F032.md` | +17/-0 | C3 — slice AMEND7 appended |

### 24592a1b feat(ui): a receipt becomes a control when a handler exists to take it
| Path | +/- | Reason |
|---|---|---|
| `apps/ui/src/components/panels/DecisionInboxCard.tsx` | +38/-7 | C4 — S2 the optional prop and its type import, S3 the two receipt arms |
| `apps/ui/src/components/panels/RightLivePanel.module.css` | +27/-0 | C4 — S5 the button chrome, hover and focus ring, scoped to `button.` |

### 8569e717 test(ui): pin the receipt entry point and the chip that stays inert
| Path | +/- | Reason |
|---|---|---|
| `tests/ui_contracts/test_decision_answer_wiring.py` | +126/-0 | C5 — S7, class `TestTheReceiptIsAnEntryPointRatherThanALink`, six tests |

### C6 (this commit) docs(agent): hand back F032 R15
| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | — | C6 — a handoff cannot table the commit that writes it (R-0149 pattern) |

## External actions

- `git worktree add --detach .remedy-wt/f032-r15-mut 8569e717` — created, used for G7's three mutations, then `git worktree remove` + `git worktree prune`; `git worktree list` back to one line.
- `gh pr list --state open --json number,headRefName,baseRefName,isDraft` — `[]`.
- `git push -u origin feature/f032-evidence-triple` after C6.
- No pull request was created. Nothing was merged.

## Verification

- **G1 HYGIENE, BASE, SENTINEL** — `git rev-parse HEAD` before C0a = `a4a24663eb3d99bdc9507d1877ba9e623462d598`, equal to the base this block names; `git rev-parse --abbrev-ref HEAD` = `feature/f032-evidence-triple`; `git status --porcelain | wc -l` = `0` after each of C0a, C0b, C1, C2, C3, C4, C5; `ls -la .agent/STOP` before C0a and again before C6 both printed `ls: cannot access '.agent/STOP': No such file or directory` (exit 2), so no sentinel exists.
- **G2 TRANSPORT** — `sha256sum` = `43605b6b924f123c59415e36f390bb4701644a0f8ab27b2751653ae7be5c9991` over all three of `.remedy-wt/f032-r15.md` (33459 bytes, 488 lines), `.agent/authored/f032-r15.md` at C0a and `.agent/last_block.md` at C0b; the two committed paths are ONE git blob, `c365552eb6019179032ee5a61345acf4a5e24f93`. The chain covers the scratch original, the saved copy and the mirror; no claim is made about any prompt's bytes.
- **G3 EXTRACTION AND CAPS** (on the committed C0a blob) — 4 regions: PLANF032R15 45, LEDGER15 1, DECISION8 65, AMEND7 16 content lines; CONTENT 127; TOTAL 488 (< 490); PROSE = 488 − 127 = 361 (< 400).
- **G4 THE PLAN, at C1** — `.agent/plan.md` byte-equal to slice PLANF032R15 extracted from the committed C0a blob: `True`. NEGATIVE CONTROL, same comparison with the slice's trailing newline removed: `False`. `wc -l` = 45 (< 50). `^## Goal$` = 1, `^## Next Steps$` = 1.
- **G5 THE THREE APPENDS** — each read with `git show <sha>:<path>`, no tracked file overwritten. `.agent/live_review.md` at C2: reader (a) `True`, 1096449 + 1 + 5039 = 1101489 = post, pre-blob is a byte PREFIX `True`; reader (b) N = 1 paragraph, last N match in order `True`; negative control (one byte flipped in the first appended paragraph) rejected by BOTH readers. `.agent/decisions.md` at C3: (a) `True`, 645690 + 1 + 4286 = 649977 = post, prefix `True`; (b) N = 6, `True`; both negative controls reject. `docs/roadmap/features/T5_F032.md` at C3: (a) `True`, 10538 + 1 + 1189 = 11728 = post, prefix `True`; (b) N = 1, `True`; both negative controls reject. LEDGER counts before → after C2: `^Gate: F\d+ R\d+ — ` 66 → 67, `^- R-\d+ — ` 274 → 274, `^Done: R-\d+ — ` 24 → 24, `^Landed: R-` 1 → 1; open set 250 → 250, maximum id `R-0713` → `R-0713`, both unmoved as the block requires; gate keys ADDED `['F032 R14']`; ids added to the registered set `[]`, to the resolved set `[]`. `^## DECISION F032 D\d+ ` in `.agent/decisions.md` before C3 = 7, after = 8; DECISION keys added: `## DECISION F032 D8 `.
- **G6 TYPECHECK AND TEXT READINGS, at C4** — `npx tsc --noEmit` from `apps/ui` chained with a marker: `TSCMARKER_OK` printed and NO other output appeared, so exit 0 and silent. Over the comment-stripped `DecisionInboxCard.tsx` using the guard module's own `strip_ts_comments`: `hidden` 0 (required 0, PASS), `ANSWER_PENDING_TITLE` 0 (0, PASS), `setSendingKeys(` 2 (2, PASS), `clarification.defaultAnswer` 1 (1, PASS), `.target` 1 (1, PASS) and the line carrying it is `const typed = event.target.value;`; `onOpenEvidence` measured 4. The LAST `aria-live="polite"` is opened by a `<p` tag: `True`. `jsx_between_answer_button_and_live_paragraph` returns `'\n                        ) : (\n                          <code className={styles.decisionAnswerText}>{answer.value}</code>\n                        )}\n                        {}\n                        '` with `?` 0, `&&` 0, `||` 0.
- **G7 THE GUARDS, GREEN THEN RED, at C5** — `python3 -m pytest tests/ui_contracts/test_decision_answer_wiring.py -q`: `55 passed in 0.31s`, exit-0 marker `G7A_EXIT0_MARKER` printed. `python3 -m pytest tests/ui_contracts/ -q`: `580 passed, 4 skipped in 5.31s`, exit-0 marker `G7B_EXIT0_MARKER` printed — growth over the reviewer's base reading of `574 passed, 4 skipped` is +6 passed (the six new guards) and skipped unmoved. In the disposable worktree `.remedy-wt/f032-r15-mut` at `8569e717`, `python3 -B` with `__pycache__` purged before every run, one mutation per run, each target byte string counted 1 in its named file before it was applied: UNMUTATED CONTROL exit 0 `55 passed`, worktree `git status --porcelain` 0 lines; (a) delete the `onClick` calling `onOpenEvidence` from `DecisionInboxCard.tsx` — count 1, exit 1, `1 failed, 54 passed`, `FAILED …::TestTheReceiptIsAnEntryPointRatherThanALink::test_the_control_arm_hands_the_handler_the_whole_ref`, 0 lines after restoration; (b) delete the `onOpenEvidence` entry from the props type in the same file — count 1, exit 1, `1 failed, 54 passed`, `FAILED …::test_the_props_type_declares_the_optional_handler`, 0 lines after restoration; (c) delete the `:focus-visible` rule this round adds for `.decisionEvidenceChip` from `RightLivePanel.module.css` — count 1, exit 1, `1 failed, 54 passed`, `FAILED …::test_the_pressable_receipt_shows_where_the_keyboard_is`, 0 lines after restoration. UNMUTATED CONTROL again after all restorations: exit 0, `55 passed`, 0 lines. Worktree removed and pruned; `git worktree list` is one line, the primary checkout.
- **G8 STRUCTURE, CANARY, DOCS AND THE PR GATE, at C5** — `python3 -m pytest tests/cli/test_golden_path.py -q`: `42 passed in 20.67s`, exit-0 marker `CANARY_EXIT0_MARKER` printed. `python3 -m pytest tests/docs/ -q`: `295 passed in 0.44s`, exit-0 marker `DOCS_EXIT0_MARKER` printed. `git diff --name-only a4a24663..8569e717` = 9 paths; residue changed-but-not-in-the-change-set `[]`, residue in-the-change-set-but-not-changed `[]` (the change set less `.agent/handoff.md`). `git diff --stat a4a24663..8569e717 -- packages/` EMPTY, and `-- apps/ui/src/api/` EMPTY. Per-commit insertions, each single-parent and each under 500: 488, 464, 21, 2, 83, 65, 126 — agreeing cell by cell with the `+/-` column of `## Commits` above. `^<<<SLICE ` and `^<<<END ` are 0 and 0 in every written file (`.agent/plan.md`, `.agent/live_review.md`, `.agent/decisions.md`, `docs/roadmap/features/T5_F032.md`, `DecisionInboxCard.tsx`, `RightLivePanel.module.css`, `test_decision_answer_wiring.py`), against a CONTROL of 4 and 4 over the committed C0a blob. `git ls-files .remedy-wt` 0 lines; `git worktree list` one line; `git branch --list "tmp/*"` empty; `gh pr list --state open --json number,headRefName,baseRefName,isDraft` = `[]`.

S1 was performed before the first edit, as ordered. What was read: the four whole-file counts in `tests/ui_contracts/test_decision_answer_wiring.py` that bind every line this round adds — `code.count("ANSWER_PENDING_TITLE") == 0`, `code.count("setSendingKeys(") == 2`, `code.count("clarification.defaultAnswer") == 1`, `code.count(".target") == 1` — plus the whole-file absence `assert "hidden" not in code`, which appears twice (in `TestTheOutcomeRegionExistsBeforeItSpeaks` and again in `TestTheCardShowsTheEvidenceTriple`); and `jsx_between_answer_button_and_live_paragraph`, which takes the LAST `aria-live="polite"`, asserts a `<p` opens it and slices back to the nearest preceding `</button>`, so a control added ABOVE the answer strip leaves it aimed where it already aimed. The whole of `TestTheCardShowsTheEvidenceTriple` was read: its `COLLAPSE_SELECTORS` tuple of four `:empty` selectors, and its eight tests pinning the refs map, the note, the two stakes fields, the `.target` count with `const typed = event.target.value;` as the named survivor, a CSS rule of its own behind each of the five receipt classes, `position: absolute` in each collapse rule with no `display: none` / `visibility: hidden`, and the stakes sitting after the live region under no conditional operator. Every one of those readings still holds at C5 — G6 reports the counts and G7 the run.

## Authored-text proofs

- `.remedy-wt/f032-r15.md` (reviewer scratch original) vs `.agent/authored/f032-r15.md` at C0a vs `.agent/last_block.md` at C0b — all three sha256 `43605b6b924f123c59415e36f390bb4701644a0f8ab27b2751653ae7be5c9991`; the two committed paths are the single blob `c365552e`.
- All four slices (PLANF032R15, LEDGER15, DECISION8, AMEND7) were extracted PROGRAMMATICALLY from `git show 7aeba650:.agent/authored/f032-r15.md`, never retyped. Byte-equality / append-identity results are under G4 and G5.

## Deviations & assumptions

1. **A comment clause inside the edited region was corrected (declared).** The
   receipts block comment in `DecisionInboxCard.tsx` said a ref's `target` "is
   carried on the model for the deep link the next task adds". This round IS
   that task, so the clause was false the moment S3 landed. Three lines were
   rewritten to say the ref travels to `onOpenEvidence` as a field of the ref it
   is part of and still appears in no text, no `title` and no attribute a
   browser shows. This is inside S3's own region and is the only prose touched;
   S6's untouched list is intact.
2. **S5's rules are SCOPED to `button.decisionEvidenceChip`, not written on the
   bare class (declared).** S5 orders the button chrome "written so the span case
   is untouched" and "Change no existing rule". Both are only satisfiable by an
   element-scoped selector: a `cursor: pointer` or a `:hover` border on the bare
   `.decisionEvidenceChip` would dress the inert span arm as a control, which is
   exactly the dishonest affordance R-0693 registered. So `.decisionEvidenceChip`
   is byte-unchanged and three NEW rules were added — `button.decisionEvidenceChip`
   (font-family / font-weight / line-height `inherit`, `text-align: left`,
   `margin: 0`, `cursor: pointer`), its `:hover` (border `--remedy-blue-strong`,
   colour `--remedy-ink`) and its `:focus-visible` (`outline: 2px solid
   var(--remedy-blue-strong)`, `outline-offset: 2px`). The new rule restates no
   value the shared rule already sets, so the higher specificity cannot silently
   override the pill radius, the tint, the border or the 11px size. Every custom
   property used is defined in `apps/ui/src/styles/tokens.css` (R-0661). All four
   `:empty` collapse rules are untouched. The S7 guard reads
   `css_rule_body(css, "button.decisionEvidenceChip:focus-visible")` accordingly.
3. **S2's optional spelling is `?:`, the first of the two equivalents.** S2
   allows either; `onOpenEvidence?: (evidenceRef: DecisionEvidenceRef) => void;`
   is the one that keeps the prop genuinely optional at a call site, which S6
   requires — `| undefined` alone would still force `RightLivePanel` to pass it
   explicitly.
4. **One S7 assertion was rewritten during authoring, before C5.** A first draft
   pinned the control arm with a literal `'<button\n<24 spaces>type="button"'`,
   which is false because `key=` precedes `type=` on that element. It was
   replaced with an indentation-independent reading that slices the control arm
   between `onOpenEvidence ? (` and the span arm and requires `<button` and
   `type="button"` inside it. Nothing was committed in the failing state.
5. No departure from the block's ordered commit sequence: C0a, C0b, C1, C2, C3,
   C4, C5, C6, in that order, one commit each, none added and none dropped.
6. The handler's arm is unreached at runtime — nothing supplies the prop, the
   shipped vitest config reaches no `.tsx`, and this repository has no DOM
   environment. It is typechecked by `tsc --noEmit` and text-pinned by S7's six
   guards, never behaviour-tested. F023 is the feature that first runs it.
7. `.remedy-wt/` holds the reviewer's scratch original plus this round's five
   helper scripts. It is gitignored and `git ls-files .remedy-wt` is 0 lines.

## Item status

| Item | Status | Reason |
|---|---|---|
| C0a save the block | done | `7aeba650` |
| C0b mirror the block | done | `8891317d` |
| C1 the plan | done | `3d15fd16` |
| C2 the R14 verdict | done | `4af8405e` |
| C3 the D8 ruling and the A7 amendment | done | `112d9922` |
| C4 the component and its styles | done | `24592a1b` |
| C5 the contract guards | done | `8569e717` |
| C6 the handback | done | this commit |
| S1 read the guards first | done | the readings are recorded under Verification |
| S2 the optional prop | done | deviation 3 names the spelling chosen |
| S3 the receipt's two arms | done | key on the outer element of both arms, same class on both |
| S4 no raw target | done | `.target` count 1, still the DOM event's |
| S5 the styles | deviated | scoped to `button.` — deviation 2 |
| S6 nothing else changes | deviated | one stale comment clause corrected — deviation 1 |
| S7 the guards | done | six tests, three red-proved |
| S8 spec and bundle agree | done | S2–S6 in C4, S7 in C5, nothing elsewhere |

## Open findings

250 open (274 paragraphs matching `^- R-\d+ — ` minus 24 lines matching
`^Done: R-\d+ — `), maximum id `R-0713` — unmoved across this round, which
registers no finding and resolves none.

## Next

Review this handback and the committed diff `a4a24663..HEAD`, re-run G1–G8, and
issue the R15 verdict. Before authoring R16, re-read `.agent/STOP` from disk
(Phase 1 rule 1) and then run the Open PR Gate (rule 2). With T003 closed, the
next work is the integration gate over the full suite, then the closure
sequence per `docs/roadmap/STATUS_closure_protocol.md`.
