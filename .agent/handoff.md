# Handback — F037 R9 (T002 part one, the diff surface)

## Session

SESSION 2 of feature F037 · round 9 · rounds so far 9

THE SESSION ENDS HERE. R9 was ordered by the operator block as the LAST ROUND OF
SESSION 2; this is not an early stop under G7 and no context or gate exhaustion
is being cited. The feature stands at 9 rounds and 2 sessions, well inside the
25-round / 7-session soft limit, so no scope report is owed and the
`SITZUNGS-LIMIT` line is deliberately absent.

## Range

Review of `98b4495d8c235053000223b3d5c15f284cd86c53`..`HEAD` (base = `98b4495d`,
branch `feature/f037-rendered-diff-viewer`). Seven commits: C0a, C0b, C1, C2,
C3, C4 and this handback commit C5.

## Commits

Every `+/-` cell below is taken from `git diff --numstat <sha>^ <sha>` and agrees
cell for cell with the per-commit reading recorded under G8.

### 87d63a66 docs(agent): save the F037 R9 step block
| Path | +/- | Reason |
|------|-----|--------|
| .agent/authored/f037-r9.md | +383/-0 | C0a — the block saved verbatim, 25955 bytes, 383 lines |

### 0ad0a7f5 docs(agent): mirror the F037 R9 block into last_block
| Path | +/- | Reason |
|------|-----|--------|
| .agent/last_block.md | +311/-259 | C0b — the C0a blob mirrored; same blob hash `131e48d9907c` |

### 80be900a docs(agent): point the plan at the F037 R9 diff surface round
| Path | +/- | Reason |
|------|-----|--------|
| .agent/plan.md | +25/-26 | C1 — whole-file replacement by slice PLANF037R9; the file is now 49 lines, under AGENTS.md's 50 |

### 618c7a3e docs(agent): book the R8 gate verdict and the plan-cap slip
| Path | +/- | Reason |
|------|-----|--------|
| .agent/live_review.md | +2/-0 | C2 — GATER8 appended at EOF; no id minted |
| .agent/prose_slips.md | +10/-0 | C2 — SLIPR9 appended at EOF; the R8 plan-cap authoring error, no id per amend0827 rule 2 |

### 7f66d85a feat(ui): add the binding diff surface stylesheet with DECISION F037 D4
| Path | +/- | Reason |
|------|-----|--------|
| .agent/decisions.md | +37/-0 | C3 — DECISION4 appended at EOF; F037 D4, the mono-family token choice |
| apps/ui/src/components/diff/DiffView.module.css | +41/-0 | C3 — new; the binding CSS of T5_F037.md as a real stylesheet, per SPEC S1–S4 |

### 5cba4674 test(ui-contracts): pin the diff surface stylesheet to its binding CSS
| Path | +/- | Reason |
|------|-----|--------|
| tests/ui_contracts/test_diff_surface_css.py | +131/-0 | C4 — new; the Python conformance guard, per SPEC S5–S11 |

### C5 — this commit
| Path | +/- | Reason |
|------|-----|--------|
| .agent/handoff.md | (self-referential) | C5 — this handback; a handoff cannot table the commit that writes it (R-0149 pattern) |

## External actions

| Action | Outcome |
|--------|---------|
| `gh pr list --state open --json number,headRefName,baseRefName,isDraft` | `[]` — no open PR. No PR created, nothing merged, as the block ordered. |
| `git worktree add .remedy-wt/g6-r9 5cba4674 --detach` | `Preparing worktree (detached HEAD 5cba4674)` — created for G6 |
| `git worktree remove .remedy-wt/g6-r9` then `git worktree prune` | removed; `git worktree list` back to 1 line, `git status --porcelain` 0 lines |
| `git push origin feature/f037-rendered-diff-viewer` | ORDERED AFTER C5 and deliberately outside every gate. Its result is not named here, because C5's text is written before the push exists; the reviewer reads the remote tip itself. |

## Verification

### G1 hygiene — PASS

