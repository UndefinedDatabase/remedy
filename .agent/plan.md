# Plan — operator amendment amend0920-selfuse-real

Branch: feature/amend0920-selfuse-real, cut from `origin/main` at `43d14817`
(the merge commit of pull request 260, F273's closure).

## Goal

A planner that is not Ollama, a self-use track that can land a fix, and the
answered operator questions deleted — the operator amendment's Parts A to E.

## Current Step

Part E: the gates, then the pull request, its hosted CI, the merge, and the
fold-in of `origin/main` into `feature/f276-data-root-hygiene`.

## Next Steps

1. Run `ruff check .`, `tests/docs/`, `tests/cli/test_golden_path.py`, the
   catalog tests, `test_do_run.py`, `test_self_use_*.py`, `test_config.py`
   and every test this branch added.
2. Push, open the pull request, watch both Python columns, merge when green.
3. Merge `origin/main` into `feature/f276-data-root-hygiene` with `--no-ff`,
   keeping BOTH sides of every append-only file, main first. Push it.
4. Restore `ORIG_BRANCH` and write the handback.

## Risks

- `do_run.py` holds no `make_structured_call_fn` call; the three sites named
  are in `do_sequence.py` (F268 round 10 moved them). DECISION D1 records it.
