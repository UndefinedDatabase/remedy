# Handoff — F037 Rendered diff viewer, round 19

## Session

SESSION 5 of feature F037 · round 19 · rounds so far 19.

Round 19 of the 25-round soft limit and session 5 of 7 — approaching both, past
neither, so no scope report is owed yet.

## Range

Review of `0a291411..HEAD`.

## Commits

### 673dcb07 docs(agent): save the F037 R19 step block
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f037-r19.md` | +365/-0 | C0a, the block saved byte for byte |

### 9ab3e879 docs(agent): mirror the F037 R19 block to last_block
| Path | +/- | Reason |
|---|---|---|
| `.agent/last_block.md` | +245/-265 | C0b, the same bytes at the mirror path |

### 6fe9b43a docs(agent): set the plan to the R19 round map
| Path | +/- | Reason |
|---|---|---|
| `.agent/plan.md` | +25/-25 | C1, full rewrite from the PLANF037R19 slice |

### 67781115 docs(agent): record the R18 verdict, R-0725 in part and R-0726
| Path | +/- | Reason |
|---|---|---|
| `.agent/live_review.md` | +10/-0 | C2, GATER18 then DONE725A then FINDING726 |

### 5a37eb0d test(ui-contracts): pin the task-run path ending, not only its segment
| Path | +/- | Reason |
|---|---|---|
| `tests/ui_contracts/test_diff_envelope_door.py` | +13/-3 | C3, SPEC S1 |
| `.agent/live_review.md` | +2/-0 | C3, the `Landed: R-0725` line |

### 7c0d52a8 fix(ui): raise the diff entry point to popover level
| Path | +/- | Reason |
|---|---|---|
| `apps/ui/src/components/detail/DetailPopover.tsx` | +25/-13 | C4, SPEC S2 |
| `.agent/live_review.md` | +2/-0 | C4, the `Landed: R-0726` line |

### 7f591ce9 feat(ui): draw the diff file sidebar and anchor its file rows
| Path | +/- | Reason |
|---|---|---|
| `apps/ui/src/components/diff/DiffFileSidebar.tsx` | +101/-0 | C5, SPEC S3, new |
| `apps/ui/src/components/diff/DiffView.tsx` | +8/-1 | C5, SPEC S4, the `id` anchor |
| `apps/ui/src/components/shell/RemedyShell.tsx` | +11/-1 | C5, SPEC S5, the mount |

### 7e263ea5 test(ui-contracts): gate the file sidebar and the row anchor it jumps to
| Path | +/- | Reason |
|---|---|---|
| `tests/ui_contracts/test_diff_file_sidebar.py` | +340/-0 | C6, SPEC S6, new |

### C7 — this commit
| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | rewrite | C7, this handback; a handoff cannot table the commit that writes it (R-0149) |

Every insertion count above is `git show --numstat` at the named commit and every
one is under 500. The largest is C6 at 340.

## External actions

- `git worktree add .remedy-wt/f037-r19-g6 7e263ea5 --detach` — created for G6.
- `git worktree remove .remedy-wt/f037-r19-g6` then `git worktree prune` — done;
  `git worktree list` afterwards shows the primary checkout alone.
- `gh pr list --state open --json number,headRefName,baseRefName,isDraft` — `[]`.
- `git push -u origin feature/f037-rendered-diff-viewer` — after C7.
- No PR created, nothing merged, no history rewritten, no force push.

## Verification

G1 HYGIENE — exit 0. `.agent/STOP` ABSENT before C0a and ABSENT again immediately
before C7. `git rev-parse` before C0a was `0a29141142785dfdd3d9ab9fc39355e80207ef2f`,
equal to `0a291411`. `git branch --show-current` is
`feature/f037-rendered-diff-viewer`. `git status --porcelain` line count after each
of C0a, C0b, C1, C2, C3, C4, C5 and C6 was 0 — eight readings, all 0.

G2 TRANSPORT — exit 0. Committed C0a blob: 28730 bytes, 365 lines, sha256
`6dad1fd45d087522d29428da793120aa5e3f84af2a3837ab20750c6481f4f7ef`. All three match
the three readings the delegation named. `git rev-parse 9ab3e879:.agent/authored/f037-r19.md`
and `git rev-parse 9ab3e879:.agent/last_block.md` are both
`7d343c0bfd2b5c03be880e34d35c76b70a316f4b` — the same blob.

G3 EXTRACTION AND CAPS — exit 0, on the committed C0a blob. Content lines:
PLANF037R19 49, GATER18 5, DONE725A 1, FINDING726 1. CONTENT 56, TOTAL 365,
PROSE 309. TOTAL <= 490 True. PROSE <= 400 True.

G4 THE PLAN AT C1 — exit 0. PLANF037R19 extracted programmatically from the
committed C0a blob is byte equal to `git show 6fe9b43a:.agent/plan.md` INCLUDING the
trailing newline: True. Negative control against the slice minus its trailing
newline: False. `wc -l` 49, strictly under 50: True. Lines exactly `## Goal`: 1.
Lines exactly `## Next Steps`: 1.

