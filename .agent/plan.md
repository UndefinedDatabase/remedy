# Plan — Steps 850-864: Provenance + Agent Tooling

## Goal
Stop file provenance from over-associating tests and add verified, safe Pi/Claude/VS Code local agent tooling docs/config.

## Current Step
863-864 — final state updates, optional fast lane, PR handoff

## Steps
- [x] 850: Handoff repair — carry review blocker and scope shift
- [x] 851: Fix file_provenance linked-test filtering
- [x] 852: Add file provenance/proof agreement tests
- [x] 853: Inspect actual `.pi`, `.claude`, MCP, package setup
- [x] 854: Verify Pi/Claude/VS Code/MCP docs and package audit inputs
- [x] 855: Add safe Claude project setup
- [x] 856: Add safe Pi project setup
- [x] 857: Add minimal inactive MCP/VS Code config with verified schemas
- [x] 858: Add docs/agent-tooling-audit.md
- [x] 859: Add read-only tooling doctor script
- [x] 860: Add tooling config/doctor/security tests
- [x] 861: Run targeted tests via wrapper
- [x] 862: Package audit/version report; no upgrades
- [ ] 863: Final state updates and PR handoff
- [ ] 864: Final report

## Risks
- `.claude/settings.local.json` remains local/ignored and was not committed.
- No MCP servers are active; future MCP installs must be audited separately.
- Full pytest not run yet; targeted suite passed.
