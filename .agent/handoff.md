# Handback — F043 round 4: book round 3's PASS, register R-1115, record DECISION F043 D4,
repair R-1115, and land the first-run tour on `TourFrame`, the overlay engine the result tour now
shares, with its spotlight, its once-per-browser record and its relaunch from the Terms panel,
against the reviewer's tests and a render harness that mounts the real shell in a fresh browser

## Session

SESSION 1 of feature F043 · round 4 · rounds so far 4. Context self-assessment: roughly a third
of the session's context window remained when this handback was written, after all eight commits
and gates G1 through G5.

## Range

Review of `32854ea06`..HEAD (this round's final commit, C6 — the push's real outcome and
`gh pr list` are reported in the worker's reply, since this file is committed as part of C6 and
cannot name a push that follows it).

## Commits

### `cf7e04670` F043 R4 C1a: copy round 4 block and plan into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f043-r4-block.md | +350/-0 | this round's block, copied verbatim via `shutil.copyfile` |
| .agent/authored/f043-r4-plan.md | +31/-0 | payload copy |

Total 381 insertions (block's 350 lines + 31), matching the block's stated formula exactly;
`git diff --cached --stat` read `2 files changed, 381 insertions(+)` before commit, under the
500 cap.

### `abc8199ef` F043 R4 C1b: copy round 4 records and tests diffs into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f043-r4-records.diff | +64/-0 | payload copy |
| .agent/authored/f043-r4-tests.diff | +218/-0 | payload copy |

Total 282 insertions, expected 282, measured 282 — exact match.

### `165cc76a8` F043 R4 C1c: copy the round 4 render page and driver into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f043-r4-render_main.tsx | +47/-0 | payload copy |
| .agent/authored/f043-r4-render_drive.mjs | +261/-0 | payload copy |

Total 308 insertions, expected 308, measured 308 — exact match.

### `6d89e3b34` F043 R4 C1d: copy the rest of the round 4 render harness into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f043-r4-render_index.html | +11/-0 | payload copy |
| .agent/authored/f043-r4-render_vite.config.mjs | +28/-0 | payload copy |
| .agent/authored/f043-r4-render_measure.py | +186/-0 | payload copy |

Total 225 insertions, expected 225, measured 225 — exact match.

### `bf03c734e` F043 R4 C2: book F043 R3, register R-1115, record D4, advance the plan
| Path | +/- | Reason |
|---|---|---|
| .agent/decisions.md | +44/-0 | `git apply records.diff`: DECISION F043 D4 appended |
| .agent/live_review.md | +4/-0 | `git apply records.diff`: round 3's Gate entry and R-1115's registration appended |
| .agent/plan.md | +11/-10 | rewrite := plan.md payload |

Every numstat reading equals the block's expected table exactly (44/0, 4/0, 11/10). `git apply
--check` on records.diff read exit 0 before the real apply, which also read exit 0. `open_finding_ids`
over the ledger text read `[]` at `32854ea06` and `['R-1115']` at this commit, matching the
block's own stated readings exactly.

### `826864cf7` F043 R4 C3: add the first-run tour on one overlay engine and repair R-1115
| Path | +/- | Reason |
|---|---|---|
| apps/ui/src/api/firstRunTour.ts | +80/-0 | S1, NEW: `FirstRunStep`, `FIRST_RUN_STEPS` (the six steps), `FIRST_RUN_TOUR_KEY`/`FIRST_RUN_TOUR_SEEN`, `FirstRunTourStorage`, `firstRunTourDue`, `markFirstRunTourSeen`, `firstRunStepLabel` |
| apps/ui/src/components/panels/ChatInput.tsx | +1/-1 | S7: the row gains `data-ui="chat-input-row"` |
| apps/ui/src/components/panels/RightLivePanel.tsx | +1/-1 | S7: the Terms button gains `data-ui="terms-button"` directly before its `onClick` |
| apps/ui/src/components/shell/RemedyShell.tsx | +8/-1 | S8: `FirstRunTourMount` imported; `tourRelaunch` state added; the Terms panel's mount gains `onStartTour`; `<FirstRunTourMount relaunch={tourRelaunch} />` mounted after it |
| apps/ui/src/components/term/Term.module.css | +1/-0 | S0/R-1115: `.tipDetail` gains `display: block;` as its first declaration |
| apps/ui/src/components/term/TermPanel.module.css | +15/-0 | S6: `.tour` button style added, in the result tour's own button style |
| apps/ui/src/components/term/TermPanel.tsx | +7/-1 | S6: optional `onStartTour` prop; "Take the tour" button rendered directly after the hint paragraph |
| apps/ui/src/components/tour/FirstRunTour.tsx | +112/-0 | S5, NEW: `FirstRunTour` (the spotlighted card, Skip tour/Previous/Next/Finish) and `FirstRunTourMount` (the storage edge, `useMemo(() => window.localStorage, [])`) |
| apps/ui/src/components/tour/TourFrame.tsx | +64/-0 | S2, NEW: `TourSpot`, `TOUR_SPOT_PAD_PX`, `TourFrame` — the shared portal/dialog/backdrop/spot engine |
| apps/ui/src/components/tour/TourOverlay.module.css | +13/-1 | S4: `.card[data-shown="true"]` extended to `.card[data-spot="true"]`; the docked-actions wrap rule added for `data-spot`; new `.spot` rule (the spotlight ring) |
| apps/ui/src/components/tour/TourOverlay.tsx | +24/-34 | S3: `createPortal` import and its return block dropped; `TourFrame` imported; the doc comment's portal paragraph replaced with one sentence; the return re-wrapped in `<TourFrame>` around the three content blocks the section held after its header |

Measured vs. the block's own reading of its reviewer's version: firstRunTour.ts 80/0 vs 81/0
(-1), ChatInput.tsx 1/1 (exact), RightLivePanel.tsx 1/1 (exact), RemedyShell.tsx 8/1 (exact),
Term.module.css 1/0 (exact), TermPanel.module.css 15/0 vs 12/0 (+3), TermPanel.tsx 7/1 vs 5/1
(+2), FirstRunTour.tsx 112/0 vs 101/0 (+11), TourFrame.tsx 64/0 vs 65/0 (-1),
TourOverlay.module.css 13/1 vs 16/1 (-3), TourOverlay.tsx 24/34 vs 7/19 (+17/+15 — the JSX
content moved one nesting level shallower when it left the dropped `<section>`/`<header>`
wrapper for `<TourFrame>`'s children, so `git diff` re-pairs every content line as both a
deletion and an insertion even though the lines themselves are unchanged). All gaps are
comment/doc-comment wording and layout choices with no functional difference — every test added
in C4 passed against this version unedited, G3's typescript/eslint/vitest/pytest gates all read
green, G4's render harness read 9 of 9, and G5 caught every one of 11 mutations. Total 326
insertions, 39 deletions, under the 500 cap; no split needed (S0-S8 fit in one commit).

### `d6ce426ad` F043 R4 C4: add the reviewer's tests for the first-run tour and the shared frame
| Path | +/- | Reason |
|---|---|---|
| apps/ui/src/api/firstRunTour.test.ts | +99/-0 | `git apply tests.diff`: NEW FILE, the six steps' order and exact wording, the step-label count, and `firstRunTourDue`/`markFirstRunTourSeen`'s storage behaviour |
| apps/ui/src/components/term/termPanel.test.ts | +6/-0 | `git apply tests.diff`: "offers the tour again only when the shell hands it a way to start one" |
| tests/ui_contracts/test_term_panel_wiring.py | +13/-2 | `git apply tests.diff`: the `TermPanel` mount string updated for `onStartTour`; the `FirstRunTourMount` mount test added; the Terms button's `data-ui` assertion added |
| tests/ui_contracts/test_tour_overlay_contract.py | +27/-7 | `git apply tests.diff`: `FRAME`/`FIRST_RUN` paths added; the dialog/backdrop assertions moved onto `FRAME`; the overlay's own assertions narrowed to its `label`/`ui` props; `test_both_tours_render_through_the_one_frame` added; the docked-card test extended to `data-spot` |

Every numstat reading equals the block's expected table exactly (99/0, 6/0, 13/2, 27/7). `git
apply --check` on tests.diff read exit 0 before the real apply, which also read exit 0.

### `95f04ef6e` F043 R4 C5: add the round 4 mutation tool
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f043-r4-mutations.py | +252/-0 | NEW, the G5 red-proof tool: 11 mutations (q1-q3 read by vitest, w1-w2 by the shell/overlay wiring pytest, h1-h6 by the render harness — h4 is R-1115's own red proof, `.tipDetail` losing `display: block`) |

### `<this commit>` F043 R4 C6: rewrite handoff for round 4
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | rewrite | this file, per docs/agents/handback_template.md |

## External actions

- `git worktree add --detach .remedy-wt/f043-r4-mut 95f04ef6e` — G5's disposable worktree,
  created and later removed (`git worktree remove --force`, then `git worktree prune`);
  `git worktree list | wc -l` read 11 before and after, matching the round's step-4 reading.
- `git push -u origin feature/f043-explanation-layer` — real outcome reported in the worker's
  reply, since it runs after this commit.
- No `gh pr create`, no `gh pr merge`, no checkout of `main`, no branch deletion, no force-push,
  no `git stash` — none ordered this round.

## Verification

**G1 TRANSPORT** — every payload's line count, byte count and sha256 matched the PAYLOADS table
exactly (all 8 payloads: records.diff, tests.diff, plan.md, and the five render_* files). Every
`.agent/authored/f043-r4-*` copy, read back with `git show <commit>:<path>` from the commit that
added it, was byte-for-byte identical to its source payload — 9 pairs (the block plus 8
payloads), all `True`.

**G2 THE RECORDS AND THE TESTS** — all 7 files' bytes and sha256 at their named commits equaled
the block's given values exactly: `.agent/decisions.md` (2532152 bytes,
`a539b446f0d63911d4f87fa7cf2353a81ad180638e5dc3146e8189964616ad72`), `.agent/live_review.md`
(127524 bytes, `60cf0ce5f8425cc54daa97e3f298761742012f64c11217801dc9be630d771511`),
`.agent/plan.md` (1102 bytes, `c02d3ca6ce875a2dd6ca7c11af2bae0ab90c4e49a34e4119b9d669ae28adc8ef`)
at C2; `apps/ui/src/api/firstRunTour.test.ts` (3905 bytes,
`18390a7abda3859eb2b58b49ce2f2eee8e1cfa7425845ab1896867d72083979a`),
`apps/ui/src/components/term/termPanel.test.ts` (2407 bytes,
`e9683195fea83460ba1e0f7545f32ce52bb581a3cb224d2544fa4d3de18ac93b`),
`tests/ui_contracts/test_term_panel_wiring.py` (2501 bytes,
`a549125669b730ba790f6e17c8cc7337f10e0ea5a5b5335e2dcd823a3aed8e86`), and
`tests/ui_contracts/test_tour_overlay_contract.py` (4678 bytes,
`7684d92f098f28ed56f1e430d1d8ce4b0f9ad317c0fcfaba932f334e5a4a46f9`) at C4. `open_finding_ids`
(from `scripts/rotate_live_review.py`) over the ledger text read `[]` at `32854ea06` and
`['R-1115']` at C2, matching the block's own stated readings exactly. The ledger's last
non-empty line at C2 begins `- R-1115 — Low, THE TERM TOOLTIP'S LIVE DETAIL RENDERS INLINE`.
`git diff --name-only 6d89e3b34 bf03c734e` named exactly the three C2 paths of the table
(`.agent/decisions.md`, `.agent/live_review.md`, `.agent/plan.md`), nothing more.

**G3 THE CODE AND THE TESTS** (at C5) —
- `python3 -m ruff check .agent/authored/f043-r4-mutations.py
  .agent/authored/f043-r4-render_measure.py tests/ui_contracts/test_term_panel_wiring.py
  tests/ui_contracts/test_tour_overlay_contract.py` → `All checks passed!`, exit 0.
- `apps/ui/node_modules/.bin/eslint src` run with `apps/ui` as cwd → exit 0, no output.
- `git show --numstat 826864cf7` is reported in full in the C3 commit table above (11 files, 326
  insertions, 39 deletions); the whole diff was authored file-by-file and reviewed again in full
  (`git diff --cached` before the C3 commit) before this handback was written.
- The ordered pytest selection, run SERIALLY in the primary checkout at C5:
  `python3 -m pytest -q -p no:cacheprovider -rs tests/ui_contracts
  tests/ui_server/test_dashboard_contract.py tests/orchestration/test_test_runner.py
  tests/orchestration/test_escalation.py tests/cli/test_plan_approval.py
  tests/orchestration/test_integrity_gate.py tests/orchestration/test_live_review_rotation.py
  tests/regression/test_resource_safety.py tests/test_agent_tooling.py tests/docs
  tests/cli/test_golden_path.py` → `1751 passed, 5 skipped in 96.20s`, `REAL_EXIT=0`
  (`${PIPESTATUS[0]}`) — two more passed than round 3's primary reading (1749), matching the two
  new pytest tests this round's `tests.diff` adds (`test_the_shell_mounts_the_first_run_tour_once_outside_main`
  and `test_both_tours_render_through_the_one_frame`); skip count unchanged (5) since this
  checkout's `dist` is built. SKIPPED lines: two in `test_graph_architecture.py` (D3 quarantine,
  F252), two in `test_ux_quality.py` (D3 quarantine, F252), one in `test_agent_tooling.py` (D12
  quarantine, F252) — the same five round 3's primary run printed. This selection separately ran
  `test_typescript_compiles` (`tests/ui_server/test_dashboard_contract.py::TestJobSummaryCommandContract::test_typescript_compiles`),
  `test_vitest_passes` (`tests/orchestration/test_test_runner.py::TestVitestFrontendTestFoundation::test_vitest_passes`)
  and `test_the_ui_lint_passes_with_no_problem` (`tests/ui_contracts/test_ui_lint.py`) as part of
  the same collected run — re-run standalone afterward to name each outcome explicitly: all three
  `passed`, exit 0. The vitest counts of the two named files, read via a standalone `vitest run`
  with the primary's own binaries: `src/api/firstRunTour.test.ts` 7 tests, all passing,
  `src/components/term/termPanel.test.ts` 5 tests, all passing — equal to the reviewer's own
  counts (7, 5). The whole vitest suite, run the same way with no file argument, read
  `Test Files 102 passed | 1 skipped (103)` and `Tests 2012 passed | 5 skipped (2017)` at exit
  0 — equal to the block's own stated reading.
