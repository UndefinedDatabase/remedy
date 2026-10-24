# Context — operator amendment amend1024-one-real-order

## Active Branch
`feature/amend1024-one-real-order`, from `main` at `6caeb480c` (the merge of pull request 390,
F158, merged by the Open PR Gate at the start of this session).

## Scope
Parts A to G of the operator's order of 2026-10-24 exactly: the claude-cli default, the scope
decision, the builder's Bash allowlist, the real isolation check, tokens before dollars, the
roadmap alignment (F317 registered and closed here) and one real run over the public API.

## Do not touch
Anything that does not serve the one goal; the non-human content policy; `dangerous-skip`.

## Active assumptions
- The order's real run uses a temporary project under `/tmp` and a supervisor started for it,
  never the operator's long-running supervisor.
- A provider call made by the real run (G) and the real binary check (D2) is ordered by name.

## Constraints
- At most 500 insertions per commit; no leading-slash tokens in commit subjects.
- No test runs per part: one full pytest run at the end, capped by `tests/conftest.py` (resource
  safety), then review and repair until green.

## Steps
The item-status table lives in the handback, `~/.remedy-loop/amend1024-one-real-order.handback.md`.
