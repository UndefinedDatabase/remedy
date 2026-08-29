# Handback — F033 Hunk-level diff approval · ROUND 16

## Session

SESSION 4 of feature F033 · round 16 · rounds so far 16

## Range

Review of `1329ef45fbd1f4e189991ffc2ce4a8b2853c1b6a`..`c924eb418b87dd41ffb87a4eb8f6477ff54a162a`
(BASE is the round 15 handback commit; branch `feature/f033-hunk-approval-v2` throughout).

The `+/-` column of every table below is the `git diff --numstat` output for that
commit, read from the tool, and it agrees cell for cell with the per-commit
insertion counts G8 produced.

## Commits

### 3ff36883 docs(f033): save the round 16 block — C0a
| Path | +/- | Reason |
|------|-----|--------|
| .agent/authored/f033-r16.md | +400 / -0 | the reviewer's block, copied byte for byte with `shutil.copyfile`, never retyped |

### b7d07efc docs(f033): mirror the round 16 block — C0b
| Path | +/- | Reason |
|------|-----|--------|
| .agent/last_block.md | +272 / -311 | the same bytes, written from the C0a COMMITTED blob so both paths hold one blob id |

### 0007cf10 docs(f033): point the plan at the partial apply state — C1
| Path | +/- | Reason |
|------|-----|--------|
| .agent/plan.md | +17 / -18 | PLANF033R16, byte-equal |

### 807f6f25 docs(f033): book the round 15 verdict and its two findings — C2
| Path | +/- | Reason |
|------|-----|--------|
| .agent/live_review.md | +6 / -0 | RECORDF033R16 appended: the R15 gate verdict, `Done: R-0744`, and the R-0745 registration |

### 64546b53 docs(f033): record the round 15 prose slip — C3
| Path | +/- | Reason |
|------|-----|--------|
| .agent/prose_slips.md | +2 / -0 | SLIPSF033R16 appended: the block's four-guard enumeration where there were five |

### eb4c697d fix(f033): fold a task's apply states by agreement, not membership — C4
| Path | +/- | Reason |
|------|-----|--------|
| packages/orchestration/ui_server.py | +17 / -3 | the apply fold in `_task_truth_maps` becomes an agreement test with a distinct `partial` state |
| apps/ui/src/components/detail/DetailPopover.tsx | +4 / -0 | `applyStatus` gains the `"partial"` branch, in the SAME commit, because the fold alone would render it as "Unknown" |

### c924eb41 test(f033): pin the partial apply state at both ends of the seam — C5
| Path | +/- | Reason |
|------|-----|--------|
| tests/ui_contracts/test_apply_state_partial.py | +318 / -0 | NEW: derives the fold's emitted label set from the AST and pins it against the popover's branch set |
| tests/ui_server/test_dashboard_cockpit_truth.py | +78 / -0 | six added tests: three preserved answers, two partial cases, one absent attribute |

### C6 (this file) — grouped, per the R-0149 self-reference exception
| Path | +/- | Reason |
|------|-----|--------|
| .agent/handoff.md | (this commit) | a handback cannot table the commit that writes it |

## External actions

| Command | Outcome |
|---------|---------|
| `git worktree add /home/decodeux/Repos/remedy/.remedy-wt/g7-r16 c924eb41 --detach` | created, detached at `c924eb41` — the ONLY place any mutation ran |
| `git worktree remove /home/decodeux/Repos/remedy/.remedy-wt/g7-r16` | removed by exact path, exit 0 |
| `git worktree prune` | exit 0; `git worktree list` then shows the primary checkout alone |
| `git push -u origin feature/f033-hunk-approval-v2` | exit 0 — `1329ef45..b511f625  feature/f033-hunk-approval-v2 -> feature/f033-hunk-approval-v2`, upstream set to `origin/feature/f033-hunk-approval-v2`. Recorded by C7; see D6 |

No PR was created, edited or merged. No force-push, no history rewrite, no branch
deletion. No `npm`, no `npx`, no vitest run — none was ordered and none was needed.

## Verification — one line per gate, real numbers, real exit codes

