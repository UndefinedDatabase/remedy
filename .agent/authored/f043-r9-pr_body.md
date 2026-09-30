## What

F043 — Explanation layer. The cockpit uses many words of Remedy's own, such as phases, statuses,
metrics and badges, and until now nothing on the page said what they mean. Now:

- T001 — one catalog, `apps/ui/src/api/terminology.ts`, holds every explanation: a title, a
  plain-language body of at most 240 characters, the file that defines the term and a phrase that
  file states. A test reads each such file back and fails when the phrase is gone, so the catalog
  quotes its single source instead of copying it. The `Term` component underlines a word, writes its
  key into `data-term`, and opens a glass tooltip on keyboard focus at once and on hover after
  120 ms; the token and cost tiles show their live breakdown under the explanation.
- T002 — the audit. It renders the real right panel, the metrics bar, the status pill in each state
  and the timeline, and fails in both directions: a term on the page that the catalog lacks, and a
  catalog entry nothing renders. Two drift fixtures hold each direction red.
- T003 — the question mark key and a Terms button open a searchable panel of every entry. A
  six-step first-run tour runs on `TourFrame`, the overlay engine the result tour now renders
  through as well; it opens by itself once per browser, records any way of ending it under
  `remedy:first-run-tour`, and starts again from the Terms panel. Its palette step points at the
  Terms button until a command palette exists. A browser test runs a real demo job, builds the
  cockpit into its own folder, and proves the audit, the tour, a tooltip and the panel on the real
  page. `docs/guides/explanation-layer-user-guide-v1.md` explains it all for a user.

The closure's own self-use item, `SU-038`, ran on `claude-cli` with Sonnet for builder and reviewer
in two provider calls ($0.57), narrowed the handler around `load_project_constitution` in
`_prepare_viewer` of `apps/cli/commands/brain.py` to `OSError`, lowered `MAX_EXCUSED` to 288, and is
landed here with two reviewer tests (DECISION F043 D6).

## Why

`docs/roadmap/features/T5_F043.md`: nothing in the cockpit should be jargon without a hand to hold,
and every explanation must come from one source so it cannot drift from the definition it explains.

## Key decisions (in `.agent/decisions.md`)

- F043 D1 — the catalog's shape, and quoting a source by file and phrase, checked by a test.
- F043 D2 — which surfaces carry terms; a term inside a button opens on hover only; two descendant
  rules of the right panel's sheet narrowed to direct children.
- F043 D3 — the tiles' breakdown moves into the term's tooltip; the '?' key and the Terms panel;
  `blocked.task` becomes `task.blocked`.
- F043 D4 — the six-step tour on the shared `TourFrame` engine, once per browser, relaunchable.
- F043 D5 — the end-to-end browser test over a real demo job, and the user guide.
- F043 D6 — `SU-038` landed as its job's own diff with two tests.

## How to review / test

- `npm --prefix apps/ui run test:unit -- src/api/terminology.test.ts src/api/terminologyAudit.test.ts src/api/termSearch.test.ts src/api/firstRunTour.test.ts src/components/term/`
- `python3 -m pytest -q tests/ui_contracts/test_term_panel_wiring.py tests/ui_contracts/test_tour_overlay_contract.py tests/ui_server/test_explanation_layer_live.py tests/test_brain_viewer.py tests/test_ble001_ratchet.py`
- The one full suite: `.agent/authored/f043-closure-suite.txt` (`20984 passed, 20 skipped`, exit 0).
- Evidence job `f043r8e1001`; package `remedy-review-20260930-033441-READY_FOR_REVIEW.zip`, SHA-256
  `a9e44274ad032d41fae6741aeaa5f891ecfd983d5af99663208d97f1560da6e1`, accepted head `79137914`.
- Round-by-round review record: `.agent/live_review.md` and its archive.

Latest verdict: round 8 PASS, booked in round 9. Open findings: 0 (R-1115, a tooltip detail that
rendered inline, was raised in round 3 and repaired in round 4).

Runtime actuals: 9 delegated rounds over 2 sessions; wall clock and token use of the building
sessions not measured; the self-use job measured $0.57 in 2 provider calls.