- `python3 -m apps.cli.main integrity check --json` → all six checks `pass`, `fail_count` 0,
  `"ok": true, "passed": true`.

**G4 THE RENDER** (at C5) — `python3 -B .agent/authored/f043-r4-render_measure.py
/home/decodeux/Repos/remedy`: vite build succeeded (`✓ 1242 modules transformed`, `built in
1.63s`), server and Chrome started, `drive.mjs` printed `PASS` for all nine checks (R-a through
R-i) and `RENDER: 9 of 9 checks pass`, exit code 0 — equal to the reviewer's own 9-of-9 reading.
Chrome and the server were stopped by their own pids (SIGTERM, both landed) and the work dir was
removed. The screenshot at `.remedy-wt/f043-r4-render-tour.png` shows the real cockpit shell with
the first-run tour open: a bright spotlight ring around the brain graph stage near the top of the
page, the rest of the page dimmed around it, and a "WELCOME TOUR" card docked at the lower left
reading "STEP 1 OF 6 — The graph" with its body text and Skip tour/Previous/Next controls.

**G5 THE RED PROOFS** — `git worktree add --detach .remedy-wt/f043-r4-mut 95f04ef6e` then
`os.symlink(.../apps/ui/node_modules, .../f043-r4-mut/apps/ui/node_modules)`, then
`python3 -B .agent/authored/f043-r4-mutations.py .../f043-r4-mut`. Full output:
```
worktree: /home/decodeux/Repos/remedy/.remedy-wt/f043-r4-mut
=== CONTROL (before) ===
control (before): vitest exit=0 pytest exit=0 harness exit=0 RENDER: 9 of 9 checks pass all_pass=True
q1: exit=1 failed=1
restored byte-identical: True
q2: exit=1 failed=1
restored byte-identical: True
q3: exit=1 failed=1
restored byte-identical: True
w1: exit=1 failed=1
restored byte-identical: True
w2: exit=1 failed=1
restored byte-identical: True
h1: exit=1 RENDER: 6 of 9 checks pass
restored byte-identical: True
h2: exit=1 RENDER: 7 of 9 checks pass
restored byte-identical: True
h3: exit=1 RENDER: 7 of 9 checks pass
restored byte-identical: True
h4: exit=1 RENDER: 8 of 9 checks pass
restored byte-identical: True
h5: exit=1 RENDER: 7 of 9 checks pass
restored byte-identical: True
h6: exit=1 RENDER: 7 of 9 checks pass
restored byte-identical: True
=== CONTROL (after) ===
control (after): vitest exit=0 pytest exit=0 harness exit=0 RENDER: 9 of 9 checks pass all_pass=True
ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: True
```
Every one of the 11 mutations went red, both controls (vitest, pytest and the harness) passed
before and after, and every restore read byte-identical. Cleanup: `os.unlink` the symlink, `git
worktree remove --force .remedy-wt/f043-r4-mut`, `git worktree prune`; `git worktree list | wc -l`
read 11, matching the round's step-4 reading.

