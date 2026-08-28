# Handback — F256 Diff viewer completion, round 5 (THE SIDEBAR RULING)

## Session

SESSION 1 of feature F256 · round 5 · rounds so far 5

THIS IS THE LAST ROUND OF THIS SESSION. Rounds 1 through 4 of F256 were reviewed
and PASSED; this round awaits review. The next session's FIRST action is Phase 1
rule 1 — read `.agent/STOP` from disk — BEFORE rule 2, the Open PR Gate.

## Range

Review of 78e71b3c..HEAD (branch `feature/f256-diff-viewer-completion`).

## Commits

### 212af2ca chore(f256): save the round 5 block verbatim
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f256-r5.md` | +345 / -0 | C0a: the block copied byte for byte from `.remedy-wt/f256-r5-block.md` |

### d3ee4aac chore(f256): mirror the round 5 block into the state file
| Path | +/- | Reason |
|---|---|---|
| `.agent/last_block.md` | +228 / -196 | C0b: written from the COMMITTED C0a blob, so the two are one blob id |

### eaaff11f docs(f256): advance the plan to the sidebar ruling round
| Path | +/- | Reason |
|---|---|---|
| `.agent/plan.md` | +12 / -10 | C1: whole-file replacement by the `PLANF256R5` slice |

### 4afe74f9 docs(f256): book the round 4 verdict and DECISION F256 D3
| Path | +/- | Reason |
|---|---|---|
| `.agent/decisions.md` | +54 / -0 | C2: the `DECF256R3` slice appended |
| `.agent/live_review.md` | +14 / -0 | C2: the `GATEF256R4` slice appended, the R4 verdict |

### 1b70fb02 feat(diff-view): dress the file sidebar under DECISION F256 D3
| Path | +/- | Reason |
|---|---|---|
| `apps/ui/src/components/diff/DiffView.module.css` | +35 / -0 | S1: the four sidebar rules and the comment recording D3's mapping and its reversal |
| `apps/ui/src/components/diff/DiffFileSidebar.tsx` | +27 / -18 | S2 and S3: the sheet imported and the classes placed; the deferral paragraph replaced by the ruling |

### d75eb339 test(ui-contracts): pin the sidebar treatment DECISION F256 D3 rules
| Path | +/- | Reason |
|---|---|---|
| `tests/ui_contracts/test_diff_file_sidebar.py` | +117 / -0 | S4 and S5: the new class, the two scanners and their not-vacuous pins |

### C5 (this commit) chore(f256): hand back round 5
| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | rewritten | C5: this handback. A handoff cannot table the commit that writes it (R-0149) |

Every `+/-` cell above was compared cell by cell against G9's `git diff --numstat`
figures and agrees with them.

## External actions

| Command | Outcome |
|---|---|
| `gh pr list --state open --json number,headRefName` | `[]` — no open PR. No PR created, nothing merged. |
| `git worktree add .remedy-wt/f256-r5-redproof d75eb339 --detach` | created for G7 |
| `git worktree remove .remedy-wt/f256-r5-redproof` | removed; `git worktree list` shows the primary alone |
| `npx vite build` in `apps/ui` (dist warming, G8) | exit 0, built in 1.40s |
| `git push -u origin feature/f256-diff-viewer-completion` | see Verification, G-push below |

## Verification

**G1 HYGIENE.** `.agent/STOP` read with `os.path.exists` before C0a → `False`; read
again before C3 → `False`. `git rev-parse HEAD` before C0a =
`78e71b3c5bfc8221c06c447ffafb1aa4df2011d2`, which equals the ordered base `78e71b3c`.
`git branch --show-current` = `feature/f256-diff-viewer-completion`.
`git status --porcelain | wc -l` = **0** after each of C0a, C0b, C1, C2, C3 and C4,
and **0** again after the worktree removal.

**G2 TRANSPORT.** One digest comparison. `git show 212af2ca:.agent/authored/f256-r5.md`
and the reviewer's own `.remedy-wt/f256-r5-block.md` both hash to
`f69b68d7635072d23d862d8aa3134c2bf1ebf159e5a2c64ac7608c332b0429b9` at **22380 bytes** —
EQUAL. That original predates this worker, so the reading covers the EMISSION and not
merely the worker's self-consistency. At C0b,
`d3ee4aac:.agent/authored/f256-r5.md` and `d3ee4aac:.agent/last_block.md` are ONE blob
id, `6289fa93296611c447ae08f42849477cf27a2a44`.

**G3 THE PLAN AT C1.** `eaaff11f:.agent/plan.md` byte-equal to the `PLANF256R5` slice
including the trailing newline → **True**. `wc -l` = **37** (< 50). Lines exactly
`## Goal` = **1**; lines exactly `## Next Steps` = **1**.