**G1 HYGIENE — PASS.** `.agent/STOP` read from disk before C0a: absent
(`ls: cannot access '.agent/STOP': No such file or directory`); read again before
C6: absent. `git status --porcelain` empty after every one of C0a, C0b, C1, C2, C3,
C4, C5 and after the worktree removal. Branch `feature/f033-hunk-approval-v2`
throughout (`git rev-parse --abbrev-ref HEAD`). No force-push, no rewrite, no branch
deletion; `git rev-parse feature/f033-hunk-approval` still `ed04081283081f237d96147da39a07fca0b1ccad`.

**G2 TRANSPORT — PASS.** `.remedy-wt/f033-r16-block.md` is 30868 bytes, sha256
`8fcdfcd2416e2410541d8b4b16b63815bcbde30af71c73625f70066c66df874d`; the C0a blob
`3ff36883:.agent/authored/f033-r16.md` is 30868 bytes, sha256
`8fcdfcd2416e2410541d8b4b16b63815bcbde30af71c73625f70066c66df874d` — EQUAL in both
length and digest. At C0b, `git rev-parse b7d07efc:.agent/authored/f033-r16.md` and
`git rev-parse b7d07efc:.agent/last_block.md` both print
`9e5db1fb84ad6f72446b7fb5c4474684391854ce` — ONE blob id.

**G3 THE RECORD APPEND at C2 — PASS.** (a) BASE blob of `.agent/live_review.md` is
1535259 bytes (as ordered); 1535259 + 1 newline + 7464 (RECORDF033R16) = 1542724,
which is the C2 blob byte for byte (`recon == C2: True`); BASE is a byte PREFIX of
C2 (`True`); C2 ends in exactly one newline (`True`); C2 sha256
`3d75875f027ff16a1a42cecbdb7bea8037274e1dffba5db7aa51ba1e2be9907d`. (b) N COUNTED by
the script at 3; the LAST 3 blank-line units of the C2 blob equal the slice's three
paragraphs IN ORDER — 3687 bytes (`Gate: F033 R15 …`), 1276 bytes (`Done: R-0744 …`),
2497 bytes (`- R-0745 …`), each `equal=True`. NEGATIVE CONTROL: the first appended
paragraph's BYTE span in C2 is [1535260, 1538947), length 3687, and
`c2[1535260:1538947] == paras[0]` is `True`; the control offset 1537103 is PROVEN
inside that span (`start <= off < end: True`, byte `b'_'`), and flipping it to `b'Z'`
is REJECTED by BOTH readers — reconstruction reader `True`, paragraph reader `True`.

**G4 THE LEDGER at C2 — PASS, every ordered reading reproduced.**
`^- R-\d+ — ` 305 lines over 305 distinct at BASE → 306 over 306 at C2, ADDED id set
exactly `['R-0745']`, removed `[]`. `^Done: R-\d+ — ` 49 lines over 47 distinct at
BASE → 50 over 48 at C2, ADDED resolved id exactly `['R-0744']`. `^Landed: R-` 17 at
BASE and 17 at C2 — UNMOVED, this round writes no `Landed:` line at all; and
`^Landed: R-0744 — ` is 1 at BASE and 1 at C2, so that line is STILL PRESENT beside
its new `Done:` paragraph. `^Gate: F\d+ R\d+ — ` 132 → 133, with `^Gate: F033 R15 — `
0 at BASE and exactly 1 at C2. `^DECISION F033 D\d+ — ` 4 at BASE and 4 at C2 —
UNMOVED. OPEN SET (registered distinct − resolved distinct) 258 at BASE and 258 at
C2 — stated explicitly, not inferred: one id added and one resolved. R-0738:
`^- R-0738 — ` is 1 at C2 and `^Done: R-0738 — ` is 0 at C2 — this round does NOT
resolve it.

**G5 THE PROSE FILES — PASS.** `.agent/plan.md` at C1 is 2453 bytes over 44 lines
(under the 50-line cap AGENTS.md sets) and is byte-EQUAL to PLANF033R16 (`True`).
`.agent/prose_slips.md`: BASE blob 24266 bytes (as ordered); BASE + one newline +
SLIPSF033R16 (715 bytes) == the C3 blob of 24982 bytes, byte for byte (`True`), with
BASE a byte PREFIX (`True`). `^2026-\d\d-\d\d · F033 R15 · ` is 0 at BASE and 1 at
C3. Lines beginning `- R-` in the whole file at C3: 0.