**G6 TREE AND PUSH** — reported in the worker's reply, since it runs after this commit.

## Authored-text proofs

Every `.agent/authored/f043-r4-*` copy (the block, plan.md, records.diff, tests.diff, and the
five render_* files) was compared byte-for-byte against its source under
`.remedy-wt/f043-r4-payloads/` (and the block itself against `.remedy-wt/f043-r4/block.md`), read
back with `git show <commit>:<path>` from the commit that added it: all 9 pairs `True` (G1
above). The mutation tool `.agent/authored/f043-r4-mutations.py` is the worker's own authored
text (not a reviewer payload), so no fidelity comparison applies to it; its correctness is
instead demonstrated by G5's own run (every mutation caught, every restore clean) and by a
pre-commit dry run of the same FROM-text uniqueness check against the primary checkout.

## Item status (AGENTS.md Completion Report)

| Item | Status | Reason |
|---|---|---|
| C1a | done | |
| C1b | done | |
| C1c | done | |
| C1d | done | |
| C2 | done | |
| C3 | done | |
| C4 | done | |
| C5 | done | |
| C6 | done | this commit |
| G1 | done | |
| G2 | done | |
| G3 | done | |
| G4 | done | |
| G5 | done | |
| G6 | done | reported in the worker's reply (runs after C6) |
| R-1115 | repaired | `.tipDetail` gains `display: block` (S0/C3); the harness's R-h and the mutation tool's h4 both prove it; the reviewer authors its `Done:`/`Landed:` resolution text at the next gate per the block's constraint 3 |

