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
R71, this round: the repair the integration gate demanded. R70 PASSED and its gate found exactly
one real branch-only regression — `test_run_tests_local_no_shell_true` pinned a spawn site that
F085 T002b moved, so it failed on a property that still holds. The test is pulled to the new seam
and its two assertions are proved reachable by mutation. Registered as R-0564; the parity-digest
blindness the same gate surfaced is registered as R-0565. No production file is touched.

## Next Steps
1. Re-run the integration gate per docs/agents/integration_gate.md: a repair landed after a gate
   invalidates that gate's comparison, so the branch-versus-base reading is taken again.
2. Then closure per docs/roadmap/STATUS_closure_protocol.md: evidence job, FRESH review zip, the
   STATUS line authored by the reviewer, and the PR the operator merges at the next Open PR Gate.

## Risks
- An allowlist bounds what the PARENT hands over, never what the child's runtime
  adds back: a CPython child sets `LC_CTYPE` itself under PEP 538. T003's
  limitations document must say so rather than claim a sealed environment.
- A stream still blocked at the grace deadline leaks one pipe read end and one
  daemon thread. Closing an fd under a blocked reader risks that thread reading
  a recycled fd after a later `open()`, so the leak is the cheaper wrong.
