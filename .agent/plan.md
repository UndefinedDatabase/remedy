# Plan — F085 Sandbox hardening (stage 1)

Branch: feature/f085-sandbox-hardening, cut from origin/main at a5a70621 after
the F083 closure PR #202 and the amendment PR #203 merged.
`.agent/live_review.md` is the source of truth for the open set, for the next
free finding id and for the round map; this file repeats none of them.

## Goal
Builder-spawned commands stop relying on prompted discipline: every builder,
test and DoD subprocess gets POSIX resource limits, a per-command wall timeout,
output-size caps, a cwd pinned inside the worktree, an environment allowlist and
a default-deny network posture — with a document that says EXACTLY what stage 1
does and does not prevent. DONE when the limits provably kill a runaway fixture
(cpu, memory, oversized output, endless sleep) and classify it `resource_limit`
with the tripped limit named, an off-scope write attempt fails, well-behaved
commands behave identically under the guard, a secret-like parent env var never
reaches a child, and the limitations document exists and is linked from the
README.

## Current Step
R3, this round: record the R2 PASS, register R-0492, and close the session on a
clean boundary. The seam inventory `.agent/f085_inventory.md` is complete and
accepted; it is not revised again.

## Next Steps
1. R4 — write the `docs/roadmap/features/T2_F085.md` amendment that DECISION
   F085 D1 names, correcting the "small number of helpers" premise the
   inventory disproved, and rule the stage-1 command classes and their policies.
   R4 changes `docs/roadmap/**`, so its gate list adds `tests/docs/`.

## Risks
- T002's seam migration is scoped against a premise the inventory disproved: 67
  real call sites in 56 enclosing functions, of which the four helpers the
  feature file names cover 24. R4 re-slices before any code is written.
- R-0202 has one reader and two seams that provably drop the variable. Naming
  them is not fixing them, and no round may fix them outside T002.