## Deviations & assumptions

- C3's per-file insertion counts differ from the block's own reviewer-version reading by a few
  lines each (see the C3 commit table above for the full list), the largest being
  TourOverlay.tsx (+17/+15) because the JSX content moved one nesting level shallower when the
  dropped `<section>`/`<header>` wrapper left it, so `git diff` re-pairs unchanged content lines
  as both a deletion and an insertion, and FirstRunTour.tsx (+11) from an extracted
  `measureSpot` helper and its doc comments. Every test added in C4 passed against this version
  unedited, G3's tsc/eslint/vitest/pytest gates all read green, G4 read 9 of 9, and G5 caught
  every one of 11 mutations, so none of these are treated as a spec deviation — S0-S8 are prose
  specifications, not literal diffs to reproduce byte-for-byte.
- S3's doc-comment sentence ("The backdrop, the card and the portal are `TourFrame`'s, the
  overlay engine this tour shares with the first-run tour (DECISION F043 D4).") paraphrases
  rather than quotes the block's own suggested wording ("...the engine it shares with the
  first-run tour..."); the content the clause orders (naming `TourFrame` as the owner of the
  backdrop/card/portal, and naming the sharing with the first-run tour) is present verbatim in
  meaning. Noted for transparency, not treated as a deviation from the specification's substance.
- No departure from the block's ordered commit sequence C1a-C6: every commit landed in order,
  none dropped, none added, none reordered; C3 fit S0-S8 in one commit (326 insertions), so the
  split clause did not trigger.

## Next

Phase 1 rule 1 (read `.agent/STOP` from disk), then the review of round 4, then the end-to-end
run over the real shell. Open findings: 1 (R-1115, repaired in this round and resolved only by
the reviewer's text). Operator questions: 0.
