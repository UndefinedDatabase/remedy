# Plan — Steps 1180-1192: Merge Closure + Operator Cockpit v1 (read-only UI)

## Goal
Close R-0070 (changed-files table) for prior block, then extend the read-only
dashboard truth (tests/proof/snapshot/continuation) and rebuild the operator
cockpit UI to the reference design pack. Strictly READ-ONLY: no mutation
endpoints, no fabricated state, no raw data in payload/UI.

## Current Step
1181 — Backend: extend `_build_dashboard` with tests/proof/snapshot/continuation truth

## Steps
- [x] 1180: R-0070 changed-files table (1155-1179) + Open PR gate + full-suite note
- [ ] 1181: Backend dashboard truth (metrics.tests/proof, snapshot, continuation) + ui_server tests
- [ ] 1182: Frontend types + API mapping (unknown-safe) + remedyApi tests
- [ ] 1183: styles/tokens.css + globals.css
- [ ] 1184: TopMetricsBar (TSX + CSS)
- [ ] 1185: CommandBar (jump-to/filter, no fake chat)
- [ ] 1186: Graph stage/node paint + GraphFilterChips + layout-dot rules
- [ ] 1187: PhaseTimeline (TSX + CSS)
- [ ] 1188: RightLivePanel cards (LiveStatusPill/AgentNow/Activity/TaskChecklist/NeedsAttention)
- [ ] 1189: DetailPopover task-detail product rule (unknown-safe)
- [ ] 1190: Truth-contract tests (ui_contract pytest + vitest)
- [ ] 1191: Real-data acceptance against reference checklist
- [ ] 1192: docs/operator-cockpit-v1.md + final handoff

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
