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
R50, this round: record the R49 PASS, register R-0552 and R-0553, and amend the F085 feature
file so the `runtime` class carries the two policies its sites actually need — the same
correction D7 made for `dod`, applied to the row D7 left standing. A planning correction; no
source file changes this round, and T002c is built at R51.

## Next Steps
1. T002c — `_run_process_check` in `packages/orchestration/dod_runners.py` onto the guard seam
   under the dod-process policy: it is a bounded check and KEEPS a wall timeout; the gap it
   closes is `env=os.environ.copy()`, which hands the child the whole parent environment.
2. T002c — `_run_app_once` in that same module under the dod-app policy: no wall timeout and
   network allowed, because it starts the app harness and probes it over HTTP.
3. T002d — the runtime sites under DECISION F085 D8: `runtime-server` takes no wall timeout,
   `runtime-build` keeps the one it already has. Then T003, the integration gate, then closure.

## Risks
- An allowlist bounds what the PARENT hands over, never what the child's runtime
  adds back: a CPython child sets `LC_CTYPE` itself under PEP 538. T003's
  limitations document must say so rather than claim a sealed environment.
- A stream still blocked at the grace deadline leaks one pipe read end and one
  daemon thread. Closing an fd under a blocked reader risks that thread reading
  a recycled fd after a later `open()`, so the leak is the cheaper wrong.
