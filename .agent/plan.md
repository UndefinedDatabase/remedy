# Plan — amend1014-do-golden-path-now

## Goal
Repair the `remedy do` golden path (operator amendment amend1014-do-golden-path-now, 2026-10-14):
a bounded one-deliverable order runs as one job and one task with no planning provider call,
opens the cockpit before the worker, shows progress at once, and proposes a diff without touching
the target; `--yes` of `do` becomes `--run-unattended`. D1 to D6, mandatory tests 1 to 10, a real
acceptance run. Not a planner rewrite; no next roadmap feature until this is handed back.

## Current Step
On `feature/do-golden-path` (from `main` at `e688b30f3`). F078 stays untouched on
`feature/f078-autonomy-levels` (committed, pushed, no pull request). Implementation and tests are
written; remaining: commits in small steps, the one closure gate, the real acceptance run, the
pull request, the handback.

## Next Steps
1. Commit in logical steps (D2 planner, D1 lane, D4/D5 progress and cockpit, D3 flag, D6 prompt).
2. Closure: the repository's required integration gate once; record command, interpreter, SHA.
3. Real acceptance run against a fresh committed one-file repository with the real provider config.
4. Push, open the pull request, write `.agent/handoff.md`; do not merge.

## Risks
- The `.data` incident tree is blocked by a deny rule here; the captured-plan fixture is rebuilt
  from the order's task titles.
- Shared audit sentence "auto-approved via --yes" stays for `job` commands that keep `--yes`.
