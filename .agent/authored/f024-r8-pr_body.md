## What

F024 — Phase timeline with scrubber. The bar under the brain graph now reads the job's six phases
from the event ledger itself, marks the decisions, failures, heals and stops on the track at their
seq, and is a scrubber: dragging or clicking the track, clicking a mark, or the keyboard (arrows one
event, Shift+arrows one phase, Home, End) shows the graph exactly as the reducer left it at that
point of the ledger. While scrubbed, a SCRUBBED banner sits on the stage, the live pill reads
REPLAY and the store keeps ingesting underneath; LIVE returns by a fast-forward capped under a
second, or by a labeled rebuild after more than 5000 queued events.

## Why

Time was not navigable: the bar showed server-derived phase states with no position and no way
back. Now any moment of a run can be replayed, and the phase boundaries are derived from events,
never from wall-clock guesses.

## Key decisions (in `.agent/decisions.md`)

- F024 D1 — the phase mapping table over the measured ledger writers; phases only move forward, a
  skipped phase is a zero-span tick, and Finalized is derived from the reducer's task states
  because no completion event exists; sub-glyphs from two tables and the review verdict.
- F024 D2 — snapshots every 200 seq, capped at 64 and dropped farthest-first, invalidated by the
  rows they should have held, held to a fresh fold at fuzzed positions.
- F024 D3 — T003's pure half: an index reading every prefix's phases from one fold, the scrubber
  machine with its keyboard and capped catch-up, and the bar's view model of six equal segments.
- F024 D4 — one ledger and one scrubber in the shell, handed to the bar, the stage and the pill.
- F024 D5 — a real fake job's ledger scrubbed at every position by the real modules, and the scrub
  budget on the 500-node fixture with the snapshot arithmetic shown and a red control.

## How to review

Start with `apps/ui/src/components/timeline/phaseMapping.ts`, then `scrubSnapshots.ts`,
`timelineIndex.ts`, `scrubState.ts` and `timelineView.ts`, then `useTimelineScrub.ts` and the
changes to `PhaseTimeline.tsx`, `RemedyShell.tsx`, `BrainGraphStage.tsx` and `LiveStatusPill.tsx`.
The Built State of `docs/roadmap/features/T5_F024.md` names the test for each acceptance line; each
round's mutation tool is `.agent/authored/f024-r<n>-mutations.py`, and the four places the bar
departs from the design pack are F024's rows of `docs/ui/design_reference/assumption_log.md`.

## Verification

- The one full suite: `19176 passed, 20 skipped` at exit 0, no bad node
  (`.agent/authored/f024-closure-suite.txt`).
- Scrub budget on the 500-node fixture: 60 frames a second while the handle sweeps one event per
  frame, worst 95th-percentile frame 16.8 ms, warm per-position cost 1.4 ms at the 95th percentile
  (`.agent/authored/f024-r5-perf.txt`); the tool's red control fails.
- Live end-to-end: `tests/ui_server/test_timeline_scrub_live.py` runs a fake-provider job and
  scrubs its real ledger at every position against a fresh fold.
- Evidence job `f024r7e1001` against the fork point `1bb3a35d`: 922 selected tests passed at exit
  0, the eslint, tsc and vitest nodes among them.
- Review package `remedy-review-20260925-082755-READY_FOR_REVIEW.zip`, SHA-256
  `1c4b4b358b97b54252a665e60acd3eaaedb134b8b3b0cbbe5ee36d80e60289e6`, READY_FOR_REVIEW.

## Findings and notes

None registered. The one open finding, R-1008, is owned by the next findings paydown, F285. The
dashboard's server-derived `phases` and `timeline_events` stay in the payload but no longer feed
the bar.

## Runtime actuals

Eight rounds in one session; reviewer and workers ran as Claude Opus 5.5; wall clock and tokens not
measured.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
