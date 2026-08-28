# Handback — F037 R10 (book the R9 verdict, repair R-0720)

## Session

SESSION 3 of feature F037 · round 10 · rounds so far 10

Session 3 opens with this round. The feature stands at 10 rounds and 3 sessions,
inside the 25-round / 7-session soft limit, so no scope report is owed and the
`SITZUNGS-LIMIT` line is deliberately absent.

## Range

Review of `c777fe83818ab7d4aa7c8150b2f387e562450483`..`HEAD` (base = `c777fe83`,
branch `feature/f037-rendered-diff-viewer`). Seven commits: C0a, C0b, C1, C2, C3,
C4 and this handback commit C5.

## Commits

Every `+/-` cell is taken from `git diff --numstat <sha>^ <sha>` and agrees cell
for cell with the per-commit reading recorded under G8.

### fc5d0a77 docs(agent): save the F037 R10 step block
| Path | +/- | Reason |
|------|-----|--------|
| .agent/authored/f037-r10.md | +301/-0 | C0a — the block saved verbatim from `.remedy-wt/f037-r10-block.md`, 25073 bytes, 301 lines |

### c8d8c860 docs(agent): mirror the F037 R10 block into last_block
| Path | +/- | Reason |
|------|-----|--------|
| .agent/last_block.md | +278/-360 | C0b — the C0a blob mirrored; same blob hash `12c20a91f4ea` |

### 899b358a docs(agent): point the plan at the F037 R10 repair round
| Path | +/- | Reason |
|------|-----|--------|
| .agent/plan.md | +25/-26 | C1 — whole-file replacement by slice PLANF037R10; the file is now 48 lines, strictly under AGENTS.md's <50 rule |

### d60de8af docs(agent): book the R9 gate verdict and register R-0720
| Path | +/- | Reason |
|------|-----|--------|
| .agent/live_review.md | +4/-0 | C2 — two appends: slice GATER9 (the R9 verdict) and slice FIND0720 (the registration) |

### 13fee147 test(ui-contracts): catch a font shorthand that resets the ligature setting
| Path | +/- | Reason |
|------|-----|--------|
| tests/ui_contracts/test_diff_surface_css.py | +32/-0 | C3 — the SPEC: helpers `_declaration_offset` and `_font_shorthand_after`, plus `test_no_font_shorthand_follows_the_ligature_declaration`. Pure additions; no existing assertion touched |

### abfd41a3 docs(agent): resolve R-0720
| Path | +/- | Reason |
|------|-----|--------|
| .agent/live_review.md | +2/-0 | C4 — one append: slice DONE0720 |

### C5 this handback commit
| Path | +/- | Reason |
|------|-----|--------|
| .agent/handoff.md | rewrite | C5 — a handoff cannot table the commit that writes it (R-0149 pattern) |

## External actions

| Command | Outcome |
|---|---|
| `git worktree add .remedy-wt/g6-r10 13fee147 --detach` | exit 0, "HEAD is now at 13fee147" |
| `git worktree remove .remedy-wt/g6-r10` (first call) | exit 0, no output; directory gone |
| `git worktree remove .remedy-wt/g6-r10` (second call, from the reporting script) | exit 128 — already removed by the first call; declared under Deviations |
| `git worktree prune` | exit 0 |
| `git worktree list` | 1 line — the primary checkout only |
| `gh pr list --state open --json number,headRefName,baseRefName,isDraft` | exit 0, stdout verbatim `[]` — NO open PR. Nothing to merge, nothing blocked |
| `git push origin feature/f037-rendered-diff-viewer` | ORDERED AFTER C5 and therefore not yet run when these bytes are written; its real exit code cannot be stated here without inventing it, and is reported in the round report instead |

No PR created, nothing merged, no force-push, no history rewrite.

## Verification

Eight gates, every one RUN, every exit code REAL and measured.

### G1 hygiene

- `.agent/STOP` read from disk BEFORE C0a: **does not exist** (literal reading:
  `os.path.exists(".agent/STOP") == False`).
- `.agent/STOP` read from disk again BEFORE C5: **does not exist** (same literal
  reading).
- `git rev-parse HEAD` before C0a → `c777fe83818ab7d4aa7c8150b2f387e562450483`.
  EQUALS the base named by the block.
- `git branch --show-current` → `feature/f037-rendered-diff-viewer`.
- `git status --porcelain` LINE COUNT after each commit: C0a **0**, C0b **0**,
  C1 **0**, C2 **0**, C3 **0**, C4 **0**.

### G2 transport — ONE digest comparison

