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
R65, this round: the two deny rows amendment F085 D1 still leaves unwired take the posture R64
built. `dod_process_exec_policy` and `managed_builder_execution._builder_exec_policy` set
`deny_network=True`, each pinned by a test in the file its own class already owns, so all three
bounded rows of that table now deny. The R64 PASS is recorded and its one finding registered in
the same round, with the counter-measure landing ahead of the record.

## Next Steps
1. T003's limitations document and its README link, stating what stage 1 does NOT prevent: a
   binary that ignores proxy variables reaches the network anyway, an app log written to a file
   takes no guard output cap, and the git, packaging and other classes never ran under the guard
   at all.
2. Then the integration gate, then closure.

## Risks
- An allowlist bounds what the PARENT hands over, never what the child's runtime
  adds back: a CPython child sets `LC_CTYPE` itself under PEP 538. T003's
  limitations document must say so rather than claim a sealed environment.
- A stream still blocked at the grace deadline leaks one pipe read end and one
  daemon thread. Closing an fd under a blocked reader risks that thread reading
  a recycled fd after a later `open()`, so the leak is the cheaper wrong.
