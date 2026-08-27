# Handoff — F032 R8 (T002c, the patch-approval card and the owed sweep)

## Session

SESSION 2 of feature F032 · round R8 · rounds so far 8

Session 1 was R1 through R5; this session began at R6. The soft limit is 25
rounds or 7 sessions, whichever comes first, and neither is near.

## Range

Review of `6286f76194c10f4b8da10f62c84f8e00efb364f6`..`428d7920` plus this
handoff commit. Branch: `feature/f032-evidence-triple`. Round base: `6286f761`.

## Commits

### d34393be docs(agent): save the F032 R8 step block
| Path | +/- | Reason |
|------|-----|--------|
| .agent/authored/f032-r8.md | +356 / -0 | C0a, byte-for-byte copy of the scratch block |

### fb914d3e docs(agent): mirror the R8 block into last_block
| Path | +/- | Reason |
|------|-----|--------|
| .agent/last_block.md | +194 / -173 | C0b, same blob as C0a |

### 68152fe0 docs(agent): make the plan current for R8
| Path | +/- | Reason |
|------|-----|--------|
| .agent/plan.md | +18 / -16 | C1, whole-file replacement from slice PLANF032R8 |

### 30b84255 docs(agent): book the R7 verdict and resolve R-0712
| Path | +/- | Reason |
|------|-----|--------|
| .agent/live_review.md | +4 / -0 | C2, pure append of slice LEDGER8 |

### a12d608b feat(orchestration): the patch-approval card cites its intent and its file
| Path | +/- | Reason |
|------|-----|--------|
| packages/orchestration/decision_queue.py | +55 / -0 | C3, S1–S3: the refs and the one unkeyed outcome |
| packages/orchestration/decision_evidence.py | +3 / -1 | C3, S4: `patch_approval` joins `TRIPLE_REQUIRED_TYPES` |

### 14f82fc9 docs(orchestration): retire the stale options-list branch counts
| Path | +/- | Reason |
|------|-----|--------|
| docs/roadmap/features/T5_F032.md | +5 / -1 | C4, S5: A3 corrected by APPENDING, its measurement left standing |
| tests/orchestration/test_decision_evidence.py | +1 / -1 | C4, S5: "six-branch case" → "five-branch case" |

### 428d7920 test(orchestration): pin the patch-approval refs, its outcome and the gate
| Path | +/- | Reason |
|------|-----|--------|
| tests/orchestration/test_decision_evidence.py | +153 / -1 | C5, S6: exact membership plus the T002c tests |

### C6 docs(agent): hand back F032 R8
| Path | +/- | Reason |
|------|-----|--------|
| .agent/handoff.md | self | a handoff cannot table the commit that writes it (R-0149) |

## Item status

| Item | Status | Reason |
|------|--------|--------|
| C0a save this block | done | |
| C0b mirror it into `last_block` | done | same git blob as C0a |
| C1 the plan | done | byte-equal to PLANF032R8 |
| C2 the R7 verdict and `Done: R-0712` | done | pure append, sets moved as ordered |
| C3 the patch-approval triple and the gate set | done | |
| C4 the stale-count sweep | done | |
| C5 its tests | done | |
| C6 the handback | done | self |
| push | done | reported in the completion report, not here |
| S1 read the branch first | done | intent record read; `type="patch_approval",` occurs once |
| S2 the refs come from the intent record | done | `decision` always, `file` only when non-empty |
| S3 the outcome is unkeyed, no payload | done | one outcome keyed `UNKEYED_OPTION`, payload stays `{}` |
| S4 `patch_approval` joins the gate set | done | same commit as its triple |
| S5 the sweep by property | done | search and every hit listed below |
| S6 the tests | done | both cases, the conditional pinned by name |

## External actions

- `git worktree add --detach .remedy-wt/r8-mut 428d7920` — exit 0.
- `git worktree remove --force .remedy-wt/r8-mut` — exit 0; `git worktree prune` — exit 0.
- `gh pr list --state open --json number,headRefName,baseRefName,isDraft` — `[]`.
  Nothing merged, nothing created.
