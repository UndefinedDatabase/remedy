# Plan — Steps 1245-1274: Bounded Overnight Preparation v0 (read-only)

## Goal
Read-only planning/readiness/stop-reason/morning-report layer for FUTURE bounded
overnight runs. No executor, no scheduler, no background worker, no apply/test/
repair/provider execution. Answer: is this job safe unattended? what next? what
limits? what would stop it? what evidence exists/missing? morning checklist?

## Current Step
1274 — Final handoff + merge recommendation (full suite re-run in progress post R-0079/80 fix)

## Steps
- [x] 1245: Mainline handoff reconciliation (PR #54 merged; scope→1245-1274; new branch)
- [x] 1246: overnight_readiness.py models
- [x] 1247: BoundedOvernightPolicy (conservative defaults: planning/report only)
- [x] 1248: Readiness inputs from real durable sources (no event-only proof)
- [x] 1249: Capability matrix (status/reason/required perm+action/evidence/next action)
- [x] 1250: Stop reason taxonomy
- [x] 1251: select_overnight_next_action (deterministic, catalog-backed, no fakes)
- [x] 1252: Morning checklist builder (every done needs evidence)
- [x] 1253: Budget summary (contract limits vs usage; unknown stays unknown)
- [x] 1254: Risk summary (blocker/high/medium/low)
- [x] 1255: CLI overnight readiness
- [x] 1256: CLI overnight plan (dry-run, ≤1 hypothetical cycle)
- [x] 1257: CLI overnight report (markdown/json)
- [x] 1258: Command catalog entries (read_only, no mutate/execute)
- [x] 1259: Progress Ledger integration
- [x] 1260: Feature Planner integration
- [x] 1261: Review Bundle overnight_readiness_summary.json
- [x] 1262: Operator Cockpit read-only overnight payload
- [x] 1263: Integrity gate integration (lightweight; fail→blocked, unknown→risk)
- [x] 1264: Runtime CLI tests
- [x] 1265: Readiness truth tests (no event-only proof)
- [x] 1266: Redaction tests
- [x] 1267: Architecture guards
- [x] 1268: Docs (bounded-overnight-prep-v0 + cross-links)
- [x] 1269: Targeted tests + full pytest once
- [x] 1270: Live review
- [x] 1271: PR discipline (clean tree, no drift; prep PR text, no PR without OK)
- [x] 1272: Product readiness update
- [x] 1273: Final handoff
- [x] 1274: Merge recommendation

## Hard rules
- READ-ONLY. No repo mutation from overnight commands (safe metadata report
  snapshot only if explicitly needed + documented). No background worker/scheduler.
- No apply/test/repair/provider execution. No auto-approve/revert/contract-relax.
- overnight_readiness must NOT import apply services, execute tests, call repair
  propose, or import provider/Ollama. No subprocess, no shell=True.
- Readiness never true from event-only proof; durable truth required; unknown
  stays unknown; stale/missing evidence → blocker/risk.
- Every next/suggested command must exist in command catalog; no fake actions.
- No raw stdout/stderr/source/diff/artifact-body/secrets/tracebacks/abs paths.

## Next block
Bounded Overnight Executor v0 OR Provider-backed Repair Builder v0.
