# Plan — Steps 1917-1960: Token-Aware Repair Loop v1/v2

## Goal
Turn test failures and review findings into a controlled, token-aware repair workflow:
Failure Artifact → Minimal Repair Context → Fix Candidate → Review → Re-Test. Remedy governs the loop,
tracks progress toward the Mission Contract, and prevents unbounded/expensive/unsafe repair attempts.
Orchestration/metadata/evaluation ONLY — no model execution, no auto-apply.

## Core principle
Workers execute. Remedy governs. Token reduction is first-class: minimal context (safe summaries +
output_ref, never raw logs/diffs). Candidate received ≠ repaired. Reviewer + re-test gates enforced.
Unknown/oversized context → compression or human decision, never blind expensive routing.

## Current Step
1939-1940 — builder work complete; targeted suites green; running full suite once, then handoff.
Awaiting reviewer verdict (R-0105+).

## Steps
- [x] 1917: mainline closure (PR #73 → main 43197d9; fresh branch) + reconcile + carried risks
- [x] 1918: architecture doc (token-aware-repair-loop-v1-v2.md)
- [x] 1919: core repair_loop_v2.py models + statuses (Policy/WorkItem/Attempt/Evaluation)
- [x] 1920: storage (atomic, corruption-aware, idempotent, bounded export)
- [x] 1921: failure artifact → repair work item
- [x] 1922: review finding → repair work item (Done ≠ Resolved)
- [x] 1923: token-aware repair context pack (minimal; oversized/unknown → compression/human)
- [x] 1924: route recommendation (Worker Registry/Route Policy/Token Economy/Tournament/Builder Routing)
- [x] 1925: candidate intake (external builder / local candidate / candidate quality; received ≠ repaired)
- [x] 1926: review gate (open finding blocks; Done ≠ Resolved; PASS WITH RISKS low-only)
- [x] 1927: re-test gate (failed blocks; passed satisfies; no-retest-after-apply blocks; max_retests)
- [x] 1928: repair loop state machine evaluate_repair_loop (no infinite loop; every state next action)
- [x] 1929: mission contract integration (required repair items block; repaired satisfies)
- [x] 1930: CLI surface (item-create-from-failure/review, show/list, context-pack, route-recommend,
      evaluate, attempts, policy-show/set, integrity)
- [x] 1931: command catalog + run_contract registration (read_only/write_metadata; no may_execute)
- [x] 1932: progress ledger integration
- [x] 1933: feature planner / IdeaFactory (required blockers vs optional ideas, Impact/Effort)
- [x] 1934: review bundle section (repair_loop_summary)
- [x] 1935: cockpit read-only surface (repair_loop)
- [x] 1936: integrity checks
- [x] 1937: user-facing doc
- [x] 1938: architecture guards
- [x] 1939: targeted tests
- [ ] 1940: full suite once
- [ ] 1941: final handoff
- [ ] 1942-1960: reserved for reviewer findings (R-0105+)

## Hard rules
- No provider/model/Claude/Pi/OpenCode/Ollama/worker execution; no automatic candidate generation by
  model; no auto-apply/approve/autonomous mutation/PR/git; no real rollback restore; no MemPalace/
  internal memory/embeddings; no UI redesign; no MCP; no shell=True; no arbitrary command execution.
- Subprocess only via the already-approved real test execution path, bounded by max_test_runs.
- Minimal token-aware context; no raw logs/stdout/stderr/candidates/diffs/secrets/abs paths public.
- Candidate ≠ repaired; reviewer PASS + re-test green required per policy; Done ≠ Resolved; no fake
  repaired; required blockers separated from optional future ideas; next_safe_action catalog-valid.
- Tests via scripts/remedy_pytest.sh; full once. Auto-merge on reviewer PASS (no PR unless asked).

## Next block
Main Builder Adapter v0: Claude/Pi/OpenCode Worker Control Plane (only after this block PASS).
