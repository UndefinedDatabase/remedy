# Plan — Steps 1180-1192: Merge Closure + Operator Cockpit v1 (read-only UI)

## Goal
Close R-0070 (changed-files table) for prior block, then extend the read-only
dashboard truth (tests/proof/snapshot/continuation) and rebuild the operator
cockpit UI to the reference design pack. Strictly READ-ONLY: no mutation
endpoints, no fabricated state, no raw data in payload/UI.

## Current Step
1192 — docs/operator-cockpit-v1.md (done) + final handoff (full suite running)

## Steps
- [x] 1180: R-0070 changed-files table (1155-1179) + Open PR gate + full-suite note
- [x] 1181: Backend dashboard truth (metrics.tests/proof, snapshot, continuation) + ui_server tests
- [x] 1182: Frontend types + API mapping (unknown-safe) + remedyApi tests
- [x] 1183: styles/tokens.css + globals.css
- [x] 1184: TopMetricsBar (TSX + CSS)
- [x] 1185: CommandBar (jump-to/filter, no fake chat)
- [x] 1186: Graph stage/node paint + GraphFilterChips + layout-dot rules
- [x] 1187: PhaseTimeline (TSX + CSS)
- [x] 1188: RightLivePanel cards (LiveStatusPill/AgentNow/Activity/TaskChecklist/NeedsAttention)
- [x] 1189: DetailPopover task-detail product rule (unknown-safe)
- [x] 1190: Truth-contract tests (pytest + vitest) + low findings R-0071/73/74/75
- [x] 1191: Real-data acceptance (data-truth+redaction+build verified; visual = operator-side)
- [x] 1192: docs/operator-cockpit-v1.md + final handoff

## Hard rules
- READ-ONLY UI: POST/PUT/DELETE stay 405. No mutation endpoints/buttons.
- No raw data in UI/payload: no diffs/stdout/tracebacks/abs paths/blobs/secrets/prompts.
- No demo/synthetic data; no element claiming unproven state.
- No new deps, no Tailwind, no CDN, no external fonts. React 19 + TS + CSS Modules.
- No shell=True. No background pytest. scripts/remedy_pytest.sh, targeted first,
  full suite at most ONCE at block end.
- No git reset/checkout/clean, no auto-push, no auto-merge. PR only on user OK.
- Done: R-XXXX markers per finding; re-check live_review.md regularly.

## Next Block
Repair Loop v1.
