# Handoff — F037 Rendered diff viewer, round 20

## Session

SESSION 5 of feature F037 · round 20 · rounds so far 20.

Round 20 of the 25-round soft limit and session 5 of 7 — approaching both, past
neither, so no scope report is owed yet. This was the LAST delegated round of
session 5.

## Range

Review of `fe3f1179..HEAD`.

## Commits

### 49cdbff4 docs(agent): save the F037 R20 block
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f037-r20.md` | +375/-0 | C0a, the block saved byte for byte |

### 05df738b docs(agent): mirror the F037 R20 block
| Path | +/- | Reason |
|---|---|---|
| `.agent/last_block.md` | +249/-239 | C0b, the same bytes at the mirror path |

### f0e1ffeb docs(agent): set the plan for F037 R20
| Path | +/- | Reason |
|---|---|---|
| `.agent/plan.md` | +23/-25 | C1, full rewrite from the PLANF037R20 slice |

### 161dc2c9 docs(agent): record the R19 gate, two resolutions and two findings
| Path | +/- | Reason |
|---|---|---|
| `.agent/live_review.md` | +14/-0 | C2, GATER19, DONE725B, DONE726, FINDING727, FINDING728 |

### 13904147 docs(ui): tell the diff view's reader who mounts it
| Path | +/- | Reason |
|---|---|---|
| `apps/ui/src/components/diff/DiffView.tsx` | +11/-8 | C3, SPEC S1, comment only — no code changed |
| `.agent/live_review.md` | +2/-0 | C3, the `Landed: R-0727` line per SPEC S6 |

### 5897d2c8 test(ui-contracts): count the collapse threshold as a whole number
| Path | +/- | Reason |
|---|---|---|
| `tests/ui_contracts/test_diff_view_model.py` | +9/-1 | C4, SPEC S2, the anchored pattern |
| `.agent/live_review.md` | +2/-0 | C4, the `Landed: R-0728` line per SPEC S6 |

### 1d29033c test(ui-contracts): pin the diff entry point at popover level
| Path | +/- | Reason |
|---|---|---|
| `tests/ui_contracts/test_diff_viewer_mount.py` | +67/-0 | C5, SPEC S3, the R-0726 placement gate |

### b2658466 feat(ui): decide which rows a virtualized diff draws
| Path | +/- | Reason |
|---|---|---|
| `apps/ui/src/api/diffViewModel.ts` | +109/-0 | C6, SPEC S4, the windowing rule |
| `apps/ui/src/api/diffViewModel.test.ts` | +200/-0 | C6, SPEC S5, the new `describe` |

### C7 (this commit) docs(agent): hand back F037 R20
| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | rewrite | C7, this handback; a handoff cannot table the commit that writes it (R-0149 pattern) |

## External actions

- `git worktree add .remedy-wt/g6 b2658466` — created, detached at `b2658466`.
- `git worktree remove --force .remedy-wt/g6` then `git worktree prune` — removed;
  `git worktree list` shows the primary checkout alone.
- `gh pr list --state open --json number,headRefName,baseRefName,isDraft` → `[]`.
- `git push -u origin feature/f037-rendered-diff-viewer` after C7.
- No PR created, nothing merged, no history rewritten.
- DENIED BY THIS SESSION'S GUARD, reported rather than routed around:
  `npx vitest run`, `apps/ui/node_modules/.bin/vitest run`, and
  `cp -a apps/ui/node_modules .remedy-wt/g6/apps/ui/node_modules`.

## Verification

- **G1 HYGIENE** — `.agent/STOP` ABSENT before C0a and ABSENT again immediately
  before C7. `git rev-parse HEAD` before C0a = `fe3f1179bff1c10226abb3de04628d20a59db1f8`,
  equal to BASE. `git branch --show-current` = `feature/f037-rendered-diff-viewer`.
  `git status --porcelain | wc -l` after each of C0a, C0b, C1, C2, C3, C4, C5, C6 = 0, 0, 0, 0, 0, 0, 0, 0.
- **G2 TRANSPORT** — committed C0a blob: 31941 bytes, 375 lines, sha256
  `aa59eaffe0e1754662c91be15745e6cbe8f28ee2797b3153ecad72d8847c3101`. All three
  equal the readings the delegation named. `git rev-parse 05df738b:.agent/authored/f037-r20.md`
  and `git rev-parse 05df738b:.agent/last_block.md` are ONE blob
  `c442a90f33feda64fd1c5d334063984dfd342348`.
- **G3 EXTRACTION AND CAPS** — content lines: PLANF037R20 47, GATER19 5,
  DONE725B 1, DONE726 1, FINDING727 1, FINDING728 1. CONTENT 56, TOTAL 375,
  PROSE 319. TOTAL <= 490 True; PROSE <= 400 True.
- **G4 THE PLAN AT C1** — byte equality of PLANF037R20 with
  `git show f0e1ffeb:.agent/plan.md` including the trailing newline: True.
  Negative control (slice minus its trailing newline): False. `wc -l` 47,
  strictly under 50: True. Lines exactly `## Goal`: 1. Lines exactly
  `## Next Steps`: 1.
