# Handback — F041 round 6: R-1106 repaired, the tour's preview anchor, and the end-to-end proof

## Session

SESSION 2 of feature F041 · round 6 · rounds so far 6. Context self-assessment: after finishing
G5's mutation run, roughly a third of the session's context budget remained — enough to write
this handoff carefully and push, not enough to start a seventh round.

## Range

Review of `fd124cc9b`..`669e6cdf1`, this handoff commit follows `669e6cdf1`.

## Commits

### 82dbb07ef F041 R6 C1a: copy round 6 block and plan into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f041-r6-block.md | +268/-0 | copy of this round's block, byte for byte |
| .agent/authored/f041-r6-plan.md | +27/-0 | copy of the plan.md payload, byte for byte |

Expected by the block: 295 (268 + 27); measured: 295. Match.

### 5b291f72e F041 R6 C1b: copy round 6 records diff into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f041-r6-records.diff | +30/-0 | copy of the records diff payload, byte for byte |

Expected: 30; measured: 30. Match.

### f95b1d3ec F041 R6 C2: book round 5, register R-1106, record D6
| Path | +/- | Reason |
|---|---|---|
| .agent/decisions.md | +10/-0 | `git apply` of records.diff: DECISION F041 D6 |
| .agent/live_review.md | +4/-0 | `git apply` of records.diff: round 5's gate entry and R-1106's registration |
| .agent/plan.md | +7/-8 | rewritten to the plan.md payload |

Expected by the block: 10/0, 4/0, 7/8; measured: identical. Match.

### a2f4696d5 F041 R6 C3: rewrite the README's images in one pass (R-1106)
| Path | +/- | Reason |
|---|---|---|
| apps/ui/src/api/artifactPreview.ts | +20/-20 | S1: `readmeCockpitHtml` now makes ONE `replace` over the alternation `README_IMG_PATTERN`; `STRAY_IMG_PATTERN` and the marker/placeholder mechanism are gone; the comment above the function names R-1106 |
| apps/ui/src/api/artifactPreview.test.ts | +16/-0 | S1: two new whole-output-literal tests over marker-shaped text (`@@artifact-image-0@@`), with no image and beside a listed capture |

No insertion count was expected by the block for C3-C7; measured 20/20 and 16/0.

### 03a238238 F041 R6 C4: offer a "See it running" stop for a job whose project can run
| Path | +/- | Reason |
|---|---|---|
| packages/orchestration/result_tour.py | +59/-4 | S2: `TOUR_PREVIEW_REF`, `TOUR_ANCHOR_KINDS` gains `"preview"`, `TourAnchorContext.previewable`, `_project_previewable`, `_preview_stop`, and the `anchor_problem`/`fallback_tour_stops`/`build_tour_prompt` branches |
| tests/orchestration/test_result_tour.py | +154/-1 | S4: the five-kind literal, `_project_previewable`'s four cases, `anchor_problem`'s three preview cases, the previewable job's whole-tour literal, the ten-area eight-stop count, and the prompt's byte-equality check |

Measured: 59/4 and 154/1.

### af8eb3d6b F041 R6 C5: open the results panel from the tour's preview stop
| Path | +/- | Reason |
|---|---|---|
| apps/ui/src/api/resultTour.ts | +8/-6 | S3: `TOUR_ANCHOR_KINDS` gains `"preview"`, `tourAnchorLabel` answers "The app preview", `tourCanShow` answers true for it |
| apps/ui/src/api/resultTour.test.ts | +4/-2 | S4: the five-kind literal, the label case, the `tourCanShow` case |
| apps/ui/src/components/shell/RemedyShell.tsx | +4/-0 | S3: `handleTourShowAnchor`'s `else if (anchor.kind === "preview")` branch, comment naming DECISION F041 D6 |
| tests/ui_contracts/test_artifact_preview.py | +10/-0 | S4: the shell's `handleTourShowAnchor` body holds `anchor.kind === "preview"` and `setResultsOpen(true)` |