- `git rev-parse HEAD:.agent/authored/f037-r10.md` → `12c20a91f4ea4e5477c1eba4a56725c2a5a22191`
- `git rev-parse HEAD:.agent/last_block.md` → `12c20a91f4ea4e5477c1eba4a56725c2a5a22191`
- SAME BLOB HASH: **True**
- Working copy of `.agent/authored/f037-r10.md`: sha256
  `fd579581a57a690f379763b89d3404d51d7f8afe70ab44fada1ec1c8c9080335`,
  **25073 bytes**, **301 lines**.

WHAT THIS CHAIN COVERS AND WHAT IT DOES NOT: it covers the saved copy
`.agent/authored/f037-r10.md` and its mirror `.agent/last_block.md`, and proves
those two are one blob. It asserts NOTHING about the bytes of any prompt. The
first link measured here is the on-disk file `.remedy-wt/f037-r10-block.md`,
which C0a copied byte for byte (`b == b2` → True); no claim is made that those
bytes equal anything that was emitted into a prompt.

### G3 extraction and caps — measured on the COMMITTED C0a blob, not on prose

| Slice | Content lines |
|---|---|
| PLANF037R10 | 48 |
| GATER9 | 1 |
| FIND0720 | 1 |
| DONE0720 | 1 |
| **CONTENT total** | **51** |

- TOTAL line count of the blob: **301**
- PROSE = TOTAL − CONTENT = **250**
- TOTAL ≤ 490: **True**
- PROSE ≤ 400: **True**

### G4 the plan at C1

- `.agent/plan.md` BYTE-EQUAL to slice PLANF037R10, newline included: **True**
- NEGATIVE CONTROL, same slice minus its trailing newline: **False**
- Lines exactly matching `## Goal`: **1**
- Lines exactly matching `## Next Steps`: **1**
- `wc -l` → **48**; STRICTLY under 50: **True**

The binding clause — strictly under 50 — holds. No numeral elsewhere in the block
disagrees with this measurement.

### G5 the record at C2 and C4

`.agent/live_review.md` measured **1176292 bytes at the base `c777fe83`**. The
block named 1176292. The figures AGREE exactly; no disagreement to declare.

| Append | Commit | before | after | reader (a) byte identity | reader (b) N units, last-N in order | NEG CONTROL (a) | NEG CONTROL (b) |
|---|---|---|---|---|---|---|---|
| GATER9 | C2 | 1176292 | 1180692 | **True** | N=1, **True** | **False** | **False** |
| FIND0720 | C2 | 1180692 | 1184016 | **True** | N=1, **True** | **False** | **False** |
| DONE0720 | C4 | 1184016 | 1185228 | **True** | N=1, **True** | **False** | **False** |

Reader (a) is `result == before + b"\n" + slice`, re-read from disk. Reader (b)
counts the blank-line-separated units in the slice and compares the LAST N units
of the file against the slice's N units IN ORDER. Each negative control flipped
ONE byte inside the first appended paragraph (offsets 1178492, 1182354, 1184622)
in memory only — the on-disk file was never mutated — and BOTH readers returned
False on all three.

Whole-file append-only proof: the file after C4 satisfies
`disk == base_blob + b"\n" + GATER9 + b"\n" + FIND0720 + b"\n" + DONE0720` →
**True**, and `disk.startswith(base_blob)` → **True**. Nothing already in the
record was edited, renumbered or deleted.

Line-anchored counts over `.agent/live_review.md` AFTER C4:

| Pattern | Count |
|---|---|
| `^- R-\d+ — ` | 281 |
| `^Done: R-\d+ — ` | 29 |
| `^Landed: R-` | 1 |
| `^Gate: F\d+ R\d+ — ` | 80 |

- Open set (registered, neither `Done:` nor `Landed:`): **252**
- Every id distinct: **True** (281 registrations, 281 distinct)
- `R-0720` occurs exactly once as a registration: **True**
- `R-0720` occurs exactly once as a resolution: **True**
- `R-0720` still in the open set: **False** (it is resolved)
- `R-0719` still open: **True** (untouched by this round, as ordered)

### G6 the red-proof of the ordering assertion

All of it inside the disposable worktree `.remedy-wt/g6-r10`, never in the
primary checkout. `__pycache__` purged and `python3 -B` used before every run.

**UNMUTATED CONTROL** at the C3 tree (`13fee147`):

    python3 -B -m pytest tests/ui_contracts/test_diff_surface_css.py -q
    REAL EXIT CODE: 0
    8 passed in 0.17s