- **G5 THE RECORD AT C2** — reader (a) pre-round blob `fe3f1179:.agent/live_review.md`
  joined to the five slices in Bundle order with exactly one newline before each
  equals `161dc2c9:.agent/live_review.md`: True. Reader (b) N = 7 units, last 7
  units equal the five slices' units in order: True. Negative control flipping one
  byte inside GATER19's FIRST paragraph: reader (a) False, reader (b) False.
  Pre-round blob is a byte PREFIX of the committed one: True. Line-anchored over
  the committed file, base figure in brackets: `^- R-\d+ — ` 289 [287];
  `^Done: R-\d+ — ` 37 [35]; `^Landed: R-` 4 [4]; `^Gate: F\d+ R\d+ — ` 90 [89];
  open set 254 [253]; every registered id distinct True. The open set rose by 1
  rather than falling: R-0727 and R-0728 registered (+2) and R-0726 newly named by
  a `Done:` line (-1), while R-0725 was ALREADY named by a `Done:` line at base
  (its partial resolution), so its full resolution removes nothing further.
  `^Landed: R-` is 5 at C3 (`13904147`) and 6 at C4 (`5897d2c8`), as ordered.
- **G6 THE RED-PROOFS** — disposable worktree `.remedy-wt/g6` at the C6 tree
  `b2658466`, `__pycache__` purged before every run, `python3 -B` throughout.
  UNMUTATED CONTROL over the five named files: exit 0, `54 passed in 0.30s`,
  before any mutation and again after the last restore (exit 0, `54 passed`).
  UNIQUENESS, taken by the worker per R-0629, each count in its own file BEFORE
  editing: the `{task && onOpenDiff && (` button block in `DetailPopover.tsx` 1;
  the `<ul className={styles.fileList}>` section tail it is re-anchored to 1; the
  two-line anchored-pattern form in `test_diff_view_model.py` 1;
  `totalRows <= DIFF_VIRTUAL_SCROLL_THRESHOLD_ROWS` in `diffViewModel.ts` 1;
  `: Math.min(totalRows, first + visible + overscan);` in `diffViewModel.ts` 1;
  `const transcribed` in `diffViewModel.ts` 0 before the addition. No string
  needed extending. Every mutation restored to its pre-mutation sha256
  (`git checkout -- .` in the worktree, shas re-read and equal each time).
  - **(c)** button moved back inside the `changedFiles` section, exactly R18's
    placement: **exit 1**, `1 failed, 53 passed in 0.32s`, failing
    `tests/ui_contracts/test_diff_viewer_mount.py::TestTheEntryPointSitsAtPopoverLevel::test_the_entry_point_is_outside_and_after_the_changed_files_section`.
    RED as required — the C5 gate really catches the move.
  - **(i)** C4's anchored pattern reverted to the bare `.count(literal)` form AND
    `const transcribed = 200;` added to `diffViewModel.ts`: **exit 1**,
    `1 failed, 53 passed in 0.32s`, failing
    `tests/ui_contracts/test_diff_view_model.py::test_collapse_threshold_literal_occurs_exactly_once`.
    C4 anchored the check rather than removing it.
  - **(g)** and **(h)** — NOT MEASURABLE; see deviation 1. Measured readings:
    the vitest-bearing node is **exit 1 UNMUTATED** in the worktree, exit 1 under
    (g) and exit 1 under (h), all three failing identically with
    `ERR_MODULE_NOT_FOUND` before any test runs. Control and both mutations give
    the same exit code, so the proof has no discriminator and is VACUOUS. The
    mutations themselves applied cleanly at count 1 each and were restored.
  - SPEC S2's three ordered readings all reproduce: the repair alone leaves the
    guard GREEN at `3 passed` (`5897d2c8`); the repair plus the `2000` constant is
    still `3 passed` (`b2658466`); and with the anchor left in place, a bare
    `200` transcribed into the module is **exit 1** on
    `test_collapse_threshold_literal_occurs_exactly_once` — the anchor removed the
    false positive without weakening what the guard was for.
