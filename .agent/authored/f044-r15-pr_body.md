## What

F044 — Command palette, keyboard, performance budget. One search bar now reaches everything in the
cockpit, one keymap drives it from the keyboard, and three automatic checks now guard how fast it
loads and runs.

- T001 — the command palette. The search bar at the top of the cockpit now opens a dropdown that
  fuzzy-matches every command the write door exposes, jumps to any task by name (capped at eight
  results), lists the projects and the help, and lets you ask a question that routes straight to the
  chat panel instead of the command list. Fuzzy matching, the command list, the routing rule, and the
  jump logic are four pure TypeScript modules the reviewer's tests hold equal to the write door's own
  exposed command set and the chat's own question-routing rule, so the two cannot silently drift
  apart. Seven form-entry commands (six plan edits plus hunk approval) are listed but stay disabled
  until F292 lands their server-side routes.
- T002 — one shared keymap and its cheat sheet. A single, DOM-free module now decides what every key
  press does anywhere in the cockpit — slash or Ctrl/Cmd+K opens the bar, "g" then "p" jumps to the
  projects view, and the same keys drive zooming the task graph — replacing several separate,
  inconsistent keyboard listeners with one. It never steals a key from a text field. Holding the
  question-mark key past 400ms opens a full list of every shortcut; releasing it early still opens the
  existing terms panel.
- T003 — three CI budgets. The project's automatic build checks now measure and enforce: the built
  cockpit page's total size against its own measured baseline plus 10%; how long the page takes to
  first become visible on a fresh load, against a 1.5-second limit, measured with a real headless
  Chrome browser; and how smoothly the task graph scrolls at 200 tasks, against a 60-frames-per-second
  pace, also measured with a real browser trace. All three join the existing `budgets` build stage,
  which was re-measured and its documentation corrected to match its real, current set of checks.

The closure's own self-use item, `SU-039`, ran a real job to narrow an excused error handler in
`apps/cli/commands/dev.py`; the job's reviewer approved it, but the job's own diff was empty — the
edit never actually landed anywhere. Remedy's own defect-detection caught this vacuous pass by
itself and is why this PR carries one open finding instead of a silently wrong "done": see R-1117
below.

## Why

`docs/roadmap/features/T5_F044.md`: reaching any command, task, project or piece of help should take
one gesture, not a memorized menu path; a cockpit built for speed needs its own speed enforced by the
same pipeline that enforces everything else, or the budget rots the first time nobody is looking.

## Key decisions (in `.agent/decisions.md`)

- F044 D1 — the seven-round order: rules, dropdown sheet, execution/argument flows, form flows,
  keymap, CI budgets, closure.
- F044 D2 — the palette sheet (Recent/Jump/Projects/Help), portalled; the shell's old substring jump
  deleted.
- F044 D3 — the Commands section, argument flows, execution through the chat's own send path.
- F044 D4 — the Ask row, routing a focused or project-wide question into the existing chat tab.
- F044 D5 — F292 registered directly after F044 for the disabled form-entry commands' server routes.
- F044 D6 — the one keymap; the graph's zoom keys and the held `?` overlay unified into it.
- F044 D7 (superseded by D8) / D8 — the bundle-size budget: a fresh `vite build` baseline plus 10%,
  keyed by each asset's stable name with the content hash stripped.
- F044 D9 — the first-paint budget: under 1.5s, measured via a real, freshly built, HTTP-served page
  in headless Chrome.
- F044 D10 — the frame-pipeline budget: p95 gap between real presented compositor frames under
  17.0ms, over a committed browser trace harness.
- F044 D11 — `docs/system/ci-self-check-v1.md` and the `budgets` stage's own test resynced to its
  real, current seven-path selection; its 300-second timeout unchanged.
- F044 D12 — the "numbers recorded per run" design line discharged as already met by each budget
  check's own detail string.

## How to review / test

- `npm --prefix apps/ui run test:unit -- src/api/fuzzyMatch.test.ts src/api/keymap.test.ts src/api/paletteArgs.test.ts src/api/paletteCommandState.test.ts src/api/paletteCommands.test.ts src/api/paletteJump.test.ts src/api/paletteRouting.test.ts src/api/paletteSend.test.ts src/api/paletteSheet.test.ts src/components/graph/zoomKeys.test.ts`
- `python3 -m pytest -q tests/ui_contracts/test_palette_contract.py tests/ui_contracts/test_palette_sheet_wiring.py tests/ui_contracts/test_semantic_zoom_wiring.py tests/ui_contracts/test_term_panel_wiring.py tests/ui_server/test_dashboard_contract.py tests/orchestration/test_ci_budgets.py tests/orchestration/test_ci_stages.py`
- The one full suite: `.agent/authored/f044-closure-suite.txt` (`21058 passed, 20 skipped`, exit 0).
- Evidence job `f044r14e1001`; package `remedy-review-20260930-121429-READY_FOR_REVIEW.zip`, SHA-256
  `a2d38929930d27bfd40e15874a545d482fd2b1abc850b95c21a185d5d59f0b41`, accepted head `eb6adff70`.
- Round-by-round review record: `.agent/live_review.md` and its archive.

Latest verdict: round 14 PASS, booked in round 15. Open findings: 1 (`R-1117`, Medium — the
self-use reviewer approved an empty diff; owned by F290, Remedy's rolling findings-paydown
feature). `R-1116` (a Low, two-comment miscitation) was fixed at round 8 and is formally closed in
this same PR after a ledger-bookkeeping gap this closure's own reviewer caught and corrected.