**THE MUTATION — a PURE REORDER of the `.diffLine` rule** in
`apps/ui/src/components/diff/DiffView.module.css`. The two rule texts:

    BEFORE: .diffLine { display: grid; grid-template-columns: 56px 56px 1fr; font: 12.5px/1.6 var(--remedy-font-mono, ui-monospace, monospace); font-feature-settings: "liga" 0; }
    AFTER : .diffLine { display: grid; grid-template-columns: 56px 56px 1fr; font-feature-settings: "liga" 0; font: 12.5px/1.6 var(--remedy-font-mono, ui-monospace, monospace); }

Proof the reorder is pure: the sorted multiset of declarations is identical
before and after (**True**), and the only differing line index in the whole file
is **[26]** — the `.diffLine` rule itself. Every other rule is byte-identical.

    python3 -B -m pytest tests/ui_contracts/test_diff_surface_css.py -q
    REAL EXIT CODE: 1
    1 failed, 7 passed in 0.19s

FAILING NODE IDS, AS MEASURED (not predicted):

    FAILED tests/ui_contracts/test_diff_surface_css.py::TestDiffSurfaceStylesheet::test_no_font_shorthand_follows_the_ligature_declaration

THE ORDERED PROPERTY IS THE COLOUR AND IT LANDS: the mutation is RED, exactly one
test fires, and it is the new one. The seven pre-existing tests stay green under
the reorder, which is the point — the substring assertions cannot see order, so
they are demonstrably not doing this work.

Restore between runs: `git checkout -- apps/ui/.../DiffView.module.css` exit 0,
restored sha256 `6f891f9acf469d936d3f2bb720a07acf8fadc7e9269bc68f4d93c14b8a86befe`
== the original sha256, byte-identical **True**; worktree `git status --porcelain`
back to **0** lines.

**BASE-GUARD NEGATIVE CONTROL** — the SAME reorder against the guard as it stands
at the base commit `c777fe83` (the guard BEFORE C3). Worktree HEAD re-checked to
`c777fe83818ab7d4aa7c8150b2f387e562450483`; guard file 131 lines and
`test_no_font_shorthand_follows_the_ligature_declaration` NOT present (**False**);
CSS sha256 identical to the C3 tree's.

    python3 -B -m pytest tests/ui_contracts/test_diff_surface_css.py -q
    REAL EXIT CODE: 0
    7 passed in 0.17s
    FAILED lines: []

GREEN, as R-0720 said it would be. The defect was real: the pure reorder passed
the old guard and fails the new one. The file was restored afterwards to the same
sha256 and the worktree left clean.

Cleanup: `git worktree remove` exit 0 (first call), `git worktree prune` exit 0,
`git worktree list` **1 line** (primary checkout only), primary
`git status --porcelain` **0 lines**, directory `.remedy-wt/g6-r10` gone
(`os.path.exists` → False).

### G7 suite, lint and canary at C3 — one pytest process at a time

    python3 -m pytest tests/ui_contracts/ -q
    REAL EXIT CODE: 0
    588 passed, 4 skipped in 5.45s
    lines matching ^FAILED: 0

EXTRACTOR-BLINDNESS CONTROL: the same counter run over a control string whose
first line is `FAILED tests/control.py::test_control - AssertionError` returns
**1**, a non-zero count. The zero above is therefore a measurement, not a blind
extractor.

    python3 -m pytest tests/ui_contracts/test_diff_surface_css.py --collect-only -q
    REAL EXIT CODE: 0
    8 tests collected in 0.01s

Full node-id inventory, from `--collect-only` (never regexed out of `-v`):

    tests/ui_contracts/test_diff_surface_css.py::TestDiffSurfaceStylesheet::test_stylesheet_exists
    tests/ui_contracts/test_diff_surface_css.py::TestDiffSurfaceStylesheet::test_diff_line_is_a_three_column_grid
    tests/ui_contracts/test_diff_surface_css.py::TestDiffSurfaceStylesheet::test_diff_line_font_is_the_binding_mono_size
    tests/ui_contracts/test_diff_surface_css.py::TestDiffSurfaceStylesheet::test_added_and_removed_lines_are_two_different_colours
    tests/ui_contracts/test_diff_surface_css.py::TestDiffSurfaceStylesheet::test_ligatures_are_off_in_the_diff_line_rule
    tests/ui_contracts/test_diff_surface_css.py::TestDiffSurfaceStylesheet::test_ligatures_are_off_in_the_hunk_head_rule
    tests/ui_contracts/test_diff_surface_css.py::TestDiffSurfaceStylesheet::test_no_font_shorthand_follows_the_ligature_declaration
    tests/ui_contracts/test_diff_surface_css.py::TestDiffSurfaceStylesheet::test_every_referenced_token_is_defined_in_the_shipped_sheet

