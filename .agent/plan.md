# Plan — operator amendment amend0920-selfuse-real

Branch: feature/amend0920-selfuse-real, cut from `origin/main` at `43d14817`
(the merge commit of pull request 260, F273's closure).

## Goal

A planner that is not Ollama, a self-use track that can land a fix, and the
answered operator questions deleted — the operator amendment's Parts A to E.

## Current Step

Part A: `ClaudeCliPlanner`, the `--planner-provider` flag, the `planner` role.

## Next Steps

1. Part B — the generator's eligibility filter and the `self_use` role.
2. Part C — the evidence skill page, the deleted operator questions, D3–D5.
3. Part D — measure the context load; register a finding only if one is owed.
4. Part E — gates, pull request, merge, fold-in, handback.

## Risks

- `do_run.py` holds no `make_structured_call_fn` call; the three sites named
  are in `do_sequence.py` (F268 round 10 moved them). Recorded as a deviation.