Runtime actuals: 15 delegated rounds over 5 sessions; wall clock and token use of the building
sessions not measured; the self-use job measured $1.13 in 4 provider calls.

## Changed files (outside `.agent/`, fork point `33f66862` to this branch)

| Path | + | - |
|---|--:|--:|
| `README.md` | 14 | 2 |
| `apps/ui/perf/index.html` | 14 | 0 |
| `apps/ui/perf/main.tsx` | 60 | 0 |
| `apps/ui/perf/vite.config.mjs` | 23 | 0 |
| `apps/ui/src/api/firstRunTour.test.ts` | 6 | 6 |
| `apps/ui/src/api/firstRunTour.ts` | 4 | 5 |
| `apps/ui/src/api/fuzzyMatch.test.ts` | 108 | 0 |
| `apps/ui/src/api/fuzzyMatch.ts` | 138 | 0 |
| `apps/ui/src/api/keymap.test.ts` | 114 | 0 |
| `apps/ui/src/api/keymap.ts` | 119 | 0 |
| `apps/ui/src/api/paletteArgs.test.ts` | 50 | 0 |
| `apps/ui/src/api/paletteArgs.ts` | 44 | 0 |
| `apps/ui/src/api/paletteCommandState.test.ts` | 112 | 0 |
| `apps/ui/src/api/paletteCommandState.ts` | 71 | 0 |
| `apps/ui/src/api/paletteCommands.test.ts` | 82 | 0 |
| `apps/ui/src/api/paletteCommands.ts` | 185 | 0 |
| `apps/ui/src/api/paletteJump.test.ts` | 73 | 0 |
| `apps/ui/src/api/paletteJump.ts` | 80 | 0 |
| `apps/ui/src/api/paletteRouting.goldens.json` | 37 | 0 |
| `apps/ui/src/api/paletteRouting.test.ts` | 95 | 0 |
| `apps/ui/src/api/paletteRouting.ts` | 80 | 0 |
| `apps/ui/src/api/paletteSend.test.ts` | 90 | 0 |
| `apps/ui/src/api/paletteSend.ts` | 71 | 0 |
| `apps/ui/src/api/paletteSheet.test.ts` | 303 | 0 |
| `apps/ui/src/api/paletteSheet.ts` | 355 | 0 |
| `apps/ui/src/api/termSearch.test.ts` | 1 | 22 |
| `apps/ui/src/api/termSearch.ts` | 4 | 20 |
| `apps/ui/src/components/command/ChatSheet.module.css` | 33 | 0 |
| `apps/ui/src/components/command/ChatSheet.tsx` | 39 | 0 |
| `apps/ui/src/components/command/CommandBar.module.css` | 12 | 0 |
| `apps/ui/src/components/command/CommandBar.tsx` | 252 | 7 |
| `apps/ui/src/components/command/KeymapOverlay.module.css` | 43 | 0 |
| `apps/ui/src/components/command/KeymapOverlay.tsx` | 24 | 0 |
| `apps/ui/src/components/command/PaletteSheet.module.css` | 122 | 0 |
| `apps/ui/src/components/command/PaletteSheet.tsx` | 153 | 0 |
| `apps/ui/src/components/graph/BrainGraphStage.tsx` | 10 | 2 |
| `apps/ui/src/components/graph/EvidenceChatTab.tsx` | 31 | 17 |
| `apps/ui/src/components/graph/brainView.ts` | 1 | 1 |
| `apps/ui/src/components/graph/useSemanticZoom.ts` | 5 | 15 |
| `apps/ui/src/components/graph/useZoomKeys.ts` | 39 | 0 |
| `apps/ui/src/components/graph/zoomKeys.test.ts` | 76 | 0 |
| `apps/ui/src/components/graph/zoomKeys.ts` | 72 | 0 |
| `apps/ui/src/components/graph/zoomView.test.ts` | 1 | 15 |
| `apps/ui/src/components/graph/zoomView.ts` | 0 | 14 |
| `apps/ui/src/components/shell/RemedyShell.tsx` | 126 | 14 |
| `apps/ui/src/components/shell/useHeldHelpKey.ts` | 62 | 0 |
| `docs/roadmap/STATUS.md` | 2 | 1 |
| `docs/roadmap/features/T16_F240.md` | 1 | 1 |
| `docs/roadmap/features/T5_F044.md` | 87 | 0 |
| `docs/roadmap/features/T5_F292.md` | 54 | 0 |
| `docs/system/ci-self-check-v1.md` | 3 | 3 |
| `docs/ui/design_reference/assumption_log.md` | 5 | 0 |
| `packages/orchestration/ci_budgets.py` | 117 | 1 |
| `scripts/self_use_queue.json` | 8 | 0 |
| `tests/docs/test_docs_consistency.py` | 1 | 1 |
| `tests/orchestration/test_ci_budgets.py` | 309 | 0 |
| `tests/orchestration/test_ci_stages.py` | 6 | 4 |
| `tests/ui_contracts/test_palette_contract.py` | 187 | 0 |
| `tests/ui_contracts/test_palette_sheet_wiring.py` | 145 | 0 |
| `tests/ui_contracts/test_semantic_zoom_wiring.py` | 7 | 1 |
| `tests/ui_contracts/test_term_panel_wiring.py` | 5 | 2 |
| `tests/ui_server/test_dashboard_contract.py` | 5 | 2 |

🤖 Generated with [Claude Code](https://claude.com/claude-code)
