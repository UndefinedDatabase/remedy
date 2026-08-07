# Self-Drive Protocol — one-session feature building (v1)

> How ONE Claude Code session builds a Remedy feature end to end when the
> operator can only start the session and invoke a single skill.
> AGENTS.md remains the highest authority. This file changes WHO relays a
> round, never WHAT is verified. The split-workflow roles
> (docs/agents/split_workflow.md) are preserved INSIDE the session — they
> are not collapsed into one actor.

## Why this exists
From 2026-08-13 the operator reaches this machine only over SSH from a
phone. Relaying paste blocks between two windows stops being possible, so
the relay moves into the session. Everything the relay protected —
evidence-first review, block conditions, PR-only merges — stays.

## Role model inside one session (load-bearing)

| Role | Who | Writes |
|---|---|---|
| Planner & reviewer | the main session | nothing in the work tree; authors step text and findings, runs verification, issues verdicts |
| Worker | a delegated subagent, one per round | all code, docs, `.agent/` state, all commits |
| Operator | human, asynchronous | starts the session; may pull a review zip; may merge manually at any time |

The single-writer rule survives: the main session never edits a work-tree
file itself. A round in which the main session both wrote and certified
the change is a protocol violation and its verdict is void —
docs/agents/planner_reviewer_prompt.md §3 forbids self-certified
production code, and in-session delegation is how that requirement is met
once no human relay exists.

Remedy deliberately does not run self-drive as a single undivided actor:
the reviewer's independence is the only thing standing between a green
word and a green run, and it is cheaper to keep than to rebuild.

## Phase 0 — state probe (deterministic, always first)
Read-only, in this order, before any decision is made:

```bash
git status --porcelain          # must be empty
git branch --show-current
git log --oneline -n 8
gh pr list --state open --json number,headRefName,baseRefName,isDraft
remedy plan status              # F080 roadmap mirror
remedy plan next                # Rule A5 — proposes, never starts
```

Then read from disk, never from session memory: `.agent/handoff.md`,
`.agent/plan.md`, `.agent/live_review.md`, `.agent/candidates.md`, and
the active feature file under `docs/roadmap/features/`.

## Phase 1 — decide
1. `.agent/STOP` exists → write the handoff, end the session, do nothing else.
2. Open PR from a `feature/*` branch into `main`, not a draft, exactly one
   → merge it at the Open PR Gate (AGENTS.md) before any new branch.
   Anything else about that PR → stop and report.
3. `.agent/candidates.md` non-empty → the first reviewed round registers
   or resolves every entry and empties the file
   (docs/roadmap/STATUS_closure_protocol.md).
4. A handback is pending review → review it first; never plan new work
   over an ungated round.
5. Otherwise claim the next feature per STATUS order (Rule A5).

## Phase 2 — the round loop
Each round is: author → delegate → review → verdict.

1. **Author.** The main session writes the step block (goal, bundle,
   exact change set, constraints, done-when with the literal verification
   commands) and any finding text, exactly as
   docs/agents/planner_reviewer_prompt.md §3 prescribes. Authored text
   that a worker will apply to a file is still saved under
   `.agent/authored/` by the worker; in-session there is no transport, so
   the hash-stamp ritual is replaced by a `cmp` of the applied file
   against the authored original — the proof obligation is unchanged.
2. **Delegate.** One worker subagent per round, given the step block and
   nothing else it did not read itself. It follows AGENTS.md in full:
   self-review loop before every commit, small commits, `.agent/plan.md`
   current, clean tree, push, handoff rewrite.
3. **Review.** The main session reads the real diff
   (`git diff <LAST_REVIEWED_SHA>..HEAD`) bottom-up and re-runs the
   round's verification commands itself. A worker's summary is never
   evidence.
4. **Verdict.** PASS → `LAST_REVIEWED_SHA` advances, next step. FAIL →
   findings persist to `.agent/live_review.md` in their own commit
   FIRST, then the repair round.

Verification tiers, the canary, the integration gate and the closure
protocol are unchanged; this file adds no exception to any of them.

## Guardrails (any one trips → stop and hand off)
- **G1 PR-only merges.** Merges happen only at the Open PR Gate, only via
  `gh pr merge <n> --merge --delete-branch`. Never merge a PR this
  session created in the same session.
- **G2 Never force-push.** No `--force`, no `--force-with-lease`, no
  history rewrite, no branch deletion beyond the gate's own
  `--delete-branch`.
- **G3 Never work on `main`.** Every change lands on a `feature/*` branch.
- **G4 Gates run, never assumed.** Every commit's gate commands are
  executed and their real exit codes recorded. "Green" as a word is a
  finding.
- **G5 Destructive verification is isolated.** Mutation and red-proof
  checks run only inside a disposable `git worktree`, never in the
  primary checkout, which satisfies `git status --porcelain` == empty at
  every verdict.
- **G6 STOP file.** If `.agent/STOP` appears at any point, finish the
  current commit if one is half-written, then hand off and end.
- **G7 Session limits.** The session states its round cap and wall-clock
  cap up front and honours them. A session that ends at its limit with a
  written handoff is a SUCCESS, not a failure.
- **G8 Ambiguity ends the round.** Any red gate, contradiction, or
  question the rules do not answer → write the handoff and end cleanly.
  Never guess, never widen scope to route around a block.

## Ending a session
Always through `.agent/handoff.md` (F079 machinery,
docs/agents/handback_template.md): feature and round, branch, commit
SHAs, changed-files table, real verification results, open-findings
count, next expected action. The handoff is the only return channel, and
a session with no handoff did not happen.

## What stays with the operator
The review zip (`scripts/make_review_zip.sh`) remains the operator's
remote window into a run, on demand and at closure. Nothing in this
protocol may assume the operator can paste anything beyond the single
command that starts the session.
