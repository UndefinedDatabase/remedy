---
description: Use when the operator starts a session to have Remedy build itself end to end with no paste relay (SSH-from-phone mode). Runs the one-session planner/reviewer discipline of docs/agents/self_drive_protocol.md — state probe, decide, delegated rounds, guardrails, clean handoff.
---

# Remedy Self-Drive Skill

Authority order: `AGENTS.md` first, then
`docs/agents/self_drive_protocol.md` (the full protocol — read it before
acting), then `docs/agents/planner_reviewer_prompt.md` for the review
loop. This skill is the entry point, not a second source of truth: where
this file is shorter than the protocol, the protocol wins.

## Invariants you may not relax
- You are the planner and reviewer. You never edit a work-tree file.
  Every write goes through a delegated worker subagent, one per round.
- Merges happen only at the AGENTS.md Open PR Gate. Never force-push.
  Never work on `main`.
- Gates are executed, never assumed. A summary is not evidence; re-run
  the round's commands yourself before any verdict.
- `.agent/STOP`, a session limit, or ambiguity the rules do not resolve
  → write `.agent/handoff.md` and end cleanly. That is a success.

## 1. State probe (always first, read-only)
```bash
git status --porcelain
git branch --show-current
git log --oneline -n 8
gh pr list --state open --json number,headRefName,baseRefName,isDraft
remedy plan status
remedy plan next
```
Then read from disk: `.agent/handoff.md`, `.agent/plan.md`,
`.agent/live_review.md`, `.agent/candidates.md`, and the active feature
file in `docs/roadmap/features/`.

## 2. Decide (first match wins)
1. `.agent/STOP` present → hand off and end.
2. Exactly one open non-draft `feature/*` → `main` PR → merge it at the
   Open PR Gate before creating any branch. Any other PR shape → stop
   and report.
3. `.agent/candidates.md` non-empty → register or resolve every entry
   and empty the file in the first reviewed round.
4. A handback is pending review → review it before planning new work.
5. Otherwise claim the next feature per `docs/roadmap/STATUS.md` order.

## 3. Round loop
Author the step block → delegate it to a worker subagent → read the real
diff bottom-up and re-run the verification yourself → verdict. On FAIL,
findings persist to `.agent/live_review.md` in their own commit before
anything is fixed.

## 4. Gates
```bash
python3 -m pytest tests/cli/test_golden_path.py -q      # canary, every round
python3 -m pytest tests/docs/ -q                        # any docs/roadmap change
python3 -m pytest -n auto -q                            # integration gate only
```
Closure follows `docs/roadmap/STATUS_closure_protocol.md` exactly:
evidence job, fresh review zip, authored STATUS line, PR created and NOT
merged.
