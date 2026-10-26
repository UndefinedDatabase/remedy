# Context — operator amendment amend1026-go-live-and-ask

## Active Branch
`feature/amend1026-go-live-and-ask`, from `main` at `3ea458349` (no open pull request).

## Scope
Parts A to E of the operator's order of 2026-10-26: go live on this machine, contract 1.30 and
the changelog, the projects list and the read-only ask, Universe's three small asks, and one
real ask as F318's evidence.

## Do not touch
The non-human content policy; the write tools of any claude-cli role other than the ask.

## Active assumptions
- Remedy's own project is the slug `remedy` (registered 2026-10-26 11:31:58 UTC, repo
  `~/Repos/remedy`); Universe's alias `remedy-backend` names no project here. The real ask uses
  `remedy`, which `orb-universe` lists.
- `luna` was found holding `host_tools`; the order says it stays without, so it was revoked.
- `max_total_tokens` counts input plus output tokens, the budget's own measure (F317's
  `order_budget_used`); the four kinds are reported beside it.

## Constraints
- At most 500 insertions per commit; no leading-slash tokens in commit subjects.
- One full pytest run at the end, then review and repair until green.