- **G7 SUITES, TYPES, LINT AND CANARY AT C6** — primary checkout, one pytest
  process at a time, base figure in brackets:
  - `python3 -m pytest tests/ui_contracts/ -q` → exit 0, `642 passed, 4 skipped in 5.89s` [641 passed, 4 skipped]
  - `python3 -m pytest tests/ui_server/ -q` → exit 0, `495 passed in 32.72s` [495 passed]
  - `python3 -m pytest tests/orchestration/test_test_runner.py -q` → exit 0, `52 passed in 5.43s` [52 passed]
  - `python3 -m pytest tests/docs/ -q` → exit 0, `295 passed in 0.44s` [295 passed]
  - `python3 -m ruff check tests/ui_contracts/test_diff_view_model.py tests/ui_contracts/test_diff_viewer_mount.py` → exit 0, `All checks passed!`
  - canary `python3 -m pytest tests/cli/test_golden_path.py -q` → exit 0, `42 passed in 20.53s` [42 passed]
  - The typescript node inside `tests/ui_server/` **PASSED**, it did not SKIP:
    `tests/ui_server/test_dashboard_contract.py -k "typescript or tsc or noEmit"`
    → exit 0, `1 passed, 73 deselected in 2.10s`, `-rs` reporting no skip reason.
  - `tests/orchestration/test_test_runner.py` is the node that runs
    `npx vitest run` and it is exit 0, so vitest itself exited 0 over
    `src/**/*.test.ts`, which includes the edited `diffViewModel.test.ts`. THE
    VITEST TEST TOTAL IS NOT REPORTABLE and the new `describe`'s execution is not
    DIRECTLY observable — see deviation 2. What IS measured: the same node run in
    a tree without `apps/ui/node_modules` is exit 1, so the node really spawns the
    tool rather than skipping it.
  - SPOT-CHECKS beyond the block, because `.agent/` state was rewritten and
    `.agent/context.md` names four state readers where G7 named two:
    `python3 -m pytest tests/regression/test_resource_safety.py tests/orchestration/test_integrity_gate.py -q`
    → exit 0, `37 passed in 11.62s`.
- **G8 STRUCTURE, ARTIFACTS AND THE OPEN PR GATE AT C6** —
  `git diff --name-only fe3f1179..b2658466` lists exactly the nine non-handoff
  paths of the Change set. ACTUAL MINUS EXPECTED is empty; EXPECTED MINUS ACTUAL
  is `.agent/handoff.md` alone. `git diff --stat` restricted to `packages/` is
  EMPTY. Restricted to `apps/ui/src/components/` it names
  `apps/ui/src/components/diff/DiffView.tsx` and NOTHING ELSE, at
  `1 file changed, 11 insertions(+), 8 deletions(-)` — constraints 3 and 4
  mechanically. Per-commit insertions from `git show --numstat`,
  each under 500: C0a 375, C0b 249, C1 23, C2 14, C3 13, C4 11, C5 67, C6 309;
  each matches the `+/-` column of the `## Commits` table above cell by cell.
  Lines matching `^<<<SLICE ` or `^<<<END ` at C6: `.agent/plan.md` 0,
  `.agent/live_review.md` 0, `apps/ui/src/api/diffViewModel.ts` 0,
  `tests/ui_contracts/test_diff_viewer_mount.py` 0; CONTROL over the C0a blob 12,
  non-zero. `git ls-files .remedy-wt | wc -l` = 0.
  `gh pr list --state open --json number,headRefName,baseRefName,isDraft` → `[]`.

## Authored-text proofs

- `.agent/authored/f037-r20.md` at C0a is sha256
  `aa59eaffe0e1754662c91be15745e6cbe8f28ee2797b3153ecad72d8847c3101`, 31941 bytes,
  375 lines — byte-identical to the reviewer's scratch original
  `.remedy-wt/f037-r20-block.md`, measured on disk before C0a and again on the
  committed blob.
- `.agent/last_block.md` at C0b is the SAME GIT BLOB as the authored file
  (`c442a90f33feda64fd1c5d334063984dfd342348`), which is byte equality by
  construction.