| Reading | Value |
|---------|-------|
| `.agent/STOP` before C0a | ABSENT (`ls: cannot access '.agent/STOP': No such file or directory`) |
| `.agent/STOP` before C5 | ABSENT (same reading, re-read from disk) |
| `git rev-parse HEAD` before C0a | `98b4495d8c235053000223b3d5c15f284cd86c53` — equals the block's base |
| `git branch --show-current` | `feature/f037-rendered-diff-viewer` |
| `git status --porcelain` line count after C0a / C0b / C1 / C2 / C3 / C4 | 0 / 0 / 0 / 0 / 0 / 0 |

### G2 transport, one digest comparison — PASS

- After C0a: `.agent/authored/f037-r9.md` sha256
  `c7face0455a87e074563b640f8837c9cc61c617e958605a4f4bc914ecf520d3a`,
  25955 bytes, 383 lines.
- After C0b: `git rev-parse HEAD:.agent/authored/f037-r9.md` and
  `git rev-parse HEAD:.agent/last_block.md` are both
  `131e48d9907ca9b2e9e764d8f0c873799c04ed8a` — the SAME blob hash.
- `sha256sum` of both working copies is the single digest above.

PLAINLY: this chain covers the saved copy, its mirror and the working copy, and
it claims NOTHING about the bytes of any prompt. The first link — prompt to
saved copy — is not measured by any gate here and is not asserted.

### G3 extraction and caps — PASS

Every slice extracted from the COMMITTED C0a blob `131e48d9907c` by its marker
lines, in Python.

| Slice | Lines |
|-------|-------|
| PLANF037R9 | 49 |
| GATER8 | 1 |
| SLIPR9 | 9 |
| DECISION4 | 36 |

TOTAL 383 (cap 490, met). CONTENT 95. PROSE = 383 − 95 = 288 (cap 400, met).

### G4 the plan at C1 — PASS on the binding clause, with one declared numeral deviation

| Reading | Value |
|---------|-------|
| `.agent/plan.md` byte-equal to PLANF037R9 (newline-included) | **True** |
| NEGATIVE CONTROL vs. the slice minus its trailing newline | **False** (as required) |
| `^## Goal$` | 1 |
| `^## Next Steps$` | 1 |
| `wc -l` | **49** |
| strictly under 50 | **True** |

STATED PLAINLY, because the gate ordered it stated plainly: the file reads 49,
NOT the 48 the block predicted in constraint 2 and in G4. The BINDING clause —
strictly under 50 — IS met, and the R8 defect this slice exists to repair is
genuinely repaired: the file went from exactly 50 lines to 49. The 48 is the
block's own arithmetic on its own slice, off by one; the slice was applied byte
for byte and was not edited to reach any number. See Deviations.

### G5 the record at C2 and the decision at C3 — PASS

Base sizes, each measured beside the block's figure:

| File | Block figure | Measured before append |
|------|--------------|------------------------|
| `.agent/live_review.md` | 1173234 | **1173234** |
| `.agent/prose_slips.md` | 8992 | **8992** |
| `.agent/decisions.md` | 657352 | **657352** |

Per append, reader (a) is the BYTE IDENTITY `result == before + b"\n" + slice`,
re-read from disk — not a length sum with a prefix check. Reader (b) is
independent: the script COUNTS N blank-line units in the slice and compares the
LAST N units of the file against the slice's N units IN ORDER.

| Append | after bytes | reader (a) | reader (b) | NEG CTRL (a) | NEG CTRL (b) |
|--------|-------------|-----------|-----------|--------------|--------------|
| GATER8 → live_review.md | 1176292 | True | True (N=1) | **False** | **False** |
| SLIPR9 → prose_slips.md | 9696 | True | True (N=1) | **False** | **False** |
| DECISION4 → decisions.md | 659752 | True | True (N=5) | **False** | **False** |

Each negative control flipped ONE byte inside the FIRST appended paragraph
(offsets 1173240, 8998, 657358 respectively) and BOTH readers came back False.

COUNTS after C3, line-anchored, each measured:

