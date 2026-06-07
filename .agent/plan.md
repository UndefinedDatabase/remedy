# Plan — Steps 715-724: Runtime File Order Hang Fix

## Goal
Find and fix any remaining environment-specific hang in propose/worker runtime files.
Add diagnostic trace + hardened cleanup as defense-in-depth.

## Current Step
724 — Final handoff (complete)

## Steps
- [x] 715: Correct handoff — reviewer reports order-dependent hang, not reproduced locally
- [x] 716: Added diagnostic trace (START/END/TIMEOUT per command)
- [x] 717: Ran propose runtime with trace — no hang (11 passed, 2.38s)
- [x] 718: No hang found — no fix needed
- [x] 719: Hardened process group cleanup — _ensure_process_group_dead with SIGTERM→wait→SIGKILL
- [x] 720: Worker runtime — 6 passed, 4.85s, clean exit
- [x] 721: Anti-regression tests — 6 tests covering timeout kill, trace log, pgid check
- [x] 722: Smoke updated — includes helper tests (183 total)
- [x] 723: Final proof — all 3 commands pass and exit cleanly
- [x] 724: Final handoff
