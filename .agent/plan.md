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
R53, this round: T002c's migration, which COMPLETES T002c. `_run_app_once` in
`packages/orchestration/dod_runners.py` takes the CHILD half alone through `plan_child_spawn`
under the `dod-app` seam R52 landed, so the whole-parent-environment copy it passed becomes an
allowlist. The `exec_guard` PARTIAL COVERAGE note is rewritten in the same round, because only
this call site's move makes it false. One test ships with it. The R52 PASS is recorded in the same
round, with findings R-0555 and R-0556.

## Next Steps
1. T002d — the runtime sites under DECISION F085 D8: `runtime-server` takes no wall timeout and
   `runtime-build` keeps the one it already has. That round also extracts the guard-result
   translation the `test` and `dod-process` seams each carry, now that three uses show its shape.
2. T003 — network posture, the limitations document, its README link. That document states what
   the CHILD-half migrations do NOT bound: an app log written to a file takes no guard output cap.
   Then the integration gate, then closure.

## Risks
- An allowlist bounds what the PARENT hands over, never what the child's runtime
  adds back: a CPython child sets `LC_CTYPE` itself under PEP 538. T003's
  limitations document must say so rather than claim a sealed environment.
- A stream still blocked at the grace deadline leaks one pipe read end and one
  daemon thread. Closing an fd under a blocked reader risks that thread reading
  a recycled fd after a later `open()`, so the leak is the cheaper wrong.
