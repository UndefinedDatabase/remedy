# Plan — Steps 1837-1876: Overnight Mission Contract + Review/Repair Spine v0

## Goal
First hard mission-contract spine for Overnight Mode. A user mission becomes a CONTRACT; Remedy tracks
it until fulfilled or safely blocked, evaluating satisfaction from durable evidence (progress ledger,
review findings, tests/proof/snapshot gates, repair status, route/token/tournament readiness).
Metadata + state-machine + evaluation + reporting only — no execution, no fake overnight autonomy.

## Core principle
Workers execute. Remedy governs. The Mission Contract decides done — never from builder self-report.
Reviewer verdict beats self-report; Done != Resolved; open Blocker/High blocks satisfaction; missing
required gates block satisfaction; no fake readiness. User never feels lost.

## Current Step
1837 — mainline reconciliation done (PR #71 merged → main 4ddd59f; fresh branch). Building core.

## Steps
- [x] 1837: mainline closure (PR #71 → main 4ddd59f; fresh branch) + carried risks + MemPalace deferred
- [ ] 1838: architecture doc (overnight-mission-contract-review-repair-spine-v0.md)
- [ ] 1839-1846: overnight_mission.py core (models; storage; contract creation; review-findings
      blockers; evaluation; next-safe-action planner; review/repair state machine; required-vs-optional queue)
- [ ] 1850-1851: CLI (contract-create/show/evaluate/next-action/cycles/readiness/integrity) + catalog +
      run_contract actions (create write_metadata; rest read_only; no may_execute)
- [ ] 1847-1849,1852: progress_ledger + review_bundle section (32) + ui_server cockpit + integrity
- [ ] 1853: user-facing doc (overnight-mission-user-guide-v0.md)
- [ ] 1854-1855: tests (unit/CLI/integration/integrity) + architecture guards
- [ ] 1856: full suite once
- [ ] 1857: final handoff report (+ auto-merge on reviewer PASS)
- [ ] 1858-1876: reserved for reviewer findings (R-0102+)

## Hard rules
- NO provider/Claude/Pi/OpenCode/Ollama/cloud/local execution, network, browser, subprocess, shell.
- NO worker execution, test run, apply/approve, git/PR automation, MemPalace/memory/embeddings/vector
  DB, UI redesign, MCP, pricing sync.
- Satisfaction ONLY from durable evidence; reviewer verdict beats self-report; Done != Resolved; open
  Blocker/High blocks satisfaction; missing required gates block satisfaction; no fake readiness.
- Required blockers separated from optional future ideas. No raw prompts (beyond scrubbed user_goal)/
  logs/diffs/secrets/abs paths in public surfaces. next_safe_action catalog-backed.
- Tests via scripts/remedy_pytest.sh; full once. NO PR unless asked (auto-merge on reviewer PASS).

## Next block
Real Test Execution + Snapshot/Rollback Proof v1 (only after this block PASS).