- PLANF037R20 extracted programmatically from the committed C0a blob equals
  `f0e1ffeb:.agent/plan.md` byte for byte including the trailing newline; the
  newline-stripped negative control is False.
- GATER19, DONE725B, DONE726, FINDING727 and FINDING728, extracted from the same
  blob and joined to the pre-round `live_review.md` with one newline each, equal
  `161dc2c9:.agent/live_review.md` byte for byte; both negative controls False.
- Every slice was extracted from the committed blob by
  `.remedy-wt/r20_extract.py`, never retyped from the prompt.

## Staleness sweep (constraint 12)

Re-read of every WHY comment in the five source files this round edits. Reported
here; only the one C3 names was repaired.

REPAIRED (C3, `R-0727`): `apps/ui/src/components/diff/DiffView.tsx` no longer
tells its reader the component is unmounted; the replacement names
`DetailPopover`'s `Open diff` button, `RemedyShell`'s open task run and
`loadDiffEnvelope`, all three verified against the files at HEAD. The
`component_spec.md:108` citation in it was read on disk before it was written.

STILL FALSE AT HEAD, REPORTED AND NOT REPAIRED — all four are the SAME defect
class as `R-0727` and all four are in `tests/ui_contracts/test_diff_viewer_mount.py`:

1. Module docstring, lines 3-4: "`DiffView.tsx` has been on disk since F037 R16
   with no caller at all. This round opens the door to it." Present perfect and
   "this round" both date from R18; the component has had a caller since R18's C5.
2. Line 260, an assertion message: "`DiffView.tsx` keeps the zero callers it has
   had since F037 R16." False at HEAD. It prints only on failure, but the
   sentence is still a false claim about the codebase.
3. Line 43, the comment above `DIFF_VIEW_DELEGATED_RULES`: "Constraint 3 of the
   F037 R18 block forbids this round from editing that component at all." "This
   round" is R18; R20's C3 did edit that component's header comment. The four
   delegated-rule assertions the comment describes are unaffected and still hold.
4. Line 369, the `TestTheDrawingHalfIsUnchanged` docstring: "this round MOUNTS
   `DiffView.tsx` and does not edit it." False for the current round for the same
   reason as 3.

Line 317's "the state F037 R16 left behind — a component on disk that nothing
draws" is NOT stale: it describes a past state in the past tense and remains true.

ONE MINOR STALENESS ELSEWHERE: `apps/ui/src/api/diffViewModel.ts:327`, inside the
`DIFF_HUNK_COLLAPSE_THRESHOLD_LINES` comment, still says "the component that WILL
render these rows". `DiffView.tsx` has rendered them since R16 and has been
mounted since R18, so the future tense is stale. Not repaired: the block's change
set permits editing that file, but constraint 12 says repair only the one C3
names, and C3 names `DiffView.tsx`.

## Deviations & assumptions

1. **BLOCK CONTRADICTION — G6(g) and G6(h) cannot be measured, and constraint 10
   already says so.** Constraint 10 states "NO TYPESCRIPT MUTATION RED-PROOF IS
   ORDERED", yet G6 orders exactly two of them, (g) and (h), both in
   `diffViewModel.ts`. Constraint 9 and G6's own header confine every run to a
   disposable worktree. MEASURED, not reasoned: `apps/ui/node_modules` is
   gitignored, so it is absent from a fresh worktree, and the vitest-bearing node
   there is **exit 1 UNMUTATED** with `ERR_MODULE_NOT_FOUND` raised before any
   test file loads. Exit 1 unmutated, exit 1 under (g), exit 1 under (h): there is
   no discriminator, so a red-proof taken that way would be vacuous. The only
   tree with the dependency is the primary checkout, and mutating there is
   forbidden by guardrail G5, constraint 9 and this worker's standing rules, so
   it was not done. Three provisioning routes were attempted and are DENIED by
   this session's command guard: `cp -a` of `node_modules` into the worktree,
   `npx vitest run`, and the local `node_modules/.bin/vitest` binary. Nothing was
   widened, weakened or worked around. The reviewer should note that the block's
   claim that "the GATER16 entry of `.agent/live_review.md` records why every
   route is blind or a startup error" is inexact: GATER16 records the R16 verdict
   and does not discuss this. The reason IS on disk, in the module docstring of
   `tests/ui_contracts/test_diff_view_model.py` and in DECISION F037 D8 — and this
   round has now measured it directly.
