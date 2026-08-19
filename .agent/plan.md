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
R74, the closure round per docs/roadmap/STATUS_closure_protocol.md: R73's PASS recorded, then the
evidence job and a FRESH review zip built from a clean tree at that record's commit, then one closure
commit carrying the reviewer-authored STATUS line, the README capability sync and the candidate
carrier, then the PR. R73 PASSED — its transport, both slice shapes, the arithmetic and all four of
its gate suites were re-run by the reviewer rather than read from the handback.

## Next Steps
1. The operator merges the closure PR at the next feature's Open PR Gate; this session merges nothing.
2. The next session claims the next feature by Rule A5, and its FIRST reviewed round empties
   `.agent/candidates.md` by registering or resolving every entry that file holds.

## Risks
- An allowlist bounds what the PARENT hands over, never what the child's runtime
  adds back: a CPython child sets `LC_CTYPE` itself under PEP 538. T003's
  limitations document must say so rather than claim a sealed environment.
- A stream still blocked at the grace deadline leaks one pipe read end and one
  daemon thread. Closing an fd under a blocked reader risks that thread reading
  a recycled fd after a later `open()`, so the leak is the cheaper wrong.