Measured: 8/6, 4/2, 4/0, 10/0.

### 8acef62cc F041 R6 C6: prove the preview flow on a real small app
| Path | +/- | Reason |
|---|---|---|
| tests/ui_server/test_preview_end_to_end.py | +246/-0 | NEW FILE: S4's end-to-end test, `pytest.mark.subprocess`, one test — a real stdlib fixture app under a real `.remedy/config.toml`, a real UI server, `job.preview-start` through the door, LIVE with the real link, THE LINK answering, the harness's own pids, IDLE read off disk (never through the route, which would re-arm the idle clock), TRUTHFUL, and a `finally` that stops the runtime if it is still recorded |

Measured: 246/0.

### 669e6cdf1 F041 R6 C7: add the round 6 mutation tool
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f041-r6-mutations.py | +217/-0 | mutations n1-n8, generated mechanically from verified file slices of the actual committed files (never hand-retyped) into `MUTATIONS`, plus the vitest/pytest runners and the control/report loop |

Measured: 217/0.

### (this commit) F041 R6 C8: rewrite handoff for round 6
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | rewrite | this handback, per the write-once rule (a handoff cannot table the commit that writes it) |

## External actions

`git worktree add --detach .remedy-wt/f041-r6-mut 669e6cdf1` (G5's disposable worktree); an
`os.symlink` from that worktree's `apps/ui/node_modules` to the primary's, made before the tool
ran. DURING the tool's own FIRST control run, the end-to-end test's `start_ui_server` call
triggered `ui_server.py`'s "auto-build if `dist/` is missing" path inside the worktree (this
round's own end-to-end test is the first thing in this feature's mutation tool to actually start
a real UI server there), which replaced that symlink with a real, independently-installed
`node_modules` (209 entries) and a built `dist/` — reported in Deviations & assumptions below.
The primary's own `apps/ui/node_modules` was NOT touched: its `.bin/vitest` symlink's mtime stayed
`Sep 24 01:17` throughout, and `git status --porcelain` in the primary stayed empty the whole
time. `git worktree remove --force .remedy-wt/f041-r6-mut` and `git worktree prune` after G5.
`git push origin feature/f041-artifact-preview` after this commit (outcome reported by the worker
applying this handback in its own reply, since this file cannot record a push that follows it).
No `gh pr` command of any kind: no PR is created, merged or touched this round.

## Verification

G1 TRANSPORT — payload readings (measured against the PAYLOADS table, all matched):
`records.diff` 30 lines / 13790 bytes /
`47a62d052dfdc2b54d34290e9ee2036c1fb7007d146204386bc1a368c931983e`;
`plan.md` 27 lines / 926 bytes /
`f75b5bc5d721c87cc25f6ad73e369823cf47343847e2b59ab7bc5639911e48a1`. Both `match=True` against the
PAYLOADS table. The block itself: 268 lines / 21772 bytes /
`3c6af51cffa0492958f87b357ef9683a5bb0be2b600148ca52995adf20164adb`, matching the two readings the
delegation message gave. Each `.agent/authored/f041-r6-*` payload copy, read back with `git show
<commit>:<path>`, is byte-identical to its source (block copy against
`.remedy-wt/f041-r6/block.md`): all three `match=True`. `git apply --check` on records.diff: real
exit 0; the real `git apply`: real exit 0.

G2 THE RECORDS — at C2 (`f95b1d3ec`): `.agent/decisions.md` 2471829 bytes,
`ff24027213680d67f95a6681cad2e50c50bc891083993e8599d9ecdaa9f2b02e`, match True;
`.agent/live_review.md` 308369 bytes,
`a4147b1205d3cdf235420170483364e28ead2311d0234800e47fad1bbd3ee09c`, match True; `.agent/plan.md`
926 bytes, `f75b5bc5d721c87cc25f6ad73e369823cf47343847e2b59ab7bc5639911e48a1`, match True.
`open_finding_ids` over `.agent/live_review.md`'s TEXT: `[]` at `fd124cc9b` and `['R-1106']` at
`f95b1d3ec`, matching the reviewer's `[]`/`['R-1106']`. `git diff --name-only 5b291f72e f95b1d3ec`:
`.agent/decisions.md`, `.agent/live_review.md`, `.agent/plan.md` — exactly the table's three paths.

