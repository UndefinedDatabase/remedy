# Plan — F262 List commands v2 (dates, sort, filter)

Branch: feature/f262-list-commands-v2, cut from `main` after pull
request 235 was merged at the Open PR Gate.

## Goal

Every list command shows a CREATED and an UPDATED date and carries the
same `--sort <field> [--desc] --since <when> --until <when> --limit <n>`
flags, with newest-first as the DEFAULT everywhere, without a flag
(docs/roadmap/features/T2_F262.md, scoped by DECISION F262 D4; the nine
remaining wirings are F267's per DECISION F262 D5).

## Current Step

Round 24, session 9 — the operator ruled Option B (2026-09-05). This
round books GATE23 and one prose slip, records DECISION F262 D5 (the
ruling) and D6 (the ordered packaging finding examined and declined on
evidence), registers F267 with ledger atomicity (STATUS line,
T2_F267.md, TOTAL_FEATURES 267, README counters), and brings
T2_F262.md's Built State current (closure precondition 4). No code.

## Next Steps

- Integration gate round (docs/agents/integration_gate.md steps 1-5,
  merge-base `7c65d9cc`): the worker measures, the reviewer issues the
  gate verdict at the following round.
- Closure preconditions 3 and 6: `integrity check --json` via the
  `apps.cli.grouped` module route; the self-use queue is exhausted (all
  eight items consumed), so `generate_and_append_if_empty` first, then
  run the item to the approval gate and register what
  `describe_self_use_run_defects` returns.
- Closure algorithm steps 1-2 (evidence job `f262-closure`, fresh review
  zip with red control), then the closure commit (STATUS `[x]`, README
  sync, `consumed_by=F262`) and the pull request.
- Merge under the operator's 2026-09-05 authorization once hosted CI
  reads green (checks read as their own command first).

## Risks

- R-0796 stays OPEN across closure as documented Medium risk, owned by
  F267 — nine commands parse the four flags and ignore them until then.
- The integration gate's base run needs UI parity in the base worktree
  (copytree symlinks=True, dist re-stamp — R-0591, R-0736).