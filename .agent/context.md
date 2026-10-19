# Context — agent-state data hygiene

## Active Branch
`feature/agent-data-hygiene` from current `main`.

## Scope
Exclude `.agent` from review packages; block newly staged credentials, machine-local paths,
provider-session links, private-network addresses, and binary agent-state files. This work is
outside the roadmap queue; F078 remains next.

## Steps
Package boundary, staged-content guard, focused verification, then review handoff.

## Assumptions
The operator's `.agents` means `.agent`. Existing Git history is retained; required append-only
workflow records are not rewritten.

## Do not touch
`.agent/STOP`, runtime data, other worktrees, provider settings, or Git history.

## Constraints
Focused changes only; no force-push or history rewrite. Tests use temporary repositories and fake
values only. Resource safety: one pytest process tree at a time.
