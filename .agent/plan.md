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
R1, this round: the Open PR Gate, the branch, the STATUS claim `[ ]` → `[~]`,
the live-review reset carrying the F083 open set forward, and the registration
of R-0490. No production code and no test content.

## Next Steps
1. R2 — the subprocess-seam inventory in `.agent/f085_inventory.md`: every
   `subprocess.*` call site in `packages/` and `apps/` with its enclosing
   symbol, command class, cwd source, environment handling, timeout and output
   bounding. The reviewer measured 73 such call sites across 33 files at
   a5a70621; the feature file's premise of "a small number of helpers" is what
   R2 tests.

## Risks
- The feature file says subprocess execution "already flows through a small
  number of helpers". At 73 call sites in 33 files that premise is unproven, and
  if R2 disproves it the seam migration T002 plans is a much larger job than the
  task slicing assumes. That is a spec finding for R3, not a reason to widen R2.
- R-0202 is carried into this feature: a spawned path once ignored
  REMEDY_UI_NO_AUTO_BUILD and the mechanism was never explained. The inventory
  must locate that path rather than assume it is gone.
