# Context — F267 List commands v2 completion

## Active Branch
feature/f267-list-commands-v2-completion, cut from `main` at `9f06c509`
(the merge commit of pull request 272, F265 Teacher learning UI v1).

## Scope
F267 (Tier 2), registered 2026-09-05 by operator ruling amend0905-throughput
(DECISION F262 D5), splitting the remaining scope off F262. T001, wiring the
last list commands to `apply_list_options`, landed in F273 (DECISION F273
D9). What remains is T002, one test proving every list command's HANDLER
refuses an unknown `--sort` field, over the set the catalog itself derives,
and T003, the ten-second demo as a test, as
`docs/roadmap/features/T2_F267.md` specifies.

## Do not touch
The stores' own schemas and the `--json` contract's existing keys. The
list handlers themselves: every one of them already honours the flags,
so this feature adds tests and no production code.

## Active assumptions
- The in-scope set is `_is_list_command` over the catalog, with no
  exclusion, and the demo seeds `run list`'s store (DECISION F267 D1).

## Constraints
- `python3 -m ruff check <path>` is the spelling every gate orders.
- A round touching `docs/roadmap/**` also gates `tests/docs/` and
  `tests/orchestration/test_roadmap_index.py`.
- Destructive verification runs only inside a disposable git worktree under
  `.remedy-wt/`, never in the primary checkout, which satisfies
  `git status --porcelain` empty at every verdict.
- Per operator amendment amend0917-throughput (2026-09-17): the full pytest
  suite runs exactly once per feature, in the closure sequence's
  integration-gate round; a round runs targeted pytest files, the golden
  path, `tests/docs/` when `docs/roadmap/**` changed, and ruff.

## Steps
The item-status table for each round lives in that round's handback,
`.agent/handoff.md`.