**G6 THE FOLD AND THE LABEL at C4 — PASS.**
(a) `python3 -m ruff check packages/orchestration/ui_server.py tests/ui_server/test_dashboard_cockpit_truth.py tests/ui_contracts/test_apply_state_partial.py`
— REAL exit 0, summary line `All checks passed!`.
(b) The SHIPPED `_task_truth_maps` exercised DIRECTLY over hand-built change objects,
not through the tests. BASE reading measured first, on the same six inputs:

| input | BASE reading | C4 reading |
|-------|--------------|------------|
| all `applied` (3) | `'applied'` | `'applied'` — UNCHANGED |
| all `reverted` (3) | `'reverted'` | `'reverted'` — UNCHANGED |
| all `not_applied` (3) | `'not_applied'` | `'not_applied'` — UNCHANGED |
| 3 `applied` + 5 `not_applied` | `'applied'` | `'partial'` |
| 1 `applied` + 1 `reverted` | `'applied'` | `'partial'` |
| 1 with `apply_state` ABSENT + 1 `applied` | `'applied'` | `'partial'` |

The three confident answers are preserved exactly; only the mixed cases move.
(c) The PROOF fold's source region is 554 bytes over 11 lines at BASE and 554 bytes
over 11 lines at C4, and `byte-identical: True` — only the apply fold moved.
(d) Labels the C4 fold can assign, derived from its AST:
`['applied', 'not_applied', 'partial', 'reverted']` (BASE:
`['applied', 'not_applied', 'reverted']`). Values `DetailPopover.tsx`'s `applyStatus`
branches on at C4, read off comment-stripped source:
`['applied', 'not_applied', 'partial', 'reverted']`. `fold - helper: []`,
`helper - fold: []` — the difference is EMPTY IN BOTH DIRECTIONS.
(e) The helper returns `'Partially applied'` for `"partial"`. The `UNKNOWN` constant
is `'Unknown'`, so the label differs from the fallback (`True`); it differs from
`'Applied'`, `'Reverted'` and `'Not applied'` (`True`); and all four branch labels
are distinct (`True`). The helper still ends in `return UNKNOWN;`.

**G7 THE MUTATION RED-PROOFS at C5 — PASS, all three RED.** Run with `python3 -B`
inside the disposable worktree `/home/decodeux/Repos/remedy/.remedy-wt/g7-r16` only,
never in the primary checkout. IMPORT PROOF first, REAL exit 0:
`packages.orchestration.ui_server` resolves to
`/home/decodeux/Repos/remedy/.remedy-wt/g7-r16/packages/orchestration/ui_server.py`
(`inside worktree: True`). UNMUTATED CONTROLS, each REAL exit 0:
`tests/ui_server/test_dashboard_cockpit_truth.py` `39 passed in 0.55s` (33 at BASE,
plus the 6 this round adds), `tests/ui_contracts/test_apply_state_partial.py`
`13 passed in 0.28s`. Then, one mutation at a time, each anchor asserted UNIQUE (`1`
occurrence) inside the named file before replacing it, and each fully reverted before
the next — `git status --porcelain` inside the worktree read empty (`''`) after every
restore and at the end.

- (i) restore the MEMBERSHIP test `if "applied" in apply_states` as the first arm of
  the apply fold, in `packages/orchestration/ui_server.py` — REAL exit **1**,
  `4 failed, 48 passed in 0.71s`. Failing:
  `test_apply_state_partial.py::TestTheBackendCanReallyEmitPartial::test_the_fold_no_longer_answers_by_membership`,
  `test_dashboard_cockpit_truth.py::TestTaskTruthMaps::test_a_missing_apply_state_never_by_itself_produces_applied`,
  `…::test_one_applied_and_one_reverted_reads_partial`,
  `…::test_some_applied_and_some_not_reads_partial_and_never_applied`.
- (ii) make the mixed arm return `"applied"` instead of `"partial"`, in
  `packages/orchestration/ui_server.py` — REAL exit **1**,
  `5 failed, 47 passed in 0.70s`. Failing:
  `test_apply_state_partial.py::TestEveryEmittedValueHasALabel::test_the_two_sets_agree_in_both_directions`,
  `test_apply_state_partial.py::TestTheBackendCanReallyEmitPartial::test_the_fold_assigns_the_partial_label`,
  `test_dashboard_cockpit_truth.py::TestTaskTruthMaps::test_a_missing_apply_state_never_by_itself_produces_applied`,
  `…::test_one_applied_and_one_reverted_reads_partial`,
  `…::test_some_applied_and_some_not_reads_partial_and_never_applied`.