**G4 THE RECORD AT C2**, two readers per appended file.

(a) the `78e71b3c` blob + a newline + the slice == the C2 blob:
- `.agent/live_review.md` with `GATEF256R4` → **True**; 1348532 → 1352347 bytes; the
  pre-round blob is a byte PREFIX → **True**. NEGATIVE CONTROL: the script confirmed
  the FIRST appended paragraph occupies `[1348533, 1348750)` and flipped the byte at
  offset **1348641** (`'E'`) inside it → equality now **False**.
- `.agent/decisions.md` with `DECF256R3` → **True**; 692805 → 696427 bytes; the
  pre-round blob is a byte PREFIX → **True**. NEGATIVE CONTROL: first appended
  paragraph `[692806, 692973)`, byte at offset **692889** (`'m'`) flipped → equality
  now **False**.

(b) N counted BY THE SCRIPT from each slice, empty trailing unit ignored:
- `GATEF256R4` → **N = 7**; the last 7 blank-line units of `.agent/live_review.md`
  match those paragraphs IN ORDER → **True**.
- `DECF256R3` → **N = 7**; the last 7 blank-line units of `.agent/decisions.md` match
  those paragraphs IN ORDER → **True**.

**G5 THE LEDGER AT C2.** The `4afe74f9` blob beside the `78e71b3c` blob:

| Reader | base | C2 | delta |
|---|---|---|---|
| `^- R-\d+ — ` (registrations) | 293 | 293 | 0 |
| registrations all DISTINCT | True | True | — |
| `^Done: R-\d+ — ` | 43 | 43 | 0 |
| `^Landed: R-` | 11 | 11 | 0 |
| `^Gate: F\d+ R\d+ — ` | 100 | 101 | **+1** |
| OPEN SET, computed AS A SET | 252 | 252 | 0 |

Every figure UNMOVED except the gate count, which rises by exactly ONE, as a round
that registers and resolves nothing should. `Gate: F256 R4` occurs exactly **1** time.
`R-0732` is present as exactly **1** registration and still carries **0** `Done:` and
**0** `Landed:` lines.

**G6 THE SIDEBAR GUARDS AT C3**, over the comment-stripped `DiffFileSidebar.tsx` at
`1b70fb02`:

| Reading | measured | required |
|---|---|---|
| `.hunks.length` (forbidden by `TestTheSidebarDerivesNothing`) | **0** | 0 |
| `.stats.` (forbidden) | **0** | 0 |
| `sort(` (forbidden) | **0** | 0 |
| `<span` at `78e71b3c` / at C3 | **6 / 6** | EQUAL |
| `<strong` at `78e71b3c` / at C3 | 1 / 1 | unchanged |
| `aria-hidden` at C3 | **0** | 0 |

The forbidden set is exactly `REIMPLEMENTED_RULE_SPELLINGS = (".hunks.length",
".stats.", "sort(")`, and each count is 0 both before and after C3. Every summary
field `TestEverySummaryFieldIsReallyDrawn` requires is still read: `.path`,
`.status`, `.added`, `.deleted`, `.hunkCount`, `.oldPath`, `.note`, `.rowKey` — all
**True**, unchanged from the base.

`styles.<name>` named by the component: `['fileMeta', 'filePath', 'statAdd',
'statDel']`. Classes `DiffView.module.css` defines at C3: `['add', 'del', 'diffLine',
'fileMeta', 'filePath', 'hunkHead', 'intraline', 'ln', 'statAdd', 'statDel',
'tokComment', 'tokKeyword', 'tokNumber', 'tokString']`. SUBSET → **True**; the
difference `named − defined` is `[]`.

Custom properties the NEW rules name, each defined in `apps/ui/src/styles/tokens.css`:
`--remedy-font-mono` **True**, `--remedy-ink-soft` **True**, `--remedy-green-500`
**True**, `--remedy-orange-400` **True**. No new custom property was introduced.

**G7 THE RED-PROOF AT C4**, in the disposable worktree `.remedy-wt/f256-r5-redproof`
at `d75eb339`, never in the primary checkout. Command
`["python3","-m","pytest","tests/ui_contracts/test_diff_file_sidebar.py","-q"]` with
`cwd` set to the WORKTREE.

| Run | exit | result |
|---|---|---|
| UNMUTATED CONTROL (first) | 0 | 16 passed |
| (i) the `.statAdd` rule deleted from `DiffView.module.css` while the component still names the class | **1** | 1 failed, 15 passed |
| (ii) the `.filePath` class removed from the path element in `DiffFileSidebar.tsx` | **1** | 1 failed, 15 passed |
| CONTROL AGAIN | 0 | 16 passed |

