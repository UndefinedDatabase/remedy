# Context

## Active Branch
feature/steps-247-252-data-honest-contract

## Scope
Steps 485-499: Dashboard visual repair round 2 — complete.

## Completed
- Graph: stable 1120x680 viewBox, ROOT_R=38, TASK_R=14, curved bezier edges
- Graph hover: tooltip near node (not fixed bottom), keyboard focus with tabIndex
- AgentNow: honest states (Idle/Working/Blocked/Needs decision), no MUI, custom glyphs
- Token tooltip: overflow:visible on metrics bar, z-index 5 for bar
- Logo: RemedyMark replaces NetworkLogoIcon
- Detail panel: Outcome/Checked/Action sections, no "Next safe action"
- 35 drift tests (13 new) protecting all changes

## Dashboard Readiness
~40-45% — graph stable and meaningful, right panel user-facing, agent card honest.
Still needs: manual QA, task outcome data from backend, visual polish iteration.

## Recommended Next Block
Steps 500+ — Real Ollama Trial Round
