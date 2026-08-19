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
R66, this round: T003's document. `docs/system/exec-guard-limitations-v0.md` states what stage 1
does NOT prevent — a proxy posture is not containment, three classes of five run under the guard
at all, an allowlist does not bound what a child's own runtime adds, and an app log written to a
file takes no cap — and `docs/README.md` links it from both tables. The R65 PASS is recorded in
the same round.

## Next Steps
1. The remaining acceptance measurement: a guarded test command is refused against a loopback
   server that is really listening, where the same child without the posture is served.
2. The integration gate: the full suite per docs/agents/integration_gate.md, the first of the two
   full-suite runs this feature owes.
3. Then closure per docs/roadmap/STATUS_closure_protocol.md.

## Risks
- An allowlist bounds what the PARENT hands over, never what the child's runtime
  adds back: a CPython child sets `LC_CTYPE` itself under PEP 538. T003's
  limitations document must say so rather than claim a sealed environment.
- A stream still blocked at the grace deadline leaks one pipe read end and one
  daemon thread. Closing an fd under a blocked reader risks that thread reading
  a recycled fd after a later `open()`, so the leak is the cheaper wrong.