- (iii) delete the `"partial"` branch from
  `apps/ui/src/components/detail/DetailPopover.tsx` so the helper falls through to
  `UNKNOWN` — REAL exit **1**, `4 failed, 48 passed in 0.71s`. Failing:
  `test_apply_state_partial.py::TestEveryEmittedValueHasALabel::test_the_two_sets_agree_in_both_directions`,
  `…::TestThePartialLabelSaysSomething::test_the_helper_returns_a_label_for_partial`,
  `…::test_the_partial_label_is_distinct_from_the_other_three`,
  `…::test_the_partial_label_is_not_the_unknown_fallback`.
  This is the one the block singled out: the PYTHON contract test really does read
  the TypeScript, and it goes RED with no vitest run anywhere in the round.

Worktree then removed by exact path and pruned; `git worktree list` shows the primary
checkout alone and `git status --porcelain` in it is empty.

**G8 SUITES AND STRUCTURE — PASS.** Serially, one pytest process at a time, in the
primary checkout, each a REAL exit 0:

| Suite | REAL exit | Result |
|-------|-----------|--------|
| `tests/ui_server/test_dashboard_cockpit_truth.py` | 0 | `39 passed in 6.13s` (33 at BASE + 6 added) |
| `tests/ui_contracts/test_apply_state_partial.py` | 0 | `13 passed in 0.28s` (new file) |
| `tests/ui_contracts/` | 0 | `677 passed, 4 skipped in 5.60s` |
| `tests/ui_server/test_command_channel.py` | 0 | `106 passed in 12.80s` (106 at BASE) |
| `tests/cli/test_patch_cmd.py` | 0 | `13 passed in 0.24s` (13 at BASE) |
| `tests/cli/test_golden_path.py` (canary) | 0 | `42 passed in 20.56s` (42 at BASE) |

STRUCTURE, over `git rev-list --reverse BASE..C5` — 7 commits, each with exactly ONE
parent, each under 500 INSERTIONS (the `+` column of `git diff --numstat`, never
insertions plus deletions):

| Commit | Parents | Insertions | Deletions | Under 500 |
|--------|---------|-----------|-----------|-----------|
| 3ff36883 | 1 | 400 | 0 | yes |
| b7d07efc | 1 | 272 | 311 | yes |
| 0007cf10 | 1 | 17 | 18 | yes |
| 807f6f25 | 1 | 6 | 0 | yes |
| 64546b53 | 1 | 2 | 0 | yes |
| eb4c697d | 1 | 21 | 3 | yes |
| c924eb41 | 1 | 396 | 0 | yes |

PATH SET, both directions: 9 paths touched in `BASE..C5`;
`touched - declared: []`; `declared - touched: ['.agent/handoff.md']`, which C6
writes after this range — declared below as D4 rather than left to be read as a match.
DELIMITER LEAKAGE at C5, `<<<SLICE ` / `<<<END `: `.agent/plan.md` 0/0,
`.agent/prose_slips.md` 0/0, `packages/orchestration/ui_server.py` 0/0,
`apps/ui/src/components/detail/DetailPopover.tsx` 0/0; NON-ZERO CONTROL
`.agent/authored/f033-r16.md` 5/6. `git ls-files .remedy-wt` reads 0 tracked files.
DO-NOT-TOUCH PATHS, blob id at BASE vs C5 — 12 of 12 byte-identical, one line each:

| Path | blob BASE → C5 | identical |
|------|----------------|-----------|
| packages/orchestration/proof_chain.py | a3a29d630523 → a3a29d630523 | yes |
| packages/orchestration/hunk_decision_record.py | 0563c5a00660 → 0563c5a00660 | yes |
| packages/orchestration/hunk_ledger.py | 57c00fcfde62 → 57c00fcfde62 | yes |
| packages/orchestration/evidence_index.py | 4d797b53312a → 4d797b53312a | yes |
| apps/cli/command_catalog.py | 7946dd67c459 → 7946dd67c459 | yes |
| apps/cli/commands/patch.py | e7257b680f08 → e7257b680f08 | yes |
| apps/cli/grouped.py | c9c5265d0b87 → c9c5265d0b87 | yes |
| tests/ui_server/test_command_channel.py | f4dc2d915703 → f4dc2d915703 | yes |
| tests/ui_server/test_command_dispatch.py | e9a8bd08f110 → e9a8bd08f110 | yes |
| apps/ui/src/api/types.ts | 9e40bb480e55 → 9e40bb480e55 | yes |
| apps/ui/src/api/remedyApi.ts | 293e1f5ce844 → 293e1f5ce844 | yes |
| docs/roadmap/STATUS.md | a370be066b7a → a370be066b7a | yes |

