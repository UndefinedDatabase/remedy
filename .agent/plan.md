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
R32, this round: record the R31 PASS, resolve R-0520 by promoting its
counter-measure into the pre-emission checklist, and move
`integrity_gate._check_collect_only` onto `run_guarded_test_command` — the
`test`-class site that pins no cwd and keeps `cwd=None` deliberately.

## Next Steps
1. T002b remainder — the three `test`-class sites still on a bare spawn, each
   differing from the shapes already migrated: `builder_bridge.py` SETS
   `PYTHONDONTWRITEBYTECODE` on a full `os.environ` copy, which the seam cannot
   express today because `run_guarded_test_command` allowlists keys rather than
   setting values — that site needs the seam widened before it can move;
   `ci_run.py` streams to the console instead of capturing and passes no timeout;
   and `mission_state.py` spawns inside a default `runner` closure. One or two per
   order, never as one group.
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
