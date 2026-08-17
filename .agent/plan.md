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
R21, this round: record the R20 PASS, rule the streaming seam's shape as DECISION
F085 D2, and migrate it. `exec_guard` gains a public `ChildSpawnPlan` and
`plan_child_spawn`, carved out of what `run_guarded` already runs before its own
`Popen`; `run_streamed_command` takes an optional policy and applies that plan at
the spawn it already has, keeping the watchdog, the process group and the byte cap
that make it a streaming supervisor. T002a closes when this lands.

## Next Steps
1. `_StreamPump` gains a lock and a `snapshot()` so PARTIAL output survives a
   bounded drain. It still returns `b""` for a stream whose pump never reached
   EOF, which `streams_complete` reports honestly but which loses bytes.
2. T002b — the twelve `test`-class sites, in ten modules, with behaviour-equality
   goldens and the environment-allowlist test that carries R-0202.
3. T002c-d, then T003 — network posture, limitations document, README link.

## Risks
- An allowlist bounds what the PARENT hands over, never what the child's runtime
  adds back: a CPython child sets `LC_CTYPE` itself under PEP 538. T003's
  limitations document must say so rather than claim a sealed environment.
- A stream still blocked at the grace deadline leaks one pipe read end and one
  daemon thread. Closing an fd under a blocked reader risks that thread reading
  a recycled fd after a later `open()`, so the leak is the cheaper wrong.
