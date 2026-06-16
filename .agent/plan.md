# Plan — Steps 2206-2225: Dogfood Run Closure + Replay Evidence Hardening v0.1

## Goal
Close R-0116/R-0117/R-0118 from Steps 2146-2205 block. Harden integrity + evidence gathering.

## Core principle
Workers execute. Remedy governs. Done != Resolved. Reviewer verdict beats self-report.

## Current Step
2206-2225 — all fixes + tests implemented; 60 targeted + 18 catalog + 6565 full suite passed.

## Steps
- [x] R-0116: 7 new deep integrity checks (satisfied_with_unsatisfied_mission, satisfied_with_open_findings, satisfied_with_failing_tests, guardrail_exceeded_without_terminal_status, active_lane_status_mismatch, replay_raw_data_leak, brainstorm_required_without_evidence)
- [x] R-0117: Evidence gathering from builder sessions, managed executions, proof chain
- [x] R-0118: Hygiene — unused _safe_path_label import removed; _RAW_MARKERS used in leak check; stopped_by_operator + not_started progress items explicit
- [x] 60 targeted tests passed; 18 catalog tests passed; 6565 full suite passed
- [ ] Commit + push + PR + reviewer verdict

## 30-task backlog
- Strict completed: 0/30
- Partially prepared: ~5/30
- Next selected: Ruff/Mypy/Coverage Baseline v0

## Hard rules
No shell=True; no provider SDK; no auto-apply/approve/PR/git; no MemPalace/embeddings.
