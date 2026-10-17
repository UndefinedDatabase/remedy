# Context — execution quality (operator order 2026-10-17, after PR 348)

## Active Branch
feature/execution-quality, cut from main `1f18396c0`, checked out in the worktree
`.remedy-wt/exec-quality`. The main checkout stays on main: the running `remedy serve start`
(editable install) executes the main checkout's code, so a branch switch there would deploy.

## Incident evidence (read through Remedy's own readers; `.data/**` is not read raw)
- Order a6a87e65809f6bd6 (HTTP, 12:54:08–13:00:49 UTC 2026-10-17), lab repo ~/Repos/remedy-lab.
- Job 84b0cc4272164bb2, runs c86f7e59702042c5 (test_command.txt) and e7e95d91a2274109 (README).

## Scope
Order scope and lane routing, planner repo facts, order test requirement → job test command,
job verification reading, Pi per-call limits and evidence, review reports + review ZIP, the
interface's execution key and HTTP provider refusal, tests and docs.

## Do not touch
The roadmap queue (F078 stays next), `.agent/STOP`, the supervisor, Universe (handoff text only), the sandbox's policy, provider defaults.

## Steps
Phases 0 to 7 of the order; the current one is in plan.md.

## Constraints
- No real model call; fake providers and recorded fixtures only.
- One pytest process tree at a time; one full local gate at the end.
- Commits at most 500 insertions; structure ratchet: listed functions/files do not grow.
