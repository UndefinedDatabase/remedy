# Plan — F279 Configuration & toolchain truth

Branch: feature/f279-configuration-toolchain-truth, cut from `main` at
`c9bc5c20`, the merge commit of pull request 266 (F278's closure).

## Goal

Three things this repository asserts about itself become measurable: which
environment variables exist, which tool versions CI installs, and which
checklist items a machine can check (`docs/roadmap/features/T2_F279.md`).

## Current Step

ROUND 3 books round 2's PASS, records DECISION F279 D3, and lands T001's
doctor and docs half: the shell scripts' `REMEDY_` names and the two
real-Ollama opt-ins are registered and guarded; `remedy doctor core` warns
about an unknown `REMEDY_` variable with its closest registered name and
about a registered one whose value does not read as its type; and
`docs/guides/environment.md` is rendered from the registry, indexed, and
held by a drift test. T002 landed in round 1, T001's registry in round 2.

## Next Steps

1. T001's reader half: the direct `REMEDY_` reads move onto one registry
   reader, so each type and default lives in its spec alone.
2. T003, `remedy block lint`, unless the operator has dropped it.
3. T004, the toolchain refresh order and `remedy doctor toolchain`.
4. The closure sequence, with the one full-suite run.

## Risks

`constraints.txt` (round 1) is F279's one declared oversize commit; no
second may follow. Hosted CI first runs the new install steps at the
closure's pull request.