The seven names R9 shipped are all present and unchanged; the eighth is the new
one.

    python3 -m ruff check tests/ui_contracts/test_diff_surface_css.py
    REAL EXIT CODE: 0
    All checks passed!

Run under the repository's own configuration; no `--isolated`.

    python3 -m pytest tests/cli/test_golden_path.py -q
    REAL EXIT CODE: 0
    42 passed in 20.72s

The base figure named by the block is `42 passed`. Measured `42 passed`. NO
DIFFERENCE.

### G8 structure, artifacts and the Open PR Gate at C4

`git diff --name-only c777fe83..abfd41a3` (exit 0):

    .agent/authored/f037-r10.md
    .agent/last_block.md
    .agent/live_review.md
    .agent/plan.md
    tests/ui_contracts/test_diff_surface_css.py

- RESIDUE actual minus expected: **[]**
- RESIDUE expected minus actual: **[]**

(Expected = the change set minus `.agent/handoff.md`, which C5 writes after C4.)

Scope restrictions:

| Scope | `git diff --stat` payload | EMPTY |
|---|---|---|
| `packages/` | `''` | **True** |
| `docs/` | `''` | **True** |
| `apps/` | `''` | **True** |

`apps/` empty confirms constraint 4: `DiffView.module.css` was READ by C3 and by
G6's mutation, and is unmodified on disk.

    git diff --stat c777fe83..abfd41a3 -- tests/
     tests/ui_contracts/test_diff_surface_css.py | 32 +++++++++++++++++++++++++++++
     1 file changed, 32 insertions(+)

Only the one file, as ordered.

Per-commit insertions from `git diff --numstat`, with parent counts:

| Commit | SHA | Insertions | Parents | Under 500 |
|---|---|---|---|---|
| C0a | fc5d0a77 | 301 | 1 | True |
| C0b | c8d8c860 | 278 | 1 | True |
| C1 | 899b358a | 25 | 1 | True |
| C2 | d60de8af | 4 | 1 | True |
| C3 | 13fee147 | 32 | 1 | True |
| C4 | abfd41a3 | 2 | 1 | True |

Marker sweep of `^<<<SLICE ` and `^<<<END `:

| Target | `^<<<SLICE ` | `^<<<END ` |
|---|---|---|
| `.agent/plan.md` at C1 (`899b358a`) | 0 | 0 |
| `.agent/live_review.md` at C4 (`abfd41a3`) | 0 | 0 |
| the C0a blob `.agent/authored/f037-r10.md` | 4 | 4 |

The C0a figures are greater than zero, so the two zeros above are a measurement
by a working counter, not a silent miss.

- `git ls-files .remedy-wt` line count: **0** — nothing from the scratch
  directory is tracked.
- Open PR Gate, verbatim:

      gh pr list --state open --json number,headRefName,baseRefName,isDraft
      REAL EXIT CODE: 0
      []

  NO open PR. Nothing to merge, no blocker, no branch created.

### Push

The block orders the push of `feature/f037-rendered-diff-viewer` AFTER C5 and
places it outside every gate above. A commit cannot record the exit code of a
command that runs after it, so no figure is written here; the push and its real
exit code are reported in the round report that accompanies this handback.

## Authored-text proofs

Every reviewer-authored text applied this round was extracted PROGRAMMATICALLY
from the COMMITTED `.agent/authored/f037-r10.md` blob by its marker lines — never
retyped, never reflowed, never trimmed — and compared disk-to-disk after
application:

| Slice | Applied to | Comparison | Result |
|---|---|---|---|
| PLANF037R10 | `.agent/plan.md` (whole-file replacement) | on-disk bytes == slice bytes | **True** (negative control against slice-minus-trailing-newline: **False**) |
| GATER9 | `.agent/live_review.md` (append) | `disk == before + b"\n" + slice` | **True** (negative control: **False**) |
| FIND0720 | `.agent/live_review.md` (append) | `disk == before + b"\n" + slice` | **True** (negative control: **False**) |
| DONE0720 | `.agent/live_review.md` (append) | `disk == before + b"\n" + slice` | **True** (negative control: **False**) |

The C3 production code is NOT a slice: per constraint 2 it was described by the
SPEC and written by the worker in the idiom of the file, after reading the whole
of `tests/ui_contracts/test_diff_surface_css.py` (131 lines at the base) and the
whole of `apps/ui/src/components/diff/DiffView.module.css`.

