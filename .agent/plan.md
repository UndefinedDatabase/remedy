# Plan — Steps 850-864: Provenance + Agent Tooling

## Goal
Stop file provenance from over-associating tests and add verified, safe Pi/Claude/VS Code local agent tooling docs/config.

## Current Step
853-854 — inspect actual tooling setup and verify docs/package audit inputs

## Steps
- [x] 850: Handoff repair — carry review blocker and scope shift
- [x] 851: Fix file_provenance linked-test filtering
- [x] 852: Add file provenance/proof agreement tests
- [ ] 853: Inspect actual `.pi`, `.claude`, MCP, package setup
- [ ] 854: Verify Pi/Claude/VS Code/MCP docs and package audit inputs
- [ ] 855: Add safe Claude project setup
- [ ] 856: Add safe Pi project setup
- [ ] 857: Add minimal MCP/VS Code config only if schema verified
- [ ] 858: Add docs/agent-tooling-audit.md
- [ ] 859: Add read-only tooling doctor script
- [ ] 860: Add tooling config/doctor/security tests
- [ ] 861: Run targeted tests via wrapper
- [ ] 862: Package audit/version report; no blind upgrades
- [ ] 863: Final state updates and PR handoff
- [ ] 864: Final report

## Risks
- Do not commit fake Claude/Pi schemas; document uncertainty instead.
- `.pi` was absent on disk; `.claude/settings.local.json` exists and must not be overwritten blindly.
- Full pytest likely out of scope unless targeted suites pass quickly.