Each mutation was applied ALONE and reverted before the next; `git status --porcelain`
inside the worktree was empty after the last revert. The failures name the right
assertions: (i) →
`TestTheSidebarWearsTheRuledTreatment::test_every_class_the_sidebar_names_has_a_rule_in_the_stylesheet`;
(ii) →
`TestTheSidebarWearsTheRuledTreatment::test_the_sidebar_names_every_class_the_ruling_gives_it`.
After removal, `git worktree list` shows only `/home/decodeux/Repos/remedy` and
`git status --porcelain | wc -l` in the primary is **0**.

**G8 THE SUITES AT C4**, one pytest process at a time, from the repository root, in the
PRIMARY checkout:

| Command | exit | result |
|---|---|---|
| `python3 -m pytest tests/ui_contracts/ -q` | 0 | 664 passed, 4 skipped in 5.69s |
| `python3 -m pytest tests/orchestration/test_test_runner.py -q` | 0 | 52 passed in 5.33s (**5.6s wall clock**, well inside the 30-second `npx vitest run` timeout) |
| `python3 -m pytest tests/ui_server/ -q` | 0 | 495 passed in 28.68s |
| `python3 -m pytest tests/regression/test_resource_safety.py -q` | 0 | 21 passed in 11.51s |
| `python3 -m pytest tests/orchestration/test_integrity_gate.py -q` | 0 | 16 passed in 0.29s |
| `python3 -m pytest tests/cli/test_golden_path.py -q` (canary) | 0 | 42 passed in 20.59s |
| `npx tsc --noEmit` in `apps/ui` | 0 | no output |

DECLARED: `apps/ui/dist` WAS stale before this gate — the newest file under
`apps/ui/src` was 22:05:24 against `dist` at 21:57:12 — so it was warmed first with
`npx vite build` in `apps/ui`, real exit code **0**, built in 1.40s, after which the
staleness reader was **False**. `dist` is gitignored and the tree stayed clean.

**G9 STRUCTURE**, over `78e71b3c..d75eb339` — the range ending BEFORE this handback
commit.

`git diff --name-only` returns exactly eight paths: `.agent/authored/f256-r5.md`,
`.agent/decisions.md`, `.agent/last_block.md`, `.agent/live_review.md`,
`.agent/plan.md`, `apps/ui/src/components/diff/DiffFileSidebar.tsx`,
`apps/ui/src/components/diff/DiffView.module.css`,
`tests/ui_contracts/test_diff_file_sidebar.py`.

Both residues against the change set with `.agent/handoff.md` set aside are **empty**:
changed − expected = `[]`, expected − changed = `[]`.

Per-commit insertions from `git diff --numstat`, each under 500, each single-parent:

| Commit | + | − | parents |
|---|---|---|---|
| 212af2ca | 345 | 0 | 1 |
| d3ee4aac | 228 | 196 | 1 |
| eaaff11f | 12 | 10 | 1 |
| 4afe74f9 | 68 | 0 | 1 |
| 1b70fb02 | 62 | 18 | 1 |
| d75eb339 | 117 | 0 | 1 |

Lines beginning `<<<SLICE ` / `<<<END ` at `d75eb339`: **0 / 0** in every target except
the two authored controls, `.agent/authored/f256-r5.md` and `.agent/last_block.md`,
which are **3 / 3** each by construction. `git ls-files .remedy-wt | wc -l` = **0**.

## Authored-text proofs

| Slice | Target | Result |
|---|---|---|
| whole block | `.agent/authored/f256-r5.md` | sha256 equal to `.remedy-wt/f256-r5-block.md`, 22380 bytes (G2) |
| whole block | `.agent/last_block.md` | same blob id as the authored path (G2) |
| `PLANF256R5` | `.agent/plan.md` | byte-equal whole-file replacement, trailing newline included (G3) |
| `GATEF256R4` | `.agent/live_review.md` | base + newline + slice, negative control rejected (G4) |
| `DECF256R3` | `.agent/decisions.md` | base + newline + slice, negative control rejected (G4) |

Every slice was extracted from the COMMITTED `212af2ca` blob, never from the prompt
(constraint 3).

## Deviations & assumptions