- `git push origin feature/f032-evidence-triple` — INTENT after C6. Its outcome is
  not a value of any file this round writes, so no exit code and no remote tip are
  recorded here; both are in the round's completion report.

## Verification

One line per gate, each executed, each exit code real.

- G1 hygiene, base and the sentinel — exit 0. `git rev-parse HEAD` before C0a was
  `6286f76194c10f4b8da10f62c84f8e00efb364f6`, the round base; branch
  `feature/f032-evidence-triple`; `git status --porcelain` 0 lines after each of
  C0a–C6; `.agent/STOP` absent at both readings.
- G2 transport — exit 0. sha256
  `2330a04d4f4aa3bea3709684b667e217719dcf9d994b52da7baf9f95950c51e3`, 30021 bytes,
  356 lines, IDENTICAL across the scratch file, the committed authored blob and the
  committed mirror; C0a and C0b are the SAME git blob `2289deea8679`. This proves the
  scratch original, the saved copy and the mirror agree — NOT the bytes of any prompt.
- G3 extraction and caps — exit 0. 2 regions: PLANF032R8 46 content lines, LEDGER8 3.
  CONTENT 49, TOTAL 356, PROSE 307. PROSE under 400: yes. TOTAL under 490: yes.
- G4 the plan — exit 0. Byte-equal to PLANF032R8 True; minus-trailing-newline negative
  control False; `wc -l` 46, under 50; `^## Goal$` 1; `^## Next Steps$` 1.
- G5 the ledger append — exit 0. 1059172 + 1 + 6251 = 1065424, matching the committed
  file; base a byte PREFIX. Second reader: N 2, last 2 blank-line units EQUAL IN ORDER
  to the slice's paragraphs (421 units before, 423 after). Negative control, one byte
  flipped in the FIRST appended paragraph in memory only, REJECTED by both readers.
  Sets: `^Gate: F\d+ R\d+ — ` 59→60 adding exactly `F032 R7`; `^Done: R-\d+ — ` 22→23
  adding exactly `R-0712`; `^- R-\d+ — ` 273→273; `^Landed: R-` 1→1; `^Gate: R\d+ — `
  19→19. Open set 251→250; maximum id `R-0712` before and after.
- G6 the code and the sweep — exit 0. `ruff check` on both modules printed
  `All checks passed!`. The real branch was driven twice; both cases and the sweep are
  written out in the completion report.
- G7 tests green then red under mutation — exit 0 green, exit 1 both mutations.
  Scoped file `55 passed` at exit 0 in the primary checkout; worktree control
  `55 passed` exit 0; mutation (a), `patch_approval` dropped from the gate set,
  exit 1 `2 failed, 53 passed`; mutation (b), the file ref made unconditional,
  exit 1 `4 failed, 51 passed`; control after both restorations `55 passed` exit 0.
  The nine decision-schema guard files as ONE process: exit 0, `324 passed`, 0 `^FAILED`.
- G8 structure, canary, PR gate — exit 0. `tests/cli/test_golden_path.py` `42 passed`
  exit 0; `tests/docs/` `295 passed` exit 0; both path residues EMPTY; `apps/` diff
  EMPTY; insertions 356, 194, 18, 4, 58, 6, 153, each single-parent and under 500;
  `^<<<SLICE `/`^<<<END ` 0/0 in all six written files against a CONTROL of 2/2 over
  the C0a blob; `git ls-files .remedy-wt` 0 lines; `git worktree list` 1 line;
  `git branch --list "tmp/*"` 0 lines; Open PR Gate `[]`.

## What the gate enforces after this round

`TRIPLE_REQUIRED_TYPES` is now `frozenset({"token_budget", "test_failure",
"patch_approval"})` — three of the eight producing branches. The five producing
branches still carrying the legacy placeholder `recorded_before_evidence_requirements`
are `stop_reason`, `repo_dirty`, `memory_review`, `flight_plan_approval` (BOTH arms —
neither the pending nor the resolved construction passes `evidence=`) and
`task_decision`.

## The S5 sweep — every sentence the search returned

