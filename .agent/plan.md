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
R72, this round: the integration gate re-taken, plus the ledger work R71 left open. R71 PASSED —
its repair is verified and R-0564 is resolved by reviewer text here — and the reviewer's own
arithmetic slip in the R71 block is registered as R-0566 and settled as DECISION F085 D7: the open
count is REGISTERED minus DONE, and a `Landed:` line is an unreviewed fix rather than a resolution.
The gate is re-run because a repair landing after a gate makes that gate's comparison stale.

## Next Steps
1. Closure per docs/roadmap/STATUS_closure_protocol.md: evidence job, FRESH review zip, the STATUS
   line authored by the reviewer, and the PR the operator merges at the next Open PR Gate — unless
   this round's gate returns a blocker, in which case its repair round comes first.

## Risks
- An allowlist bounds what the PARENT hands over, never what the child's runtime
  adds back: a CPython child sets `LC_CTYPE` itself under PEP 538. T003's
  limitations document must say so rather than claim a sealed environment.
- A stream still blocked at the grace deadline leaks one pipe read end and one
  daemon thread. Closing an fd under a blocked reader risks that thread reading
  a recycled fd after a later `open()`, so the leak is the cheaper wrong.