## Item status

| Item | Status | Reason |
|------|--------|--------|
| C0a save the block | done | |
| C0b mirror into last_block | done | |
| C1 the plan | done | |
| C2 the R9 verdict and R-0720 | done | |
| C3 the ordering assertion | done | S1–S5 all implemented; red-proved |
| C4 the resolution | done | |
| C5 the handback | done | |
| S1 `_declaration_offset` | done | negative lookbehind `(?<![-\w])`, returns -1 when absent |
| S2 `_font_shorthand_after` | done | same guard; docstring carries the WHY |
| S3 the new test, both selectors | done | `.diffLine` and `.hunkHead`; both messages name the selector |
| S4 consequence + `assets_spec.md` section 2 citation | done | cited in the file's existing register |
| S5 nothing else changed | done | diff is +32/-0, pure additions |
| G1 hygiene | run | exit codes above |
| G2 transport | run | same blob |
| G3 extraction and caps | run | 301 total / 250 prose |
| G4 the plan | run | 48 lines, byte-equal |
| G5 the record | run | three appends, six readers, three negative controls |
| G6 the red-proof | run | RED at exit 1 at C3, GREEN at exit 0 at base |
| G7 suite, lint, canary | run | 0, 0, 0, 0 |
| G8 structure and Open PR Gate | run | zero residue both ways |

## Deviations & assumptions

The block's ordered commit sequence C0a → C0b → C1 → C2 → C3 → C4 → C5 was
followed exactly: seven commits, one each, in that order, no extra commit, none
dropped, none reordered.

1. **`git worktree remove` was invoked twice; the second call returned exit
   128.** The first call (the real one) succeeded silently and deleted
   `.remedy-wt/g6-r10`. My cleanup-reporting script then re-issued the same
   command in order to capture an exit code for the transcript, and got exit 128
   because the worktree was already gone. This is an artifact of my own
   reporting, not a failed cleanup: `git worktree list` is 1 line, `git worktree
   prune` exited 0, and the directory does not exist. I am declaring it rather
   than quietly reporting only the successful call.
2. **The base-guard negative control reused the same disposable worktree.**
   The block orders "the SAME mutation against the file as it stands at the BASE
   commit `c777fe83`" without naming a mechanism. Rather than add a second
   worktree, I restored the mutated file in `.remedy-wt/g6-r10`, verified the
   restore byte-identical, `git checkout --detach c777fe83` inside that same
   worktree, confirmed HEAD and confirmed the new test is absent from the guard
   there, then applied the identical mutation. Constraint 8 is satisfied — every
   mutation ran in a disposable worktree under `.remedy-wt/`, never in the
   primary checkout.
3. **No numeral in the block disagreed with any measurement.** The two figures
   the block predicted — `.agent/live_review.md` at 1176292 bytes at the base,
   and the canary at `42 passed` — were both measured exactly. `.agent/plan.md`
   measures 48 lines, strictly under the binding <50; the block asserts no
   competing figure for it. No slice was edited for any reason.
4. **`tests/ui_contracts/` moved from 587 to 588 passed.** The block predicts no
   figure here. The delta is exactly the one test C3 adds; the 4 skips are
   unchanged.
5. **Assumption, stated rather than assumed silently:** the SPEC's "same
   left-boundary guard" is implemented as the negative lookbehind `(?<![-\w])`,
   copied from the existing `_declaration`. The right boundary of the `font`
   shorthand needs no separate guard because the pattern requires `font` to be
   followed by optional whitespace and a `:` — `font-size` and
   `font-feature-settings` are excluded by the `-` that follows their `font`.
   This is verified behaviourally, not merely argued: `.hunkHead`, which carries
   `font-size` and `font-feature-settings` and NO shorthand, is green in the
   control and stays green under the `.diffLine` mutation.
6. **No frontend code was written and no frontend runner was attempted.**
   Constraint 3 holds: no `.ts`, `.tsx`, `.jsx` or React component this round.
7. **No `.agent/STOP` appeared** at either reading, so no G6-guardrail stop was
   triggered. `.agent/candidates.md` was not touched; no id other than `R-0720`
   was registered or resolved.

## Next

The planner/reviewer reviews `c777fe83..HEAD` and issues the R10 verdict, then
authors R11, which closes T001's last named corpus shape — the huge diff — per
`.agent/plan.md` Next Steps 1. Phase 1 rule 1 (`.agent/STOP`) is read before
rule 2 (the Open PR Gate), which currently reports `[]`.
