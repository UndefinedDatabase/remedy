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
R58, this round: T002d's second half. The two `runtime-build` call sites in
`_auto_build_frontend` (`packages/orchestration/ui_server.py`) move onto
`run_guarded_runtime_build_command` with `check=True`, reached as a module attribute so a test
can patch it, and one new test pins that no bare `subprocess.run` survives in that function.
The R57 PASS and the resolution of R-0558 are recorded in the same round.

## Next Steps
1. The three `runtime-server` sites (`runtime_cmd.py`, `dev_server.py`,
   `runtime_supervisor.py`) — `Popen`-shaped, and taking NO wall timeout, because a clock
   would kill them mid-service.
2. T003 — network posture, the limitations document, its README link. That document states what
   the CHILD-half migrations do NOT bound: an app log written to a file takes no guard output
   cap, and a build behind an HTTP proxy does not run under the guard at all, because the proxy
   variables are `FORBIDDEN_ENV_KEYS` members and the floor is not a row's to lift.
   Then the integration gate, then closure.

## Risks
- An allowlist bounds what the PARENT hands over, never what the child's runtime
  adds back: a CPython child sets `LC_CTYPE` itself under PEP 538. T003's
  limitations document must say so rather than claim a sealed environment.
- A stream still blocked at the grace deadline leaks one pipe read end and one
  daemon thread. Closing an fd under a blocked reader risks that thread reading
  a recycled fd after a later `open()`, so the leak is the cheaper wrong.
