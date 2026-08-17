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
R55, this round: a RECORD round only. It persists the R54 PASS to `.agent/live_review.md` and
advances this file; it writes no production code and ships no test. It exists because the
reviewer's session ended at its declared round cap, and a verdict that lives only in a chat reply
is one the next session would have to re-derive from the diff.

## Next Steps
1. T002d's second half — migrate the two `runtime-build` sites in `_auto_build_frontend`
   (`packages/orchestration/ui_server.py`) onto `run_guarded_runtime_build_command` with
   `check=True`, settling the npm environment risk below FIRST. Then the three `runtime-server`
   sites, which take no wall timeout because a clock would kill them mid-service.
2. T003 — network posture, the limitations document, its README link. That document states what
   the CHILD-half migrations do NOT bound: an app log written to a file takes no guard output cap.
   Then the integration gate, then closure.

## Risks
- `RUNTIME_BUILD_ENV_ALLOWLIST` is `TEST_COMMAND_ENV_ALLOWLIST`, read at 1812c219: it carries
  `HOME` and `PATH`, so a public-registry `npm install` survives the scrub, but it names no
  `NPM_CONFIG_*`, no `NODE_*` and no proxy variable. A project on a private registry or behind a
  proxy would break at the migration, not at the seam. R56 settles this BEFORE it migrates —
  widen that row, or take the `extra_env_keys` knob the `test` row already carries.
- An allowlist bounds what the PARENT hands over, never what the child's runtime
  adds back: a CPython child sets `LC_CTYPE` itself under PEP 538. T003's
  limitations document must say so rather than claim a sealed environment.
- A stream still blocked at the grace deadline leaks one pipe read end and one
  daemon thread. Closing an fd under a blocked reader risks that thread reading
  a recycled fd after a later `open()`, so the leak is the cheaper wrong.
