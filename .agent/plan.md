# Plan — Steps 1961-2025: Main Builder Adapter v0 + Token-Controlled External Session Rail

## Goal
Add a controlled external builder session rail: adapter types (Claude Code / Pi.dev / OpenCode /
generic CLI / fixture), token-aware request packages, session lifecycle metadata, fixture builder
for deterministic tests, External Builder Sandbox integration. Remedy governs; workers execute.
Builder output is untrusted until sandbox/trust/quality/review/retest gates pass.
Metadata/policy/evaluation/reporting ONLY — no model execution.

## Core principle
Workers execute. Remedy governs. No provider monopoly — all adapter types replaceable and user-
selectable. Token reduction is first-class. Builder output untrusted until verified.

## Current Step
2001-2002 — builder work complete; targeted + full suites green; awaiting reviewer verdict (R-0106+).

## Steps
- [x] 1961: mainline closure (PR #74 → main 719a4de; fresh branch) + reconcile + carried risks
- [x] 1962: architecture doc (main-builder-adapter-v0-token-controlled-session-rail.md)
- [x] 1963-1964: core adapter module (models + storage + redaction)
- [x] 1965-1966: adapter registry + policy (defaults, integrity)
- [x] 1967-1968: token-aware builder request package
- [x] 1969-1970: controlled session lifecycle
- [x] 1971-1972: fixture builder
- [x] 1973-1974: External Builder Sandbox integration (via intake path)
- [x] 1975-1976: Repair Loop integration (session status consumption)
- [x] 1977-1978: Mission Contract integration (builder_adapter_mission_signal)
- [x] 1979-1980: Token Economy / Tournament / Worker Registry integration (recommend_builder_adapter)
- [x] 1981-1984: CLI surface (10 commands)
- [x] 1985-1986: Command Catalog + Run Contract
- [x] 1987-1988: Progress Ledger integration
- [x] 1989-1990: Feature Planner / IdeaFactory integration
- [x] 1991-1992: Review Bundle integration (34→35 sections)
- [x] 1993-1994: Cockpit read-only surface
- [x] 1995-1996: Integrity checks
- [x] 1997: user-facing doc
- [x] 1998: architecture guards
- [x] 1999-2000: targeted tests (591 passed)
- [x] 2001: full suite once (6360 passed, 8 skipped, 1 deselected, 0 failed)
- [ ] 2002: final handoff
- [ ] 2003-2025: reserved for reviewer findings (R-0106+)

## Hard rules
- No provider/model/Claude/Pi/OpenCode/Ollama/worker execution; no automatic candidate generation by
  model; no auto-apply/approve/autonomous mutation/PR/git; no real rollback restore; no MemPalace/
  internal memory/embeddings; no UI redesign; no MCP; no shell=True; no arbitrary command execution.
- All real adapters disabled by default. Fixture adapter only in explicit test/fixture mode.
- No provider SDK imports. No secrets/env tokens stored. No hardcoded provider monopoly.
- Builder output is ALWAYS untrusted: goes through External Builder Sandbox / Trust Gate / Candidate
  Quality / review / re-test gates. No direct repo write in v0.
- Tests via scripts/remedy_pytest.sh; full once. Auto-merge on reviewer PASS (no PR unless asked).

## Next block
Managed External Builder Execution v1 OR Ollama Cheap-Task Adapter v0 (only after this block PASS).