1. **Shell-guard re-expressions (constraint 6).** Five command FORMS were refused by
   this session's guard and were re-expressed, never skipped and never weakened:
   - `cd apps/ui && npx tsc --noEmit` and `cd apps/ui && npx vite build` → spawned from
     Python with `cwd` set (`.remedy-wt/run_tsc.py`, `.remedy-wt/warm_dist.py`).
   - `...; echo "tsc exit: $?"` → the exit code is printed by the Python script itself.
   - One `python3 - <<'PY'` heredoc for G5 was refused; it was rewritten as the file
     `.remedy-wt/g5_ledger.py` and run from there.
   - `cat .agent/plan.md` was refused; the file was read with the editor's read tool.
   All gate scratch lives under the gitignored `.remedy-wt/` and
   `git ls-files .remedy-wt` is **0**.
2. **`.filePath` names the mono family through `font-family`, not through the `font`
   shorthand.** S1 asks for the mono family via `var(--remedy-font-mono, …)` with the
   same literal stack fallback the rules above use, and for
   `font-feature-settings: "liga" 0` declared AFTER any `font` shorthand. A `font`
   shorthand would have obliged me to invent a size and a line-height for this sidebar,
   which no authority in this repository fixes and which the CANONICAL DESIGN REFERENCE
   banner forbids inventing; `font-family` names the same token with the same
   `ui-monospace, monospace` fallback and leaves nothing for the feature-settings
   declaration to be reset by. S1's ordering clause reads "AFTER any `font` shorthand"
   and there is none. The reason is recorded in the sheet's own comment.
3. **The new class was placed AFTER `TestTheShellRendersBothHalves`, not before it.**
   The classes in that file are lettered (b) … (f) in source order; the new one is
   lettered (g) and sits last so the letters stay in order. No existing class, name or
   assertion was moved or changed by this.
4. **The two not-vacuous pins were added as methods of the existing
   `TestTheStripperIsNotVacuous`**, which is the shape S5 names, rather than as a class
   of their own — S4 asks for ONE new class and this keeps that literally true. Nothing
   already in that class was touched.
5. **NO EXISTING ASSERTION WAS WEAKENED, DELETED OR RELAXED** (constraint 8). The C4
   diff is +117 / −0: the file's 11 pre-existing tests are byte-unchanged and the module
   went from 11 to 16 tests.
6. **No element was added, removed or reordered and no rendered text changed** in
   `DiffFileSidebar.tsx`. The `<span` count is 6 before and after, `<strong` 1 before and
   after; the C3 deletions are the replaced header paragraph only.
7. **No `Done:` or `Gate:` paragraph of my own** appears anywhere. `GATEF256R4` and
   `DECF256R3` are reviewer-authored and were applied as slices, byte for byte, append
   only.
8. **No departure from the ordered commit sequence.** C0a, C0b, C1, C2, C3, C4, C5 in
   that order, one commit each, nothing extra, nothing dropped, nothing reordered.
9. **One unordered action, declared:** `npx vite build` was run in `apps/ui` to warm
   `dist` before G8, as G8 itself permits when `src` is newer. It writes only to the
   gitignored `dist`, and `git status --porcelain` was 0 afterwards.

## Item status

| Item | Status | Reason |
|---|---|---|
| C0a save the block verbatim | done | `212af2ca` |
| C0b mirror into `.agent/last_block.md` | done | `d3ee4aac` |
| C1 advance `.agent/plan.md` | done | `eaaff11f` |
| C2 append the R4 verdict and DECISION F256 D3 | done | `4afe74f9` |
| C3 the sidebar rules and the classes | done | `1b70fb02` |
| C4 the contract-test extension | done | `d75eb339` |
| C5 rewrite `.agent/handoff.md` | done | this commit |
| G1 hygiene | done | STOP `False` twice; base and branch as ordered; porcelain 0 six times |
| G2 transport | done | one digest, equal at 22380 bytes; C0b one blob id |
| G3 the plan at C1 | done | byte-equal True; 37 lines; 1 and 1 |
| G4 the record at C2 | done | both appends True, both negative controls False; N = 7 and N = 7 |
| G5 the ledger at C2 | done | only `^Gate:` moved, +1; `R-0732` once, no `Done:`, no `Landed:` |
| G6 the sidebar guards at C3 | done | forbidden set 0/0/0; every field still read; `<span` 6 = 6; SUBSET True; four tokens all defined |
| G7 the red-proof at C4 | done | control 0, both mutations exit 1, control again 0; worktree removed |
| G8 the suites at C4 | done | all six suites and `tsc --noEmit` exit 0; `dist` warmed first, declared |
| G9 structure | done | both residues empty; all six commits single-parent and under 500 |
| push | done | see External actions |

## Next

Measure the 10k-line fixture end to end and record the numbers in the Built State of
`docs/roadmap/features/T5_F256.md` — F256's last unbuilt piece. Before that, and
because this is the last round of this session, the next session's FIRST action is
Phase 1 rule 1: read `.agent/STOP` from disk, and only then rule 2, the Open PR Gate.