G3 THE CODE — `python3 -m ruff check packages/orchestration/result_tour.py
tests/orchestration/test_result_tour.py tests/ui_contracts/test_artifact_preview.py
tests/ui_server/test_preview_end_to_end.py .agent/authored/f041-r6-mutations.py`: real exit 0,
"All checks passed!". The whole of `readmeCockpitHtml`, `_project_previewable`, `_preview_stop`,
`fallback_tour_stops`, the changed lines of `anchor_problem` and `build_tour_prompt`,
`resultTour.ts`'s changed lines, `RemedyShell.tsx`'s changed lines, and the whole end-to-end test
are quoted in the worker's chat reply to the delegating message (this file summarizes rather than
repeats the source; every quoted block there is read verbatim from the commits named above).

G4 THE TESTS — at C7 (`669e6cdf1`), serially:
- `pytest` selection (tests/orchestration/test_result_tour.py, test_tour_route.py,
  test_tour_e2e_live.py, test_job_show.py, test_preview_end_to_end.py, test_preview_commands.py,
  test_preview_worker.py, test_preview_control.py, test_preview_runner.py, test_command_channel.py,
  tests/ui_contracts, test_dashboard_contract.py, test_import_reachability.py,
  test_no_orphan_modules.py, tests/docs, test_golden_path.py): `1758 passed, 4 skipped` at real
  exit 0. The four skips are exactly the D3 quarantine nodes of `test_graph_architecture.py` (2)
  and `test_ux_quality.py` (2) — the same four the reviewer's own `fd124cc9b` run (without the new
  file) showed as `1748 passed, 4 skipped`. `--collect-only -q` over the same selection: 1762 nodes
  (1758 + 4). Per-file growth this round: `test_result_tour.py` 61 nodes (+8: the four
  `_project_previewable` cases, the three `anchor_problem`/tour-shape/ten-area cases, and the
  prompt case); `test_artifact_preview.py` 11 nodes (+1: the shell's preview-anchor contract case);
  `test_preview_end_to_end.py` 1 node (+1, NEW FILE). 1748 + 8 + 1 + 1 = 1758, matching exactly.
- `apps/ui/node_modules/.bin/vitest run --root apps/ui`: `93 passed | 1 skipped (94)` test files,
  `1907 passed | 5 skipped (1912)` tests, real exit 0. The reviewer's own `fd124cc9b` run showed
  `1905 passed | 5 skipped`; this round's two new `it()` cases in `artifactPreview.test.ts` (the
  R-1106 marker-safety literals) account for the whole +2 — `resultTour.test.ts`'s new preview
  assertions were added to EXISTING `it()` bodies, not new cases. 1905 + 2 = 1907, matching.
- The end-to-end test's own duration from a second, solo run with `--durations=0`:
  `16.17s call tests/ui_server/test_preview_end_to_end.py::TestPreviewEndToEnd::
  test_the_preview_flow_runs_end_to_end_on_a_real_fixture_app`, `1 passed in 16.36s`, real exit 0.
  `ps aux | grep -i server.py | grep -v grep` immediately after: no output (grep exit 1) — no
  `server.py` of its project runs.
- `python3 -m apps.cli.main integrity check --json`: all six checks `"status": "pass"`,
  `"fail_count": 0`, `"ok": true`, real exit 0.