## Changed files (outside `.agent/`, fork point `21bfc188` to this branch)

| Path | + | - |
|---|--:|--:|
| `README.md` | 12 | 2 |
| `apps/cli/commands/brain.py` | 1 | 1 |
| `apps/ui/src/api/firstRunTour.test.ts` | 99 | 0 |
| `apps/ui/src/api/firstRunTour.ts` | 80 | 0 |
| `apps/ui/src/api/termSearch.test.ts` | 82 | 0 |
| `apps/ui/src/api/termSearch.ts` | 67 | 0 |
| `apps/ui/src/api/terminology.test.ts` | 345 | 0 |
| `apps/ui/src/api/terminology.ts` | 210 | 0 |
| `apps/ui/src/api/terminologyAudit.test.ts` | 43 | 0 |
| `apps/ui/src/api/terminologyAudit.ts` | 34 | 0 |
| `apps/ui/src/components/graph/BrainGraphStage.tsx` | 2 | 1 |
| `apps/ui/src/components/metrics/TopMetricsBar.module.css` | 3 | 14 |
| `apps/ui/src/components/metrics/TopMetricsBar.tsx` | 44 | 27 |
| `apps/ui/src/components/panels/ActivityFeedCard.tsx` | 3 | 2 |
| `apps/ui/src/components/panels/AgentNowCard.tsx` | 3 | 2 |
| `apps/ui/src/components/panels/ChatInput.tsx` | 1 | 1 |
| `apps/ui/src/components/panels/DecisionInboxCard.tsx` | 2 | 1 |
| `apps/ui/src/components/panels/LiveStatusPill.tsx` | 5 | 4 |
| `apps/ui/src/components/panels/RightLivePanel.module.css` | 4 | 2 |
| `apps/ui/src/components/panels/RightLivePanel.tsx` | 4 | 1 |
| `apps/ui/src/components/panels/TaskChecklistCard.tsx` | 14 | 3 |
| `apps/ui/src/components/shell/RemedyShell.tsx` | 28 | 1 |
| `apps/ui/src/components/term/Term.module.css` | 73 | 0 |
| `apps/ui/src/components/term/Term.tsx` | 125 | 0 |
| `apps/ui/src/components/term/TermPanel.module.css` | 65 | 0 |
| `apps/ui/src/components/term/TermPanel.tsx` | 68 | 0 |
| `apps/ui/src/components/term/termAudit.test.ts` | 267 | 0 |
| `apps/ui/src/components/term/termPanel.test.ts` | 47 | 0 |
| `apps/ui/src/components/timeline/PhaseTimeline.tsx` | 13 | 10 |
| `apps/ui/src/components/tour/FirstRunTour.tsx` | 112 | 0 |
| `apps/ui/src/components/tour/TourFrame.tsx` | 64 | 0 |
| `apps/ui/src/components/tour/TourOverlay.module.css` | 13 | 1 |
| `apps/ui/src/components/tour/TourOverlay.tsx` | 24 | 34 |
| `apps/ui/src/styles/tokens.css` | 7 | 0 |
| `docs/README.md` | 2 | 0 |
| `docs/agents/planner_reviewer_prompt.md` | 6 | 0 |
| `docs/guides/explanation-layer-user-guide-v1.md` | 49 | 0 |
| `docs/roadmap/STATUS.md` | 1 | 1 |
| `docs/roadmap/features/T5_F043.md` | 52 | 0 |
| `docs/ui/design_reference/assumption_log.md` | 1 | 0 |
| `scripts/self_use_queue.json` | 8 | 0 |
| `tests/test_ble001_ratchet.py` | 1 | 1 |
| `tests/test_brain_viewer.py` | 42 | 0 |
| `tests/ui_contracts/test_design_drift.py` | 4 | 1 |
| `tests/ui_contracts/test_term_panel_wiring.py` | 55 | 0 |
| `tests/ui_contracts/test_tour_overlay_contract.py` | 27 | 7 |
| `tests/ui_server/test_explanation_layer_live.py` | 253 | 0 |

🤖 Generated with [Claude Code](https://claude.com/claude-code)