`.agent/context.md` was deliberately not touched, as the change set orders.

## The shipped apply fold, in full (at `eb4c697d`)

    # Finding R-0738. The apply fold agrees or it says "partial", taking the
    # shape of the PROOF fold three lines above: unanimity for each confident
    # answer, one distinct state reserved for the mixed case. The membership
    # test this replaces — `if "applied" in apply_states` — reported "applied"
    # for a task where ONE change of eight had applied, indistinguishable from
    # a task where all eight had, and hunk-level approval makes that mixed case
    # the normal one. `grouped` is built by setdefault(...).append(...), so a
    # task's list is never empty and the all() below cannot be vacuously true.
    # ONLY the mixed case moves: the three unanimous inputs still read exactly
    # what the old fold returned for them.
    apply_states = [getattr(c, "apply_state", "") for c in changes]
    if all(s == "applied" for s in apply_states):
        apply_by_task[tid] = "applied"
    elif all(s == "reverted" for s in apply_states):
        apply_by_task[tid] = "reverted"
    elif not any(s in ("applied", "reverted") for s in apply_states):
        # Absorbs the getattr default "" exactly as the old `else` did: a
        # change with no apply_state attribute is not evidence of an apply.
        apply_by_task[tid] = "not_applied"
    else:
        apply_by_task[tid] = "partial"

(Indentation above is reduced by 12 columns for readability; the shipped block sits
inside the `for tid, changes in grouped.items():` loop.) The `apply_status` default
at the dashboard payload — `task_apply_map.get(tid, …)` — is UNCHANGED.

The label the popover helper returns for `"partial"` is **`"Partially applied"`**.

## The tests written, and the property each pins

`tests/ui_server/test_dashboard_cockpit_truth.py`, added as methods of the existing
`TestTaskTruthMaps` so they build their chains through that class's own `_change` /
`_chain` helpers rather than through a second idiom:

| Test | Property pinned |
|------|-----------------|
| `test_all_applied_still_reads_applied` | a task whose changes are ALL `applied` still reads `applied` |
| `test_all_reverted_still_reads_reverted` | ALL `reverted` still reads `reverted` |
| `test_all_not_applied_still_reads_not_applied` | ALL `not_applied` still reads `not_applied` |
| `test_some_applied_and_some_not_reads_partial_and_never_applied` | THE DISCRIMINATOR: one `applied` and two `not_applied` reads `partial` AND NOT `applied` |
| `test_one_applied_and_one_reverted_reads_partial` | one `applied` beside one `reverted` also reads `partial` |
| `test_a_missing_apply_state_never_by_itself_produces_applied` | a change with no `apply_state` attribute reads `partial` beside an `applied` one, and `not_applied` on its own — never `applied` |

`tests/ui_contracts/test_apply_state_partial.py` (new, 13 tests):

| Test | Property pinned |
|------|-----------------|
| `TestTheReadersAreNotVacuous::test_the_stripper_removes_both_comment_forms` | the `//` and `/* */` stripper really strips |
| `…::test_the_popover_really_loses_text_to_the_stripper` | the popover carries comments, so stripping is not a no-op |
| `…::test_the_helper_scoper_returns_less_than_the_whole_module` | `helper_body` scopes to `applyStatus` and does not reach `testStatusLabel` |
| `…::test_the_ast_derivation_finds_labels_at_all` | the AST walk over the fold returns a non-empty set |
| `…::test_the_branch_scan_finds_branches_at_all` | the popover branch scan returns a non-empty set |
| `TestTheBackendCanReallyEmitPartial::test_the_fold_assigns_the_partial_label` | the SOURCE of the fold really can emit `"partial"` |
| `…::test_the_three_confident_labels_survive_beside_it` | `applied` / `reverted` / `not_applied` are still emitted |
| `…::test_the_fold_no_longer_answers_by_membership` | no AST membership test of `apply_states` against a string literal survives |
| `TestEveryEmittedValueHasALabel::test_the_two_sets_agree_in_both_directions` | every value the fold emits has a popover branch, and every branch is reachable |
| `TestThePartialLabelSaysSomething::test_the_helper_returns_a_label_for_partial` | the `"partial"` branch exists and returns a label |
| `…::test_the_partial_label_is_not_the_unknown_fallback` | that label is not the `UNKNOWN` string |
| `…::test_the_partial_label_is_distinct_from_the_other_three` | and is distinct from all three existing labels |
| `…::test_the_helper_still_ends_in_the_fallback` | the helper still ends in `return UNKNOWN;` for a value it has never heard of |