| Pattern | Ordered | Measured |
|---------|---------|----------|
| `^- R-\d+ — ` | 280, unchanged | **280** |
| `^Done: R-\d+ — ` | 28, unchanged | **28** |
| `^Landed: R-` | 1, unchanged | **1** |
| `^Gate: F\d+ R\d+ — ` | 79 | **79** |
| `^## DECISION ` in `.agent/decisions.md` | 170 | **170** |
| `F037 D4` occurrences | exactly once | **1** |

Open set: **252**. `R-0719` is still in it: **True**. No id was minted.

### G6 red-proofs — PASS, all three mutations RED

Run ONLY inside the disposable worktree `.remedy-wt/g6-r9` at the C4 tree
`5cba4674`, never in the primary checkout. `__pycache__` purged and `python3 -B`
used before EVERY run; the stylesheet restored to the C4 bytes between
mutations and verified identical after each restore.

UNMUTATED CONTROL — `python3 -B -m pytest tests/ui_contracts/test_diff_surface_css.py -q`
→ REAL EXIT CODE **0**, verbatim summary `7 passed in 0.17s`, 0 failing node ids.

**(a) the track list.**
FROM `56px 56px 1fr` TO `56px 1fr`; occurrences of FROM in the file before the
edit: **1**.
→ REAL EXIT CODE **1**, verbatim summary `1 failed, 6 passed in 0.18s`.
Failing node ids, in full:
`FAILED tests/ui_contracts/test_diff_surface_css.py::TestDiffSurfaceStylesheet::test_diff_line_is_a_three_column_grid`

**(b) ligatures deleted from `.diffLine` ONLY.**
FROM `font-feature-settings: "liga" 0` TO the empty string; occurrences of FROM
in the whole file before the edit: **2**; the edit was scoped to the single line
beginning `.diffLine {` (line 27), which holds **1** of them, leaving the
`.hunkHead` declaration in place.
→ REAL EXIT CODE **1**, verbatim summary `1 failed, 6 passed in 0.19s`.
Failing node ids, in full:
`FAILED tests/ui_contracts/test_diff_surface_css.py::TestDiffSurfaceStylesheet::test_ligatures_are_off_in_the_diff_line_rule`
This is the mutation the block wanted most, and it lands: exactly ONE of the two
ligature tests fired and `test_ligatures_are_off_in_the_hunk_head_rule` stayed
green, so S10's assertion is genuinely PER RULE and not a count over the file
that the surviving `.hunkHead` declaration could have masked.

**(c) the `.ln` colour token.**
FROM `var(--remedy-ink-soft, #6f82a8)` TO `var(--remedy-ink-nonexistent, #6f82a8)`;
occurrences of FROM in the whole file before the edit: **2** (the `.ln` rule and
the `.hunkHead` rule); the edit was scoped to the single line beginning
`.diffLine .ln {` (line 30), which holds **1** of them.
→ REAL EXIT CODE **1**, verbatim summary `1 failed, 6 passed in 0.19s`.
Failing node ids, in full:
`FAILED tests/ui_contracts/test_diff_surface_css.py::TestDiffSurfaceStylesheet::test_every_referenced_token_is_defined_in_the_shipped_sheet`
No mutation came back GREEN, so no diagnosis of a silent assertion is owed. No
test was changed and no mutation was substituted.

Afterwards: `git worktree remove .remedy-wt/g6-r9` and `git worktree prune`;
`git worktree list` **1** line, `git status --porcelain` **0** lines in the
primary checkout.

### G7 suite, lint and canary at C4 — PASS

ONE pytest process at a time; never two in parallel.

- `python3 -m pytest tests/ui_contracts/ -q` → REAL EXIT CODE **0**, verbatim
  summary `587 passed, 4 skipped in 5.62s`; lines matching `^FAILED`: **0**.
  This is the WHOLE-DIRECTORY figure as measured — the selection was never
  narrowed.
- EXTRACTOR-BLINDNESS CONTROL: the SAME counter run over the control string
  `FAILED tests/ui_contracts/test_diff_surface_css.py::test_control_string`
  returns **1**. The 0 above is therefore a measurement, not a blind spot.
