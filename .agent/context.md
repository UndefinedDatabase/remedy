# Context

## Active Branch
feature/steps-247-252-data-honest-contract

## Scope
Steps 253-260: Contract Repair, Safety Quick Wins, Real Runtime Tests.

## Current Problems (from review)
- R-1001: `live.running` defaults to `true` when live-state API fails (remedyApi.ts)
- R-1002: Dashboard missing spec fields (generated_at, source, redaction, graph_summary)
- Readiness endpoint imports nonexistent `packages.orchestration.readiness`
- UI server auto-runs npm install/build by default (mutation from read-only command)
- Frontend silently converts failed endpoints to `{}`
- `remedy test list` is not a valid command (should be `remedy test discover`)
- `remedy job permit` arg order wrong in some generated strings
- Autonomy loop levels diverge from readiness definitions at levels 2-6
- source_apply.py has no permission/approval boundary
- test_runner.py persists unbounded raw output
- command_discovery.py uses `.split()` not `shlex.split()` for constitution commands

## Constraints
- No mutation endpoints, no shell=True, no 0.0.0.0
- No fake state, no optimistic LIVE
- React 19 + TypeScript + MUI + CSS Modules
- Redaction: no raw content in UI/API surfaces
