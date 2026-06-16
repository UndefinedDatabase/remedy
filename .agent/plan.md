# Plan — Steps 2026-2075: Managed External Builder Execution v1 + Dogfood Observability

## Goal
Add first managed execution seam for external builder adapters: bounded command templates,
operator approval gate, managed subprocess runner (argv only, no shell), session event tracking,
redacted output refs, dogfood debug bundle, sandbox intake integration. Remedy governs; workers
execute. Builder output untrusted until verified.

## Core principle
Workers execute. Remedy governs. No provider monopoly. Subprocess ONLY through bounded command
templates with sanitized env, argv list, timeout, output cap.

## Current Step
2050-2051 — builder work complete; targeted + full suites green; awaiting reviewer verdict (R-0106+).

## Steps
- [x] 2026: mainline closure (PR #75 → main 8e7d2e5; fresh branch) + reconcile
- [x] 2027: architecture doc (managed-external-builder-execution-v1.md)
- [x] 2028-2030: core managed execution module (command templates + approval gate + managed runner)
- [x] 2031-2032: session event ledger + dogfood debug bundle
- [x] 2033-2034: sandbox intake integration + repair/mission state consumption
- [x] 2035-2038: CLI surface (9 commands) + command catalog + run_contract
- [x] 2039-2040: progress ledger / feature planner integration
- [x] 2041-2042: review bundle (35→36 sections) / cockpit integration
- [x] 2043-2044: integrity checks
- [x] 2045: user-facing doc
- [x] 2046: architecture guards
- [x] 2047-2048: targeted tests (630 passed)
- [x] 2049: full suite once (6427 passed, 8 skipped, 1 deselected, 0 failed)
- [ ] 2050: final handoff
- [ ] 2051-2075: reserved for reviewer findings (R-0106+)

## Hard rules
- Subprocess ONLY with argv list (no shell=True), sanitized env, timeout, output cap.
- No arbitrary shell; no provider SDK; no auto-apply/approve/PR/git; no MemPalace/memory/embeddings.
- All real adapters disabled by default. Managed runner disabled by default.
- Builder output ALWAYS untrusted: goes through External Builder Sandbox / Trust Gate / Candidate
  Quality / review / re-test gates. No direct repo write.
- Tests via scripts/remedy_pytest.sh; full once. Auto-merge on reviewer PASS (no PR unless asked).

## Next block
Ollama Cheap-Task Adapter v0 OR Overnight Autonomy Gate v1 (only after this block PASS).