Searched by PROPERTY, not by list: every sentence in `packages/orchestration/`,
`tests/orchestration/test_decision_evidence.py` and
`docs/roadmap/features/T5_F032.md` stating HOW MANY producing branches do or do not
carry an options list. The measurement was taken by an AST walk of `list_decisions`,
not from prose: eight numbered producing branches, `payload["options"]` set at three
(the budget stop, the flight plan's PENDING arm, the task decision), so FIVE carry none.

CHANGED (2):

1. `tests/orchestration/test_decision_evidence.py:333`, the docstring of
   `test_an_enforced_optionless_decision_reads_no_options_from_the_payload`, from
   `A payload with no ``options`` key is the six-branch case (DECISION F032 D3).`
   to `A payload with no ``options`` key is the five-branch case (DECISION F032 D3).`
2. `docs/roadmap/features/T5_F032.md`, amendment A3. Its measurement — "Only two of
   the eight producing branches carry an options list" and "the other six branches" —
   is LEFT STANDING as ordered, and one sentence was APPENDED: "That count moved once
   and only once, under A6 below, which had the budget stop state in `payload` the two
   options its `next_actions` already offered: three of the eight producing branches
   now carry an options list and five carry none, and A3's scope ruling is unchanged —
   no branch has GROWN options it did not already have."

FOUND AND ALREADY CORRECT, left untouched (2): `decision_evidence.py:66-67` "five of
the eight producing branches carry no options list" and `decision_evidence.py:190`
"five of the eight producing branches carry none". Both match the measurement; R7
corrected these two.

FOUND BUT OUTSIDE THE PROPERTY, left untouched (2), reported because the search
returned them: `packages/orchestration/decision_inbox.py:98` "of the eight producing
branches of ``list_decisions`` only ``task_decision`` mints a non-``fp:`` id" — a count
of producing branches (eight, correct) but not of options lists; and
`docs/roadmap/features/T5_F032.md:162` A6 "A3 counts the branches carrying an options
list and the budget stop is not among them" — states the relationship and no numeral.

## Authored-text proofs

Two slices applied, both disk-to-disk against the committed
`.agent/authored/f032-r8.md`:

- PLANF032R8 → `.agent/plan.md` at C1: byte-equal True; minus-trailing-newline
  negative control False.
- LEDGER8 → `.agent/live_review.md` at C2: appended byte for byte, base a byte
  prefix, arithmetic 1059172 + 1 + 6251 = 1065424, and the independent
  paragraph reader agreeing in order.

No FROM/TO replacement pairs existed this round (constraint 13).

## Deviations & assumptions

- The ordered commit sequence C0a, C0b, C1, C2, C3, C4, C5, C6 was followed exactly.
  NO extra commit was made, none was dropped, and none was reordered.
- No slice contradicted anything measured, so nothing was applied over a contradiction.
- No finding id, `Gate:`, `Done:` or `Landed:` text was authored (constraint 7). The
  only text entering `.agent/live_review.md` is the LEDGER8 slice.
- OBSERVATION FOR THE REVIEWER, NOT REGISTERED (constraint 7 forbids minting an id):
  when a patch intent carries no `file` key, `list_patch_intents` returns
  `target_path` as `""` rather than omitting it, so the card's PRE-EXISTING
  `safe_summary` renders `Patch intent for  awaits approval.` — a double space where
  the `'?'` default was intended, because `pi.get('target_path', '?')` finds the key
  present and empty. This round did not touch that line and the tests do not assert
  on it. The evidence refs are unaffected: the file ref is correctly omitted.
- The reviewer's reference numerals for the round base all reproduced exactly:
  ledger base 1059172 bytes / 421 units, `All checks passed!` at exit 0, `324 passed`,
  `42 passed`, Open PR Gate `[]`. No divergence to reconcile.
- The block's slice-content total is measured here as 49 lines over 2 regions
  (PLANF032R8 46, LEDGER8 3), TOTAL 356, PROSE 307; the block states no numeral of its
  own for these, as G3 requires.

## Next

The reviewer re-runs G1 through G8 at `428d7920` and records the F032 R8 verdict.
Open findings after this round: 250. T002 then continues with the memory-review and
stop-reason producers, each joining `TRIPLE_REQUIRED_TYPES` in the commit that gives
it a real triple.
