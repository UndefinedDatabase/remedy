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
R51, this round: T002c's first half. `_run_process_check` moves onto a new `dod-process` seam in
`packages/orchestration/exec_guard.py` that keeps the check's wall timeout and its cwd pin and
replaces the `env=os.environ.copy()` copy with an allowlist; four tests ship with it. The R50
PASS is recorded in the same round.

## Next Steps
1. T002c — `_run_app_once` in `packages/orchestration/dod_runners.py` under the dod-app policy:
   no wall timeout and network allowed, because it starts the app harness and probes it over
   HTTP. It takes the CHILD half alone through `plan_child_spawn`, since it owns its own
   parent-side deadline and writes the app's output to a file rather than to a pipe.
2. T002d — the runtime sites under DECISION F085 D8: `runtime-server` takes no wall timeout and
   `runtime-build` keeps the one it already has. That round also extracts the guard-result
   translation the `test` and `dod-process` seams each carry, once three uses show its shape.
3. T003 — network posture, the limitations document, its README link. Then the integration gate,
   then closure.

## Risks
- An allowlist bounds what the PARENT hands over, never what the child's runtime
  adds back: a CPython child sets `LC_CTYPE` itself under PEP 538. T003's
  limitations document must say so rather than claim a sealed environment.
- A stream still blocked at the grace deadline leaks one pipe read end and one
  daemon thread. Closing an fd under a blocked reader risks that thread reading
  a recycled fd after a later `open()`, so the leak is the cheaper wrong.