## Authored-text proofs

| Slice | Applied to | Result |
|-------|-----------|--------|
| the whole block | `.agent/authored/f033-r16.md` (C0a) | 30868 bytes, sha256 `8fcdfcd2…df874d` — EQUAL to `.remedy-wt/f033-r16-block.md` in length and digest |
| the whole block | `.agent/last_block.md` (C0b) | same blob id `9e5db1fb84ad6f72446b7fb5c4474684391854ce` as the C0a path |
| PLANF033R16 | `.agent/plan.md` (C1) | 2453 bytes, byte-EQUAL |
| RECORDF033R16 | `.agent/live_review.md` (C2) | 7464 bytes appended; BASE + `\n` + slice == C2 blob byte for byte; BASE a byte prefix; 3 paragraphs matched in order |
| SLIPSF033R16 | `.agent/prose_slips.md` (C3) | 715 bytes appended; BASE + `\n` + slice == C3 blob byte for byte; BASE a byte prefix |

Every slice was extracted from the COMMITTED C0a blob with `git show`, per convention
4 — none was retyped from the delegation prompt.

## Deviations & assumptions

**D1 — the contract test's membership assertion is an AST PREDICATE, not a token
search, and the block's SPEC asked for the token form.** The SPEC's last paragraph
for `tests/ui_contracts/test_apply_state_partial.py` says to "strip comments before
asserting a token is present". I applied that literally to the TypeScript. On the
PYTHON side it is not enough, and I found this by colour rather than by reading: my
first draft asserted `'if "applied" in apply_states' not in SERVER.read_text()`, and
it went RED against the SHIPPED code, because the fold's own WHY comment QUOTES the
membership test it replaced — which is what the SPEC for `ui_server.py` explicitly
orders it to do ("name finding R-0738 and the proof fold beside it as the shape being
copied"). The two SPEC paragraphs cannot both be satisfied by a text search. I
replaced that one assertion with `fold_membership_tests_over_apply_states()`, an AST
walk that collects every literal compared with `ast.In` against the `apply_states`
NAME, and asserts the set is empty. It is strictly stronger than the token form (it
sees a membership test however it is spelled and cannot be answered by prose), and
mutation (i) proves it discriminates: REAL exit 1, that test named among the four
failures. The other Python-side reads in this file were AST or scoped-region reads
already and needed no comment stripping.

**D2 — the six cockpit tests were added as METHODS of the existing
`TestTaskTruthMaps` class rather than in a new class.** The SPEC ordered "READ the
existing `_task_truth_maps` tests in this file and follow their idiom for building a
proof chain; do not invent a second one". That idiom is two INSTANCE helpers,
`self._change(...)` and `self._chain(...)`. A new sibling class could only have
duplicated them (a second idiom, forbidden) or subclassed `TestTaskTruthMaps` (which
would re-collect and re-run all five of its existing tests under a second name). I
took the third route and appended to the class, behind a comment naming R-0738. Every
pre-existing test in the file is untouched and all 39 pass.

**D3 — G7's and G8's control count for `tests/ui_server/test_dashboard_cockpit_truth.py`
reads 39, not the 33 the block states.** The block annotates that path "(33 at BASE)"
in both gates, and 33 is correct AT BASE; this round adds six tests to that file, so
the control at C5 is 39. I state it rather than let the reviewer meet an unexplained
number: 33 + 6 = 39, and no pre-existing test was removed or renamed (the path set
and the additive `+78 / -0` numstat both show it).

**D4 — G8's path-set comparison is non-empty in one direction, by construction.**
`declared - touched` is `['.agent/handoff.md']`. The change set names that path, but
C6 — the commit writing this file — falls OUTSIDE the `BASE..C5` range G8 orders
walked, so it cannot appear in it. `touched - declared` is empty, which is the
direction that would show scope drift.

**D5 — no `Landed:` line and no `Done:` paragraph of my own were written**, as the
block orders. R-0738 is ADVANCED, not resolved: its resolution condition names three
surfaces (viewer badge, task-node glyph, report line) and this round delivers the
TRUTH plus the detail-popover label only. `^- R-0738 — ` is still 1 and
`^Done: R-0738 — ` is still 0 at C2. I reviewed none of my own work and wrote no
verdict on it; the `Done: R-0744` paragraph in `.agent/live_review.md` is the
reviewer's authored text, applied verbatim from the RECORDF033R16 slice.

**D6 — ONE EXTRA COMMIT beyond the block's ordered sequence: C7, which fills the real
push outcome into External actions.** The block's Bundle ends at C6 and the
handback template carries a write-once rule for `.agent/handoff.md`, so this is a
departure and is declared here rather than left to the commit table. The reason is
that the same template mandates "Every push … command + outcome", and the push of
the handback commit necessarily happens AFTER that commit exists: C6 could only
carry the command with a promise where the outcome belongs. C7 changes exactly one
table row — the push line — plus this paragraph, and nothing else in this file. It
is not a trim (nothing was shortened; the handback has no length cap), and the
recursion is bounded at one: C7's own push is the last action of the round and is
reported in the delegation response rather than by a C8.

Departure from the block's ordered commit sequence, stated in full: C0a, C0b, C1,
C2, C3, C4, C5, C6 were committed in that order, one commit each, with no dropped
and no reordered commit; C7 is the single EXTRA commit, for the reason in D6 above.

## Item-status table

| Item | Status | Reason |
|------|--------|--------|
| C0a save the block to `.agent/authored/f033-r16.md` | done | |
| C0b mirror it to `.agent/last_block.md` | done | |
| C1 `.agent/plan.md` = PLANF033R16 | done | |
| C2 RECORDF033R16 into `.agent/live_review.md` | done | |
| C3 SLIPSF033R16 into `.agent/prose_slips.md` | done | |
| C4 the agreement fold + the popover label, ONE commit | done | |
| C5 the tests for both halves | done | |
| C6 the handback | done | this file |
| SPEC `packages/orchestration/ui_server.py` | done | proof fold byte-identical; `apply_status` default unchanged |
| SPEC `apps/ui/src/components/detail/DetailPopover.tsx` | done | one branch added; `types.ts` and `remedyApi.ts` untouched, as measured |
| SPEC `tests/ui_server/test_dashboard_cockpit_truth.py` | deviated | D2 — added as methods of the existing class to reuse its chain helpers |
| SPEC `tests/ui_contracts/test_apply_state_partial.py` | deviated | D1 — the membership assertion is an AST predicate, not a token search |
| G1 HYGIENE | done | |
| G2 TRANSPORT | done | |
| G3 THE RECORD APPEND at C2 | done | |
| G4 THE LEDGER at C2 | done | |
| G5 THE PROSE FILES | done | |
| G6 THE FOLD AND THE LABEL at C4 | done | |
| G7 THE MUTATION RED-PROOFS at C5 | done | all three RED, real exit 1 |
| G8 SUITES AND STRUCTURE | deviated | D3 (39 not 33), D4 (`declared - touched` holds `.agent/handoff.md`) |
| Write NO `Landed:` line, NO `Done:` paragraph of my own | done | D5 |
| Push the branch | done | exit 0, `1329ef45..b511f625`; outcome recorded by C7, declared as D6 |

## Next

SESSION 4 carries forward. The next session's first actions, in this order:

1. Read `.agent/STOP` from disk.
2. Run the Open PR Gate (`gh pr list --state open --json number,headRefName,baseRefName,isDraft`).
3. Book this round's verdict — no verdict on round 16 exists anywhere; this worker
   wrote none and is not permitted to.
4. Then the plan's step 2: the two surfaces R-0738 still names — the task-node glyph
   and the report line. Only after both is R-0738 resolvable.