- Node-id inventory from
  `python3 -m pytest tests/ui_contracts/test_diff_surface_css.py --collect-only -q`
  — **7 tests collected**, never derived by regexing `-v` output:
  1. `tests/ui_contracts/test_diff_surface_css.py::TestDiffSurfaceStylesheet::test_stylesheet_exists`
  2. `tests/ui_contracts/test_diff_surface_css.py::TestDiffSurfaceStylesheet::test_diff_line_is_a_three_column_grid`
  3. `tests/ui_contracts/test_diff_surface_css.py::TestDiffSurfaceStylesheet::test_diff_line_font_is_the_binding_mono_size`
  4. `tests/ui_contracts/test_diff_surface_css.py::TestDiffSurfaceStylesheet::test_added_and_removed_lines_are_two_different_colours`
  5. `tests/ui_contracts/test_diff_surface_css.py::TestDiffSurfaceStylesheet::test_ligatures_are_off_in_the_diff_line_rule`
  6. `tests/ui_contracts/test_diff_surface_css.py::TestDiffSurfaceStylesheet::test_ligatures_are_off_in_the_hunk_head_rule`
  7. `tests/ui_contracts/test_diff_surface_css.py::TestDiffSurfaceStylesheet::test_every_referenced_token_is_defined_in_the_shipped_sheet`
- `python3 -m ruff check tests/ui_contracts/test_diff_surface_css.py`, repository
  configuration, NO `--isolated` → REAL EXIT CODE **0**, verbatim output
  `All checks passed!`.
- Canary `python3 -m pytest tests/cli/test_golden_path.py -q` → REAL EXIT CODE
  **0**, verbatim summary `42 passed in 20.71s`. That matches the base figure of
  `42 passed` exactly; there is no difference to report.

### G8 structure, artifacts and the Open PR Gate at C4 — PASS

`git diff --name-only 98b4495d..5cba4674` returns exactly the eight paths of the
change set minus `.agent/handoff.md`:
`.agent/authored/f037-r9.md`, `.agent/decisions.md`, `.agent/last_block.md`,
`.agent/live_review.md`, `.agent/plan.md`, `.agent/prose_slips.md`,
`apps/ui/src/components/diff/DiffView.module.css`,
`tests/ui_contracts/test_diff_surface_css.py`.
RESIDUE actual minus expected: `[]`. RESIDUE expected minus actual: `[]`.

Restricted `git diff --stat`:

| Prefix | Reading |
|--------|---------|
| `packages/` | EMPTY |
| `docs/` | EMPTY |
| `apps/` | only `apps/ui/src/components/diff/DiffView.module.css` (+41) |
| `tests/` | only `tests/ui_contracts/test_diff_surface_css.py` (+131) |

Per-commit insertions from `git diff --numstat`, every commit single-parent and
every insertion count under 500:

| Commit | SHA | Parents | Insertions | Deletions | <500 |
|--------|-----|---------|------------|-----------|------|
| C0a | 87d63a66 | 1 | 383 | 0 | yes |
| C0b | 0ad0a7f5 | 1 | 311 | 259 | yes |
| C1 | 80be900a | 1 | 25 | 26 | yes |
| C2 | 618c7a3e | 1 | 12 | 0 | yes |
| C3 | 7f66d85a | 1 | 78 | 0 | yes |
| C4 | 5cba4674 | 1 | 131 | 0 | yes |

C5 is deliberately absent from this table: its own count cannot exist while its
text is being written.

Marker sweep, line-anchored:

| Blob | `^<<<SLICE ` | `^<<<END ` |
|------|-------------|------------|
| `.agent/plan.md` at C1 `80be900a` | 0 | 0 |
| `.agent/live_review.md` at C2 `618c7a3e` | 0 | 0 |
| the C0a blob `87d63a66:.agent/authored/f037-r9.md`, SAME counter | **4** | **4** |

Both C0a figures are greater than zero, so the two zeros above are a measurement
and not a blind counter.

- `import` statements naming the new stylesheet across `apps/ui/src`: **0**. A
  wider grep for `components/diff` or `diff/DiffView` anywhere under
  `apps/ui/src` also returns **0** lines. Constraint 8 was kept, and this is the
  reading that proves it rather than asserting it.
