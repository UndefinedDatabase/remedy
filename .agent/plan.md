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
R43, this round: record the R42 PASS and register R-0537 and R-0538, both defects in
R-0536's own text. A RECORD round by measurement, not by choice: the `ci_run.py` migration
is authored, dry-run and red-controlled, but its block measured 487 lines against the
400-line cap of DECISION F105 D5, so R44 applies it.

## Next Steps
1. T002b remainder — the two `test`-class sites still on a bare spawn. At c3201976 BOTH
   overlay one variable onto a copy of `os.environ`, so both were blocked on the same
   missing capability rather than `builder_bridge.py` alone: `ci_run.py` sets the
   per-stage pytest budget, `builder_bridge.py` sets `PYTHONDONTWRITEBYTECODE`. R38's
   `extra_env` overlay unblocks both (DECISION F085 D3). `ci_run.py` goes first and its
   design is ruled in DECISION F085 D4: capture and re-emit the stage output, set the
   guard's wall ABOVE the child's own budget as a backstop, and carry that budget through
   `extra_env`. R44 applies it, then `builder_bridge.py` as the last site of this
   sub-slice. One or two per order, never as one group.
2. T002c-d — the two DoD sites and the five runtime sites, whose policy differs:
   no wall timeout, because their children are the long-lived harness.
3. T003 — network posture, the honest limitations document, the README link. Then
   the integration gate, then closure.

## Risks
- An allowlist bounds what the PARENT hands over, never what the child's runtime
  adds back: a CPython child sets `LC_CTYPE` itself under PEP 538. T003's
  limitations document must say so rather than claim a sealed environment.
- A stream still blocked at the grace deadline leaks one pipe read end and one
  daemon thread. Closing an fd under a blocked reader risks that thread reading
  a recycled fd after a later `open()`, so the leak is the cheaper wrong.
