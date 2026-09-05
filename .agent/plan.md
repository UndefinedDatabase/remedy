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

Round 25, session 9 — the INTEGRATION GATE (docs/agents/integration_gate.md
steps 1-5) before closure: branch run vs. a base run at the merge-base
`7c65d9cc` (PR 235's merge into main), UI parity restored in a
disposable worktree on a throwaway branch, every branch-only and
base-only failure attributed, evidence under `.agent/gate_f262_r25/`.
The worker measures; the reviewer issues the gate verdict next round.

## Next Steps

- If the gate is clean: closure preconditions 3 and 6 (`integrity check
  --json` via the `apps.cli.grouped` module route; the self-use queue is
  exhausted, so `generate_and_append_if_empty`, then run the item to the
  approval gate and register what `describe_self_use_run_defects`
  returns), then closure algorithm steps 1-2 (evidence job
  `f262-closure`, fresh review zip with red control), then the closure
  commit (STATUS `[x]`, README sync, `consumed_by=F262`) and the PR.
- A reproducible branch-only failure coupled to F262 code is a BLOCKER
  and gets its own reviewer-gated repair round before closure.
- Merge under the operator's 2026-09-05 authorization once hosted CI
  reads green (checks read as their own command first).

## Risks

- The gate is where xdist-flake noise (F135/F052 class) surfaces; every
  branch-only id gets a serial re-run and a stated attribution.
- UI parity in the base worktree must be restored exactly (copytree
  symlinks=True, dist re-stamp — R-0591, R-0736) or false base-only
  failures mask real ones.