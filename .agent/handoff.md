# Handoff — F281 R25

**Session:** F281's fourth session

## Round Summary

Round 25 books round 24's PASS verdict and lands R-0805, implementing dead-session archiving with a new --all flag on `remedy ui status`. Dead sessions are archived to `<data_root>/ui/sessions_dead/` (capped at ten most-recently-ended), shown only when --all is passed, and pruned on every ui start/ui status/ui stop call. Four new tests cover archive behavior, default-view/--all distinction, cap enforcement, and grouped CLI round-trip.

## Commits

| Commit | Message | Files |
|--------|---------|-------|
| C1 (92d7ec3e) | F281 R25 C1: book round 24 PASS, update plan | .agent/live_review.md, .agent/plan.md, .agent/authored/f281-r25.md, .agent/last_block.md |
| C2 (1a54e4b6) | F281 R25 C2: land R-0805 — prune dead UI sessions, add ui status --all | apps/cli/commands/ui.py, apps/cli/command_catalog.py, tests/ui_server/test_live_state.py |
| C3 (pending) | F281 R25 C3: resolve R-0805, handback — Round 25 complete | .agent/live_review.md, .agent/handoff.md |

## Changes Summary

**C1:** Appended R24 gate entry to live_review.md and replaced plan.md reflecting R25 work scope (R-0805 implementation, R-0895 remaining).

**C2:** Rewrote `apps/cli/commands/ui.py` with dead-session archive functions (`_dead_sessions_dir`, `_archive_dead_session`, `_prune_dead_archive`, `_read_dead_sessions`, `_prune_dead_and_get_live`); updated `_cmd_ui_status` to show live-only by default and archived ten when --all is passed; updated ui.start, ui.stop to call pruning. Updated `apps/cli/command_catalog.py` ui.status entry with --all flag (is_flag=True). Added four tests to `tests/ui_server/test_live_state.py` covering archive-not-delete, default/--all distinction, ten-entry cap with eviction, and grouped CLI flag round-trip.

**C3:** Appended R-0805 resolution to live_review.md documenting archive implementation and test coverage.

## Gate Results

**G1 - TARGETED:**
```
python3 -m pytest tests/ui_server/test_live_state.py tests/test_command_catalog.py tests/cli/test_command_catalog.py -q
Result: 122 passed in 4.59s
```

**G2 - CANARY:**
```
python3 -m pytest tests/cli/test_golden_path.py -q
Result: 42 passed in 19.40s
```

**G3 - RUFF:**
```
python3 -m ruff check apps/cli/commands/ui.py apps/cli/command_catalog.py
Result: All checks passed!
```

**G4 - DIRECT MEASUREMENT:**
End-to-end sequence with fresh temp dir:
- Call 1 (show_all=False, one dead session): `_cmd_ui_status(show_all=False)` outputs `"No UI sessions.\n"` (dead pruned silently)
- Call 2 (show_all=True, two dead sessions): `_cmd_ui_status(show_all=True)` outputs `"Last dead sessions:"` header, two [DEAD] lines with ended= timestamps

**G5 - MUTATION RED-PROOF:**
- With fix applied: `test_status_default_never_shows_dead_but_all_does` → `1 passed`
- With mutation (always show dead sessions): test → `1 failed` (assertion "DEAD" not in output fails when dead shown by default)
- With fix reapplied: test → `1 passed`
- Worktree removed after verification

**G6 - TREE:**
```
git status --porcelain: empty
git worktree list: one row (primary checkout)
HEAD: 1a54e4b6 on origin/feature/f281-cli-help-surface
```

## Findings

**R-0805 — CLOSED this round in C2**

Dead-session archive implemented with acceptance criteria fully met: dead sessions are archived (never just deleted) into `<data_root>/ui/sessions_dead/`, capped at ten most-recently-ended entries (oldest evicted), each carrying an `ended_at` timestamp, shown only with --all flag (is_flag=True, guarding against the repo's known prefix-match pitfall), pruned on every ui start/ui status/ui stop call. Tests cover archive behavior, default-view hiding, --all display, ten-entry cap, and real round-trip through grouped CLI argparse wiring. `docs/roadmap/features/T2_F261.md`'s Acceptance line now holds.

**Open Acceptance items:** R-0895 (README quickstart) is the only remaining item — it quotes the finished catalog, running last.

## Next Action

R-0895 is next: verify the catalog is stable and write the README quickstart prose quoting finished vocabulary.
