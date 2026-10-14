# Plan — amend1014-do-golden-path-now

## Goal
Repair the `remedy do` golden path (operator amendment amend1014-do-golden-path-now, 2026-10-14):
a bounded one-deliverable order runs as one job and one task with no planning provider call,
opens the cockpit before the worker, shows progress at once, and proposes a diff without touching
the target; `--yes` of `do` becomes `--run-unattended`. D1 to D6, mandatory tests 1 to 10, a real
acceptance run. Not a planner rewrite; no next roadmap feature until this is handed back.

## Current Step
Done and pushed: code commits C1 to C10, the closure gate green at `b6741dfbb` (23134 passed), the
real acceptance run reached the builder and stopped on a provider limit (the Ollama builder is
prose-only), the handback written, the pull request open and not merged.

## Next Steps
1. Operator: review the pull request; answer the one question in `.agent/handoff.md` about the
   Ollama builder.
2. After the merge, F078 resumes on `feature/f078-autonomy-levels` (its plan names round 4).

## Risks
- The `.data` incident tree is blocked by a deny rule here; the captured-plan fixture is rebuilt
  from the order's task titles.
- Shared audit sentence "auto-approved via --yes" stays for `job` commands that keep `--yes`.