- `git ls-files .remedy-wt` line count: **0**.
- Open PR Gate, verbatim:
  `gh pr list --state open --json number,headRefName,baseRefName,isDraft`
  → `[]`. No PR was created and nothing was merged.

## Authored-text proofs

All four reviewer-authored texts were extracted from the COMMITTED C0a blob
`131e48d9907ca9b2e9e764d8f0c873799c04ed8a` by their marker LINES in Python and
applied byte for byte. None was retyped and none was edited.

| Slice | Target | Disk-to-disk result |
|-------|--------|---------------------|
| PLANF037R9 | `.agent/plan.md` (whole-file) | byte-equal **True**; negative control **False** (G4) |
| GATER8 | `.agent/live_review.md` (EOF append) | identity **True**, ordered-units **True**, negative control **False** on both readers (G5) |
| SLIPR9 | `.agent/prose_slips.md` (EOF append) | identity **True**, ordered-units **True**, negative control **False** on both readers (G5) |
| DECISION4 | `.agent/decisions.md` (EOF append) | identity **True**, ordered-units **True**, negative control **False** on both readers (G5) |

## Item status

| Item | Status | Reason |
|------|--------|--------|
| C0a save the block | done | `87d63a66`, 25955 bytes, 383 lines |
| C0b mirror into last_block | done | `0ad0a7f5`, same blob hash as C0a |
| C1 the plan | done | `80be900a`, byte-equal to PLANF037R9, 49 lines |
| C2 the record | done | `618c7a3e`, GATER8 + SLIPR9 appended |
| C3 decision and stylesheet | done | `7f66d85a`, DECISION4 + the new `.module.css` |
| C4 the conformance guard | done | `5cba4674`, 7 tests, all three mutations red |
| C5 the handback | done | this commit |
| S1 header comment | done | binding + authority + A4 + camelCase mapping + the ligature reason from `assets_spec.md` §2 |
| S2 package CSS-module idiom | done | `DetailPopover.module.css` read first; camelCase names, one rule per line, `var(--remedy-x, <fallback>)` |
| S3 the five rules with exact values | done | every numeral and colour transcribed unchanged; only the family is tokenised, per DECISION F037 D4 |
| S4 no other class, absence documented | done | five selectors only; the closing comment states why no intraline treatment exists |
| S5 test idiom | done | `test_main_layout_guard.py` read first; docstring, `from __future__`, three-parent `ROOT`, module-level paths, plain asserts in a class, nothing imported from `apps/` |
| S6 stylesheet exists | done | `test_stylesheet_exists` |
| S7 grid and track list as a value | done | `test_diff_line_is_a_three_column_grid`; the track list is extracted as its own declaration value, not matched as a loose substring |
| S8 12.5px / 1.6 / `--remedy-font-mono` | done | `test_diff_line_font_is_the_binding_mono_size` |
| S9 both backgrounds and they differ | done | `test_added_and_removed_lines_are_two_different_colours` |
| S10 ligatures off, per rule | done | two separate tests; mutation (b) proves the per-rule reading |
| S11 cross-file token guard | done | `test_every_referenced_token_is_defined_in_the_shipped_sheet`; names collected by regex, subset assertion, offenders named in the message; mutation (c) proves it bites |
| G1 hygiene | done | STOP ABSENT twice, base and branch confirmed, six clean-tree readings all 0 |
| G2 transport | done | one digest comparison, same blob hash |
| G3 extraction and caps | done | TOTAL 383 ≤ 490, PROSE 288 ≤ 400 |
| G4 the plan | deviated | the binding clause (strictly under 50) is MET at 49; the block's predicted 48 is off by one. The slice was not edited to reach a number. |
| G5 record and decision | done | all three base sizes match, all six readers True, all six negative controls False, every count as ordered |
| G6 red-proofs | done | control green at exit 0, three mutations red at exit 1, each failing the intended node id; worktree removed and pruned |
| G7 suite, lint, canary | done | `587 passed, 4 skipped`, `^FAILED` 0 with the control returning 1, ruff exit 0, canary `42 passed` |
| G8 structure and Open PR Gate | done | both residues empty, restricted stats as ordered, six single-parent commits all under 500, marker sweep proven non-blind, 0 imports, `[]` from the gate |