2. **The vitest test TOTAL is not reportable.** G7 asks for it and for a statement
   that the new `describe` really EXECUTED. `tests/orchestration/test_test_runner.py::TestVitestFrontendTestFoundation::test_vitest_passes`
   runs vitest under `capture_output=True` and surfaces its stdout ONLY in the
   assertion message, i.e. only on failure; the node is exit 0, so no summary is
   printed. Invoking vitest directly is denied to this session. Making it print by
   inverting that assertion would require editing a test in the primary checkout,
   which G5 forbids, and doing it in the worktree is impossible for the reason in
   deviation 1. What is stated is therefore what is measured: the node is exit 0,
   `52 passed`, so vitest exited 0 over its configured include glob
   `src/**/*.test.ts`, which matches the edited `diffViewModel.test.ts`.
3. **`Done:` was written to `.agent/live_review.md` this round, and that is
   correct.** Constraint 11 and the worker's standing rules forbid the worker
   AUTHORING a `Done:` paragraph. The two `Done:` lines added at C2 are the
   REVIEWER's own slices DONE725B and DONE726, applied byte for byte. The worker
   authored only the two `Landed:` lines SPEC S6 orders, one each at C3 and C4.
4. **The C5 test is one test method, not several.** SPEC S3 says "one test"; the
   non-vacuity assertions the module's own discipline requires were folded into
   that method rather than added to the existing
   `test_every_scanner_finds_its_subject_and_returns_less_than_the_file`
   enumeration, so that no existing test was edited. The new scoper
   `changed_files_guarded_block` therefore proves its own scoping inside the new
   test.
5. **No marker was added to `DetailPopover.tsx`.** SPEC S3 allows naming one if
   pinning the placement requires it. It did not: the component already carries
   the `{changedFiles && ...}` condition, and the guard anchors on that. The
   docstring says so, as SPEC S3 requires.
6. **No departure from the ordered commit sequence.** C0a, C0b, C1, C2, C3, C4,
   C5, C6, C7 were committed in exactly that order, none added, none dropped, none
   reordered. C4 preceded C6 as constraint 6 requires, and the C6 run of
   `test_diff_view_model.py` is `3 passed`, which is that ordering paying off.
7. **Assumption.** `docs/ui/design_reference/component_spec.md:108` and the Design
   line "virtual scrolling >2k lines" of `docs/roadmap/features/T5_F037.md` were
   both read on disk before being cited in code comments, rather than carried from
   the block's prose.

## Item-status table

| Item | Status | Reason |
|---|---|---|
| C0a save the block | done | |
| C0b mirror the block | done | |
| C1 the plan | done | |
| C2 the record | done | |
| C3 the R-0727 comment repair | done | |
| C4 the R-0728 count-anchor repair | done | |
| C5 the R-0726 placement gate | done | |
| C6 the windowing rule and its vitest tests | done | |
| C7 the handback | done | this commit |
| G1 hygiene | done | |
| G2 transport | done | |
| G3 extraction and caps | done | |
| G4 the plan at C1 | done | |
| G5 the record at C2 | done | |
| G6 red-proofs | deviated | (c) and (i) measured RED; (g) and (h) not measurable — deviation 1 |
| G7 suites, types, lint, canary | deviated | every gate run and exit 0; the vitest TOTAL is unreadable — deviation 2 |
| G8 structure, artifacts, PR gate | done | |

## Next

THIS ROUND HAS NO GATE ENTRY ON DISK. `.agent/live_review.md` carries no
`Gate: F037 R20 —` paragraph, because the reviewer writes it and the reviewer is
the NEXT session. Do not read this handback as a verdict; it is a worker report.

The next session's first action, in this order:

1. Re-read `.agent/STOP` from disk — Phase 1 rule 1 of
   `docs/agents/self_drive_protocol.md`, BEFORE rule 2. It was ABSENT at both
   readings this round.
2. The Open PR Gate — `gh pr list --state open --json number,headRefName,baseRefName,isDraft`.
   It was `[]` at C6.
3. Review THIS round at its C6 commit `b2658466`, over the range
   `fe3f1179..b2658466`, re-running the verification independently, and book the
   verdict — plus deviations 1 and 2, which are reviewer-block defects rather than
   worker findings — in the FIRST substantive commit of round 21, per operator
   amendment amend0827-process-diet rule 1.

Then round 21's own work: wire the window into `DiffView` with the perf fixture
Acceptance requires, per `.agent/plan.md`'s Next Steps.
