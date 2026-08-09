# Live Review — F105 Cache-optimal prompt ordering

> Reviewer: the main session of a one-session self-drive build
> (docs/agents/self_drive_protocol.md). Worker: one delegated subagent per
> round. Findings are authored here by the reviewer only. A worker marks a
> landed fix `Landed: R-XXXX`; only reviewer-authored `Done:` text sets
> Resolved (docs/agents/planner_reviewer_prompt.md §4.4).
> Branch: feature/f105-cache-optimal-prompt-ordering. Next free ID: R-0229.

## Findings

- R-0221 (Low, carried from F103 R5 through the whole of F104):
  `TestAutoBuildBehavior::test_auto_build_runs_by_default` in
  `tests/ui_server/test_dashboard_contract.py` pops `REMEDY_UI_NO_AUTO_BUILD`
  and runs a real `npm install` + `npm run build` in whatever checkout it runs
  in, refreshing `apps/ui/dist` mtimes mid-suite. That costs every integration
  gate six or seven phantom base-only failures through the mtime comparison in
  `_frontend_is_stale()`. Carried into F105 unchanged: it is not this feature's
  code either, AGENTS.md Scope Control bars the "while I'm here" edit, and it
  stays routed to the F252 flake-debt class, to be attributed by controlled
  evidence at the integration gate rather than chased. OPEN.

## Steps

- R1: claim F105 `[~]` under Rule A5, sweep both F104 closure candidates into
  docs/agents/planner_reviewer_prompt.md (§4.4 `Landed:` versus `Done:`, §4.13
  the terminating convention), empty `.agent/candidates.md`, and reset the
  `.agent/` state to F105. No `packages/`, `apps/`, `tests/` or `README.md`
  byte changed.