G5 THE RECORD AT C2 — exit 0. Reader (a), pre-round blob + `\n` + GATER18 + `\n` +
DONE725A + `\n` + FINDING726 == `git show 67781115:.agent/live_review.md`: True.
Reader (b), N = 5 blank-line-separated units across the three slices; the last 5
units of the committed file equal those 5 in order: True. Negative control, one byte
flipped inside GATER18's FIRST paragraph (offset 851, `n` -> `N`): reader (a) False,
reader (b) False. Pre-round blob is a byte PREFIX of the committed one: True.
Line-anchored counts, base at `0a291411` -> C2: `^- R-\d+ — ` 286 -> 287;
`^Done: R-\d+ — ` 34 -> 35; `^Landed: R-` 2 -> 2; `^Gate: F\d+ R\d+ — ` 88 -> 89.
Open set (registered ids minus ids named by a `Done:` line) 253 at base and 253 at
C2. Every registered id distinct at both: True. The only id new at C2 is `R-0726`.
`^Landed: R-` measured 3 at C3 and 4 at C4 (see the authored-text proofs below).

G6 THE RED-PROOFS — run in the disposable worktree `.remedy-wt/f037-r19-g6` at the
C6 tree `7e263ea5`, `__pycache__` purged before every run, `python3 -B` throughout,
one mutation at a time, each restored byte-identically to its pre-mutation sha256
before the next (each restore verified True). Node set for every run:
`tests/ui_contracts/test_diff_envelope_door.py tests/ui_contracts/test_diff_file_sidebar.py tests/ui_contracts/test_diff_viewer_mount.py tests/ui_contracts/test_diff_view_render.py`.

- control BEFORE any mutation — exit 0, `50 passed in 0.29s`.
- (a) `remedyApi.ts`, task-run template `/diff?` -> `/diffs?`. Uniqueness reading:
  `task-runs/${encodeURIComponent(taskId)}/diff?` occurs 1x, so it was mutated as
  written. Exit 1, `1 failed, 49 passed`. FAILED
  `test_diff_envelope_door.py::TestTheTaskRunScopeRouteAgrees::test_the_client_addresses_the_task_run_segment`.
  RED, and it was GREEN before C3 — the C3 repair's own proof.
- (b) `remedyApi.ts`, job template `/diff?` -> `/diffs?`. Uniqueness reading:
  `/api/jobs/${job}/diff?` occurs 1x. Exit 1, `1 failed, 49 passed`. FAILED
  `test_diff_envelope_door.py::TestTheJobScopeRouteAgrees::test_the_client_addresses_the_diff_endpoint`.
  Still RED, so C3 did not repair one sibling by breaking another.
