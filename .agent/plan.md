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
R73, this round: R72's verdict recorded, the findings its gate produced registered, and the feature
file's Built State written — so the closure round that follows touches only the paths
docs/roadmap/STATUS_closure_protocol.md item 5 allows. R72 PASSED: its transport, its slice shapes,
its arithmetic and its integration gate were re-taken by the reviewer rather than read, and the
branch-side full-suite failure the reviewer's own repeated runs produced passes serially, which
docs/agents/integration_gate.md step 4 classifies as the xdist-flake class to record and not to block.

## Next Steps
1. Closure per docs/roadmap/STATUS_closure_protocol.md: evidence job, FRESH review zip, the STATUS
   line and the README capability sync authored by the reviewer, and the PR the operator merges at
   the next Open PR Gate.
2. R-0567, R-0568 and R-0569 close as documented risks in that closure under precondition 1 of that
   protocol, rather than by a repair round inside this feature.

## Risks
- An allowlist bounds what the PARENT hands over, never what the child's runtime
  adds back: a CPython child sets `LC_CTYPE` itself under PEP 538. T003's
  limitations document must say so rather than claim a sealed environment.
- A stream still blocked at the grace deadline leaks one pipe read end and one
  daemon thread. Closing an fd under a blocked reader risks that thread reading
  a recycled fd after a later `open()`, so the leak is the cheaper wrong.