## Deviations & assumptions

1. **G4 / constraint 2 — the PLANF037R9 slice measures 49 lines, not the 48 the
   block states, twice.** The block asserts "That slice is 48 lines as authored"
   in constraint 2 and "is expected to read 48" in G4. Measured from the
   COMMITTED C0a blob, the slice body between its marker lines is **49** lines,
   and `.agent/plan.md` after C1 is **49** lines. NOTHING WAS EDITED TO CHANGE
   THIS: constraint 1 forbids editing a slice, and trimming one to make a
   predicted numeral come true would destroy the only evidence that the file on
   disk is the reviewer's text — the same precedence R8 applied and the R8 gate
   text endorses. The LOAD-BEARING clause is met: AGENTS.md requires
   `.agent/plan.md` strictly under 50, G4 orders strictly under 50, and 49 is
   strictly under 50. The R8 defect is genuinely repaired — 50 became 49. Only
   the block's own prediction is wrong, by one, and it is not load-bearing. This
   is a reviewer-prose inaccuracy with no product effect, so per operator
   amendment amend0827 rule 2 it earns no R-id, and per the same rule's fourth
   bullet it does not earn a correction round either.

2. **No ordered commit was added, dropped or reordered.** C0a, C0b, C1, C2, C3,
   C4, C5 ran in exactly the block's order, one commit each.

3. **The new stylesheet is not imported anywhere, by design.** Constraint 8
   forbids wiring it, and G8 measures 0 imports. STATED PLAINLY RATHER THAN
   HIDDEN: an unimported CSS module is INERT. Vite bundles only imported
   modules, so `DiffView.module.css` currently ships in no bundle and renders on
   no screen. It is a committed, guarded transcription of the binding CSS
   waiting for the component that will import it — which is blocked by
   constraint 6. Nothing was wired to a placeholder to make the round look
   finished.

4. **Two assertions the SPEC did not order were NOT added**, so the guard's
   reach is stated honestly: there is no assertion on the `.ln` rule's
   `text-align`, `padding-right` or `user-select`, and none on `.hunkHead`'s
   `padding`, `font-size` or `letter-spacing`. Those values are transcribed in
   the sheet but are pinned only by the cross-file token guard where they
   reference a token. A drift in one of them would not be caught by this test
   file today.

5. **No assumption_log entry is claimed for DECISION F037 D4.** The decision
   text itself argues the tokenised font family is not a visual deviation, since
   size, line-height and weight are untouched and the token's own stack is
   monospace throughout. That reasoning is the reviewer's, authored in the
   slice; the worker applied it byte for byte and did not independently verify
   the rendered type, which cannot be rendered here.

## Next

**FIRST, AND THIS IS THE ONE THING THE NEXT SESSION MOST NEEDS TO KNOW: THE
FRONTEND TEST RUNNER IS REFUSED IN THIS ENVIRONMENT, FOR BOTH ROLES.** R8's G7
measured all three routes — `npx vitest run --root apps/ui`,
`npm --prefix apps/ui run test:unit` and
`apps/ui/node_modules/.bin/vitest run --root apps/ui` — and every one was
REFUSED before execution with `This command requires approval`, for the worker
and for the reviewer alike, so no exit code exists for any of them.
CONSEQUENCE: **T002's rendering core and the whole of T003 are BLOCKED** on the
operator permitting one of those three commands. No `.ts`, `.tsx` or React
component of this feature can be red-proved, and therefore none may be
certified, until that permission exists. R9 landed the half of T002 that Python
CAN verify — the stylesheet and its conformance guard — and that half is now
done; the half that remains cannot be started honestly.

THEN, the first action of the next round is to re-read `.agent/STOP` from disk
(Phase 1 rule 1 — the sentinel can appear mid-session and is otherwise
invisible), and only after that the Open PR Gate
`gh pr list --state open --json number,headRefName,baseRefName,isDraft`, which
returned `[]` at C4.