- (c) `DetailPopover.tsx`, the "Open diff" button moved back inside the
  `changedFiles` section. Uniqueness readings: the popover-level block occurs 1x and
  the section's `</ul>` + `</section>` ending occurs 1x, so both halves of the move
  were unique. Exit 0, `50 passed in 0.29s`. **GREEN — the mutation was NOT caught.**
  Saying so plainly as the block ordered: this is a true reading about the guard, not
  an adjusted test. The reason is stated as deviation 1 below.
- (d) `DiffFileSidebar.tsx`, `buildDiffFileSummaries(envelope)` replaced by a direct
  walk of `envelope.files`. Uniqueness reading:
  `const summaries = buildDiffFileSummaries(envelope);` occurs 1x. Exit 1,
  `2 failed, 48 passed`. FAILED
  `test_diff_file_sidebar.py::TestTheSidebarDerivesNothing::test_the_sidebar_calls_the_model_builder`
  and `::test_the_sidebar_reimplements_no_rule_of_the_model`.
- (e) `DiffFileSidebar.tsx`, navigation by `summary.path` instead of `summary.rowKey`.
  Uniqueness reading: `onClick={() => goToFileRow(summary.rowKey)}` occurs 1x. Exit 1,
  `3 failed, 47 passed`. FAILED
  `test_diff_file_sidebar.py::TestTheEntryIsARealControl::test_the_entry_is_a_button_with_an_explicit_type`,
  `::TestTheStripperIsNotVacuous::test_both_tag_scanners_find_their_subject` and
  `::TestTheTwoHalvesAgreeOnOneString::test_the_sidebar_navigates_by_the_models_key`.
- (f) `DiffView.tsx`, the file row's `id` deleted, its React `key` left. Uniqueness
  reading: `<div key={row.key} id={row.key}>` occurs 1x. Exit 1, `1 failed, 49 passed`.
  FAILED
  `test_diff_file_sidebar.py::TestTheTwoHalvesAgreeOnOneString::test_the_file_row_carries_a_dom_anchor_holding_the_same_string`.
- control AFTER the last restore — exit 0, `50 passed in 0.29s`.

Every one of these six mutations was run TWICE, in two full independent passes over
the same worktree, and every colour above was identical in both passes. The second
pass existed only because the first pass's node-id extraction was misparsed; no
colour changed.

G7 SUITES, TYPES, LINT AND CANARY AT C6 — primary checkout, ONE pytest process at a
time, no two concurrent.

