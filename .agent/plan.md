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
R2, this round: record the R1 PASS, register R-0491, and write
`.agent/f085_inventory.md` — every `subprocess.*` call site in `packages/` and
`apps/` with its enclosing symbol, its command class and the keyword facts of
the call itself. No production code and no test content.

## Next Steps
1. R3 — record R2, rule the stage-1 command classes and their policies as a
   DECISION, and rule on the premise the inventory tests: the feature file
   assumes subprocess execution already flows through a small number of
   helpers, and the measured call-site count is what decides whether T002's
   seam migration is the job the task slicing assumes.

## Risks
- If the inventory shows the seams are many rather than few, T002 as sliced is
  under-scoped. That is a spec finding for R3 to route, not a reason for any
  round to widen itself.
- R-0202 is carried into this feature: a spawned path once ignored
  REMEDY_UI_NO_AUTO_BUILD and the mechanism was never explained. R2 locates the
  path; it does not fix it.