G5 THE RED PROOFS — `git worktree add --detach .remedy-wt/f041-r6-mut 669e6cdf1`, then
`.agent/authored/f041-r6-mutations.py` run against it: `control (first) vitest: exit=0 failed=0`,
`control (first) pytest: exit=0 failed=0`, `control (first) pytest (end-to-end): exit=0 failed=0`;
all eight mutations n1-n8 `caught=True` with `restored byte-identical: True` after each (n1 exit=1
failed=2; n2 exit=1 failed=1; n3 exit=1 failed=7; n4 exit=1 failed=2; n5 exit=1 failed=1; n6 exit=1
failed=1; n7 exit=1 failed=1; n8 exit=1 failed=1); `control (last) vitest: exit=0 failed=0`,
`control (last) pytest: exit=0 failed=0`, `control (last) pytest (end-to-end): exit=0 failed=0`;
`ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: True`, real exit 0. n8 mutates `idle_stop_due` so it
never answers true; run against the end-to-end test alone, it FAILED (its own 60-second wait for
`stopped` timed out and the assertion raised) rather than hanging, and the test's own `finally`
still ran `run_runtime_verb("stop", project)` since the runtime was still recorded — `ps aux | grep
-i server.py | grep -v grep` after the whole tool run: no output, no `server.py` of n8's project
left running. `git worktree remove --force .remedy-wt/f041-r6-mut` and `git worktree prune`:
`git worktree list | wc -l` read 62 (equal to the step 4 reading) and `git status --porcelain` was
empty.

## Authored-text proofs

Every `.agent/authored/f041-r6-*` payload copy (block, plan.md, records.diff) is byte-identical,
read back from the commit that added it, to its source under `.remedy-wt/f041-r6-payloads/` or
`.remedy-wt/f041-r6/block.md` — see G1 above. `records.diff` applied cleanly with `git apply`
(real exit 0 on both `--check` and the real apply), and `git diff --name-only` across C1b..C2
names exactly the three paths its own hunks touch. No other reviewer text was applied this round —
S1 to S4's production code, its tests, the end-to-end test and the mutation tool are all
worker-authored per the block's ROLE AND AUTHORITY.

## Item status

| Item | Status | Reason |
|---|---|---|
| C1a | done | |
| C1b | done | |
| C2 | done | |
| C3 | done | |
| C4 | done | |
| C5 | done | |
| C6 | done | |
| C7 | done | |
| C8 | done | |
| G1 | done | |
| G2 | done | |
| G3 | done | |
| G4 | done | |
| G5 | done | |
| G6 | done | |

## Deviations & assumptions

1. No commit was split, reordered or added beyond the block's ordered C1a..C8 sequence; every
   commit stayed well under the 500-line cap (largest: C4 at 154 insertions in its test file).
2. The worktree `node_modules`/`dist` divergence noted in External actions is not a deviation from
   the block's own instruction (it names only "an `os.symlink`... then removed with the worktree",
   which still holds in full — the worktree, whatever it grew inside it, was removed whole by
   `git worktree remove --force`); it is recorded for the same transparency reason round 5's
   handback records its own render-harness `node_modules` gotcha, and because it is new to this
   round: earlier rounds' mutation tools never started a real UI server inside the disposable
   worktree, so the auto-build path never fired there before.
3. No test this round wrote was found wrong; no EXISTING test went red at any point.
4. The top-of-file comment in `artifactPreview.ts` describing `readmeCockpitHtml`'s old two-pass
   marker mechanism was rewritten in the same C3 commit to describe the one-pass fix instead (S1
   itself only names the comment directly above the function). Declared because it is prose the
   block did not explicitly order changed, though leaving it describing a mechanism the same
   commit deletes would have been a stale, self-contradicting comment in the file S1 governs.

## Next

1. Phase 1 rule 1: read `.agent/STOP` from disk.
2. The review of round 6 with the resolution of R-1106.
3. F041's closure sequence: the one full-suite run, the evidence, the close.

Open findings: 1 (R-1106, repaired and awaiting review). Operator questions open: 1.