- `python3 -m pytest tests/ui_contracts/ -q` — exit 0, `641 passed, 4 skipped in 4.31s`
  (base 630 passed, 4 skipped; +11 is this round's new guard).
- `python3 -m pytest tests/ui_server/ -q` — exit 0, `495 passed in 33.17s` (base 495).
- `python3 -m pytest tests/regression/test_named_bugs.py -q` — exit 0,
  `64 passed, 6 skipped in 1.31s` (base 64 passed, 6 skipped).
- `python3 -m pytest tests/orchestration/test_test_runner.py -q` — exit 0,
  `52 passed in 5.37s` (base 52).
- `python3 -m pytest tests/docs/ -q` — exit 0, `295 passed in 0.44s` (base 295).
- `python3 -m ruff check tests/ui_contracts/test_diff_file_sidebar.py tests/ui_contracts/test_diff_envelope_door.py`
  — exit 0, `All checks passed!`.
- canary `python3 -m pytest tests/cli/test_golden_path.py -q` — exit 0,
  `42 passed in 20.64s` (base 42).

THE TYPESCRIPT NODE INSIDE `tests/ui_server/` PASSED — it did NOT skip.
`python3 -m pytest tests/ui_server/test_dashboard_contract.py -q -k "tsc or typescript" -rs`
reported exit 0, `1 passed, 73 deselected in 2.00s`, with no skip line;
`apps/ui/node_modules/.bin/tsc` is present. So `tsc --noEmit` really type-checked
this round's three `.tsx` files — the new `DiffFileSidebar.tsx`, the edited
`DiffView.tsx` and the edited `RemedyShell.tsx` — which is most of this round's gate.

G8 STRUCTURE, ARTIFACTS AND THE OPEN PR GATE AT C6 — exit 0.
`git diff --name-only 0a291411..7e263ea5` lists 10 paths. ACTUAL MINUS EXPECTED is
empty. EXPECTED MINUS ACTUAL is `.agent/handoff.md` alone, as the block requires.
`git diff --stat` restricted to `packages/` is EMPTY, and restricted to
`apps/ui/src/api/` is ALSO EMPTY — constraints 3 and 4 made mechanical.
Per-commit insertions: 365, 245, 25, 10, 15, 27, 120, 340 — each under 500, and each
matches the `+/-` column of the `## Commits` table above cell by cell.
`^<<<SLICE ` plus `^<<<END ` line counts at C6: `.agent/plan.md` 0,
`.agent/live_review.md` 0, `apps/ui/src/components/diff/DiffFileSidebar.tsx` 0,
`tests/ui_contracts/test_diff_file_sidebar.py` 0; CONTROL over the C0a blob 8, which
is non-zero, so the marker scanner is not vacuous. `git ls-files .remedy-wt | wc -l`
is 0. `gh pr list --state open --json number,headRefName,baseRefName,isDraft`
returned `[]` — no open PR.

## Authored-text proofs

- `.agent/authored/f037-r19.md` at C0a: 28730 bytes, 365 lines, sha256
  `6dad1fd45d087522d29428da793120aa5e3f84af2a3837ab20750c6481f4f7ef`, byte-identical
  to `.remedy-wt/f037-r19-block.md` as measured by `sha256sum` on both paths. It was
  copied with `cp`, never retyped and never reflowed.
- `.agent/last_block.md` at C0b: same blob object as
  `.agent/authored/f037-r19.md`, `7d343c0bfd2b5c03be880e34d35c76b70a316f4b`.
- PLANF037R19 -> `.agent/plan.md` at C1: byte equal INCLUDING the trailing newline,
  negative control False. Extracted programmatically from the committed C0a blob, not
  from the delegation prompt.
- GATER18, DONE725A, FINDING726 -> `.agent/live_review.md` at C2: reader (a) True,
  reader (b) True at N = 5, both negative controls False, pre-round blob a byte
  prefix. Also extracted from the committed C0a blob.
- The two `Landed:` lines are MINE, not reviewer-authored text, and carry no
  authored-text proof by construction. `^Landed: R-` reads 2 at C2, 3 at C3 and 4 at
  C4, which is the progression the block predicted.

## Deviations & assumptions

1. **DEVIATION — G6 mutation (c) came back GREEN, and the guard the block relies on
   cannot see it.** The block's G6 says "The C6 guard must catch this, so if it comes
   back GREEN say so plainly". It came back GREEN at exit 0, 50 passed. THE CAUSE IS
   IN THE BLOCK, not in the code: SPEC S6 defines the C6 guard as "reading
   `DiffFileSidebar.tsx`, `DiffView.tsx` and `RemedyShell.tsx`", and `DetailPopover.tsx`
   — the only file mutation (c) touches — is not among them. No assertion in
   `tests/ui_contracts/test_diff_file_sidebar.py` reads that file at all, so the
   mutation is invisible to it by construction. The other three nodes in the G6 set do
   not close the gap either: `test_diff_viewer_mount.py` scopes its popover assertion
   to the button's own opening tag, which the move leaves untouched, and that is
   exactly what `R-0726` itself records — "the R18 mount guard asserts that the button
   EXISTS in the source and cannot see the condition it renders under, so no gate in
   this repository would notice". I did NOT widen the guard to reach `DetailPopover.tsx`,
   because S6 enumerates the files it reads and constraint 1 says to apply the block
   and declare rather than to route around it. **The consequence is that the C4 repair
   of `R-0726` is real in the source but is UNGATED: nothing in this repository would
   go red if the button were moved back.** A follow-up round should add a
   placement-scoped assertion over `DetailPopover.tsx` — the honest shape is to scope
   to the `DetailPopover` function body, take the region after the `changedFiles`
   section closes, and require the button's tag inside it. That is a decision for the
   reviewer, not for me.
2. **ASSUMPTION — the `Landed:` lines name their commit by its C-label, not by a SHA.**
   SPEC S5 asks for "what changed, and the commit" in a line that is written and
   committed in the same operation, so the SHA cannot exist while the text is written.
   Both lines therefore say "landed by C3 of F037 R19" and "landed by C4 of F037 R19".
   The C-labels resolve through this handback's `## Commits` table to `5a37eb0d` and
   `7c0d52a8`.
3. **OBSERVATION, not acted on — `DiffView.tsx`'s header comment is now stale.** It
   still reads "THIS COMPONENT IS NOT MOUNTED YET, AND THAT IS THE PLAN RATHER THAN AN
   OMISSION", which stopped being true at R18 when `RemedyShell.tsx` mounted it, and is
   further out of date now that the same paragraph says T003 will bring "the file
   sidebar" as future work. SPEC S4 says "Change nothing else in that file", so I left
   it exactly as it stands rather than fixing it inside a commit that was not scoped for
   it. It is one paragraph of prose in a production file and no gate reads it.
4. **No deviation from the ordered commit sequence.** C0a, C0b, C1, C2, C3, C4, C5, C6,
   C7 were committed in exactly that order, nine commits, none added, none dropped,
   none reordered.
5. Assumptions carried, none new: `.agent/context.md`'s standing constraints were
   re-read and hold; the four state readers were run as four (`tests/ui_server/`,
   `tests/orchestration/test_test_runner.py`, `tests/docs/` for the docs side and the
   canary), and `tests/regression/test_resource_safety.py` and
   `tests/orchestration/test_integrity_gate.py` were NOT ordered by this block's G7 —
   G7 named `tests/regression/test_named_bugs.py` and `tests/docs/` in their place, and
   I ran the list the block gave rather than substituting my own.
6. The `remedy` CLI is denied to subagents in this environment. No step of this block
   needed it, so nothing was routed around.

## Item status

| Item | Status | Reason |
|---|---|---|
| C0a save the block | done | `673dcb07` |
| C0b mirror the block | done | `9ab3e879` |
| C1 the plan | done | `6fe9b43a` |
| C2 the record | done | `67781115` |
| C3 the R-0725 remainder | done | `5a37eb0d` |
| C4 the R-0726 repair | done | `7c0d52a8` |
| C5 the sidebar and the anchor | done | `7f591ce9` |
| C6 the sidebar guard | done | `7e263ea5` |
| C7 the handback | done | this commit |
| G1 hygiene | done | STOP ABSENT twice, base matched, 8 clean readings |
| G2 transport | done | three readings matched, one blob at C0b |
| G3 extraction and caps | done | TOTAL 365, PROSE 309, both under cap |
| G4 the plan at C1 | done | byte equal, control False, 49 lines |
| G5 the record at C2 | done | both readers True, both controls False |
| G6 the red-proofs | deviated | (a) (b) (d) (e) (f) RED at exit 1; (c) GREEN at exit 0 — see deviation 1 |
| G7 suites, types, lint, canary | done | all seven exit 0; the tsc node PASSED |
| G8 structure, artifacts, PR gate | done | set difference as required, no open PR |

## Next

The reviewer reads `git diff 0a291411..HEAD` bottom-up, re-runs G1 through G8 itself,
and rules on deviation 1 — whether the ungated `R-0726` repair earns a finding of its
own and a placement-scoped assertion over `DetailPopover.tsx` in the next round.
Before anything else that next round re-reads `.agent/STOP` from disk (Phase 1 rule 1)
and only then the Open PR Gate (rule 2).
